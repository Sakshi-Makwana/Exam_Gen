from bertopic import BERTopic
from sklearn.feature_extraction.text import CountVectorizer
import nltk

# Download the stopwords list (only needs to be done once)
try:
    nltk.data.find('corpora/stopwords')
except nltk.downloader.DownloadError:
    nltk.download('stopwords')

def get_document_topics(text_chunks, num_topics=20):
    """
    Analyzes text chunks to find the main topics using BERTopic,
    while ignoring common English stop words.
    """
    
    # --- TOPIC MODEL IMPROVEMENT ---
    # Create a vectorizer that knows to ignore common English words.
    # This is the key to generating clean, meaningful topics.
    vectorizer_model = CountVectorizer(stop_words="english")

    # Initialize BERTopic with our new vectorizer.
    topic_model = BERTopic(
        vectorizer_model=vectorizer_model,
        min_topic_size=3, 
        nr_topics=num_topics, 
        verbose=True
    )
    # --- END OF IMPROVEMENT ---

    # Fit the model to find topics
    topics, _ = topic_model.fit_transform(text_chunks)

    # Get the topic info
    topic_info = topic_model.get_topic_info()
    
    # Extract and clean the topic names
    topic_names = []
    for index, row in topic_info.iterrows():
        if row['Topic'] != -1:
            clean_name = row['Name'].split('_', 1)[1].replace('_', ', ')
            topic_names.append(clean_name)
            
    if not topic_names:
        return ["general concepts"] # Fallback

    return topic_names