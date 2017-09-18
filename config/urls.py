# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views import defaults as default_views
from django.views.generic import TemplateView, RedirectView

from referral_platform.users.views import PasswordChangeView, PasswordChangeDoneView, \
    LoginRedirectView

urlpatterns = [
                  url(r'^$', RedirectView.as_view(url='/clm/index')),
                  url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name='about'),
                  url(r'^login-redirect/$', LoginRedirectView.as_view(), name='login-redirect'),
                  url(r'^change-password/$', PasswordChangeView.as_view(), name='change_password'),
                  url(r'^change-password-done/$', PasswordChangeDoneView.as_view(), name='change_password_done'),

    # User management
    url(r'^users/', include('referral_platform.users.urls', namespace='users')),
    url(r'^accounts/', include('allauth.urls')),

    # Your stuff: custom urls includes go here
    url(r'^partners/', include('referral_platform.partners.urls', namespace='partners')),
    url(r'^locations/', include('referral_platform.locations.urls', namespace='locations')),
    url(r'^clm/', include('referral_platform.clm.urls', namespace='clm')),
    url(r'^students/', include('referral_platform.students.urls', namespace='students')),
    url(r'^schools/', include('referral_platform.schools.urls', namespace='schools')),
    url(r'^outreach/', include('referral_platform.schools.urls', namespace='outreach')),

    url(r'^i18n/', include('django.conf.urls.i18n')),
                  url(r'^youth/', include('referral_platform.youth.urls', namespace='youth')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
