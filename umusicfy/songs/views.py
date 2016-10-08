
from rest_framework import viewsets
from django.views.generic import DetailView, View
from .serializers import ArtistSerializer, SongSerializer, AlbumSerializer
from .models import Artist, Album, Song

from user_profile.models import UserProfile
from django.http import HttpResponseRedirect


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


class ArtistDetailView(DetailView):

    model = Artist
    template_name = 'artist_detail.html'
    slug_url_kwarg = 'artist_name_slug'
    slug_field = 'name_slug'

    def get_context_data(self, **kwargs):
        context = super(ArtistDetailView, self).get_context_data(**kwargs)
        context['top_albums'] = Album.objects.filter(artist=self.object).order_by('-rating')[:5]
        context['top_songs'] = Song.objects.filter(album__artist=self.object).order_by('-rating')[:5]
        context['albums'] = Album.objects.filter(artist=self.object).order_by('-rating')
        context['songs'] = Song.objects.filter(album__artist=self.object).order_by('-rating')
        return context


class AlbumDetailView(DetailView):

    model = Album
    template_name = 'album_detail.html'
    slug_url_kwarg = 'album_name_slug'
    slug_field = 'name_slug'

    def get_context_data(self, **kwargs):
        context = super(ArtistDetailView, self).get_context_data(**kwargs)
        context['songs'] = Song.objects.filter(album__artist=self.object).order_by('-rating')
        return context


class FollowArtistView(View):

    def get(self, request, *args, **kwargs):
        '''
        '''
        user_to_folow = Artist.objects.get(id=self.kwargs['artist_name_slug'])
        request.user.following.add(user_to_folow)
        return HttpResponseRedirect('/user-profile/' + str(request.user.id))
