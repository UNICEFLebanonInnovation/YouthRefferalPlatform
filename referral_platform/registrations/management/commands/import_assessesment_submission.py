__author__ = 'achamseddine'

from django.core.management.base import BaseCommand

from referral_platform.registrations.tasks import import_assessment_submission


class Command(BaseCommand):
    help = 'Update old registration data'

    def add_arguments(self, parser):
        parser.add_argument('--filename', type=str, default=None)


    def handle(self, *args, **options):
        import_assessment_submission(
            filename=options['filename'],

        )
