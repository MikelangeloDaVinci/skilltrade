# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.functional import cached_property
from django_countries.fields import CountryField
from enumfields import Enum, EnumField


class CityManager(models.Manager):

    def get_distinct_by_name(self):
        cities = []
        city_names = []
        for city in City.objects.all():
            if city.name not in city_names:
                city_names.append(city.name)
                cities.append(city)
        return cities


class City(models.Model):
    name = models.CharField(max_length=1024, null=False, blank=False)
    country = CountryField()

    objects = CityManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"


class Skill(models.Model):
    name = models.CharField(max_length=128, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Skill"
        verbose_name_plural = "Skills"


class Level(Enum):
    BEGINNER = 0
    AMATEUR = 1
    INTERMEDIATE = 2
    EXPERT = 3
    GENIUS = 4


class BaseSkill(models.Model):
    skill = models.ForeignKey(Skill)
    profile = models.ForeignKey("Profile")

    class Meta:
        abstract = True


class NeededSkill(BaseSkill):
    hours = models.IntegerField()
    description = models.CharField(max_length=512)

    def __str__(self):
        return self.profile.__str__() + ": " + self.skill.__str__() + " - " + self.hours.__str__()

    class Meta:
        verbose_name = "Needed skill"
        verbose_name_plural = "Needed skills"


class ProfileSkill(BaseSkill):
    level = EnumField(Level, max_length=1)

    def __str__(self):
        return self.profile.__str__() + ": " + self.skill.__str__() + " - " + self.level.__str__()

    class Meta:
        verbose_name = "Profile skill"
        verbose_name_plural = "Profile skills"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(null=True, blank=True)
    about = models.CharField(null=True, blank=True, max_length=8192)
    country = CountryField()
    city = models.ForeignKey(City, null=True, blank=True)

    @cached_property
    def skills(self):
        return ProfileSkill.objects.filter(profile=self)

    @cached_property
    def needs(self):
        return NeededSkill.objects.filter(profile=self)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def has_missing_user_data(self):
        for field in settings.REQUIRED_USER_FIELDS:
            try:
                if not getattr(self, field):
                    return True
            except AttributeError:
                if not getattr(self.user, field):
                    return True

        return False


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
