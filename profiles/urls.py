from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('',
    url(r'^register/$', 'profiles.views.register', name='register'),
    url(r'^login/$', 'profiles.views.user_login', name='login'),
    url(r'^logout/$', 'profiles.views.user_logout', name='logout'),
    url(r'^dashboard/$', 'profiles.views.dashboard', name='dashboard'),
    url(r'^update_profile/$', 'profiles.views.update_profile', name='update_profile'),
    url(r'^profile/(?P<user_id>\d+)/$', 'profiles.views.profile'),
	url(r'^new_project/$', 'projects.views.new_project', name='new_project'),
	url(r'^project/(?P<project_id>\d+)/$', 'projects.views.project'),
	url(r'^project/(?P<project_id>\d+)/(?P<cell_id>\d+)/$', 'projects.views.jv'),
    url(r'^upload/', include('upload.urls')),
	
)
