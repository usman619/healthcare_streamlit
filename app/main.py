import streamlit as st
from components.audio_input import audio_input, upload_audio
from components.transcription import transcribe_audio
from components.translation import translate_transcript
from gtts import gTTS
import tempfile

st.title("Healthcare Translation Web App with Generative AI")

with st.expander("Project Description"):
    st.markdown("""
    # Healthcare Translation Web App 🏥

    A FastAPI and Streamlit–based application that provides real-time medical transcription and translation services.

    ## Features 🌟

    - **Audio Input & Processing**
    - Real-time voice recording via microphone
    - Support for both WAV and MP3 file uploads
    - Chunked audio processing for long recordings
    - Audio duration validation

    - **Transcription Capabilities**
    - Speech-to-text conversion with real-time feedback
    - Medical terminology validation
    - Grammar and punctuation correction
    - Support for multiple audio formats

    - **Translation Services**
    - Multi-language support (11+ languages)
    - Medical context–aware translations
    - Real-time translation processing
    - Customizable source and target language selection

    - **Audio Output**
    - Text-to-speech conversion for translated text
    - Downloadable translated audio
    - Audio playback controls
    - Support for multiple accents

    - **User Interface**
    - Mobile-responsive design
    - Dual transcript display (original and corrected)
    - Real-time processing indicators
    - Intuitive language selection

    ## Architecture 🏗️
    """)
    
    st.image("screenshots/a_diagram.png", caption="Architecture Diagram")
    st.markdown("""
    ## Tech Stack 🛠️

    - **Backend Framework**: FastAPI
    - **AI Services**: 
    - Google Speech Recognition
    - Google Gemini AI
    - **Audio Processing**: pydub
    - **Frontend: Streamlit**: Streamlit
    - **Environment**: Python 3.8+

    ## Project Structure 📁

    ```
    healthcare_translation_web_app/
    ├── server/
    │   ├── routes/
    │   │   ├── transcribe.py      # Audio transcription endpoint
    │   │   └── translate.py       # Translation endpoint
    │   └── server.py              # Main server configuration
    ├── streamlit_app/
    │   ├── components/
    │   │   ├── audio_input.py     # Audio input options (record/upload)
    │   │   ├── transcription.py   # Calls transcription API
    │   │   └── translation.py     # Calls translation API
    │   ├── utils/
    │   │   └── config.py          # Configuration constants (e.g., API_BASE_URL)
    │   └── app.py                 # Main Streamlit app
    ├── .env                       # Environment variables
    └── README.md                  # Project documentation
    ```

    ## API Endpoints 🔌

    ### Transcription

    ```http
    POST /transcribe/
    ```

    - Accepts WAV/MP3 audio files
    - Returns original and corrected transcripts
    - Handles medical terminology validation

    ### Translation

    ```http
    POST /translate/
    ```
    - Accepts source language, target language, and text to be translated
    - Returns the translated text

    ## Setup & Installation 💻

    1. Clone the repository:
    ```bash
    git clone https://github.com/usman619/healthcare_web_app
    cd healthcare_web_app
    ```

    2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

    3. Install ffmpeg in conda or on your device
    ```bash
    conda install -c conda-forge ffmpeg
    ```
    ```bash
    sudo apt-get update
    sudo apt-get install ffmpeg
    ```

    4. Configure environment variables:
    ```bash
    cp .env.example .env
    # Edit .env with your API keys
    ```

    5. Start the server:
    ```bash
    cd server
    fastapi dev server.py
    ```

    6. Start the Streamlit app:
    ```bash
    cd ../streamlit_app
    streamlit run app.py
    ```

    ## Environment Variables 🔐

    Required environment variables in `.env`:
    - `GEMINI_API_KEY`: Google Gemini AI API key
    - `API_BASE_URL`: The base URL of your FastAPI server (including the port)

    ## API Documentation 📚

    Access the interactive API documentation:
    - Swagger UI: `http://localhost:8000/docs`
    - ReDoc: `http://localhost:8000/redoc`

    ## Deployment 🖥️
    **FastAPI code**: [healthcare_server](https://github.com/usman619/healthcare_server)
    **Streamlit code**: [healthcare_streamlit](https://github.com/usman619/healthcare_streamlit)

    **Streamlit frontend Link**: https://healthcare-translation-web-app.streamlit.app/

    I have deployed this project using [Streamlit](https://streamlit.io/) for the frontend and [Railway](https://railway.com/) for the backend.

    Streamlit deployment was simple and but I am having issues with `healthcare_server` deployment. I have tested it by creating docker image and testing it locally and that is working perfectly. The following are the deployment images on `railway.com` and 

    - Railway server deployment:

    """)   
    st.image("screenshots/railway_deployment_1.png", caption="Railway server deployment")

    st.markdown("- The main issue is `ffmpeg` not working correctly which is resulting in the APIs not working once deployed:")
    st.image("screenshots/railway_deployment_2.png", caption="Railway server deployment")

    st.markdown("This is the docker image creation and testing locally:")
    st.image("screenshots/creating_docker_image.png", caption="Creating docker image")
    st.image("screenshots/running_docker_image.png", caption="Running docker image")

    st.markdown("This is the Healthcare Translation Web App working output:")
    st.image("screenshots/healtcare_app_1.png", caption="Healthcare Translation Web App working output")
    st.image("screenshots/healtcare_app_2.png", caption="Healthcare Translation Web App working output")
    st.image("screenshots/healtcare_app_3.png", caption="Healthcare Translation Web App working output")

