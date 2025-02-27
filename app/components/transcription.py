import requests
from utils.config import API_BASE_URL

def transcribe_audio(audio_data, file_name):
    """
    Calls the transcription API with the given audio file.
    """
    url = f"{API_BASE_URL}/transcribe"
    files = {"file": (file_name, audio_data, "audio/mp3" if file_name.endswith(".mp3") else "audio/wav")}
    
    try:
        response = requests.post(url, files=files)
        response.raise_for_status()

        # print("API Response:", response.json()) 
        json_data = response.json()

        original_transcript = json_data.get("transcript_original", "")
        checked_transcript = json_data.get("transcript_checked", "")

        # print("Original Transcript:", original_transcript)
        # print("Checked Transcript:", checked_transcript)

        return original_transcript, checked_transcript
    
    except Exception as e:
        return f"Error during transcription: {e}"
