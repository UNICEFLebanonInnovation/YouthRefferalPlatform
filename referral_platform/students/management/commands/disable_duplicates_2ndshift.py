__author__ = 'achamseddine'

from django.core.management.base import BaseCommand

from referral_platform.students.tasks import *


class Command(BaseCommand):
    help = 'Disable duplicate enrolments'

    def add_arguments(self, parser):
        parser.add_argument('offset', nargs='+', type=int)

    def handle(self, *args, **options):
        for offset in options['offset']:
            disable_duplicate_enrolments(offset)
