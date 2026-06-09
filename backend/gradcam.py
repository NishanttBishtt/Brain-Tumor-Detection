import tensorflow as tf
import numpy as np
import cv2
import os


def make_gradcam_heatmap(
    img_array,
    model,
    last_conv_layer_name,
    pred_index=None
):

    grad_model = tf.keras.models.Model(
        [model.inputs],
        [
            model.get_layer(last_conv_layer_name).output,
            model.outputs[0]
        ]
    )

    with tf.GradientTape() as tape:

        conv_outputs, predictions = grad_model(img_array)

        if pred_index is None:
            pred_index = tf.argmax(predictions[0])

        class_channel = predictions[:, pred_index]

    grads = tape.gradient(
        class_channel,
        conv_outputs
    )

    pooled_grads = tf.reduce_mean(
        grads,
        axis=(0, 1, 2)
    )

    conv_outputs = conv_outputs[0]

    # safer than @ operator
    heatmap = tf.reduce_sum(
        conv_outputs * pooled_grads,
        axis=-1
    )

    heatmap = tf.maximum(
        heatmap,
        0
    )

    max_val = tf.reduce_max(
        heatmap
    )

    if max_val > 0:
        heatmap = heatmap / max_val

    return heatmap.numpy()

def save_gradcam(
    img_path,
    heatmap,
    output_path,
    alpha=0.4
):

    img = cv2.imread(img_path)

    heatmap = cv2.resize(
        heatmap,
        (img.shape[1], img.shape[0])
    )

    heatmap = np.uint8(
        255 * heatmap
    )

    heatmap = cv2.applyColorMap(
        heatmap,
        cv2.COLORMAP_JET
    )

    superimposed_img = cv2.addWeighted(
        img,
        1,
        heatmap,
        alpha,
        0
    )

    cv2.imwrite(
        output_path,
        superimposed_img
    )

    return output_path