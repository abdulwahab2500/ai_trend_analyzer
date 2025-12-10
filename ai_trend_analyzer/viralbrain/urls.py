from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('trends.urls')),  # root points to trends app
    # django-allauth URLs (social login)
    path('accounts/', include('allauth.urls')),
]
