from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from .youtube_fetcher import fetch_trending_videos
from .ai_analysis.keyword_analyzer import extract_keywords
from .ai_analysis.hashtag_extractor import extract_hashtags
from .ai_analysis.sentiment_analyzer import analyze_sentiment
from .ai_analysis.engagement_calculator import calculate_engagement
from .ai_analysis.summarizer import generate_trend_summary  # ✅ AI summarizer


def home(request):
    # Country dropdown
    countries = {
        "US": "United States",
        "IN": "India",
        "PK": "Pakistan",
        "GB": "United Kingdom",
        "CA": "Canada",
        "AU": "Australia",
        "DE": "Germany",
        "FR": "France",
        "JP": "Japan",
        "KR": "South Korea",
    }

    # YouTube Categories
    categories = {
        "1": "Film & Animation",
        "2": "Autos & Vehicles",
        "10": "Music",
        "17": "Sports",
        "20": "Gaming",
        "22": "People & Blogs",
        "23": "Comedy",
        "24": "Entertainment",
        "25": "News & Politics",
        "26": "Howto & Style",
    }

    # Get user selection from dropdown
    selected_country = request.GET.get("country", "US")
    selected_category = request.GET.get("category", None)
    selected_engagement = request.GET.get("engagement", "")

    # Fetch trending videos from YouTube API
    videos = fetch_trending_videos(selected_country, selected_category)

    # Map categoryId → categoryName for each video
    for video in videos:
        cat_id = str(video.get("categoryId", ""))
        video["categoryName"] = categories.get(cat_id, "Miscellaneous")

    # Extract titles for AI analysis
    video_titles = [v.get("title", "") for v in videos]

    # AI Analysis: keywords from titles
    keywords = extract_keywords(video_titles)

    # Add sentiment and engagement score for each video
    for video in videos:
        # Combine title + description for better context
        text = f"{video.get('title', '')} {video.get('description', '')}"

        # Sentiment
        video["sentiment"] = analyze_sentiment(text, country=selected_country)

        # Engagement
        engagement = calculate_engagement(
            views=video.get("views", 0),
            likes=video.get("likes", 0),
            comments=video.get("comments", 0),
            subscribers=video.get("channel_subscribers", 0)
        )
        video["engagement_score"] = engagement["ratio"]
        video["engagement_text"] = engagement["text"]

    # Filter videos by engagement level if selected
    if selected_engagement:
        if selected_engagement == "high":
            videos = [v for v in videos if v.get("engagement_score", 0) > 5]
        elif selected_engagement == "medium":
            videos = [v for v in videos if 2 <= v.get("engagement_score", 0) <= 5]
        elif selected_engagement == "low":
            videos = [v for v in videos if v.get("engagement_score", 0) < 2]

    # Sort videos by engagement descending
    videos = sorted(videos, key=lambda x: x.get("engagement_score", 0), reverse=True)

    # Extract hashtags from video data (after engagement is calculated)
    hashtags = extract_hashtags(videos)

    # ✅ Generate AI summary
    summary = generate_trend_summary(videos, keywords, hashtags)

    # Render template with all data
    return render(request, "trends/trending_videos.html", {
        "videos": videos,
        "countries": countries,
        "categories": categories,
        "selected_country": selected_country,
        "selected_category": selected_category,
        "keywords": keywords,
        "hashtags": hashtags,
        "selected_engagement": selected_engagement,
        "summary": summary
    })


def login_page(request):
    """Handle both email/password login and social auth (Google).
    If the user is already authenticated, redirect to dashboard.
    """
    if request.user.is_authenticated:
        return redirect('trends:dashboard')

    error = None
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Login successful
            login(request, user)
            return redirect('trends:dashboard')
        else:
            # Invalid credentials
            error = "Invalid username or password. Please try again."
    
    return render(request, 'trends/login.html', {'error': error})


