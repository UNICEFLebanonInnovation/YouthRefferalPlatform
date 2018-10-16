__author__ = 'achamseddine'

from django.core.management.base import BaseCommand

from referral_platform.registrations.tasks import update_registrations


class Command(BaseCommand):
    help = 'Update old registration data'

    def add_arguments(self, parser):
        parser.add_argument('--filename', type=str, default=None)
        parser.add_argument('--url', type=str, default=None)
        parser.add_argument('--token', type=str, default=None)
        parser.add_argument('--protocol', type=str, default='HTTPS')

    def handle(self, *args, **options):
        update_registrations(
            filename=options['filename'],
            base_url=options['url'],
            token=options['token'],
            protocol=options['protocol']
        )
