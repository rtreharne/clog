from django.shortcuts import render
from profiles.models import UserProfile
from django.contrib.auth.models import User

def home(request):
	profiles = UserProfile.objects.order_by('user__last_name')
	return render(request, 'home.html', {'profiles': profiles})

def profile(request, user_id=1):
	profile = UserProfile.objects.get(user = User.objects.get(id=user_id))
	dictionary = {'profile': profile}
	return render(request, 'profile.html', dictionary)

