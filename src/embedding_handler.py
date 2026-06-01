from sentence_transformers import SentenceTransformer
import numpy as np

def create_embeddings(chunks):
    """
    Creates embeddings for a list of text chunks using a pre-trained model.
    
    Args:
        chunks: A list of text strings.
        
    Returns:
        A list of embeddings, where each embedding is a numerical vector.
    """
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    
    # The model generates embeddings as numpy arrays, which we convert to lists
    embeddings = embedder.encode(chunks, show_progress_bar=True)
    
    # It's good practice to convert to a list of lists for compatibility
    return embeddings.tolist()