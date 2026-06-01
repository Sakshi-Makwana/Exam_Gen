# In src/uniqueness_filter.py

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def select_unique_questions(generated_questions, n_required):
    """
    Selects a unique set of questions by filtering out semantic duplicates.
    
    Args:
        generated_questions: A list of question data dictionaries 
                             (each dict has "question" and "answer").
        n_required: The final number of unique questions needed.
        
    Returns:
        A list containing the required number of unique questions.
    """
    if len(generated_questions) <= n_required:
        return generated_questions

    # Extract just the question strings for embedding
    question_strings = [q['question'] for q in generated_questions]

    # 1. Embed all generated questions
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = embedder.encode(question_strings, show_progress_bar=False)

    # 2. Calculate cosine similarity between all question pairs
    # This creates a matrix where similarity_matrix[i][j] is the similarity
    # between question i and question j.
    similarity_matrix = cosine_similarity(embeddings)

    # 3. Filter out questions that are too similar
    unique_indices = set(range(len(question_strings)))
    indices_to_remove = set()
    similarity_threshold = 0.95 # We'll consider questions >95% similar as duplicates

    for i in range(len(question_strings)):
        if i in indices_to_remove:
            continue
        for j in range(i + 1, len(question_strings)):
            if j in indices_to_remove:
                continue
            
            if similarity_matrix[i][j] > similarity_threshold:
                # Mark the j-th question for removal
                indices_to_remove.add(j)

    # Create the final list of unique questions
    final_questions = []
    for i in range(len(generated_questions)):
        if i not in indices_to_remove:
            final_questions.append(generated_questions[i])

    # 4. Return the required number of unique questions
    return final_questions[:n_required]