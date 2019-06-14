from flask import Flask
from flask import request
from flask import render_template
from flask_cors import CORS, cross_origin

# import tensorflow as tf
# import tensorflow.keras as keras



app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route("/", methods=['GET','POST'])
@cross_origin(supports_credentials=True)
def predict():
    if request.method == "GET":
        result = request.json
        print(result)
        return render_template('index.html')

@app.after_request
def creds(response):
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response
 
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)


######## Steps to get data, generate a board score, and send back to client ########

# 1.) Get data from ajax POST in script.js evaluateBoard(); request.json??
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


# 4.) Send score back to client
# {. . . .}