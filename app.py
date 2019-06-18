from flask import Flask
from flask import request
from flask import render_template
from flask_cors import CORS, cross_origin

import numpy as np
import tensorflow as tf
import tensorflow.keras as keras


app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def main():
    """get board data from client, input to Keras model, and send board scores back to client"""
    piece_list = ('p','n','b','r','q','k')

    if request.method == "POST":
        board_data = request.json
        feature_vector = []

        for row in board_data:
            for square in row:
                if square == None:
                    for i in range(12):
                        feature_vector.append(np.int8(0))
                elif square['color'] == 'w': #find a way to keep track of who's move it is! Send all board positions at once???
                    for piece in piece_list: # this is only 6 iterations, not 12!! needs to be 12 iterations per square
                        if square['type'] == piece:
                            feature_vector.append(np.int8(1))
                        else:
                            feature_vector.append(np.int8(0))
                # { more if else conditionals }

        # example logic from parser

        # if square.islower() and move_num % 2 != 0: #whites move
        #         for piece in piece_list:
        #             if square == piece:
        #                 feature_vector.append(np.int8(-1)) 
        #             else:
        #                 feature_vector.append(np.int8(0))
        #     elif square.islower() and move_num % 2 == 0: #blacks move
        #         for piece in piece_list:
        #             if square == piece:
        #                 feature_vector.append(np.int8(1))
        #             else:
        #                 feature_vector.append(0)
        #     elif square.isupper() and move_num % 2 != 0: #whites move
        #         for piece in piece_list:
        #             if square == piece:
        #                 feature_vector.append(np.int8(1))
        #             else:
        #                 feature_vector.append(0)
        #     elif square.isupper() and move_num % 2 == 0: #blacks move
        #         for piece in piece_list:
        #             if square == piece:
        #                 feature_vector.append(np.int8(-1))
        #             else:
        #                 feature_vector.append(np.int8(0))
        #     else: # if the square is empty, append 12 0s (one for each piece)
        #         for i in range(12):
        #             feature_vector.append(np.int8(0))


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

    return render_template('index.html')

 
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)







