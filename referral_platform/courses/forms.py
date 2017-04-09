from __future__ import unicode_literals, absolute_import, division

from django.utils.translation import ugettext as _
from django import forms

from model_utils import Choices
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions, Accordion, PrependedText, InlineRadios, Alert
from crispy_forms.layout import Layout, Fieldset, Button, Submit, Div, Field, HTML

YES_NO_CHOICE = ((False, _('No')), (True, _('Yes')))


class LifeSkillsAssessmentForm(forms.Form):

    CHOICES = Choices(
        ('disagree', _('Completely disagree')),
        ('somewhat_disagree', _('Somewhat disagree')),
        ('neither', _('Neither agree nor disagree')),
        ('somewhat_agree', _('Somewhat agree')),
        ('agree', _('Completely agree')),
    )

    # comms skills
    articulation = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('I can articulate/state my thoughts, feelings and ideas to others well'))
    express_opinions = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('I can express my opinions when my classmates/friends/peers disagree with me'))
    not_interrupting = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('I communicate without interrupting others and allowing others too to communicate'))
    listening = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('I listen carefully to my classmates/friends/peers when they speak to me'))

    # self esteem
    satisfied = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('In general, I am satisfied with myself'))
    good_qualities =forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('I feel that I have a number of good qualities'))
    set_goals = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('I have set long term goals for myself'))
    make_decisions = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('I make decisions to help achieve my long term goals'))
    solve_problems = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('I can always manage to solve my problems if I try hard enough'))

    # analysis
    clarify_issues = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('Usually I have discussions with my friends/parents/classmates '
                  'to clarify issues before taking important decisions'))
    take_advice = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('I am flexible in changing my mind if I am convinced by my friends/parents/classmates opinions'))
    no_wrong_activities = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('I can say no to activities that I think are wrong.'))
    determine_facts = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('I know how to distinguish between facts and opinions'))
    consider_options = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('I try to consider different points of view and different solutions to problems'))
    creative_ideas = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_("I'm confident that I can develop creative ideas to solve problems"))

    # team building
    like_teams = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('Being part of a team is fun'))
    build_on_ideas = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('I build on the ideas of others.'))
    compromise= forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('I am willing to compromise my own view to obtain a group consensus.'))
    teamwork = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('I think working as a team helps accomplish better achievement'))
    constructive_feedback = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('I support and praise as well as give constructive criticisms to people I work with as part of a team'))

    # social cohesion
    trust_peers = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('In my social environment, if I have a problem, I have a friend of my own age that I trust to talk to'))
    accept_others = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('In my community, I accept others who are from different religion and nationality'))
    community_belonging = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('I feel I belong to my community'))

    # community
    conflict_concern = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_("I feel that any conflict in my community should be the everyone's concern"))
    social_activities = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('I like to be involved in social activities that help develop my community'))
    volunteering = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('I know where to volunteer in my community'))
    feel_appreciated = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('I feel I am appreciated for my contributions to my community'))
    contribute = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('I believe I can contribute towards the development (betterment) of my community'))

    # advocacy
    discuss_concerns = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('I am able to address/discuss community concerns in interactions with community leaders/people of authority at the local level'))
    awareness_raising = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('I participate actively in addressing my community concerns through media/social media'))

    # lifestyle
    wash_hands_before_food = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('I wash my hands before and after having food'))
    use_soap = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('I use soap to wash my hands'))
    wash_hands_after_toilet = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('I wash my hands after using toilet'))
    take_baths = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('I take bath after playing'))
    brush_teeth = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('I brush my teeth twice daily'))
    eat_well = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('When eating, I am mindful of my food intake by watching my portion sizes and nutritional intake'))
    exercise = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('I do some kind of stretching, strength or physical activities at least 3 times a week'))
    limit_screen_time = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('I spend no more than 2 hours a day on recreational screen time such as watching TV, gaming, or on the internet'))
    respect_environment = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('I respect the environment around me, I manage my solid waste in a way that causes no harm to nature'))


    def _generate_rows(self, *fields):
        return [
            Div(
                Div(
                    HTML("<p>{}</p>".format(self.fields[field].label)),
                    css_class='col-md-3',
                ),
                Div(
                    InlineRadios(field),
                    css_class='col-md-9',
                ),
                css_class='row'
            ) for field in fields
        ]

    def __init__(self, *args, **kwargs):
        super(LifeSkillsAssessmentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.help_text_inline = False
        self.helper.label_class = 'hidden'
        self.helper.layout = Layout(
            Fieldset(
                _('Part 1: Communication Skills'),
                *self._generate_rows('articulation',
                                     'express_opinions',
                                     'not_interrupting',
                                     'listening')
            ),
            Fieldset(
                _('Part 2: Self-esteem'),
                *self._generate_rows('satisfied',
                                     'good_qualities',
                                     'set_goals',
                                     'make_decisions',
                                     'solve_problems')
            ),
            Fieldset(
                _('Part 3: Critical thinking and analysis skills'),
                *self._generate_rows('clarify_issues',
                                     'take_advice',
                                     'no_wrong_activities',
                                     'determine_facts',
                                     'consider_options',
                                     'creative_ideas')
            ),
            Fieldset(
                _('Part 4: Teambuilding skills'),
                *self._generate_rows('like_teams',
                                     'build_on_ideas',
                                     'compromise',
                                     'teamwork',
                                     'constructive_feedback')
            ),
            Fieldset(
                _('Part 5: Social Cohesion & Sense of belonging'),
                *self._generate_rows('trust_peers',
                                     'accept_others',
                                     'community_belonging')
            ),
            Fieldset(
                _('Part 6: Social Responsibility & Volunteerism'),
                *self._generate_rows('conflict_concern',
                                     'social_activities',
                                     'volunteering',
                                     'feel_appreciated',
                                     'contribute')
            ),
            Fieldset(
                _('Part 7: Advocacy and Mobilization'),
                *self._generate_rows('discuss_concerns',
                                     'awareness_raising')
            ),
            Fieldset(
                _('Part 8: Healthy LifeStyle'),
                *self._generate_rows('wash_hands_before_food',
                                     'use_soap',
                                     'wash_hands_after_toilet',
                                     'take_baths',
                                     'brush_teeth',
                                     'eat_well',
                                     'exercise',
                                     'limit_screen_time',
                                     'respect_environment')
            ),
            FormActions(
                Submit('save', _('Save')),
                Button('cancel', _('Cancel'))
            )
        )


class DigitalSkillsAssessmentForm(forms.Form):

    CHOICES = Choices(
        (1, _('Not good')),
        (2, _('Some')),
        (3, _('Neutral')),
        (4, _('Good')),
        (5, _('Very good')),
    )

    can_use_computers = forms.TypedChoiceField(
        coerce=lambda x: x == 'True',
        choices=YES_NO_CHOICE,
        widget=forms.RadioSelect
    )

    reason_can_not_use_computers = forms.ChoiceField(
        choices=Choices(
            (_("I don't know how to use it")),
            (_("I don't have a computer at home")),
            (_("It's too expensive to use computers")),
            (_("I never felt the need to use it")),
            (_("There are not a lot of computers available in the community")),
            (_('Other')),
        ),
        widget=forms.RadioSelect,
        required=True
    )

    familiar_with = forms.MultipleChoiceField(
        choices=Choices(
            (_("Social networks & Forums")),
            (_("Presentation Software")),
            (_("Word Processing")),
            (_("Software applications")),
            (_("Internet/Search Engines")),
            (_('Spreadsheets')),
            (_('Operating systems')),
        ),
        widget=forms.RadioSelect,
        required=True
    )

    # ICT Skills
    know_computers = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('Types of computers and related parts'))
    importance_of_computers = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_("Describe the importance of computers in today's world"))
    computer_parts = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('Identify the main parts of computers'))
    use_keyboard = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('Identify the different groups of keys on a keyboard'))
    use_mouse = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('Perform different tasks by using a mouse'))
    media_presentations = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('Add photos, video and music to a presentation'))
    filling_system = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('Create a document filing system for easy retrieval'))
    media_documents = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('Insert graphics, text boxes and columns into a document'))
    presentations = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('Create a slideshow that is clear and visually interesting'))
    send_emails = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('Send emails with attachments'))
    sync_files = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('Sync data and media files across a number of devices'))
    internet_research = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('Conduct effective research on the Internet using a variety of resources'))
    utilize_cloud = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('Utilize the cloud to share files across devices'))

    # Graphic skills
    resize_images = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('Use Paint.net to resize images'))
    crop_images = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('Use Paint.net to crop images'))
    reformat_images = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('Use Paint.net to change from JPEG to PNG'))
    search_for_logo = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('Search for graphics on logomkr'))
    edit_logo = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('Move, resize and change the color of your logo'))
    add_text_to_logo = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('Adding text to logo'))
    save_logo = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('Save your logo'))

    # social networks
    create_social_account = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('Create a private account on social media (FB, Instagram)'))
    structure_social_media = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('Structure a frame work on social media'))
    create_youtube_account = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('Create a YouTube account'))
    create_facebook_page = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('Create a page on Facebook to market my business'))
    create_website = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('Develop a website for my business'))

    # audiovisual skills
    import_to_movie_maker = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('Use Windows Movie Maker to import and edit slide shows and videos.'))
    edit_in_movie_maker = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('Use Windows Movie Maker to edit your movies and use effects & transitions.'))
    add_audio_in_movie_maker = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('Use Windows Movie Maker to add and edit audio.'))

    # entrepreneurial skills
    produce_work_plan = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('Produce a work plan'))
    set_goals = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('Setting specific goals'))
    identify_targets = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('Identify the target group'))
    identify_issues = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('Identify issues that should be targeted'))

    # website skills
    use_wordpress = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('Developing a website with a cloud-based web development platform such as WordPress'))
    create_resources = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        label=_('Develop digital resources such as Main page, About Us and Contact us, Etc...'))

    def _generate_rows(self, *fields):
        return [
            Div(
                Div(
                    HTML("<p>{}</p>".format(self.fields[field].label)),
                    css_class='col-md-3',
                ),
                Div(
                    InlineRadios(field),
                    css_class='col-md-9',
                ),
                css_class='row'
            ) for field in fields
        ]

    def __init__(self, *args, **kwargs):
        super(DigitalSkillsAssessmentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.help_text_inline = False
        self.helper.label_class = 'hidden'
        self.helper.layout = Layout(
            'can_use_computers',
            'reason_can_not_use_computers',
            Alert(_('If you have used a computer before, please continue answering the questions below. '
                    'If you have not please STOP here.')),
            'familiar_with',
            Fieldset(
                _('ICT Literacy'),
                *self._generate_rows('know_computers',
                                     'importance_of_computers',
                                     'computer_parts',
                                     'use_keyboard',
                                     'use_mouse',
                                     'media_presentations',
                                     'filling_system',
                                     'media_documents',
                                     'presentations',
                                     'send_emails',
                                     'sync_files',
                                     'internet_research',
                                     'utilize_cloud')
            ),
            Fieldset(
                _('Graphic skills'),
                *self._generate_rows('resize_images',
                                     'crop_images',
                                     'reformat_images',
                                     'search_for_logo',
                                     'edit_logo',
                                     'add_text_to_logo',
                                     'save_logo')
            ),
            Fieldset(
                _('Social communication skills'),
                *self._generate_rows('create_social_account',
                                     'structure_social_media',
                                     'create_youtube_account',
                                     'create_facebook_page',
                                     'create_website')
            ),
            Fieldset(
                _('Audiovisual skills'),
                *self._generate_rows('import_to_movie_maker',
                                     'edit_in_movie_maker',
                                     'add_audio_in_movie_maker')
            ),
            Fieldset(
                _('Entrepreneurial skills'),
                *self._generate_rows('produce_work_plan',
                                     'set_goals',
                                     'identify_targets',
                                     'identify_issues')
            ),
            Fieldset(
                _('Website skills'),
                *self._generate_rows('use_wordpress',
                                     'create_resources')
            ),
            FormActions(
                Submit('save', _('Save')),
                Button('cancel', _('Cancel'))
            )
        )
