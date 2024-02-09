import pymongo

def getFlipCardContent():
    client = pymongo.MongoClient("mongodb+srv://hearme:hearme678@cluster0.kz66vdr.mongodb.net")
    db = client['word_card']
    collection = db['card']

    card_data = collection.find_one()

    if card_data:
        main_image_data = {
            'isMainImage': True,
            'image': card_data['image'],
            'audio': card_data['audio']
        }

        other_images_data = [
            {
                'isMainImage': False,
                'image': card['image'],
                'audio': card['audio']
            } for card in card_data['card_0']
        ]

        images_data = [main_image_data] + other_images_data

        return images_data

    return []
