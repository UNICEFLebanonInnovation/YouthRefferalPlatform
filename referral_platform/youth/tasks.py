
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


@app.task
def create_assessment_submission():

    from referral_platform.clm.models import AssessmentSubmission as CLMAssessment
    from referral_platform.registrations.models import Registration, AssessmentSubmission

    old_assessments = CLMAssessment.objects.all()
    for old_ass in old_assessments:
        youth = old_ass.youth
        registry = youth.registrations.all().first()
        assessment = AssessmentSubmission.objects.create(
            youth=old_ass.youth,
            registration=registry,
            assessment=old_ass.assessment,
            data=old_ass.data
        )
        assessment.save()
