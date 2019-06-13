from flask import Flask
from flask import render_template
# import tensorflow as tf
# import tensorflow.keras as keras

app = Flask(__name__)
# app._static_folder = '/static'
 
@app.route("/")
def predict():
    return render_template('index.html')
 
if __name__ == "__main__":
    app.run(debug=True)



# 1.) Get data with ajax
# {. . . .}


# 2.) Preprocess Data (convert 8x8 array into 1x768 array)
# {. . . .}


# 3.) Input data to pre-trained Keras model

# def get_model():
#     return keras.Sequential([
#         keras.layers.Dense(2048, input_dim=768, activation=tf.nn.elu),
#         keras.layers.Dense(2048, activation=tf.nn.elu),
#         keras.layers.Dense(2048, activation=tf.nn.elu),
#         keras.layers.Dense(1)
#     ])

# prediction_model = get_model()
# prediction_model.load_weights('model_weights.h5')
# board_score = prediction_model.predict()


# 4.) Send score back to client with ajax
# {. . . .}