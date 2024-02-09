import numpy as np
from flask import Flask, request, jsonify, request
from flask_cors import CORS
#import pickle

from word_card_game import wordGameData
from word_generation import get_similar_words
from flip_card_content import getFlipCardContent



app = Flask(__name__)

#### Load pretrained models here ####

#model1 = pickle.load(open('model1.pkl','rb'))


# send a json {'exp':1.8,} as a post request to make a prediction
'''
@app.route('/api/predict',methods=['POST'])
def predict():
    data = request.get_json(force=True)
    prediction = model1.predict([[np.array(data['exp'])]])
    output = prediction[0]
    return jsonify(output)

#path to check server status
@app.route("/")
def default_get():
    return "<p>HereMe Backend !</p>"

'''
@app.route('/api/word-game', methods=['GET'])
def word_game_api():
    w1 = request.args.get('w1')
    w2 = request.args.get('w2')
    w3 = request.args.get('w3')

    if not all([w1, w2, w3]):
        return jsonify({'error': 'All three words must be provided'}), 400

    data = wordGameData(w1, w2, w3)
    return jsonify(data)

@app.route('/api/similar-words', methods=['GET'])
def similar_words_api():
    word = request.args.get('word')

    if not word:
        return jsonify({'error': 'A word must be provided'}), 400

    similar_words = get_similar_words(word)
    return jsonify({'similar_words': similar_words})

@app.route('/api/flip-card-content')
def flip_card_content():
    data = getFlipCardContent()
    return jsonify(data)

@app.route('/api/images_data', methods=['GET'])
def get_images_data():
    images_data = wordGameData()
    return jsonify(images_data)

if __name__ == '__main__':
    CORS(app.run(host='0.0.0.0', port=5000, debug=True))
    #app.run(host='0.0.0.0', port=5000, debug=True)