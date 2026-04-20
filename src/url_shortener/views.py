from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from rest_framework import generics, request

from src.url_shortener.models import ShortURLModel
from src.url_shortener.serializers import URLSerializer

class URLShortenerView(generics.CreateAPIView):

    serializer_class = URLSerializer


class ShortURLView(generics.GenericAPIView):

    queryset = ShortURLModel.objects.all()
    serializer_class = URLSerializer
    lookup_field = "hash"
    lookup_url_kwarg = "hash"

    def get(self, _: request.Request, *__, **___) -> HttpResponseRedirect:
        instance: ShortURLModel = self.get_object()
        return redirect(instance.original_url)
