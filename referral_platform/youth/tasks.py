
from referral_platform.taskapp.celery import app


@app.task
def create_youth_registration():

    from referral_platform.youth.models import YoungPerson
    from referral_platform.registrations.models import Registration

    youths = YoungPerson.objects.all()
    for youth in youths:
        registry = Registration.objects.create(
            youth=youth,
            partner_organization=youth.partner_organization,
            governorate=youth.governorate,
            location=youth.location,
            center=youth.center,
            trainer=youth.trainer,
        )
        registry.save()
