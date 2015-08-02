from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^(?P<project_id>\d+)/$', views.ContactView.as_view()),
]
