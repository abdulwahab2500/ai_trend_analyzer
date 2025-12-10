import re
from collections import Counter

def extract_keywords(video_titles, top_n=10):
    """
    Analyze and return most common keywords in trending video titles.
    """
    text = " ".join(video_titles).lower()
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text)  # only words with 3+ letters
    stopwords = {"the", "and", "you", "your", "with", "for", "from", "this", "that", "what", "when", "where", "how", "are", "was", "will", "has"}
    words = [w for w in words if w not in stopwords]
    return Counter(words).most_common(top_n)
