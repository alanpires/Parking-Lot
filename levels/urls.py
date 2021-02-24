from django.urls import path
from .views import LevelView

urlpatterns = [
    path('levels/', LevelView.as_view())
]