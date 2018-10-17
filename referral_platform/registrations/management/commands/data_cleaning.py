__author__ = 'achamseddine'

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Update old registration assessment data'

    def add_arguments(self, parser):
        parser.add_argument('--filename', type=str, default=None)

    def handle(self, *args, **options):

        from referral_platform.registrations.models import AssessmentSubmission
        newmaping = AssessmentSubmission.objects.filter(assessment__slug='filename')
        for obj in newmaping:
            obj.update_field()

