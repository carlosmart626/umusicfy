# encoding:utf-8

from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from .models import Playlist


class UserProfileUpdateForm(ModelForm):
    """
    A form that lets a user update it's data
    """
    class Meta:
        model = User

        fields = ('first_name', 'last_name', 'email', 'profile_picture', 'biography', )
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'datos_usuario form-control', 'placeholder': _('First Name'), }),
            'last_name': forms.TextInput(attrs={'class': 'datos_usuario form-control', 'placeholder': _('Last Name'), }),
            'email': forms.TextInput(attrs={'class': 'datos_usuario form-control', 'placeholder': _('e-mail'), }),
            'biography': forms.TextInput(attrs={'class': 'datos_usuario form-control', 'placeholder': _('biography'), }),
        }

    class Media:
        css = {
            'screen': ('/static/css/forms.css',),
            'print': ()
        }


class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set his/her password without entering the
    old password
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    new_password1 = forms.CharField(label=_("New password"),
                                    widget=forms.PasswordInput(attrs={'class': 'datos_usuario form-control', 'placeholder': 'Nueva clave', }))
    new_password2 = forms.CharField(label=_("New password confirmation"),
                                    widget=forms.PasswordInput(attrs={'class': 'datos_usuario form-control', 'placeholder': 'Confirmar clave', }))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'])
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user


class PlaylistForm(ModelForm):

    def init_form_data(self, user):
        self.fields['owner'] = forms.ModelChoiceField(
            widget=forms.Select(
                attrs={
                    'class': 'datos_usuario form-control'
                }
            ),
            queryset=User.objects.filter(id=user.id),
            initial=User.objects.filter(id=user.id)[0]
        )

    class Meta:
        model = Playlist

        fields = ('title', 'owner',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'datos_usuario form-control', 'placeholder': 'Procedimiento'}),
        }

    def clean(self):
        cleaned_data = super(PlaylistForm, self).clean()
        title = cleaned_data.get("title")
        owner = cleaned_data.get("owner")
        if Playlist.objects.filter(owner__id=owner, title=title).first() is not None:
            raise forms.ValidationError("You already have a playlist named %s" % title)
