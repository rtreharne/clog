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
import time
from datetime import datetime

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

def get_stats(data):
    import numpy
    build = []
    elist = []
    stats = []
    delta =86400.0 
    current = time.mktime(data[0].date.timetuple())
    for dat in data:
        build.append([float(dat.eff), time.mktime(dat.date.timetuple())])
        if build[-1][1] > current - delta:
            elist.append(build[-1][0])
            continue

        else:
            stats.append([datetime.fromtimestamp(current).strftime("%Y-%m-%dT%H:%M:%S"), numpy.mean(elist)])
            current = build[-1][1]
            elist = [build[-1][0]]

    current = build[-1][1]
    stats.append([datetime.fromtimestamp(current).strftime("%Y-%m-%dT%H:%M:%S"), numpy.mean(elist)])

    #stats_json = json.dumps(list(stats), cls=DjangoJSONEncoder)
    return stats 

def project(request, project_id=1):
    project = Project.objects.get(id=project_id)
    try:
        cells = Cell.objects.filter(project=project).order_by('-date')
        stats = get_stats(cells)
    except IndexError:
        stats = None
    data = Cell.objects.filter(project=project).values_list('eff', 'jsc', 'voc', 'ff',  'date', 'id')
    data_json = json.dumps(list(data), cls=DjangoJSONEncoder)
    dict = {'project': project,
            'cells': cells,
            'data_json': data_json,
            'stats': stats}
    return render(request, 'project.html', dict)

def focus(request, project_id=1):
    project = Project.objects.get(id=project_id)
    try:
        cells = Cell.objects.filter(project=project).order_by('-date')
        stats = get_stats(cells)
    except IndexError:
        stats = None
    data = Cell.objects.filter(project=project).values_list('eff', 'jsc', 'voc', 'ff',  'date', 'id')
    data_json = json.dumps(list(data), cls=DjangoJSONEncoder)
    dict = {'project': project,
            'cells': cells,
            'data_json': data_json,
            'stats': stats}
    return render(request, 'focus.html', dict)

def jv(request, project_id=1, cell_id=1):
    project = Project.objects.get(id=project_id)
    cell = Cell.objects.get(id=cell_id)
    dict = {'project': project,
            'cell': cell}
    return render(request, 'jv.html', dict)
