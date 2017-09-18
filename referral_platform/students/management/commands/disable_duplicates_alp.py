__author__ = 'achamseddine'

from django.core.management.base import BaseCommand

from referral_platform.students.tasks import *


class Command(BaseCommand):
    help = 'Disable duplicate ALP'

    def add_arguments(self, parser):
        parser.add_argument('--schools', nargs='+', type=str, default=None)

    def handle(self, *args, **options):
        if options['schools']:
            for school in options['schools']:
                disable_duplicate_outreaches(school)
        else:
            disable_duplicate_outreaches()
