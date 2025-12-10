from django.core.management.base import BaseCommand
from googleapiclient.discovery import build
from django.conf import settings

class Command(BaseCommand):
    help = "Fetch real trending YouTube videos by country"

    def handle(self, *args, **options):
        api_key = settings.YOUTUBE_API_KEY
        if not api_key:
            self.stdout.write(self.style.ERROR("❌ Missing YOUTUBE_API_KEY in .env"))
            return

        youtube = build("youtube", "v3", developerKey=api_key)
        countries = ["US", "IN", "PK", "GB", "CA"]

        for country in countries:
            self.stdout.write(self.style.NOTICE(f"🌍 Fetching trending videos for {country}..."))

            request = youtube.videos().list(
                part="snippet,statistics",
                chart="mostPopular",
                regionCode=country,
                maxResults=5
            )
            response = request.execute()

            for item in response.get("items", []):
                title = item["snippet"]["title"]
                channel = item["snippet"]["channelTitle"]
                views = item["statistics"].get("viewCount", "0")
                video_url = f"https://www.youtube.com/watch?v={item['id']}"
                self.stdout.write(f"🎬 {title} — {channel} ({views} views)\n🔗 {video_url}\n")

        self.stdout.write(self.style.SUCCESS("✅ Successfully fetched trending videos!"))
