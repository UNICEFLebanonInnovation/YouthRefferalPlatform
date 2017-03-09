
from django.conf.urls import include, url
from django.views.generic import TemplateView

urlpatterns = [

    url(r'^$', TemplateView.as_view(template_name='portfolio/portfolio.html'), name='home'),
    url(r'^resume/$', TemplateView.as_view(template_name='portfolio/resume.html'), name='resume'),

]


