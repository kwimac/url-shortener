from django.urls import path

from . import views

urlpatterns = [
    path("", views.URLShortenerView.as_view()),
    path("<str:hash>", views.ShortURLView.as_view()),
]
