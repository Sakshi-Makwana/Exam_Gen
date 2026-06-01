import chromadb

def create_vector_store(chunks, embeddings):
    """
    Creates a vector store from text chunks and their embeddings.
    
    Args:
        chunks: The list of original text chunks.
        embeddings: The list of embeddings corresponding to the chunks.
        
    Returns:
        The ChromaDB collection object.
    """
    # Create a new in-memory ChromaDB client
    client = chromadb.Client()
    
    # Create a new collection or get it if it already exists
    collection = client.get_or_create_collection("exam_docs")
    
    # Generate unique IDs for each chunk
    ids = [str(i) for i in range(len(chunks))]
    
    # Add the documents and their embeddings to the collection
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids
    )
    
    return collection