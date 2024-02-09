import requests
import json

def is_word_safe(word):
    # Replace the placeholder values with your Azure Content Moderator endpoint and key
    endpoint = "https://hearmeinstance.cognitiveservices.azure.com/"
    subscription_key = "8d339b48de6d401f801459770e345532"

    # Construct the URL for text moderation
    url = f"{endpoint}/contentmoderator/moderate/v1.0/ProcessText/Screen?language=eng&classify=True"

    # Prepare the headers
    headers = {
        'Content-Type': 'text/plain',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }

    # Make the POST request to the API
    response = requests.post(url, headers=headers, data=word)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response
        result = response.json()

        # Check for the presence of Terms that are not safe
        if result.get('Terms'):
            return False
        else:
            return True
    else:
        # In case of a failure, return None
        return None, f"Error: {response.text}"


