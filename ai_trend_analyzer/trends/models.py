from django.db import models

class Video(models.Model):
    PLATFORM_CHOICES = [
        ('youtube', 'YouTube'),
        ('tiktok', 'TikTok'),
        ('instagram', 'Instagram'),
    ]

    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    video_url = models.URLField()
    thumbnail_url = models.URLField(blank=True, null=True)
    views = models.BigIntegerField(default=0)
    likes = models.BigIntegerField(default=0)
    published_at = models.DateTimeField()
    fetched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.platform.capitalize()} - {self.title[:50]}"
