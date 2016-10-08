from django.contrib.auth.decorators import login_required

from django.conf.urls import url

# Import Class Based Views
from .views import ArtistDetailView, AlbumDetailView, FollowArtistView

urlpatterns = [
    url(r'^/(?P<artist_name_slug>[\w-]+)/$', login_required(ArtistDetailView.as_view()), name='artist_detail_view'),
    url(r'^/folow/(?P<artist_name_slug>[\w-]+)/$', login_required(FollowArtistView.as_view()), name='follow_artist_view'),
    url(r'^/(?P<artist_name_slug>[\w-]+)/(?P<album_name_slug>[\w-]+)/$', login_required(AlbumDetailView.as_view()), name='album_detail_view'),
]
