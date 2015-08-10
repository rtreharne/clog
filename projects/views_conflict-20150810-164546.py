from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from projects.models import Project
from projects.forms import ProjectForm
from profiles.forms import UserProfile
from upload.models import Cell
import json
from django.core.serializers.json import DjangoJSONEncoder

def get_average(cells):
    average = []
    av = 0
    for i in range(len(cells)-1):
        n = 1
        average.append(cells[0][0])
        if cells[4][i] == cells[4][i+1]:
            n += 1
            av = (average[len(average)-1] + cells[0][i+1])/n
        else:
            average.append(av)
            n=1
    return average

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
    data = Cell.objects.filter(project=project).values_list('eff', 'jsc', 'voc', 'ff',  'date', 'id')
    data_json = json.dumps(list(data), cls=DjangoJSONEncoder)
    dict = {'project': project,
            'cells': cells,
            'data_json': data_json}
    return render(request, 'project.html', dict)

def jv(request, project_id=1, cell_id=1):
    project = Project.objects.get(id=project_id)
    cell = Cell.objects.get(id=cell_id)
    dict = {'project': project,
            'cell': cell}
    return render(request, 'jv.html', dict)
