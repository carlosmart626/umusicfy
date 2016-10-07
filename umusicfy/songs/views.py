
from rest_framework import viewsets
from .serializers import ArtistSerializer, SongSerializer, AlbumSerializer
from .models import Artist, Album, Song


class ArtistViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Artist.objects.all().order_by('name')
    serializer_class = ArtistSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Album.objects.all().order_by('-rating')
    serializer_class = AlbumSerializer


class SongViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Song.objects.all().order_by('-rating')
    serializer_class = SongSerializer
