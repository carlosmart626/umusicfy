from django.contrib.auth.decorators import login_required

from django.conf.urls import patterns, url

# Import Class Based Views
from .views import UserProfileView, UpdateUserProfileView, UpdateUserPasswordView, \
    UserProfileDetailView, PlaylistDetailView, PlaylistCreateView, FollowUserProfileView, \
    FollowPlaylistView

urlpatterns = patterns(
    '',
    url(r'^$', login_required(UserProfileView.as_view()), name='user_profile'),
    url(r'^password/$', login_required(UpdateUserPasswordView.as_view()), name='user_change_password'),
    url(r'^update/$', login_required(UpdateUserProfileView.as_view()), name='user_update_profile'),

    url(r'^(?P<pk>[0-9]+)/$', login_required(UserProfileDetailView.as_view()), name='user_update_profile'),
)