def optional_dashboard(request):
    """Shows a personalized dashboard for authenticated users, or a
    default dashboard for anonymous visitors.

    This keeps the logic minimal and template-driven (the template
    uses `user` and `is_authenticated` to adjust the UI).
    """
    if request.user.is_authenticated:
        context = {
            'is_authenticated': True,
            'user': request.user,
        }
    else:
        context = {
            'is_authenticated': False,
        }

    return render(request, 'trends/dashboard.html', context)


def compare_trends(request):
    """Compare trending videos between two countries side-by-side.
    
    Takes two query parameters: country1 and country2.
    Fetches trending videos for both countries, calculates engagement,
    sentiment, keywords, and hashtags for each.
    """
    # Country dictionary
    countries = {
        "US": "United States",
        "IN": "India",
        "PK": "Pakistan",
        "GB": "United Kingdom",
        "CA": "Canada",
        "AU": "Australia",
        "DE": "Germany",
        "FR": "France",
        "JP": "Japan",
        "KR": "South Korea",
    }
    
    # Get country codes from query parameters
    country1 = request.GET.get("country1", "US")
    country2 = request.GET.get("country2", "IN")
    
    # Fetch trending videos for both countries with error handling
    try:
        videos1 = fetch_trending_videos(country1, None)
    except Exception as e:
        print(f"Error fetching videos for {country1}: {e}")
        videos1 = []
    
    try:
        videos2 = fetch_trending_videos(country2, None)
    except Exception as e:
        print(f"Error fetching videos for {country2}: {e}")
        videos2 = []
    
    # Helper function to analyze videos
    def analyze_videos(videos, country_code):
        # Handle empty video list
        if not videos:
            return {
                "videos": [],
                "keywords": [],
                "hashtags": [],
                "avg_engagement": 0,
                "sentiment_counts": {"positive": 0, "neutral": 0, "negative": 0},
                "total_videos": 0
            }
        
        # Extract titles for keyword analysis
        titles = [v.get("title", "") for v in videos]
        keywords = extract_keywords(titles)
        
        # Calculate sentiment and engagement for each video
        for video in videos:
            text = f"{video.get('title', '')} {video.get('description', '')}"
            video["sentiment"] = analyze_sentiment(text, country=country_code)
            
            engagement = calculate_engagement(
                views=video.get("views", 0),
                likes=video.get("likes", 0),
                comments=video.get("comments", 0),
                subscribers=video.get("channel_subscribers", 0)
            )
            video["engagement_score"] = engagement["ratio"]
            video["engagement_text"] = engagement["text"]
        
        # Sort by engagement score
        videos = sorted(videos, key=lambda x: x.get("engagement_score", 0), reverse=True)
        
        # Extract hashtags from video data (after engagement is calculated)
        # This allows hashtag extraction to use engagement scores and full video metadata
        hashtags = extract_hashtags(videos)
        
        # Calculate average engagement
        avg_engagement = sum(v.get("engagement_score", 0) for v in videos) / len(videos) if videos else 0
        
        # Calculate sentiment distribution
        sentiment_counts = {"positive": 0, "neutral": 0, "negative": 0}
        for v in videos:
            sentiment_label = v.get("sentiment", {}).get("label", "neutral")
            sentiment_counts[sentiment_label] = sentiment_counts.get(sentiment_label, 0) + 1
        
        return {
            "videos": videos[:10],  # Top 10 videos
            "keywords": keywords,
            "hashtags": hashtags,
            "avg_engagement": round(avg_engagement, 2),
            "sentiment_counts": sentiment_counts,
            "total_videos": len(videos)
        }
    
    # Analyze both countries
    data1 = analyze_videos(videos1, country1)
    data2 = analyze_videos(videos2, country2)
    
    # Prepare context
    context = {
        "country1_code": country1,
        "country1_name": countries.get(country1, country1),
        "country2_code": country2,
        "country2_name": countries.get(country2, country2),
        "data1": data1,
        "data2": data2,
        "countries": countries,
    }
    
    return render(request, "trends/compare_trends.html", context)
