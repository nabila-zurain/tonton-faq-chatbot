import streamlit as st
import requests
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# =========================
# Streamlit config
# =========================
st.set_page_config(page_title="📺 Tonton FAQ Chatbot", layout="wide")

# =========================
# Gemini API setup
# =========================
API_KEY = st.secrets["GEMINI_API_KEY"]

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
# UI
# =========================
st.title("📺 Tonton FAQ Chatbot")
st.write("Tanya sebarang soalan berkaitan langganan Tonton")

user_question = st.text_input("Soalan anda:")

if user_question:
    # =========================
    # 1. Retrieve relevant chunks
    # =========================
    docs_and_scores = vectorstore.similarity_search_with_score(
        user_question, k=6
    )

    # Guardrail: no good match
    if not docs_and_scores or docs_and_scores[0][1] > 0.6:
        st.warning("Maaf, maklumat tidak ditemui dalam FAQ.")
        st.stop()

    docs = [doc for doc, score in docs_and_scores]
    context = "\n\n".join([doc.page_content for doc in docs])

    # =========================
    # 2. Build prompt
    # =========================
    prompt = f"""
Anda ialah chatbot sokongan pelanggan.

Jawab soalan pengguna BERDASARKAN MAKLUMAT FAQ DI BAWAH SAHAJA.
JANGAN guna pengetahuan luar.

Jika maklumat tiada atau tidak berkaitan, jawab:
"Maaf, maklumat tidak ditemui dalam FAQ."

Maklumat FAQ:
{context}

Soalan pengguna:
{user_question}
"""

    # =========================
    # 3. Call Gemini API
    # =========================
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY
    }

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    response = requests.post(
        GEMINI_URL,
        headers=headers,
        json=payload,
        timeout=30
    )

    if response.status_code == 200:
        answer = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        st.success(answer)
    else:
        st.error(f"❌ Gemini API error: {response.status_code}")
