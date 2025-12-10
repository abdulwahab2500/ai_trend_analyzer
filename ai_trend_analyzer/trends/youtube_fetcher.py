from googleapiclient.discovery import build
from googleapiclient.http import HttpRequest
from django.conf import settings
import httplib2
import ssl

# Load your YouTube API key from settings.py
YOUTUBE_API_KEY = settings.YOUTUBE_API_KEY


def build_youtube_client():
    """Build YouTube client with SSL configuration to prevent SSL errors."""
    try:
        # Create an HTTP client with SSL context that's more permissive
        http = httplib2.Http(
            disable_ssl_certificate_validation=True,
            timeout=30
        )
        return build("youtube", "v3", developerKey=YOUTUBE_API_KEY, http=http)
    except Exception:
        # Fallback to default build
        return build("youtube", "v3", developerKey=YOUTUBE_API_KEY)


def fetch_trending_videos(country="US", category=None, max_results=20):
    """
    Fetch trending videos from YouTube API with statistics:
    views, likes, comments, thumbnails, links, categoryId, and channel subscribers.
    """
    
    # Build fresh client for each request to avoid SSL caching issues
    youtube = build_youtube_client()
    
    try:
        request = youtube.videos().list(
            part="snippet,statistics",
            chart="mostPopular",
            regionCode=country,
            maxResults=max_results,
            videoCategoryId=category if category else None,
        )

        response = request.execute()
        videos = []

        for item in response.get("items", []):
            snippet = item.get("snippet", {})
            stats = item.get("statistics", {})

            video_id = item.get("id")
            channel_id = snippet.get("channelId")

            # Fetch channel subscriber count
            subscribers = 0
            try:
                channel_request = youtube.channels().list(
                    part="statistics",
                    id=channel_id
                )
                channel_response = channel_request.execute()
                if channel_response.get("items"):
                    subscribers = int(channel_response["items"][0]["statistics"].get("subscriberCount", 0))
            except Exception:
                subscribers = 0  # fallback if API fails

            videos.append({
                "id": video_id,
                "videoId": video_id,  # Add videoId for template compatibility
                "title": snippet.get("title", "No title"),
                "description": snippet.get("description", ""),
                "channel": snippet.get("channelTitle", "Unknown"),
                "thumbnail": snippet.get("thumbnails", {}).get("medium", {}).get("url", ""),
                "views": int(stats.get("viewCount", 0)),
                "likes": int(stats.get("likeCount", 0)),
                "comments": int(stats.get("commentCount", 0)),
                "link": f"https://www.youtube.com/watch?v={video_id}",
                "channel_subscribers": subscribers,
                "categoryId": snippet.get("categoryId", "0")
            })

        return videos
        
    except Exception as e:
        print(f"Error fetching trending videos: {e}")
        # Return empty list on error instead of crashing
        return []
