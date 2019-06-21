from flask import Flask, current_app
from flask import request
from flask import render_template, json
from flask_cors import CORS, cross_origin

import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow.keras as keras


app = Flask(__name__)
def load_model():
    global prediction_model
    def get_model():
        return keras.Sequential([
            keras.layers.Dense(2048, input_dim=768, activation=tf.nn.elu),
            keras.layers.Dense(2048, activation=tf.nn.elu),
            keras.layers.Dense(2048, activation=tf.nn.elu),
            keras.layers.Dense(1)
        ])
    prediction_model = get_model()
    prediction_model.load_weights('model_weights.h5')
    prediction_model._make_predict_function()
    return prediction_model


@app.route("/")
def main():
    global session
    session = tf.Session()
    keras.backend.set_session(session)
    load_model() 
    return render_template('index.html')


@app.route("/api/predict", methods = ['GET','POST'])
def predict():
    """get board data from client, input to Keras model, and send board scores back to client"""
    piece_list = ('p','n','b','r','q','k','P','N','B','R','Q','K')

    if request.method == "POST":
        board_data = request.json
        turn = board_data['turn']
        board = board_data['board']
        feature_vector = []

        for row in board:
            for square in row:
                if square != None and square['color'] == 'w':
                    square['type'] = square['type'].upper()
                if square == None:
                    for i in range(12):
                        feature_vector.append(np.int8(0))
                elif square['color'] == 'w' and turn == 'w':
                    for piece in piece_list:
                        if square['type'] == piece:
                            feature_vector.append(np.int8(1))
                        else:
                            feature_vector.append(np.int8(0))
                elif square['color'] == 'w' and turn == 'b':
                    for piece in piece_list:
                        if square['type'] == piece:
                            feature_vector.append(np.int8(-1))
                        else:
                            feature_vector.append(np.int8(0))
                elif square['color'] == 'b' and turn == 'w':
                    for piece in piece_list:
                        if square['type'] == piece:
                            feature_vector.append(np.int8(-1))
                        else:
                            feature_vector.append(np.int8(0))
                elif square['color'] == 'b' and turn == 'b':
                    for piece in piece_list:
                        if square['type'] == piece:
                            feature_vector.append(np.int8(1))
                        else:
                            feature_vector.append(np.int8(0))

        with session.as_default():
            with session.graph.as_default():
                board_score = prediction_model.predict(np.array(pd.Series(feature_vector)).reshape(1, 768))

    return json.jsonify({'score':board_score.item()})

 
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)







