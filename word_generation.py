import torch
from transformers import RobertaTokenizer, RobertaForMaskedLM
import pymongo
from content_filter_azure import is_word_safe
from gtts import gTTS
import os

# Load the pretrained RoBERTa model and tokenizer
tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
model = RobertaForMaskedLM.from_pretrained('roberta-base')

def generate_audio_save_locally(word):
    # Define the path where you want to save the audio file
    # Using a temporary directory or a specific path
    temp_dir = "./temp_audio"
    os.makedirs(temp_dir, exist_ok=True)  # Ensure the directory exists
    
    # Define the full path for the audio file
    file_path = os.path.join(temp_dir, f"{word}.mp3")
    
    # Generate the audio using gTTS
    tts = gTTS(text=word, lang='en')
    tts.save(file_path)
    
    # Return the local path of the generated audio file
    return file_path

def get_similar_words(input_word, top_k=3):
    # Create a masked sentence with the input word
    masked_sentence = f"The {input_word} is related to the {tokenizer.mask_token}."
    
    # Tokenize the masked sentence
    inputs = tokenizer(masked_sentence, return_tensors='pt')
    
    # Get the index of the mask token
    mask_token_index = torch.where(inputs['input_ids'][0] == tokenizer.mask_token_id)[0].item()
    
    # Predict words for the mask token
    with torch.no_grad():
        output = model(**inputs)
        predictions = output.logits[0, mask_token_index]
    
    # Get the top k predicted words
    top_k_indices = torch.topk(predictions, top_k).indices.tolist()
    related_words = [tokenizer.decode(idx).strip() for idx in top_k_indices]
    safe_related_words = []
    for item in related_words:
        if is_word_safe(item)==True:
            safe_related_words.append(item)
            
    
    # Create the result array
    result = []
    for word in related_words:
        image_url = f'https://fyp-word-images.s3.us-east-2.amazonaws.com/{word}.png'
        audio_url = generate_audio_save_locally(word)
        result.append({
            'word': word,
            'image': image_url,
            'audio': audio_url
        })
    
    
    #connect mongo
    client = pymongo.MongoClient("mongodb+srv://user123:hhCsLKxVQoWDsO2M@hearme.5yquvxf.mongodb.net/")
    db = client['word_card']
    collection = db['card']

    document = {"card_0": result}
    print('---------------')
    print(document)

    collection.delete_many({})
    collection.insert_one(document)

    return result
