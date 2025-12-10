def calculate_engagement(views, likes=None, comments=None, subscribers=None):
    """
    Robust Engagement Formula:
    1. If likes/comments available:
        engagement = (likes + comments) / views * 100
    2. If not available, use views/subscribers ratio (if subscribers given)
    3. Always returns a percentage

    Returns:
        {
            "ratio": float (0.0 - 100.0),
            "text": "5.42% Engagement"
        }
    """

    views = views or 0
    likes = likes or 0
    comments = comments or 0
    subscribers = subscribers or 0

    if views == 0:
        return {"ratio": 0.0, "text": "0% Engagement"}

    if likes > 0 or comments > 0:
        ratio = ((likes + comments) / views) * 100
    elif subscribers > 0:
        ratio = (views / subscribers) * 100
    else:
        ratio = 0.0

    ratio = round(ratio, 2)

    return {"ratio": ratio, "text": f"{ratio}% Engagement"}
