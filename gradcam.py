import tensorflow as tf
import numpy as np
import cv2

def get_gradcam(model, img_array):
    grad_model = tf.keras.models.Model(
        [model.inputs],
        [model.get_layer("top_conv").output, model.output]
    )

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img_array)
        loss = predictions[:, np.argmax(predictions[0])]

    grads = tape.gradient(loss, conv_outputs)

    heatmap = tf.reduce_mean(grads, axis=(0,1,2))
    heatmap = np.maximum(heatmap, 0) / np.max(heatmap)

    return heatmap