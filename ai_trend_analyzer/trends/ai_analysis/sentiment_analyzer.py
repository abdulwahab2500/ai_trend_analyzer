from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize once per process
analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text, country=None):
    """Analyze sentiment for a text, optionally adjusting for country."""
    if text is None:
        text = ""
    elif not isinstance(text, str):
        text = str(text)

    scores = analyzer.polarity_scores(text)
    compound = scores.get('compound', 0.0)

    # Optional: small country-specific adjustment
    country_multiplier = {
        "US": 1.0,
        "IN": 1.05,
        "PK": 1.03,
        "GB": 0.98,
        "CA": 1.0,
        "AU": 0.97,
        "DE": 0.95,
        "FR": 0.95,
        "JP": 0.92,
        "KR": 0.90,
    }
    if country:
        compound *= country_multiplier.get(country, 1.0)

    # Lower thresholds to reduce Neutral bias
    if compound >= 0.02:
        label = "positive"
    elif compound <= -0.02:
        label = "negative"
    else:
        label = "neutral"

    return {
        "label": label,
        "score": compound,
        "raw": scores,
    }
