import streamlit as st
from components.audio_input import audio_input, upload_audio
from components.transcription import transcribe_audio
from components.translation import translate_transcript
from gtts import gTTS
import tempfile

st.title("Healthcare Translation Web App with Generative AI")

with st.expander("Project Description"):
    st.markdown("""
    ## Core Functionalities:

    Voice-to-Text with Generative AI: Convert spoken input into a text transcript, using AI to enhance transcription accuracy, especially for medical terms.
    Real-Time Translation and Audio Playback: Provide real-time translation of the transcript with a "Speak" button for audio playback.
    Mobile-First Design: Ensure the app is responsive and optimized for mobile and desktop use.

    ## User Interface and Experience:

    - **Dual Transcript Display:** Show both original and translated transcripts in real-time.
    - **Speak Button:** Accessible for audio playback of translated text.
    - **Language Selection:** Allow users to choose input and output languages easily.

    ## Technical Requirements:

    - **Generative AI Tools:** Use generative AI (e.g., OpenAI API or similar) for both translation and coding assistance.
    - **Speech Recognition API:** Integrate a speech recognition API (e.g., Web Speech API or Google Speech-to-Text).
    - **Deployment Platform:** Deploy on a platform like Vercel, V0, or Cursor. Provide a live link.
    - **Data Privacy and Security:** Ensure patient confidentiality with basic security measures.

    ## Testing and Quality Assurance:

    - Ensure transcription, translation, and audio playback functions work as intended.
    - Include error handling for transcription or translation failures.
""")

# ================== Initialize Session State ==================
if "original_transcript" not in st.session_state:
    st.session_state.original_transcript = ""
if "checked_transcript" not in st.session_state:
    st.session_state.checked_transcript = ""
if "translation" not in st.session_state:
    st.session_state.translation = ""

# ================== Upload an Audio File ==================
st.header("Audio Input")
upload_audio_button = st.button("Upload an Audio File")
if upload_audio_button:
    audio_data, file_name = upload_audio()

    if audio_data:
        st.audio(audio_data, format="audio/wav")

        if st.button("Transcribe Audio"):
            with st.spinner("Transcribing audio... Please wait"):
                original, checked = transcribe_audio(audio_data, file_name)
            
            st.success("Transcription completed!")

            # Store in session state
            st.session_state.original_transcript = original
            st.session_state.checked_transcript = checked

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
