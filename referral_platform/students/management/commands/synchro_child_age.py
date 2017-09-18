__author__ = 'achamseddine'

from django.core.management.base import BaseCommand

from referral_platform.students.tasks import *


class Command(BaseCommand):
    help = 'Synchronize Child age with UNHCR'

    def handle(self, *args, **options):
        synchronize_child_age()
