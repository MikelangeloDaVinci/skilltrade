# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your views here.
import json

from annoying.functions import get_object_or_None
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, TemplateView

from core.models import City, Skill, ProfileSkill, NeededSkill
from website.forms import SignUpForm, UserSettingsForm, ProfilePictureForm, SkillForm, EditSkillForm, NeedForm, \
    EditNeedForm
from django.utils.translation import ugettext as _


class LoginErrorView(TemplateView):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseForbidden()
        return super(LoginErrorView, self).dispatch(request, *args, **kwargs)


class SignUpView(FormView, LoginErrorView):
    form_class = SignUpForm
    template_name = "website/sign_up.html"

    def form_valid(self, form):
        User.objects.create_user(username=form.cleaned_data['username'],
                                        email=form.cleaned_data['email'],
                                        password=form.cleaned_data['password'])
        user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password"])
        login(self.request, user)
        return redirect(reverse("index"))


class IndexView(TemplateView):
    template_name = "website/index.html"


class UserSettingsView(SuccessMessageMixin, FormView):
    form_class = UserSettingsForm
    template_name = "website/user_settings.html"
    success_url = reverse_lazy("user_settings")
    success_message = _('Your settings are now updated')

    def form_valid(self, form):
        country = form.cleaned_data["country"]
        city, created = City.objects.get_or_create(name=form.cleaned_data["city"], country=country)
        self.request.user.profile.city = city
        self.request.user.profile.country = country
        self.request.user.profile.about = form.cleaned_data['about']
        self.request.user.first_name = form.cleaned_data["first_name"]
        self.request.user.last_name = form.cleaned_data["last_name"]
        self.request.user.email = form.cleaned_data["email"]
        self.request.user.save()
        return super(UserSettingsView, self).form_valid(form)

    def get_initial(self):
        self.initial.update({'request': self.request})
        self.initial.update({'email': self.request.user.email})
        self.initial.update({'first_name': self.request.user.first_name})
        self.initial.update({'last_name': self.request.user.last_name})
        if self.request.user.profile.city:
            self.initial.update({'city': self.request.user.profile.city.name})
        self.initial.update({'country': self.request.user.profile.country})
        self.initial.update({'about': self.request.user.profile.about})
        return super(FormView, self).get_initial()


class ProfilePictureView(SuccessMessageMixin, FormView):
    form_class = ProfilePictureForm
    template_name = "website/profile_picture.html"
    success_url = reverse_lazy("user_settings")
    success_message = _('Your profile picture has been uploaded')

    def form_valid(self, form):
        self.request.user.profile.profile_picture = form.cleaned_data["profile_picture"]
        self.request.user.save()
        return super(ProfilePictureView, self).form_valid(form)


