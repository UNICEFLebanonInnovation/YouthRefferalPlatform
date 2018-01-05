__author__ = 'achamseddine'

from django.core.management.base import BaseCommand

from referral_platform.youth.tasks import create_assessment_submission


class Command(BaseCommand):
    help = 'Create youth registration assessment submission'

    def handle(self, *args, **options):
        create_assessment_submission()
