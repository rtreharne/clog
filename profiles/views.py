from django.shortcuts import render
from profiles.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from profiles.models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from projects.models import Project
from invite.models import Invitation
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse

def register(request, key=''):

    registered = False

    try:
        invite_record = Invitation.objects.get(key=key)
        if invite_record.activated == True:
            return HttpResponseRedirect(reverse('home'))
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('home'))

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.save()

            profile = profile_form.save(commit=False)
			invite_record = Invitation.objects.get(key=key)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True
			invite_record.activated = True

        else:
            print user_form.errors, profile_form.errors
    
    else:
        user_form = UserForm(instance=invite_record)
        profile_form = UserProfileForm()

    return render(request,
            'register.html',
			{'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
    invalid = False
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('dashboard'))
            else:
                return HttpResponse("Your account is disabled")

        else:
            invalid = True 
            return render(request, 'login.html', {'invalid': invalid})
                
    else:
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('home'))
        else:
            return render(request, 'login.html', {'invalid': invalid})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def dashboard(request):
    profile = UserProfile.objects.get(user=request.user)
    projects = Project.objects.filter(owner = profile)
    dict = {'profile': profile, 'projects': projects}
    return render(request, 'dashboard.html', dict) 
    
@login_required
def update_profile(request):
    submitted = False
    inst = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(data=request.POST, instance=inst)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user= request.user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            submitted=True

        else:
            print profile_form.errors
        
    else:
        profile_form = UserProfileForm(instance=inst)
    
    return render(request, 'update_profile.html', {'profile_form': profile_form, 'submitted': submitted})

def profile(request, user_id=1):
	profile = UserProfile.objects.get(user = User.objects.get(id=user_id))
        if profile.user == request.user:
            return HttpResponseRedirect(reverse('dashboard'))
        
        projects = Project.objects.filter(owner=profile)
	dictionary = {'profile': profile,
                      'projects': projects}
	return render(request, 'profile.html', dictionary)
