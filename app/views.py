from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from users.models import Profile
from matching.models import Partner, RelationshipRequest
from app.forms import FilterForm

@login_required
def home(request):
    partner_objects = Partner.objects.filter(current_user=request.user)
    partners = []
    for partner_object in partner_objects:
        partners.append(partner_object.its_partner)

    excluded_user_list = [request.user]

    if request.method == 'POST':
        form = FilterForm(request.POST)
        if form.is_valid():
            gender_pref = form.cleaned_data['gender']
            profiles = Profile.objects.filter(gender=gender_pref)
            show_matched = form.cleaned_data['show_matched']
            if show_matched == 'True':
               profiles = profiles.filter(user__in=partners) 
            else:
                excluded_user_list += partners
                profiles = profiles.exclude(user__in=excluded_user_list)
    else:
        form = FilterForm()
        profiles = Profile.objects.exclude(user__in=excluded_user_list)
    
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

    # setting context to none in case none of the profiles matched
    if all( len(value) == 0 for value in context.values() ):
        context = None
    # sorting context by matched_interests
    else:
        sorted_context = {}
        for k in sorted(context, key=lambda k: len(context[k]), reverse=True):
            sorted_context[k] = context[k]
        context = sorted_context   

    return render(request, 'app/home.html', {'context': context, 'partners': partners, 'req_received': req_received, 'form': form})


#https://stackoverflow.com/questions/8000022/django-template-how-to-look-up-a-dictionary-value-with-a-variable
from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def index(request):
    return render(request, 'app/index.html')