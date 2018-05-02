__author__ = 'achamseddine'

import time
import datetime
import tablib
from django.utils.translation import ugettext as _
from import_export.formats import base_formats
from referral_platform.taskapp.celery import app
from .file import store_file
from referral_platform.registrations.mappings import *


@app.task
def export_initiative_assessments(params=None, return_data=False):
    from referral_platform.registrations.models import AssessmentSubmission
    from referral_platform.partners.models import PartnerOrganization
    from referral_platform.locations.models import Location

    submission_set = AssessmentSubmission.objects.all()

    book = tablib.Databook()
    title = 'initiative_assessments'
    if 'partner' in params and params['partner']:
        partner = PartnerOrganization.objects.get(id=int(params['partner']))
        title = title + '-partner-'+partner.name
        submission_set = submission_set.filter(registration__partner_organization_id=partner.id)
    if 'governorate' in params and params['governorate']:
        location = Location.objects.get(id=int(params['governorate']))
        title = title + '-governorate-'+location.name
        submission_set = submission_set.filter(registration__governorate_id=location.id)

    data5 = tablib.Dataset()
    data5.title = "Initiative registration"
    data5.headers = [
        'Country',
        'Governorate',
        'Location',
        'Partner',

        'Unique number',
        'First Name',
        "Father's Name",
        'Last Name',
        'Trainer',
        'Bayanati ID',
        'Jordanian ID',
        'Gender',
        'birthday day',
        'birthday month',
        'birthday year',
        'age',
        'Date of birth',
        'Nationality',
        'Marital status',
        'address',

        'Initiative Title',
        'Initiative Location',
        'Gender of members who were engaged in the initiative implementation',
        'Number of members who were engaged in the initiative implementation',
        'Planned start date of the initiative',
        'Duration of the initiative',

        'Type of Initiative',
        'basic services',
        'health service',
        'educational',
        'protection',
        'environmental',
        'political',
        'advocacy',
        'economic, artistic',
        'religious or spiritual',
        'sports',
        'social cohesion',
        'other',

        'Other initiatives',

        'How many people are estimated to benefit/will be reached by implementing the initiative?',
        '1-10 year old',
        '11-24 year old',
        '25-50 year old',
        '50 years and above',

        'The estimated Age groups of the beneficiaries?',
        'Gender of beneficiaries',
        'Did your group have a mentor/facilitator/teacher to support you with planning of the initiative?',
        'The team expects to implement the initiative as expected',
        'Team members expect to participate effectively in the implementation of the initiative',
        'The group aims to communicate with each other for the implementation of the initiative',
        'The group members expects to play leading roles for the implementation of the initiative',
        'The group expects to collect and analyse data for the implementation of the initiative',
        'The group expects to have a sense of belonging while implementing of the initiatives',
        'The group is confident in coming up with solutions if challenges are faced',
        'The group feels certain that the initiative will address the problem(s) faced by our communities',
        'The group expects to find the mentorship in the planning phase very helpful',
        'Are you planning to mobilize resources for this project?',

        'If yes, from whom?',
        'unicef',
        'Local business',
        'NGO',
        'Governmental body',
        'other',

        'What kind of support are you planning to receive?',
        'technical',
        'inkind',
        'financial',
        'other',

        'Can you tell us more about the problem you/your community is facing?',
        'Can you please tell us your planned results/what will the initiative achieve?',
        'start',
        'end',
        'submission time',
    ]

    data6 = tablib.Dataset()
    data6.title = "Initiative implementation"
    data6.headers = [
        'Country',
        'Governorate',
        'Location',
        'Partner',

        'Unique number',
        'First Name',
        "Father's Name",
        'Last Name',
        'Trainer',
        'Bayanati ID',
        'Jordanian ID',
        'Gender',
        'birthday day',
        'birthday month',
        'birthday year',
        'age',
        'Date of birth',
        'Nationality',
        'Marital status',
        'address',

        'Initiative Title',
        'Type of Initiative',
        'basic services',
        'health service',
        'educational',
        'protection',
        'environmental',
        'political',
        'advocacy',
        'economic, artistic',
        'religious or spiritual',
        'sports',
        'social cohesion',
        'other',

        'Other initiatives',
        'How many people benefited/ reached by implementing the initiative?',

        'The Age groups of the beneficiaries reached?',
        '1-10 year old',
        '11-24 year old',
        '25-49 year old',
        '50 years and above',
        'We don''t know',

        'Gender of beneficiaries',
        'The initiative was implemented as expected',

        'Types of challenges while implementing the initiative',
        'financial',
        'inkind',
        'physical',
        'technical',
        'other',
        'no_challenges',

        'Other challenges',

        'Team members participated effectively in the implementation of the initiative',
        'The group communicated with each other for the implementation of the initiative',
        'The group members played leading roles for the implementation of the initiative',
        'The group collected and analysed data for the implementation of the initiative',
        'The group had a sense of belonging while planning for the initiatives',
        'The group confidently came up with solutions when challenges were faced',
        'The group effectively addressed  the problem(s) faced by the community',
        'Did your group have a mentor/facilitator/teacher to support the implementation of the initiative',
        'The group found the mentorship in the planning phase very helpful',
        'Were resources mobilized for this project?',

        'If so, from whom?',
        'unicef',
        'Local business',
        'NGO',
        'Governmental body',
        'other',

        'What kind of support did you receive?',
        'technical',
        'inkind',
        'financial',
        'other',

        'The support we received was helpful and consistent with what the group was expecting',
        'If you answer is disagree or strongly disagree, can you tell us why?',
        'start',
        'end',
        'submission_time',
    ]

    submission_set1 = submission_set.filter(assessment__slug='init_registration')
    for line2 in submission_set1:
        youth = line2.youth
        registry = line2.registration
        submission_date = line2.data.get('_submission_time', '')
        try:
            submission_date = datetime.datetime.strptime(submission_date, '%Y-%m-%dT%H:%M:%S').strftime(
                '%d/%m/%Y') if submission_date else ''
        except Exception:
            submission_date = ''

        content = [
            registry.governorate.parent.name if registry.governorate else '',
            registry.governorate.name if registry.governorate else '',
            registry.location,
            registry.partner_organization.name if registry.partner_organization else '',

            youth.number,
            youth.first_name,
            youth.father_name,
            youth.last_name,
            registry.trainer,
            youth.bayanati_ID,
            youth.id_number,
            youth.sex,
            youth.birthday_day,
            youth.birthday_month,
            youth.birthday_year,
            youth.calc_age,
            youth.birthday,
            youth.nationality.name if youth.nationality else '',
            youth.marital_status,
            youth.address,

            line2.data.get('respid_initiativeID_title', ''),
            line2.data.get('initiative_loc', ''),
            get_choice_value(line2.data, 'gender_implem_initiatives', 'gender'),
            line2.data.get('No_of_team_members_executed', ''),
            line2.data.get('start_date_implementing_initia', ''),
            get_choice_value(line2.data, 'duration_of_initiative', 'how_many'),

            # get_choice_value(line2.data, 'type_of_initiative', 'initiative_types'),
            line2.data.get('type_of_initiative', ''),
            line2.get_data_option('type_of_initiative', 'basic_services'),
            line2.get_data_option('type_of_initiative', 'health_service'),
            line2.get_data_option('type_of_initiative', 'educational'),
            line2.get_data_option('type_of_initiative', 'protection'),
            line2.get_data_option('type_of_initiative', 'environmental'),
            line2.get_data_option('type_of_initiative', 'political'),
            line2.get_data_option('type_of_initiative', 'advocacy'),
            line2.get_data_option('type_of_initiative', 'economic_artis'),
            line2.get_data_option('type_of_initiative', 'religious_&_sp'),
            line2.get_data_option('type_of_initiative', 'sports'),
            line2.get_data_option('type_of_initiative', 'social_cohesio'),
            line2.get_data_option('type_of_initiative', 'other'),

            line2.get_data_option('other_type_of_initiative', ''),

            # get_choice_value(line2.data, 'number_of_direct_beneficiaries', 'how_many'),
            line2.data.get('number_of_direct_beneficiaries', ''),
            line2.get_data_option('number_of_direct_beneficiaries', '1-10'),
            line2.get_data_option('number_of_direct_beneficiaries', '11-24'),
            line2.get_data_option('number_of_direct_beneficiaries', '25-50'),
            line2.get_data_option('number_of_direct_beneficiaries', 'above_50'),

            get_choice_value(line2.data, 'age_group_range', 'how_many'),
            get_choice_value(line2.data, 'gender_of_beneficiaries', 'gender'),
            get_choice_value(line2.data, 'mentor_assigned', 'yes_no'),

            get_choice_value(line2.data, 'initiative_as_expected', 'rates'),
            get_choice_value(line2.data, 'team_involovement', 'rates'),
            get_choice_value(line2.data, 'communication', 'rates'),
            get_choice_value(line2.data, 'leadership', 'rates'),
            get_choice_value(line2.data, 'analytical_skills', 'rates'),
            get_choice_value(line2.data, 'sense_of_belonging', 'rates'),
            get_choice_value(line2.data, 'problem_solving', 'rates'),
            get_choice_value(line2.data, 'assertiveness', 'rates'),
            get_choice_value(line2.data, 'mentorship_helpful', 'rates'),

            get_choice_value(line2.data, 'planning_to_mobilize_resources', 'yes_no'),

            # get_choice_value(line2.data, 'if_so_who', 'third_parties'),
            line2.data.get('if_so_who', ''),
            line2.get_data_option('if_so_who', 'unicef'),
            line2.get_data_option('if_so_who', 'private,_local'),
            line2.get_data_option('if_so_who', 'NGO'),
            line2.get_data_option('if_so_who', 'Governmental_i'),
            line2.get_data_option('if_so_who', 'other'),

            # get_choice_value(line2.data, 'type_of_support_required', 'challenges'),
            line2.data.get('type_of_support_required', ''),
            line2.get_data_option('type_of_support_required', 'technical'),
            line2.get_data_option('type_of_support_required', 'inkind'),
            line2.get_data_option('type_of_support_required', 'financial'),
            line2.get_data_option('type_of_support_required', 'other'),

            line2.data.get('problem_addressed', ''),
            line2.data.get('planned_results', ''),
            line2.data.get('start', ''),
            line2.data.get('end', ''),

            submission_date,
        ]
        data5.append(content)

    submission_set2 = submission_set.filter(assessment__slug='init_exec')
    for line2 in submission_set2:
        youth = line2.youth
        registry = line2.registration
        submission_date = line2.data.get('_submission_time', '')
        try:
            submission_date = datetime.datetime.strptime(submission_date, '%Y-%m-%dT%H:%M:%S').strftime(
                '%d/%m/%Y') if submission_date else ''
        except Exception:
            submission_date = ''
        content = [
            registry.governorate.parent.name if registry.governorate else '',
            registry.governorate.name if registry.governorate else '',
            registry.location,
            registry.partner_organization.name if registry.partner_organization else '',

            youth.number,
            youth.first_name,
            youth.father_name,
            youth.last_name,
            registry.trainer,
            youth.bayanati_ID,
            youth.id_number,
            youth.sex,
            youth.birthday_day,
            youth.birthday_month,
            youth.birthday_year,
            youth.calc_age,
            youth.birthday,
            youth.nationality.name if youth.nationality else '',
            youth.marital_status,
            youth.address,

            line2.data.get('respid_initiativeID_title', ''),

            # get_choice_value(line2.data, 'type_of_initiative', 'initiative_types'),
            line2.data.get('type_of_initiative', ''),
            line2.get_data_option('type_of_initiative', 'basic_services'),
            line2.get_data_option('type_of_initiative', 'health_service'),
            line2.get_data_option('type_of_initiative', 'educational'),
            line2.get_data_option('type_of_initiative', 'protection'),
            line2.get_data_option('type_of_initiative', 'environmental'),
            line2.get_data_option('type_of_initiative', 'political'),
            line2.get_data_option('type_of_initiative', 'advocacy'),
            line2.get_data_option('type_of_initiative', 'economic_artis'),
            line2.get_data_option('type_of_initiative', 'religious_&_sp'),
            line2.get_data_option('type_of_initiative', 'sports'),
            line2.get_data_option('type_of_initiative', 'social_cohesio'),
            line2.get_data_option('type_of_initiative', 'other'),

            line2.data.get('other_type_of_initiative', ''),
            line2.data.get('integer_0259d46e', ''),

            # get_choice_value(line2.data, 'select_multiple_e160966a', 'how_many'), split the options
            line2.data.get('select_multiple_e160966a', ''),
            line2.get_data_option('select_multiple_e160966a', '1-10'),
            line2.get_data_option('select_multiple_e160966a', '11-24'),
            line2.get_data_option('select_multiple_e160966a', '25-49'),
            line2.get_data_option('select_multiple_e160966a', '50'),
            line2.get_data_option('select_multiple_e160966a', 'unknown'),

            get_choice_value(line2.data, 'select_one_a3c4ea99', 'gender'),
            get_choice_value(line2.data, 'initiative_as_expected', 'rates'),

            # get_choice_value(line2.data, 'challenges_faced', 'challenges'), split the options
            line2.data.get('challenges_faced', ''),
            line2.get_data_option('challenges_faced', 'financial'),
            line2.get_data_option('challenges_faced', 'inkind'),
            line2.get_data_option('challenges_faced', 'physical'),
            line2.get_data_option('challenges_faced', 'technical'),
            line2.get_data_option('challenges_faced', 'other'),
            line2.get_data_option('challenges_faced', 'no_challenges'),

            line2.data.get('other_challenges', ''),

            get_choice_value(line2.data, 'team_involovement', 'rates'),
            get_choice_value(line2.data, 'communication', 'rates'),
            get_choice_value(line2.data, 'leadership', 'rates'),
            get_choice_value(line2.data, 'analytical_skills', 'rates'),
            get_choice_value(line2.data, 'sense_of_belonging', 'rates'),
            get_choice_value(line2.data, 'problem_solving', 'rates'),
            get_choice_value(line2.data, 'assertiveness', 'rates'),

            get_choice_value(line2.data, 'mentor_assigned', 'yes_no'),
            get_choice_value(line2.data, 'mentorship_helpful', 'rates'),
            get_choice_value(line2.data, 'did_you_mobilize_resources', 'yes_no'),

            # get_choice_value(line2.data, 'mobilized_resources_through', 'third_parties'), split the options
            line2.data.get('mobilized_resources_through', ''),
            line2.get_data_option('mobilized_resources_through', 'unicef'),
            line2.get_data_option('mobilized_resources_through', 'private,_local'),
            line2.get_data_option('mobilized_resources_through', 'NGO'),
            line2.get_data_option('mobilized_resources_through', 'Governmental_i'),
            line2.get_data_option('mobilized_resources_through', 'other'),

            # get_choice_value(line2.data, 'type_of_support_required', 'challenges'), split the options
            line2.data.get('type_of_support_received', ''),
            line2.get_data_option('type_of_support_received', 'technical'),
            line2.get_data_option('type_of_support_received', 'inkind'),
            line2.get_data_option('type_of_support_received', 'financial'),
            line2.get_data_option('type_of_support_received', 'other'),

            get_choice_value(line2.data, 'support_received_helpful', 'rates'),
            line2.data.get('support_not_helpful_why', ''),
            line2.data.get('start', ''),
            line2.data.get('end', ''),

            submission_date,
        ]
        data6.append(content)

    book.add_sheet(data5)
    book.add_sheet(data6)

    timestamp = '{}-{}'.format(title, time.time())
    data = book.export("xlsx")
    if return_data:
        return data
    # store_file(data, timestamp, params)
    return True
