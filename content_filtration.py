from flask import request
from pymongo import MongoClient

def check_word_safety(word):
    client = MongoClient("mongodb+srv://hearme:hearme678@cluster0.kz66vdr.mongodb.net")
    db = client['word_filtration']
    blacklist_col = db['blacklist']
    whitelist_col = db['whitelist']
    moderate_col = db['moderate']

    word = word.lower()
    # Check if the word exists in the blacklist
    if blacklist_col.find_one({"word": word}):
        return "unsafe"

    # Check if the word exists in the whitelist
    whitelist_entry = whitelist_col.find_one({"word": word})
    if whitelist_entry:
        sensitive_score = whitelist_entry.get("sensitivity_score")
        print(sensitive_score)
        if sensitive_score == 1:
            return "safe"
        else:
            return "unsafe"

    # If the word does not exist in the whitelist
    moderate_col.insert_one({"word": word, "status": "not_verified"})
    return "not_verified"
