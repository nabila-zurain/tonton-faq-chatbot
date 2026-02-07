# 📺 Tonton FAQ Chatbot (RAG-based)

This is a chatbot that answers user questions based on a FAQ document using **Retrieval-Augmented Generation (RAG)**.  
It uses **FAISS** for vector search and **Gemini v2.5** for generating answers.

---

## Features

- Retrieves relevant FAQ chunks for a user query
- Generates answers using the Gemini API
- Simple web interface using **Streamlit**
- Handles questions not in FAQ gracefully

---

## Setup Instructions

1. **Clone this repository:**

```bash
git clone <YOUR_GITHUB_REPO_URL>
cd <YOUR_REPO_FOLDER>
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Prepare the vector store:**

```bash
python ingest.py
```

This will read `faq.txt`, split it into chunks, embed it, and save a FAISS index locally.

4. **Run the chatbot:**

```bash
streamlit run app.py
```

Then open the link provided by Streamlit (usually `http://localhost:8501`) in your browser.

---

## How it works

1. User types a question in the Streamlit app
2. The app retrieves the most relevant FAQ chunks from FAISS
3. Gemini API generates a detailed answer conditioned on those chunks
4. Answer is displayed in the app

---

## Example Usage

**Question:** `Bagaimana cara langganan Tonton?`
**Answer:** `Langkah-langkah untuk melanggan Tonton adalah: ...`

---

## Notes

* Ensure your Gemini API key is valid
* The chatbot currently only uses the FAQ data (`faq.txt`)
* For production, consider adding guardrails for harmful prompts