# ================== Initialize Session State ==================
if "original_transcript" not in st.session_state:
    st.session_state.original_transcript = ""
if "checked_transcript" not in st.session_state:
    st.session_state.checked_transcript = ""
if "translation" not in st.session_state:
    st.session_state.translation = ""

# ================== Upload an Audio File ==================
# st.header("Audio Input")
# upload_audio_button = st.button("Upload an Audio File")
# if upload_audio_button:
#     audio_data, file_name = upload_audio()

#     if audio_data:
#         st.audio(audio_data, format="audio/wav")

#         if st.button("Transcribe Audio"):
#             with st.spinner("Transcribing audio... Please wait"):
#                 original, checked = transcribe_audio(audio_data, file_name)
            
#             st.success("Transcription completed!")

#             # Store in session state
#             st.session_state.original_transcript = original
#             st.session_state.checked_transcript = checked

# ================== Record a Voice Message ==================
audio_value = st.audio_input("Record a voice message...")
if audio_value:
    st.audio(audio_value, format="audio/wav")
    audio_data = audio_value.read()
    file_name = "recorded_audio.wav"  # Use a default file name

    if st.button("Transcribe Audio"):
        with st.spinner("Transcribing audio... Please wait"):
            original, checked = transcribe_audio(audio_data, file_name)
        
        st.success("Transcription completed!")

        # Store in session state
        st.session_state.original_transcript = original
        st.session_state.checked_transcript = checked

# ================== Display Transcripts ==================
st.text_area("Transcription Result (Original)", st.session_state.original_transcript, height=200)
st.text_area("Checked Transcription (Post-processing: Grammar and Medical Vocabulary)", st.session_state.checked_transcript, height=200)

# ================== Translation ==================
st.header("Translation")

transcript_to_translate = st.selectbox("Select transcript to translate:", ["Original", "Checked"])
transcript = st.session_state.original_transcript if transcript_to_translate == "Original" else st.session_state.checked_transcript

source_lang = st.selectbox("Select source language:", ["English", "Urdu", "Spanish", "French", "German", "Italian", "Japanese", "Korean", "Portuguese", "Russian", "Chinese"])
target_lang = st.selectbox("Select target language:", ["English", "Urdu", "Spanish", "French", "German", "Italian", "Japanese", "Korean", "Portuguese", "Russian", "Chinese"])

if st.button("Translate"):
    if not transcript:
        st.warning("Please transcribe an audio file before translating.")
    else:
        with st.spinner("Translating... Please wait"):
            st.session_state.translation = translate_transcript(transcript, source_lang, target_lang)
        
        st.success("Translation completed!")

st.text_area("Translation Result", st.session_state.translation, height=200)

# ================== Audio Playback ==================
if st.session_state.translation:
    if st.button("Speak Translation"):
        with st.spinner("Generating speech... Please wait"):
            tts = gTTS(text=st.session_state.translation, lang=target_lang[:2].lower())  # Convert target language to short code
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tts.save(temp_file.name)
        
        st.audio(temp_file.name, format="audio/mp3")
        st.success("Audio generated!")

        # Download the audio file
        with open(temp_file.name, "rb") as file:
                    st.download_button(
                        label="Download Audio",
                        data=file,
                        file_name="translated_speech.mp3",
                        mime="audio/mp3"
                    )
