import tensorflow as tf
import tensorflow.keras as keras
import tensorflowjs as tfjs

# connector script to save model as full .h5 for loading into tensorflow.js
def get_model():
    return keras.Sequential([
        keras.layers.Dense(2048, input_dim=768, activation=tf.nn.elu),
        keras.layers.Dense(2048, activation=tf.nn.elu),
        keras.layers.Dense(2048, activation=tf.nn.elu),
        keras.layers.Dense(1)
    ])
prediction_model = get_model()
prediction_model.load_weights('./model/model_weights.h5')

prediction_model.save('./model/pretrained_model.h5')

tfjs.converters.save_keras_model(prediction_model, './model/tensorflowjs_model')