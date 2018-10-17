__author__ = 'achamseddine'

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Update old registration assessment data'

    def add_arguments(self, parser):
        parser.add_argument('--filename', type=str, default=None)
        parser.add_argument('--updated', type=str, default=None)

    def handle(self, *args, **options):
        filename = options['filename'],
        updated = options['updated'],
        # # help = 'use all to update all, or new to update only empty new data'
        # if filename:
        #     from referral_platform.registrations.models import AssessmentSubmission
        #     newmaping = AssessmentSubmission.objects.filter(assessment__slug=filename)
        #     for obj in newmaping:
        #         obj.update_field()
        # else:
        from referral_platform.registrations.models import AssessmentSubmission
        newmaping = AssessmentSubmission.objects.filter(registration__partner_organization='Nour')
        for obj in newmaping:
            obj.update_field()
