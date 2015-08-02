from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from projects.models import Project
from projects.forms import ProjectForm
from profiles.forms import UserProfile
from upload.models import Cell

@login_required
def new_project(request):
    submitted = False

    if request.method == 'POST':
        project_form = ProjectForm(data=request.POST)
		
        if project_form.is_valid():
            project = project_form.save(commit=False)
            project.owner = UserProfile.objects.get(user=request.user)
            project.save()
            submitted = True

        else:
			print project_form.errors
    
    else:	    
	    project_form = ProjectForm()
	
    return render(request, 'new_project.html', {'project_form': project_form, 'submitted': submitted})

def project(request, project_id=1):
    project = Project.objects.get(id=project_id)
    cells = Cell.objects.filter(project=project).order_by('-date')
    dict = {'project': project,
            'cells': cells}
    return render(request, 'project.html', dict)
