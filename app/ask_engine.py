import os
import faiss

from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    ServiceContext,
    load_index_from_storage
)
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.llms.llama_cpp import LlamaCPP


# ---------------- CONFIG ----------------
PROJECT_PATH = "demo_project"
MODEL_PATH = "models/deepseek.gguf"
INDEX_DIR = "faiss_index"
FAISS_FILE = os.path.join(INDEX_DIR, "faiss.index")


# ---------------- LLM ----------------
llm = LlamaCPP(
    model_path=MODEL_PATH,
    temperature=0.1,
    max_new_tokens=300,
    context_window=4096,
)

# ✅ Force use of local LLM (avoid OpenAI)
service_context = ServiceContext.from_defaults(
    llm=llm,
    embed_model="local"
)


# ---------------- INDEX ----------------
if os.path.exists(INDEX_DIR) and os.path.exists(FAISS_FILE):
    print("✅ Loading existing FAISS index...")

    # Reload raw FAISS index
    faiss_index = faiss.read_index(FAISS_FILE)
    vector_store = FaissVectorStore(faiss_index=faiss_index)

    #storage_context = StorageContext.from_defaults(vector_store=vector_store)
    # Reload metadata
    storage_context = StorageContext.from_defaults(
        persist_dir=INDEX_DIR,
        vector_store=vector_store
    )

    index = load_index_from_storage(
        storage_context,
        service_context=service_context
    )

else:
    print("🧠 Creating new FAISS index... (first run is slow)")

    documents = SimpleDirectoryReader(
        PROJECT_PATH,
        required_exts=[".py", ".js"],
        recursive=True
    ).load_data()

    # ✅ Match dimension to your embedding model (384 for local HF, 1536 for OpenAI)
    faiss_index = faiss.IndexFlatL2(384)

    vector_store = FaissVectorStore(faiss_index=faiss_index)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        service_context=service_context
    )

    # Ensure the folder exists
    print("\n\n Creating Dir: ", INDEX_DIR)
    os.makedirs(INDEX_DIR, exist_ok=True)

    # Persist both LlamaIndex metadata and raw FAISS index
    index.storage_context.persist(persist_dir=INDEX_DIR)
    faiss.write_index(faiss_index, FAISS_FILE)

    print("✅ FAISS index created and saved!")


# ---------------- QUERY ENGINE ----------------
query_engine = index.as_query_engine(service_context=service_context)


def ask_question(query: str) -> str:
    print(f"Processing query: {query}", flush=True)
    response = query_engine.query(query)
    print("Finished query!", flush=True)
    return str(response)
