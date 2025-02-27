import requests
from utils.config import API_BASE_URL

def translate_transcript(transcript, source_lang, target_lang):
    """
    Calls the translation API with the given transcript and language options.
    """
    url = f"{API_BASE_URL}/translate"
    data = {
        "text": transcript,
        "source_lang": source_lang,
        "target_lang": target_lang
    }
    
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        translation = response.json().get("translation", "")
        return translation
    except Exception as e:
        return f"Error during translation: {e}"
