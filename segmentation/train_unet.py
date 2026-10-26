
from pathlib import Path
import random

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

SEED = 42
IMG_SIZE = 256
BATCH_SIZE = 8
EPOCHS = 40
VAL_FRACTION = 0.15

tf.keras.utils.set_random_seed(SEED)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "dataset" / "brisc2025" / "segmentation_task"
MODEL_PATH = (
    BASE_DIR.parent / "backend" / "tumor_segmentation.keras"
)

# Pair MRI images and masks by filename

def get_pairs(split):
    image_dir = DATA_DIR / split / "images"
    mask_dir = DATA_DIR / split / "masks"

    images = sorted(image_dir.glob("*.jpg"))
    masks = {p.stem: p for p in mask_dir.glob("*.png")}

    pairs = []
    missing = []

    for image_path in images:
        mask_path = masks.get(image_path.stem)

        if mask_path is None:
            missing.append(image_path.name)
        else:
            pairs.append((str(image_path), str(mask_path)))

    if missing:
        raise ValueError(
            f"{len(missing)} images in {split} have no matching mask. "
            f"Examples: {missing[:5]}"
        )

    if not pairs:
        raise ValueError(f"No image-mask pairs found for {split}")

    return pairs


all_pairs = get_pairs("train")
test_pairs = get_pairs("test")

# Deterministic training/validation split.
random.Random(SEED).shuffle(all_pairs)
val_count = max(1, int(len(all_pairs) * VAL_FRACTION))

val_pairs = all_pairs[:val_count]
train_pairs = all_pairs[val_count:]

print(f"Training pairs:   {len(train_pairs)}")
print(f"Validation pairs: {len(val_pairs)}")
print(f"Test pairs:       {len(test_pairs)}")

def load_pair(image_path, mask_path):
    image_bytes = tf.io.read_file(image_path)
    image = tf.io.decode_jpeg(image_bytes, channels=3)
    image = tf.image.resize(
        image, [IMG_SIZE, IMG_SIZE],
        method="bilinear"
    )
    image = tf.cast(image, tf.float32) / 255.0

    mask_bytes = tf.io.read_file(mask_path)
    mask = tf.io.decode_png(mask_bytes, channels=1)

    # Nearest-neighbor resizing preserves mask regions.
    mask = tf.image.resize(
        mask, [IMG_SIZE, IMG_SIZE],
        method="nearest"
    )

    # Convert grayscale mask into a binary tumor mask.
    mask = tf.cast(mask > 127, tf.float32)

    image = tf.ensure_shape(
        image, [IMG_SIZE, IMG_SIZE, 3]
    )
    mask = tf.ensure_shape(
        mask, [IMG_SIZE, IMG_SIZE, 1]
    )

    return image, mask


def make_dataset(pairs, training=False):
    image_paths = [p[0] for p in pairs]
    mask_paths = [p[1] for p in pairs]

    ds = tf.data.Dataset.from_tensor_slices(
        (image_paths, mask_paths)
    )

    if training:
        ds = ds.shuffle(
            buffer_size=min(len(pairs), 1000),
            seed=SEED,
            reshuffle_each_iteration=True
        )

    ds = ds.map(
        load_pair,
        num_parallel_calls=2
    )
    ds = ds.batch(BATCH_SIZE)
    ds = ds.prefetch(1)

    return ds


train_ds = make_dataset(train_pairs, training=True)
val_ds = make_dataset(val_pairs)
test_ds = make_dataset(test_pairs)


# U-Net architecture
def conv_block(x, filters):
    x = layers.Conv2D(
        filters, 3, padding="same",
        kernel_initializer="he_normal"
    )(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)

    x = layers.Conv2D(
        filters, 3, padding="same",
        kernel_initializer="he_normal"
    )(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)

    return x


