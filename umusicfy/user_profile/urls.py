from django.contrib.auth.decorators import login_required

from django.conf.urls import url

# Import Class Based Views
from .views import UserProfileView, UpdateUserProfileView, UpdateUserPasswordView, \
    UserProfileDetailView, PlaylistDetailView, PlaylistCreateView, FollowUserProfileView, \
    FollowPlaylistView

urlpatterns = [
    url(r'^$', login_required(UserProfileView.as_view()), name='user_profile'),
    url(r'^password/$', login_required(UpdateUserPasswordView.as_view()), name='user_change_password'),
    url(r'^update/$', login_required(UpdateUserProfileView.as_view()), name='user_update_profile'),
    url(r'^create-playlist/$', login_required(PlaylistCreateView.as_view()), name='user_create_playlist'),

    url(r'^(?P<pk>[0-9]+)/$', login_required(UserProfileDetailView.as_view()), name='visit_user_profile'),
    url(r'^/follow-user/(?P<user_id>[0-9]+)/$', login_required(FollowUserProfileView.as_view()), name='visit_user_profile'),
    url(r'^/follow-playlist/(?P<playlist_id>[0-9]+)/$', login_required(FollowPlaylistView.as_view()), name='visit_user_profile'),
]
