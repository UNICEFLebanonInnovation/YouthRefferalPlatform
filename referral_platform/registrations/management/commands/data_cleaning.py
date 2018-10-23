__author__ = 'achamseddine'

from django.core.management.base import BaseCommand
class Command(BaseCommand):
    help = 'Update old registration assessment data, enter id for partner to it on partner level, or par = to All to update all or OE for only empty entries'

    def add_arguments(self, parser):
        parser.add_argument('--id', type=int, default=None)
        parser.add_argument('--par', type=str, default=None)

    def handle(self, *args, **options):
        id = options['id'],
        par = options['par'],

        # help = 'use all to update all, or new to update only empty new data'
        if id:
            from referral_platform.registrations.models import AssessmentSubmission
            newmaping = AssessmentSubmission.objects.filter(registration__partner_organization=id)
            for obj in newmaping:
                obj.update_field()
        elif par == 'all':
            from referral_platform.registrations.models import AssessmentSubmission
            newmaping = AssessmentSubmission.objects.all()
            for obj in newmaping:
                obj.update_field()
        elif par == 'OE':
            from referral_platform.registrations.models import AssessmentSubmission
            newmaping = AssessmentSubmission.objects.filter(self.new_data == "")
            for obj in newmaping:
                obj.update_field()
