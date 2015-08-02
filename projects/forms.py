from django import forms
from django.contrib.auth.models import User
from projects.models import Project

class ProjectForm(forms.ModelForm):
	class Meta:
		model = Project
		fields = ('title', 'description',)