class EditSkillsView(SuccessMessageMixin, FormView):
    form_class = SkillForm
    template_name = "website/edit_skills.html"
    success_url = reverse_lazy("edit_skills")
    success_message = _('Your skill was added')

    def get(self, request, *args, **kwargs):
        profile_skill_to_delete = get_object_or_None(ProfileSkill, pk=self.request.GET.get("delete_skill_id"),
                                                     profile=self.request.user.profile)
        if profile_skill_to_delete:
            profile_skill_to_delete.delete()
        return super(EditSkillsView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        skill, created = Skill.objects.get_or_create(name=form.cleaned_data["skill"])
        profile_skill = ProfileSkill()
        profile_skill.skill = skill
        profile_skill.profile = self.request.user.profile
        profile_skill.level = form.cleaned_data["level"]
        profile_skill.save()
        return super(EditSkillsView, self).form_valid(form)

    def get_initial(self):
        self.initial.update({'request': self.request})
        self.initial.update({'skill': ""})
        self.initial.update({'level': ""})
        return super(EditSkillsView, self).get_initial()


class EditNeedsView(SuccessMessageMixin, FormView):
    form_class = NeedForm
    template_name = "website/edit_needs.html"
    success_url = reverse_lazy("edit_needs")
    success_message = _('Your need was added')

    def get(self, request, *args, **kwargs):
        needed_skill_to_delete = get_object_or_None(NeededSkill, pk=self.request.GET.get("delete_need_id"),
                                                     profile=self.request.user.profile)
        if needed_skill_to_delete:
            needed_skill_to_delete.delete()
        return super(EditNeedsView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        skill, created = Skill.objects.get_or_create(name=form.cleaned_data["skill"])
        needed_skill = NeededSkill()
        needed_skill.skill = skill
        needed_skill.profile = self.request.user.profile
        needed_skill.hours = form.cleaned_data["hours"]
        needed_skill.description = form.cleaned_data["description"]
        needed_skill.save()
        return super(EditNeedsView, self).form_valid(form)

    def get_initial(self):
        self.initial.update({'request': self.request})
        self.initial.update({'skill': ""})
        self.initial.update({'hours': ""})
        self.initial.update({'description': ""})
        return super(EditNeedsView, self).get_initial()


class EditSkillView(SuccessMessageMixin, FormView):
    form_class = EditSkillForm
    template_name = "website/edit_skill.html"
    success_url = reverse_lazy("edit_skills")
    success_message = _('Your skill has been updated')

    def form_valid(self, form):
        profile_skill = ProfileSkill.objects.get(skill__name=form.cleaned_data["skill"], profile=self.request.user.profile)
        profile_skill.level = form.cleaned_data["level"]
        profile_skill.save()
        return super(EditSkillView, self).form_valid(form)

    def get_initial(self):
        profile_skill = ProfileSkill.objects.get(pk=self.request.GET.get("skill_id"))
        self.initial.update({'skill': profile_skill.skill.name})
        self.initial.update({'level': profile_skill.level})
        return super(EditSkillView, self).get_initial()

    def get_context_data(self, **kwargs):
        context_data = super(EditSkillView, self).get_context_data(**kwargs)
        context_data["profile_skill"] = ProfileSkill.objects.get(pk=self.request.GET.get("skill_id"))
        return context_data


class EditNeedView(SuccessMessageMixin, FormView):
    form_class = EditNeedForm
    template_name = "website/edit_need.html"
    success_url = reverse_lazy("edit_needs")
    success_message = _('Your need has been updated')

    def form_valid(self, form):
        needed_skill = NeededSkill.objects.get(skill__name=form.cleaned_data["skill"], profile=self.request.user.profile)
        needed_skill.hours = form.cleaned_data["hours"]
        needed_skill.description = form.cleaned_data["description"]
        needed_skill.save()
        return super(EditNeedView, self).form_valid(form)

    def get_initial(self):
        needed_skill = NeededSkill.objects.get(pk=self.request.GET.get("need_id"))
        self.initial.update({'skill': needed_skill.skill.name})
        self.initial.update({'hours': needed_skill.hours})
        self.initial.update({'description': needed_skill.description})
        return super(EditNeedView, self).get_initial()

    def get_context_data(self, **kwargs):
        context_data = super(EditNeedView, self).get_context_data(**kwargs)
        context_data["needed_skill"] = NeededSkill.objects.get(pk=self.request.GET.get("need_id"))
        return context_data


class LogoutView(TemplateView):
    template_name = "website/logout.html"

    def get(self, request, *args, **kwargs):
        logout(request)
        return render(request, "website/logout.html")


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _("Your password is now changed"))
            return redirect('change_password')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'website/change_password.html', {
        'form': form
    })


def api_cities_json_view(request):
    response_data = []
    for city in City.objects.get_distinct_by_name():
        data = {}
        data["name"] = city.name
        response_data.append(data)
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def api_skills_json_view(request):
    response_data = []
    for skill in Skill.objects.all():
        data = {}
        data["name"] = skill.name
        response_data.append(data)
    return HttpResponse(json.dumps(response_data), content_type="application/json")
