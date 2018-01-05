__author__ = 'achamseddine'

from django.core.management.base import BaseCommand

from referral_platform.youth.tasks import create_youth_registration


class Command(BaseCommand):
    help = 'Create youth registration on the new structure'

    def handle(self, *args, **options):
        create_youth_registration()
