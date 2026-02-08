# app.py
import streamlit as st
import requests
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# =========================
# Gemini API setup
# =========================
API_KEY = "AIzaSyAswOdUfkTOUfVexwMI3UsWzyWjsddLabQ"
GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/"
    "models/gemini-2.5-flash:generateContent"
)

# =========================
# Load vector database
# =========================
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

# =========================
# Helper functions
# =========================
BLACKLIST = ["hack", "malware", "virus", "http://", "https://", "<script>"]

def is_safe_input(user_input: str) -> bool:
    """Check for malicious content in the user input."""
    return not any(word in user_input.lower() for word in BLACKLIST)

def get_answer(user_question: str, vectorstore) -> str:
    """Retrieve relevant chunks from FAISS and call Gemini API to generate answer."""
    
    # Retrieve top 6 most similar chunks
    docs = vectorstore.similarity_search(user_question, k=6)
    context = "\n\n".join([doc.page_content for doc in docs])
    
    # Build prompt for Gemini
    prompt = f"""
Anda ialah chatbot sokongan pelanggan.

Jawab soalan pengguna berdasarkan maklumat FAQ di bawah SAHAJA.
Jika soalan berbentuk "bagaimana" atau "langkah-langkah",
senaraikan SEMUA langkah secara terperinci.

Jika maklumat tiada, jawab:
"Maaf, maklumat tidak ditemui dalam FAQ."

Maklumat FAQ:
{context}

Soalan pengguna:
{user_question}
"""

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY
    }

    data = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

    try:
        response = requests.post(GEMINI_URL, headers=headers, json=data)
        response.raise_for_status()
        answer = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        return answer
    except requests.exceptions.RequestException as e:
        return f"❌ Error calling Gemini API: {e}"
    except (KeyError, IndexError):
        return "❌ Unexpected response format from Gemini API."

# =========================
# Streamlit UI
# =========================
st.set_page_config(page_title="📺 Tonton FAQ Chatbot", layout="wide")
st.title("📺 Tonton FAQ Chatbot")
st.write("Tanya sebarang soalan berkaitan langganan Tonton")

user_question = st.text_input("Soalan anda:")

if user_question:
    if is_safe_input(user_question):
        answer = get_answer(user_question, vectorstore)
        st.success(answer)
    else:
        st.warning("❌ Input tidak dibenarkan. Sila tanya soalan FAQ yang biasa.")
