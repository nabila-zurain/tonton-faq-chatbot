from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# 1. Load FAQ file
with open("faq.txt", "r", encoding="utf-8") as f:
    faq_text = f.read()

# 2. Split text into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100
)

chunks = text_splitter.split_text(faq_text)

# 3. Create embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 4. Store into FAISS vector DB
vectorstore = FAISS.from_texts(chunks, embeddings)

# 5. Save vector DB locally
vectorstore.save_local("faiss_index")

print("✅ FAQ successfully indexed into FAISS")