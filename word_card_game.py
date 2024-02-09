import random
import pymongo

client = pymongo.MongoClient("mongodb+srv://user123:hhCsLKxVQoWDsO2M@hearme.5yquvxf.mongodb.net/")
db = client['word_card']
collection = db['card']

def get_words():
    doc = collection.find_one()
    if doc and 'card_0' in doc:
        words = doc['card_0']
        #print(words)
        return words
    else:
        return []



def wordGameData():
    words_data = get_words()
    main_word_data = random.choice(words_data)
    card_words_data = random.sample(words_data, len(words_data))

    def create_links(word_data):
        return {'word': word_data['word'], 'image_link': word_data['image'], 'audio_link': word_data['audio']}

    return {
        'main_word': create_links(main_word_data),
        'card_word1': create_links(card_words_data[0]),
        'card_word2': create_links(card_words_data[1]),
        'card_word3': create_links(card_words_data[2])
    }
