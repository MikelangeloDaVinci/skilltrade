# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from django_countries.fields import Country

from core.models import Profile, City, Skill, ProfileSkill, NeededSkill

admin.site.register(Profile)
admin.site.register(City)
admin.site.register(Skill)
admin.site.register(ProfileSkill)
admin.site.register(NeededSkill)
