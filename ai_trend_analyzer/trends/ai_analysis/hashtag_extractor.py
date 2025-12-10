import re
from collections import Counter

def extract_hashtags(video_list, top_n=10):
    """
    Extract trending hashtags based on video content, categories, and viral patterns.
    Analyzes video titles, descriptions, categories, and engagement to find what's actually trending.
    Returns list of tuples: [(hashtag, count), ...]
    """
    # Extended stopwords list
    stopwords = {
        "the", "and", "you", "your", "with", "for", "from", "this", "that", 
        "what", "when", "where", "how", "are", "was", "will", "has", "have",
        "but", "not", "they", "been", "more", "can", "all", "just", "now",
        "get", "like", "about", "out", "new", "who", "its", "some", "than",
        "here", "there", "why", "my", "me", "we", "our", "us", "am", "is", "be",
        "do", "did", "does", "made", "make", "makes", "day", "time", "year",
        "way", "one", "two", "best", "top", "most", "see", "look", "watch"
    }
    
    # If video_list is actually a list of strings (titles), convert format
    if video_list and isinstance(video_list[0], str):
        video_list = [{"title": title, "description": ""} for title in video_list]
    
    trending_terms = []
    category_tags = []
    
    # Extract from actual hashtags first
    actual_hashtags = []
    for video in video_list:
        if isinstance(video, dict):
            title = video.get("title", "")
            description = video.get("description", "")
            text = f"{title} {description}"
        else:
            text = str(video)
        
        # Extract actual hashtags
        tags = re.findall(r"#(\w+)", text)
        actual_hashtags.extend([tag.lower() for tag in tags])
    
    if actual_hashtags:
        return Counter(actual_hashtags).most_common(top_n)
    
    # Analyze video data for trending topics
    for video in video_list:
        if not isinstance(video, dict):
            continue
            
        title = video.get("title", "").lower()
        description = video.get("description", "").lower()
        category = video.get("categoryName", "")
        engagement = video.get("engagement_score", 0)
        
        # Extract meaningful phrases and words
        combined_text = f"{title} {description}"
        
        # Look for capitalized words/phrases (often important topics)
        important_words = re.findall(r'\b[A-Z][a-z]+\b', video.get("title", ""))
        trending_terms.extend([word.lower() for word in important_words])
        
        # Extract all meaningful words (3+ chars)
        words = re.findall(r'\b[a-zA-Z]{3,}\b', combined_text)
        
        # Weight words by engagement score (high engagement = more important)
        engagement_weight = max(1, int(engagement / 2))  # Weight based on engagement
        for word in words:
            if word not in stopwords and len(word) > 3:
                trending_terms.extend([word] * engagement_weight)
        
        # Add category as potential hashtag
        if category and category not in ["Miscellaneous", "Unknown"]:
            category_clean = category.lower().replace(" & ", "").replace(" ", "")
            category_tags.append(category_clean)
    
    # Combine category tags with trending terms
    all_tags = trending_terms + category_tags * 3  # Weight categories higher
    
    if all_tags:
        # Get most common, filter out very short or stopwords
        common_tags = Counter(all_tags).most_common(top_n * 2)
        filtered_tags = [
            (tag, count) for tag, count in common_tags 
            if len(tag) > 3 and tag not in stopwords
        ]
        return filtered_tags[:top_n]
    
    return []  # Return empty list if nothing found


def extract_hashtags_from_titles(text_list, top_n=10):
    """
    Legacy function for backward compatibility.
    Extracts hashtags from list of title strings.
    """
    # Convert text list to video format
    video_list = [{"title": text, "description": ""} for text in text_list]
    return extract_hashtags(video_list, top_n)
