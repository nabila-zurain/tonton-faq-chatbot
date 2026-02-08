import streamlit as st
import requests
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

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
# Streamlit UI
# =========================
st.title("📺 Tonton FAQ Chatbot")
st.header("Tanya sebarang soalan berkaitan langganan Tonton")
st.subheader("Soalan anda:")
user_question = st.text_input("")

if user_question:
    # 1. Retrieve relevant FAQ chunks
    docs = vectorstore.similarity_search(user_question, k=6)
    context = "\n\n".join([doc.page_content for doc in docs])

    # 2. Build prompt
    prompt = f"""
Anda ialah chatbot sokongan pelanggan.

Gunakan maklumat di bawah sahaja untuk menjawab soalan pengguna.
Jika jawapan berbentuk senarai atau langkah-langkah, senaraikan SEMUA langkah secara lengkap.
Jika maklumat tiada, jawab: "Maaf, maklumat tidak ditemui dalam FAQ."

Maklumat FAQ:
{context}

Soalan pengguna:
{user_question}

Sila pastikan jawapan lengkap dan tidak dipotong.
"""

    # 3. Call Gemini API
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY
    }

    data = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    response = requests.post(GEMINI_URL, headers=headers, json=data)

    if response.status_code == 200:
        answer = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        st.success(answer)
    else:
        st.error("❌ Error calling Gemini API")