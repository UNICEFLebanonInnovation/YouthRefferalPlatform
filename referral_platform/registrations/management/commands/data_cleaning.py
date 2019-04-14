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
            newmaping = AssessmentSubmission.objects.filter(updated='0', assessment__slug__in=["pre_asseessment", "post_asseessment",
                                                                                               "pre_entrepreneurship", "post_entrepreneurship"])
            for obj in newmaping:
                obj.update_field()
                print(obj)
        elif par == 'OE':
            from referral_platform.registrations.models import AssessmentSubmission
            newmaping = AssessmentSubmission.objects.filter(new_data__isnull=True)
            for obj in newmaping:
                obj.update_field()
