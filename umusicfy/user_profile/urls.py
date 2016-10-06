from django.contrib.auth.decorators import login_required

from django.conf.urls import patterns, url

# Import Class Based Views
from .views import UserProfileView, UpdateUserProfileView, UpdateUserPasswordView

urlpatterns = patterns(
    '',
    url(r'^password/$', login_required(UpdateUserPasswordView.as_view()), name='user_change_password'),
    url(r'^update/$', login_required(UpdateUserProfileView.as_view()), name='user_update_profile'),
    url(r'^$', login_required(UserProfileView.as_view()), name='user_profile'),
)
