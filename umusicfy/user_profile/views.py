# encoding:utf-8

from django.views.generic import DetailView, UpdateView, View, CreateView
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from .forms import UserProfileUpdateForm, SetPasswordForm
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from pusher import Pusher

from .models import PlayList, UserProfile, SongsPlaylist
from .forms import PlaylistForm

from songs.models import Song


class UserProfileView(DetailView):
    model = User
    template_name = 'userprofile_main.html'

    def get(self, request, *args, **kwargs):
        self.object = request.user
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class UpdateUserProfileView(UpdateView):
    template_name = 'userprofile_update.html'
    form_class = UserProfileUpdateForm
    success_url = '/user-profile/'

    def get(self, request, *args, **kwargs):
        self.object = request.user
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        self.object = request.user.userprofile
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            form.save()
            print ('FORMULARIO VALIDO')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class UpdateUserPasswordView(UpdateView):
    template_name = 'userprofile_chagepassword.html'
    form_class = SetPasswordForm
    success_url = '/perfil/'

    def get(self, request, *args, **kwargs):
        self.object = request.user
        form = SetPasswordForm(request.user)
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        self.object = request.user
        form = SetPasswordForm(request.user, self.request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class UserProfileDetailView(DetailView):
    model = User
    template_name = 'userprofile_main.html'
    slug_url_kwarg = 'artist_name_slug'
    slug_field = 'name_slug'

    def get_context_data(self, **kwargs):
        context = super(UserProfileDetailView, self).get_context_data(**kwargs)
        context['playlist'] = PlayList.objects.filter(owner=self.object).order_by('-creation_time')
        return context


class PlaylistDetailView(DetailView):
    model = PlayList
    template_name = 'userprofile_playlist.html'
    slug_url_kwarg = 'playlist_slug'
    slug_field = 'title_slug'


class PlaylistCreateView(CreateView):
    template_name = 'userprofile_playlist_create.html'
    model = PlayList
    form_class = PlaylistForm

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form.init_form_data(request.user)
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        """
        Returns the supplied success URL.
        """
        return '/user-profile/' + str(self.object.owner) + "/" + str(self.object.title_slug)


class PlayListListView(ListView):

    model = PlayList
    template_name = 'userprofile_playlists_list.html'

    def get_context_data(self, **kwargs):
        context = {}
        context['object_list'] = self.request.user.userprofile.get_user_playlist()
        context['playlist_following'] = self.request.user.userprofile.get_playlists_following()
        return context


class AddToPlaylistView(View):

    def get(self, request, *args, **kwargs):
        '''
        '''
        playlist = PlayList.objects.get(id=self.kwargs['playlist_id'])
        song = Song.objects.get(id=self.kwargs['song_id'])
        song.rating = song.rating + 1
        song.save()
        SongsPlaylist.objects.create(
            playlist=playlist,
            song=song,
        )
        pusher = Pusher(app_id=u'256573', key=u'ba23c5dd4731d5bfa933', secret=u'173bf632b3736f3e3d20')
        pusher.trigger('playlist_%d' % playlist.id, 'update', {'song': song.title})
        return HttpResponse("Added!")


class FollowUserProfileView(View):

    def get(self, request, *args, **kwargs):
        '''
        '''
        user_to_folow = UserProfile.objects.get(id=self.kwargs['user_id'])
        request.user.following.add(user_to_folow)
        return HttpResponseRedirect('/user-profile/' + str(request.user.id))


class FollowPlaylistView(View):

    def get(self, request, *args, **kwargs):
        '''
        '''
        playlist_to_folow = PlayList.objects.get(id=self.kwargs['playlist_id'])
        playlist_to_folow.followers.add(request.user)
        return HttpResponseRedirect('/user-profile/' + str(playlist_to_folow.owner) + "/" + str(playlist_to_folow.id))
