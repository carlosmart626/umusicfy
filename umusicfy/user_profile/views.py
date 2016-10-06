# encoding:utf-8

from django.views.generic.edit import FormView
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.models import User
from .forms import UserProfileUpdateForm, SetPasswordForm


class UpdateUserProfileView(UpdateView):
    template_name = 'userprofile_update.html'
    form_class = UserProfileUpdateForm
    success_url = '/perfil/'

    def get(self, request, *args, **kwargs):
        self.object = request.user
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        self.object = request.user
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
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


class UserProfileView(DetailView):
    model = User
    template_name = 'userprofile_main.html'

    def get(self, request, *args, **kwargs):
        self.object = request.user
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
