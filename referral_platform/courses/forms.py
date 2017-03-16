from __future__ import unicode_literals, absolute_import, division

from django.utils.translation import ugettext as _
from django import forms

from model_utils import Choices
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import FormActions, Accordion, PrependedText, InlineRadios
from crispy_forms.layout import Layout, Fieldset, Button, Submit, Div, Field, HTML




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
        help_text='I can articulate/state my thoughts, feelings and ideas to others well')
    express_opinions = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        help_text='I can express my opinions when my classmates/friends/peers disagree with me')
    not_interrupting = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        help_text='I communicate without interrupting others and allowing others too to communicate')
    listening = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        help_text='I listen carefully to my classmates/ friends/ peers when they speak to me')

    # self esteem
    satisfied = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        help_text='In general, I am satisfied with myself')
    good_qualities =forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        help_text='I feel that I have a number of good qualities')
    set_goals = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        help_text='I have set long term goals for myself')
    make_decisions = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        help_text='I make decisions to help achieve my long term goals')
    solve_problems = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        help_text='I can always manage to solve my problems if I try hard enough')

    # analysis
    clarify_issues = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        help_text='Usually I have discussions with my friends/parents/classmates '
                  'to clarify issues before taking important decisions')
    take_advice = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        help_text='I am flexible in changing my mind if I am convinced by my friends/parents/classmates opinions.')
    no_wrong_activities = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        help_text='I can say no to activities that I think are wrong.')
    determine_facts = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        help_text='I know how to distinguish between facts and opinions')
    consider_options = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        help_text='I try to consider different points of view and different solutions to problems.')
    creative_ideas = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        help_text="I'm confident that I can develop creative ideas to solve problems")

    # team building
    like_teams = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        help_text='Being part of a team is fun')
    build_on_ideas = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        help_text='I build on the ideas of others.')
    compromise= forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        help_text='I am willing to compromise my own view to obtain a group consensus.')
    teamwork = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        help_text='I think working as a team helps accomplish better achievement')
    constructive_feedback = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        help_text='I support and praise as well as give constructive criticisms to people I work with as part of a team')

    # social cohesion
    trust_peers = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        help_text='In my social environment, if I have a problem, I have a friend of my own age that I trust to talk to')
    accept_others = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        help_text='In my community, I accept others who are from different religion and nationality')
    community_belonging = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        help_text='I feel I belong to my community')

    # community
    conflict_concern = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        help_text="I feel that any conflict in my community should be the everyone's concern")
    social_activities = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        help_text='I like to be involved in social activities that help develop my community')
    volunteering = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        help_text='I know where to volunteer in my community')
    feel_appreciated = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        help_text='I feel I am appreciated for my contributions to my community')
    contribute = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        help_text='I believe I can contribute towards the development (betterment) of my community')

    # advocacy
    discuss_concerns = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        help_text='I am able to address/discuss community concerns in interactions with community leaders/people of authority at the local level')
    awareness_raising = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect,
        help_text='I participate actively in addressing my community concerns through media/social media')



    def _generate_rows(slef, *fields):
        return [
            Div(
                Div(
                    HTML("<p>{}</p>".format(slef.fields[field].help_text)),
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
        self.helper.layout = Layout(
            Fieldset(
                'Part 1: Communication Skills',
                *self._generate_rows('articulation',
                                     'express_opinions',
                                     'not_interrupting',
                                     'listening')
            ),
            Fieldset(
                'Part 2: Self-esteem',
                *self._generate_rows('satisfied',
                                     'good_qualities',
                                     'set_goals',
                                     'make_decisions',
                                     'solve_problems')
            ),
            Fieldset(
                'Part 3: Critical thinking and analysis skills',
                *self._generate_rows('clarify_issues',
                                     'take_advice',
                                     'no_wrong_activities',
                                     'determine_facts',
                                     'consider_options',
                                     'creative_ideas')
            ),
            Fieldset(
                'Part 4: Teambuilding skills',
                *self._generate_rows('like_teams',
                                     'build_on_ideas',
                                     'compromise',
                                     'teamwork',
                                     'constructive_feedback')
            ),
            Fieldset(
                'Part 5: Social Cohesion & Sense of belonging',
                *self._generate_rows('trust_peers',
                                     'accept_others',
                                     'community_belonging')
            ),
            Fieldset(
                'Part 6: Social Responsibility & Volunteerism',
                *self._generate_rows('conflict_concern',
                                     'social_activities',
                                     'volunteering',
                                     'feel_appreciated',
                                     'contribute')
            ),
            Fieldset(
                'Part 7: Advocacy and Mobilization',
                *self._generate_rows('discuss_concerns', 'awareness_raising')
            ),
            FormActions(
                Submit('save', 'Save changes'),
                Button('cancel', 'Cancel')
            )
        )

