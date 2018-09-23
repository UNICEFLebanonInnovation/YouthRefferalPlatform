__author__ = 'achamseddine'

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Update old registration assessment data'

    def handle(self, *args, **options):
        from referral_platform.registrations.models import AssessmentSubmission
        newmaping = AssessmentSubmission.objects.all()[1:10000]
        for obj in newmaping:
            obj.update_field()

