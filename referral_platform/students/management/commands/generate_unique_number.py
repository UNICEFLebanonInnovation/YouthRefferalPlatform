__author__ = 'achamseddine'

from django.core.management.base import BaseCommand

from referral_platform.students.tasks import *


class Command(BaseCommand):
    help = 'Generate unique number'

    def add_arguments(self, parser):
        parser.add_argument('models', nargs='+', type=str)

    def handle(self, *args, **options):
        if 'adult' in options['models']:
            print('Generate hash number for Adults')
            generate_adult_unique_number()
        if 'child' in options['models']:
            print('Generate hash number for Children')
            generate_child_unique_number()
        if '2ndshift' in options['models']:
            print('Generate hash number for 2nd shift students')
            generate_2ndshift_unique_number()
        if 'alp' in options['models']:
            print('Generate hash number for ALP students')
            generate_alp_unique_number()