def build_unet():
    inputs = keras.Input(
        shape=(IMG_SIZE, IMG_SIZE, 3)
    )

    # Encoder
    c1 = conv_block(inputs, 32)
    p1 = layers.MaxPooling2D()(c1)

    c2 = conv_block(p1, 64)
    p2 = layers.MaxPooling2D()(c2)

    c3 = conv_block(p2, 128)
    p3 = layers.MaxPooling2D()(c3)

    c4 = conv_block(p3, 256)
    p4 = layers.MaxPooling2D()(c4)

    # Bottleneck
    c5 = conv_block(p4, 512)

    # Decoder
    u6 = layers.Conv2DTranspose(
        256, 2, strides=2, padding="same"
    )(c5)
    u6 = layers.Concatenate()([u6, c4])
    c6 = conv_block(u6, 256)

    u7 = layers.Conv2DTranspose(
        128, 2, strides=2, padding="same"
    )(c6)
    u7 = layers.Concatenate()([u7, c3])
    c7 = conv_block(u7, 128)

    u8 = layers.Conv2DTranspose(
        64, 2, strides=2, padding="same"
    )(c7)
    u8 = layers.Concatenate()([u8, c2])
    c8 = conv_block(u8, 64)

    u9 = layers.Conv2DTranspose(
        32, 2, strides=2, padding="same"
    )(c8)
    u9 = layers.Concatenate()([u9, c1])
    c9 = conv_block(u9, 32)

    outputs = layers.Conv2D(
        1, 1, activation="sigmoid"
    )(c9)

    return keras.Model(inputs, outputs, name="BrainSight_UNet")

@keras.utils.register_keras_serializable()
def dice_coefficient(y_true, y_pred):
    y_true = tf.cast(y_true, tf.float32)
    y_pred = tf.cast(y_pred >= 0.5, tf.float32)

    intersection = tf.reduce_sum(
        y_true * y_pred, axis=[1, 2, 3]
    )
    denominator = (
        tf.reduce_sum(y_true, axis=[1, 2, 3])
        + tf.reduce_sum(y_pred, axis=[1, 2, 3])
    )

    dice = (
        2.0 * intersection + 1e-6
    ) / (denominator + 1e-6)

    return tf.reduce_mean(dice)


@keras.utils.register_keras_serializable()
def iou_score(y_true, y_pred):
    y_true = tf.cast(y_true, tf.float32)
    y_pred = tf.cast(y_pred >= 0.5, tf.float32)

    intersection = tf.reduce_sum(
        y_true * y_pred, axis=[1, 2, 3]
    )
    union = tf.reduce_sum(
        y_true + y_pred - y_true * y_pred,
        axis=[1, 2, 3]
    )

    iou = (
        intersection + 1e-6
    ) / (union + 1e-6)

    return tf.reduce_mean(iou)


@keras.utils.register_keras_serializable()
def combined_loss(y_true, y_pred):
    bce = keras.losses.binary_crossentropy(
        y_true, y_pred
    )
    bce = tf.reduce_mean(bce)

    intersection = tf.reduce_sum(
        y_true * y_pred, axis=[1, 2, 3]
    )
    denominator = (
        tf.reduce_sum(y_true, axis=[1, 2, 3])
        + tf.reduce_sum(y_pred, axis=[1, 2, 3])
    )

    dice_loss = 1.0 - tf.reduce_mean(
        (2.0 * intersection + 1e-6)
        / (denominator + 1e-6)
    )

    return bce + dice_loss


model = build_unet()

model.compile(
    optimizer=keras.optimizers.Adam(
        learning_rate=1e-4
    ),
    loss=combined_loss,
    metrics=[
        dice_coefficient,
        iou_score
    ]
)

model.summary()

MODEL_PATH.parent.mkdir(
    parents=True, exist_ok=True
)

callbacks = [
    keras.callbacks.ModelCheckpoint(
        filepath=str(MODEL_PATH),
        monitor="val_loss",
        save_best_only=True,
        verbose=1
    ),
    keras.callbacks.EarlyStopping(
        monitor="val_loss",
        patience=7,
        restore_best_weights=True,
        verbose=1
    ),
    keras.callbacks.ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.5,
        patience=3,
        min_lr=1e-7,
        verbose=1
    )
]

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS,
    callbacks=callbacks
)
best_model = keras.models.load_model(
    MODEL_PATH
)

results = best_model.evaluate(
    test_ds,
    return_dict=True,
    verbose=1
)

print("\nOfficial test results:")
for metric, value in results.items():
    print(f"{metric}: {value:.4f}")

print(f"\nBest model saved at: {MODEL_PATH}")
