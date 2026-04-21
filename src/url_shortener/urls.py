from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.URLShortenerView.as_view()),
    re_path(r"^(?P<hash>[a-zA-Z0-9]{10})$", views.ShortURLView.as_view()),
]
