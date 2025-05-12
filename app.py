import streamlit as st
import sounddevice as sd
import scipy.io.wavfile as wavfile
import tempfile
import os
from openai import OpenAI
import pandas as pd
from sentence_transformers import SentenceTransformer, util
import pyttsx3

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Set your key in env or hardcode here

# Constants
AUDIO_DURATION = 5  # seconds
SAMPLE_RATE = 16000
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
WHISPER_MODEL = "whisper-1"
FAQ_FILE = "faq.xlsx"
SIMILARITY_THRESHOLD = 0.7

# Load FAQ and embedding model
@st.cache_resource
def load_faq_data():
    faq_df = pd.read_excel(FAQ_FILE)
    questions = faq_df['Question'].tolist()
    answers = faq_df['Answer'].tolist()
    embedder = SentenceTransformer(EMBEDDING_MODEL)
    embeddings = embedder.encode(questions, convert_to_tensor=True)
    return faq_df, questions, answers, embedder, embeddings

faq_df, questions, answers, embedder, question_embeddings = load_faq_data()

# Text-to-Speech
def speak(text):
    tts = pyttsx3.init()
    tts.say(text)
    tts.runAndWait()

# Audio Recording + Whisper Transcription
def record_and_transcribe():
    st.info("🎙️ Recording for 5 seconds...")
    recording = sd.rec(int(AUDIO_DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='int16')
    sd.wait()

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        wavfile.write(f.name, SAMPLE_RATE, recording)
        audio_path = f.name

    try:
        with open(audio_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model=WHISPER_MODEL,
                language="en",
                file=audio_file
            )
        os.remove(audio_path)
        return transcript.text
    except Exception as e:
        st.error(f"❌ Whisper API Error: {e}")
        return None

# Semantic search for best answer
def get_best_answer(query, threshold):  # You can adjust the threshold as needed
    user_embedding = embedder.encode(query, convert_to_tensor=True)
    scores = util.pytorch_cos_sim(user_embedding, question_embeddings)[0]
    best_score = scores.max().item()
    best_idx = scores.argmax().item()

    if best_score >= threshold:
        return questions[best_idx], answers[best_idx]
    else:
        return None, "Sorry, I couldn't understand. Can you repeat that?"


# UI
st.title("🤖 Voice FAQ Assistant")
st.write("Click the button below to speak your question. The assistant will find the best-matching FAQ answer and read it aloud.")

if st.button("🎤 Ask a Question"):
    user_query = record_and_transcribe()
    if user_query:
        st.success(f"🗣️ You asked: {user_query}")
        matched_q, matched_a = get_best_answer(user_query,SIMILARITY_THRESHOLD)
        if matched_q:
            st.info(f"📌 Matched FAQ: {matched_q}")
        st.success(f"💬 Answer: {matched_a}")
        speak(matched_a)