# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.views.i18n import JavaScriptCatalog

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView, RedirectView
from django.views import defaults as default_views

from rest_framework_nested import routers
from rest_framework_swagger.views import get_swagger_view

from referral_platform.youth.views import YoungPersonViewSet
from referral_platform.backends.views import ExporterViewSet
from referral_platform.registrations.views import RegistrationViewSet, AssessmentSubmissionViewSet

api = routers.SimpleRouter()
api.register(r'young-person', YoungPersonViewSet, base_name='young-person')
api.register(r'registration', RegistrationViewSet, base_name='registration')
api.register(r'assessment-submission', AssessmentSubmissionViewSet, base_name='assessment-submission')
api.register(r'backend-exporter', ExporterViewSet, base_name='backend-exporter')


schema_view = get_swagger_view(title='EMS API')

urlpatterns = [
    url(r'^referral_platform/admin/jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    # url(r'^', include('referral_platform.youth.urls', namespace='youth')),
    url(r'^$', TemplateView.as_view(template_name='pages/home.html'), name='home'),
    url(r'^home/$', TemplateView.as_view(template_name='pages/home.html'), name='home'),
    url(r'^courses/', include('referral_platform.courses.urls', namespace='courses')),
    url(r'^initiatives/', include('referral_platform.initiatives.urls', namespace='initiatives')),

    #url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name='about'),

    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, include(admin.site.urls)),

    # User management
    url(r'^users/', include('referral_platform.users.urls', namespace='users')),
    url(r'^accounts/', include('allauth.urls')),

    # Your stuff: custom urls includes go here
    url(r'^partners/', include('referral_platform.partners.urls', namespace='partners')),
    url(r'^locations/', include('referral_platform.locations.urls', namespace='locations')),
    url(r'^youth/', include('referral_platform.youth.urls', namespace='youth')),
    url(r'^registrations/', include('referral_platform.registrations.urls', namespace='registrations')),
    url(r'^clm/', include('referral_platform.clm.urls', namespace='clm')),
    url(r'^dashboard/', include('referral_platform.dashboard.urls', namespace='dashboard')),
    url(r'^backends/', include('referral_platform.backends.urls', namespace='backends')),

    url(r'^i18n/', include('django.conf.urls.i18n')),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/docs/', schema_view),

    url(r'^api/', include(api.urls)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    import debug_toolbar
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
