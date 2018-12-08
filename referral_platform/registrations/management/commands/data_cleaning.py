__author__ = 'achamseddine'

from django.core.management.base import BaseCommand
class Command(BaseCommand):
    help = 'Update old registration assessment data, enter id for partner to it on partner level, or par = to All to update all or OE for only empty entries'

    def add_arguments(self, parser):
        parser.add_argument('--partner', type=int, default=None)
        parser.add_argument('--par', type=str, default=None)

    def handle(self, *args, **options):
        partner = options['partner']
        par = options['par']

        # help = 'use all to update all, or new to update only empty new data'
        if partner:
            from referral_platform.registrations.models import AssessmentSubmission
            newmaping = AssessmentSubmission.objects.filter(registration__partner_organization=partner)
            for obj in newmaping:
                obj.update_field()
        elif par == 'all':
            from referral_platform.registrations.models import AssessmentSubmission
            newmaping = AssessmentSubmission.objects.all()
            for obj in newmaping:
                obj.update_field()
        elif par == 'OE':
            from referral_platform.registrations.models import AssessmentSubmission
            newmaping = AssessmentSubmission.objects.filter(new_data__isnull=True)
            for obj in newmaping:
                obj.update_field()
        elif par == 'id':
            from referral_platform.registrations.models import AssessmentSubmission
            newmaping = AssessmentSubmission.objects.filter(registration__youth__number=id)
            for obj in newmaping:
                obj.update_field()
