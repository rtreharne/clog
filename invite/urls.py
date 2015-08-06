from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', 'invite.views.invite', name='invite'),
]
