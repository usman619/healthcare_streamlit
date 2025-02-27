import streamlit as st


def audio_input():
    # Check if we already stored a recording in session_state.
    if "recorded_audio" not in st.session_state:
        # Use a unique key for the audio input widget
        recorded_file = st.audio_input("Speak into your microphone...", key="audio_input")
        if recorded_file is not None:
            # Read the audio bytes
            audio_bytes = recorded_file.read()
            # Store the audio and filename in session_state for persistence
            st.session_state["recorded_audio"] = audio_bytes
            st.session_state["recorded_file_name"] = getattr(recorded_file, "name", "recorded_audio.wav")
            return audio_bytes, st.session_state["recorded_file_name"]
        else:
            return None, None
    else:
        # Return the stored audio if it exists
        return st.session_state["recorded_audio"], st.session_state["recorded_file_name"]

def upload_audio():
    st.subheader("Upload an Audio File")
    uploaded_file = st.file_uploader("Choose an audio file...", type=["mp3", "wav"])
    
    if uploaded_file is not None:
        audio_bytes = uploaded_file.read()
        return audio_bytes, uploaded_file.name
    else:
        return None, None