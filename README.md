📢 Voice AI FAQ Assistant
An interactive Voice AI application built with Streamlit, OpenAI Whisper, and sentence-transformers, which listens to a user's question, transcribes it, finds the most relevant FAQ from an Excel file, and replies using text-to-speech.

🚀 Features
🎤 Voice input from microphone

🔊 Voice output using Text-to-Speech

📁 FAQ loaded from an Excel file

🤖 Semantic search using Sentence Transformers

🧠 Uses OpenAI Whisper (local or API) for speech-to-text

❌ Gracefully handles unmatched queries

🛠️ Tech Stack
Streamlit — UI

Whisper — Speech-to-text (local or API)

sentence-transformers — Semantic question matching

pyttsx3 — Offline text-to-speech

pandas — Reading FAQ data from Excel

torch — Backend for embeddings

📂 Project Structure
voice-ai-faq/
├── app.py                  # Main Streamlit app
├── faq.xlsx                # Excel file with FAQs
├── requirements.txt        # All dependencies
└── .env


💻 Setup Instructions
1. Clone the Repo
git clone https://github.com/karan00713/voice_assistant.git
cd voice_assistant
2. Create a Virtual Environment
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
3. Install Dependencies
pip install -r requirements.txt
4. ENV creation
create .env file in the root directory, add OPENAI_API_KEY="sk-uj4b...jd" # Your API KEY
5. Run the App
streamlit run app.py


🙋‍♂️ Example Usage
Click "🎤 Ask a Question"

Speak into your mic (e.g., "What are your opening hours?")

The assistant will:

Transcribe your voice

Match it with the FAQ

Speak the answer aloud