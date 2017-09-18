__author__ = 'achamseddine'

from django.core.management.base import BaseCommand

from referral_platform.students.tasks import *


class Command(BaseCommand):
    help = 'Generate unique number for 2ndshift'

    def add_arguments(self, parser):
        parser.add_argument('offset', nargs='+', type=int)

    def handle(self, *args, **options):
        for offset in options['offset']:
            print('Generate hash number for 2nd shift students')
            generate_2ndshift_unique_number(offset)
