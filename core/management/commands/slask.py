from django.contrib.auth.models import User
from django.core.management import BaseCommand

from core.models import Profile, NeededSkill, ProfileSkill


class Command(BaseCommand):

    def handle(self, *args, **options):
        for needed_skill in NeededSkill.objects.all():
            print "%s is a needed skill" %(needed_skill.skill.name)
            print "and that skill is known by ", ProfileSkill.objects.filter(skill=needed_skill.skill).count()