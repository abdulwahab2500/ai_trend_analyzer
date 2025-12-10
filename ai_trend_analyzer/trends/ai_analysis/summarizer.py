def generate_trend_summary(videos, keywords, hashtags):
    """
    Creates a short summary of what is trending this week.
    Handles missing categories, keywords, hashtags, and engagement data.
    """

    if not videos:
        return "No trending data available to summarize."

    # Initialize counts
    sentiments = {"Positive": 0, "Neutral": 0, "Negative": 0}
    categories = {}
    total_engagement = 0
    count_engaged = 0

    for v in videos:
        # Sentiment counting
        label = v.get("sentiment", {}).get("label", "")
        if label in sentiments:
            sentiments[label] += 1

        # Category counting
        cat = v.get("categoryName")
        if not cat or cat.strip() == "":
            cat = "Miscellaneous"  # fallback if category is missing
        categories[cat] = categories.get(cat, 0) + 1

        # Engagement calculation
        if "engagement_score" in v and isinstance(v["engagement_score"], (int, float)):
            total_engagement += v["engagement_score"]
            count_engaged += 1

    # Determine top category and dominant sentiment
    top_category = max(categories, key=categories.get)
    dominant_sentiment = max(sentiments, key=sentiments.get)
    avg_engagement = round(total_engagement / (count_engaged or 1), 2)

    # Process keywords
    keyword_list = []
    for kw in keywords[:5]:
        if isinstance(kw, tuple):
            keyword_list.append(kw[0])
        else:
            keyword_list.append(str(kw))
    keywords_text = ', '.join(keyword_list) if keyword_list else "N/A"

    # Process hashtags
    hashtag_list = []
    for ht in hashtags[:5]:
        if isinstance(ht, tuple):
            hashtag_list.append(ht[0])
        else:
            hashtag_list.append(str(ht))
    hashtags_text = ', '.join(hashtag_list) if hashtag_list else "N/A"

    # Build summary
    summary = (
        f"This week, **{top_category}** content is dominating the trends. "
        f"The overall audience mood is **{dominant_sentiment.lower()}**. "
        f"Average engagement across videos is **{avg_engagement}%**, with users interacting strongly with trending posts. "
        f"Popular keywords include: {keywords_text}. "
        f"Top hashtags: {hashtags_text}. "
        "Overall, this week shows strong activity and clear viewer interest patterns."
    )

    return summary
