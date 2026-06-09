# test_model.py

import tensorflow as tf

print("Loading model...")

model = tf.keras.models.load_model(
    "brain_tumor_model (1).keras",
    compile=False
)

print("SUCCESS!")