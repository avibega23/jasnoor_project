import time as t
import streamlit as st
from moviepy import VideoFileClip
import speech_recognition as sr
from translate import Translator
from gtts import gTTS


def extract_audio(video_path, output_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    if audio is None:
        raise ValueError("The video file has no audio stream.")
    audio.write_audiofile(output_path)
    video.close()
    return output_path

def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition service; {e}"

def translate_text(text, source_lang, target_lang):
    translator = Translator(from_lang=source_lang, to_lang=target_lang)

    chunk_size = 500
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

    translated_chunks = []
    for chunk in chunks:
        translated_chunk = translator.translate(chunk)
        translated_chunks.append(translated_chunk)

    translated_text = " ".join(translated_chunks)
    return translated_text

def text_to_speech(text, lang='hi', output_path='output_audio.mp3'):
    tts = gTTS(text=text, lang=lang)
    tts.save(output_path)
    return output_path

def main():
    page_bg_color = '''
    <style>
    .stApp {
        background-color: white;
    }
    .title-section img {
        height: 50px;
        margin-right: 20px;
    }
    .title-section {
        background-color: darkblue;
        padding: 20px;
        text-align: center;
    }
    .title {
        color: white;
        font-size: 3em;
        font-weight: bold;
    }
    .subheader {
        color: maroon;
        font-size: 1.5em;
        font-weight: bold;
    }
    .text {
        color: navy;
        font-size: 1.2em;
    }
    </style>
    '''

    st.set_page_config(page_title="Video Language Converter", page_icon=":movie_camera:", layout="wide")
    st.markdown(page_bg_color, unsafe_allow_html=True)

    st.markdown('''
        <div class="title-section">
            <h1 class="title">Video Language Converter</h1>
        </div>
    ''', unsafe_allow_html=True)
    st.write("##")
    st.markdown('<p class="text">Upload a video, and we will convert its audio from English to Hindi.</p>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi", "mkv"])
    st.write("---")
    
    if uploaded_file is not None:
        with st.spinner("Processing video and extracting audio..."):
            t.sleep(2)
        st.video(uploaded_file)
        video_path = "uploaded_video.mp4"
        with open(video_path, "wb") as f:
            f.write(uploaded_file.read())

        st.subheader("English audio: :headphones:")
        audio_path = "extracted_audio.wav"
        extract_audio(video_path, audio_path)

        st.audio(audio_path)
        with st.spinner("Transcripting audio..."):
            t.sleep(2)

        transcribed_text = transcribe_audio(audio_path)
        if transcribed_text == "Could not understand audio":
            st.error("Could not understand audio. Please try again.")
        
        st.markdown('<h2 class="subheader">Transcribed Text:</h2>', unsafe_allow_html=True)
        st.markdown(f'<p class="text">{transcribed_text}</p>', unsafe_allow_html=True)

        st.success("TRANSCRIPTION IS SUCCESSFULLY DONE.")
        st.write("---")
        
        with st.spinner("Translating..."):
            t.sleep(2)

        translated_text = translate_text(transcribed_text, "en", "hi")
        st.markdown('<h2 class="subheader">Translated Text:</h2>', unsafe_allow_html=True)
        st.markdown(f'<p class="text">{translated_text}</p>', unsafe_allow_html=True)
        st.success("TRANSLATION IS SUCCESSFULLY DONE.")
        
        with st.spinner("Processing audio..."):
            t.sleep(2)
        st.subheader("Hindi audio: :headphones:")
        hindi_audio_path = text_to_speech(translated_text, lang='hi', output_path='hindi_audio.mp3')
        st.audio(hindi_audio_path)
        st.write("---")
        st.subheader("Thank you! :smile:")

if __name__ == "__main__":
    main()
