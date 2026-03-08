"""
Sprint 0 Pipeline Proof Script

Simple demonstration that the core RAG pipeline works:
- Load markdown documents
- Chunk text
- Generate embeddings
- Store in vector database
- Retrieve relevant results

Run: python prove_pipeline_simple.py
"""
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()


def main() -> None:
    """Execute the RAG pipeline proof of concept."""
    print("🔍 Sprint 0: Proving RAG Pipeline\n")
    print("✅ Using FREE local embeddings (HuggingFace)")
    print("   Model: all-MiniLM-L6-v2")
    print("   Cost: $0 - No API key needed!\n")

    # Load documents from synthetic-docs directory
    print("\n📁 Loading synthetic docs...")
    docs_path = Path(__file__).parent.parent / "synthetic-docs"

    if not docs_path.exists():
        print(f"❌ ERROR: Synthetic docs not found at {docs_path}")
        return

    loader = DirectoryLoader(
        str(docs_path),
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    documents = loader.load()

    if not documents:
        print("❌ ERROR: No markdown files loaded")
        return

    print(f"✅ Loaded {len(documents)} documents")

    # Split documents into chunks
    print("\n✂️  Chunking documents...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,
        separators=["\n\n", "\n", " ", ""],
    )
    chunks = splitter.split_documents(documents)
    print(f"✅ Created {len(chunks)} chunks")

    # Generate embeddings and store in vector database
    print("\n🧠 Generating embeddings (first run downloads model ~90MB, then fast)...")
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./chroma_db_test",
    )
    print("✅ Generated embeddings and stored in Chroma")

    # Test retrieval with sample query
    print("\n🔎 Testing retrieval...")
    query = "How do I set up my development environment?"
    results = vectorstore.similarity_search(query, k=3)

    if not results:
        print("❌ ERROR: No results retrieved")
        return

    print(f"✅ Retrieved {len(results)} relevant chunks")
    print(f"\nQuery: '{query}'")
    print("\nTop result:")
    print(f"  Source: {results[0].metadata.get('source', 'unknown')}")
    print(f"  Content: {results[0].page_content[:200]}...")

    # Success summary
    print("\n" + "=" * 60)
    print("🎉 SUCCESS! Core RAG pipeline is functional!")
    print("=" * 60)
    print("\n💰 Total cost: $0 (using free local embeddings)")
    print("\nNext steps:")
    print("  1. Create GitHub repo")
    print("  2. Share with quantic-grader")
    print("  3. Sign up for free Groq API (14,400 requests/day)")
    print("  4. Begin Sprint 1 implementation")


if __name__ == "__main__":
    main()
