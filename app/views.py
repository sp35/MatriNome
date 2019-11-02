from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from users.models import Profile

@login_required
def home(request):
	profiles = Profile.objects.exclude(user=request.user)
	user_interests = request.user.profile.interests.all()
	context = {}
	for profile in profiles:
		matched_interests = []
		count = 0
		for interest in profile.interests.all():
			if interest in user_interests.all():
				count += 1
				matched_interests.append(interest)

		context[profile] = matched_interests
	return render(request, 'app/home.html', {'context': context})