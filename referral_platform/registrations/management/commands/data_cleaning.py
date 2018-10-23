__author__ = 'achamseddine'

from django.core.management.base import BaseCommand
class Command(BaseCommand):
    help = 'Update old registration assessment data'

    def add_arguments(self, parser):
        parser.add_argument('--id', type=int, default=None)
        parser.add_argument('--updated', type=str, default=None)

    def handle(self, *args, **options):
        id = options['id'],
        updated = options['updated'],
        # help = 'use all to update all, or new to update only empty new data'
        if id:
            from referral_platform.registrations.models import AssessmentSubmission
            newmaping = AssessmentSubmission.objects.filter(registration__partner_organization=id)
            for obj in newmaping:
                obj.update_field()
        else:
            from referral_platform.registrations.models import AssessmentSubmission
            newmaping = AssessmentSubmission.objects.all()
            for obj in newmaping:
                obj.update_field()
