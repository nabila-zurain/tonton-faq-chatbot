# ingest.py
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# 1️⃣ Load FAQ file
with open("faq.txt", "r", encoding="utf-8") as f:
    faq_text = f.read()

# 2️⃣ Split text into chunks (keep paragraphs and numbered steps intact)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,          # larger chunk to avoid splitting steps
    chunk_overlap=50,
    separators=["\n\n", "\n", "Question:", ".", " "],  # Add "Question:" as a strong separator
)
chunks = text_splitter.split_text(faq_text)

# 3️⃣ Create embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 4️⃣ Store into FAISS vector DB
vectorstore = FAISS.from_texts(chunks, embeddings)

# 5️⃣ Save vector DB locally
vectorstore.save_local("faiss_index")

print("✅ FAQ successfully indexed into FAISS")