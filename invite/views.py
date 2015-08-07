from django.shortcuts import render
from django.template.loader import render_to_string
from invite.forms import InviteForm
from django.core.mail import send_mail, EmailMultiAlternatives
from profiles.models import UserProfile
import random
from django.core.exceptions import ObjectDoesNotExist
from invite.models import Invitation

def key_gen():
	return ''.join(random.choice('1234567890ABCDEF') for i in range(8))

def invite(request):

	submitted = False

	if request.method == 'POST':
		invite_form = InviteForm(data=request.POST)
                inviter = UserProfile.objects.get(user=request.user)

                try:
                    obj = Invitation.objects.get(owner=inviter, email=request.POST['email'])

                    flag = True
                    return render(request, 'invite.html', {'flag': flag})
                except ObjectDoesNotExist:
                    flag = False

		if invite_form.is_valid():
			invite = invite_form.save(commit=False)
			invite.key = key_gen()
			invite.message = request.POST['message'] + 'test_string'
			invite.owner = inviter
                        invite.activated = True
			invite.save()

			# Email message
			subject = '%s %s invites YOU!' % (inviter.user.first_name, inviter.user.last_name)

			text_content = render_to_string("email_text.txt", {'message': request.POST['message'], 'key': invite.key, 'inviter': inviter})
			html_content = render_to_string("email_html.html", {'message': request.POST['message'], 'key': invite.key, 'inviter': inviter})
			email = request.POST['email']

			msg = EmailMultiAlternatives(subject, text_content, 'rob.pvsat@gmail.com', [email])
			msg.attach_alternative(html_content, "text/html")
			msg.send()
                        
			submitted=True
		else:
			print invite_form.errors

	else:
		invite_form = InviteForm()

	return render(request, 'invite.html', {'invite_form': invite_form, 'submitted': submitted})



