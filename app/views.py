from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from users.models import Profile
from matching.models import Partner, RelationshipRequest

@login_required
def home(request):
    profiles = Profile.objects.exclude(user=request.user)
    user_interests = request.user.profile.interests.all()
    context = {}
    req_received = {}
    for profile in profiles:
        matched_interests = []
        count = 0
        for interest in profile.interests.all():
            if interest in user_interests.all():
                count += 1
                matched_interests.append(interest)
        context[profile] = matched_interests
        req_received[profile.user] = RelationshipRequest.objects.filter(from_user=profile.user,
                                                         to_user=request.user).exists()

    partner_objects = Partner.objects.filter(current_user=request.user)
    partners = []
    for partner_object in partner_objects:
        partners.append(partner_object.its_partner)

    # setting context to none in case none of the profiles matched
    if all( len(value) == 0 for value in context.values() ):
        context = None

    # sorting context by matched_interests
    sorted_context = {}
    for k in sorted(context, key=lambda k: len(context[k]), reverse=True):
        sorted_context[k] = context[k]
    context = sorted_context   

    return render(request, 'app/home.html', {'context': context, 'partners': partners, 'req_received': req_received})


#https://stackoverflow.com/questions/8000022/django-template-how-to-look-up-a-dictionary-value-with-a-variable
from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)