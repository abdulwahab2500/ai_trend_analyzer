from django.urls import path
from . import views

app_name = 'trends'

urlpatterns = [
    path('', views.home, name='home'),  # root page (trending videos)
    path('login/', views.login_page, name='login'),
    path('dashboard/', views.optional_dashboard, name='dashboard'),
    path('compare/', views.compare_trends, name='compare'),  # country comparison
]
