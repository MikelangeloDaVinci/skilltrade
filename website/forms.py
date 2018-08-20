import re
from annoying.functions import get_object_or_None
from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import Form
from django.utils.translation import ugettext as _
from django_countries.fields import CountryField
from enumfields import EnumField

from core.models import Level, ProfileSkill


class UserForm(Form):
    email = forms.EmailField()


class SignUpForm(UserForm):
    username = forms.CharField(max_length=32, min_length=1)
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")

        if len(password) < 8:
            raise ValidationError(_("Your password is too short. It must contain at least 8 characters."))

        if password != confirm_password:
            raise ValidationError(_("Password doesn't match confirmed password"))

        user = get_object_or_None(User, username=username)
        if user:
            raise ValidationError(_("Username is already in use"))

        user = get_object_or_None(User, email=email)
        if user:
            raise ValidationError(_("Email address is already in use"))

        if not re.match("^[a-zA-Z0-9_.-]+$", username):
            raise ValidationError(_("Invalid username. Valid characters are alphanumeric (a-z, 0-9) and .-_"))


class UserSettingsForm(UserForm):
    first_name = forms.CharField(max_length=64, min_length=1)
    last_name = forms.CharField(max_length=128, min_length=1)
    city = forms.CharField(max_length=128, min_length=1)
    country = CountryField().formfield()
    about = forms.CharField(max_length=8192, widget=forms.Textarea)

    def clean(self):
        cleaned_data = super(UserSettingsForm, self).clean()
        user = get_object_or_None(User, email=cleaned_data.get("email"))

        if user and (self.initial['request'].user != user):
            raise ValidationError(_("Email address is already in use"))


class ProfilePictureForm(Form):
    profile_picture = forms.ImageField()


class LoginForm(auth.forms.AuthenticationForm):
    username = forms.CharField(label=_("Username or email"), max_length=128)


class SkillBaseForm(Form):
    level = EnumField(Level, max_length=1).formfield()


class SkillForm(SkillBaseForm):
    skill = forms.CharField(max_length=64)

    def clean(self):
        cleaned_data = super(SkillForm, self).clean()
        user_skill = get_object_or_None(ProfileSkill, skill__name=cleaned_data["skill"],
                                        profile=self.initial['request'].user.profile)

        if user_skill:
            raise ValidationError(_("You have already added that skill. Edit that skill to change the skill level."))


class EditSkillForm(SkillBaseForm):
    skill = forms.CharField(max_length=64, widget=forms.HiddenInput())


class NeedForm(Form):
    skill = forms.CharField(max_length=64)
    hours = forms.IntegerField()
    description = forms.CharField(max_length=512, widget=forms.Textarea)


class EditNeedForm(NeedForm):
    skill = forms.CharField(max_length=64, widget=forms.HiddenInput())

