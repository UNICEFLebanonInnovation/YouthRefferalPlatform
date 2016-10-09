
from django.conf.urls import include, url
from django.views.generic import TemplateView

urlpatterns = [

    url(r'^$', TemplateView.as_view(template_name='portfolio/portfolio.html'), name='home'),
    url(r'^about/$', TemplateView.as_view(template_name='portfolio/about.html'), name='about'),

]


