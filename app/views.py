from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from users.models import Profile, InterestChoice
from matching.models import Partner, RelationshipRequest
from app.forms import FilterForm, SearchForm
from datetime import date, timedelta

@login_required
def home(request):
    partner_objects = Partner.objects.filter(current_user=request.user)
    partners = []
    for partner_object in partner_objects:
        partners.append(partner_object.its_partner)

    excluded_user_list = [request.user] + partners
    profiles = Profile.objects.exclude(user__in=excluded_user_list)
    
    # showing profiles of opposite gender
    if request.user.profile.gender is 'M':
        profiles = profiles.filter(gender='F')
    else:
        profiles = profiles.filter(gender='M')

    if request.method == 'POST':
        if 'btnformfilter' in request.POST: 
            form = FilterForm(request.POST)
            s_form = SearchForm()
            if form.is_valid():
                age_pref = form.cleaned_data['age']
                if not age_pref is None:
                    profiles = profiles.filter(dob__lte=date.today() - timedelta(days=365*age_pref),
                                                    dob__gte=date.today() - timedelta(days=(365*(age_pref+1) + 1)))
                state_pref = form.cleaned_data['state']
                if not state_pref is "":
                    profiles = profiles.filter(state=state_pref)
                interests_pref_list = [ interest for interest in form.cleaned_data['interests'] ]
                if len(interests_pref_list): #checking for empty list
                    interest_query = InterestChoice.objects.filter(interest__in=interests_pref_list)
                    profiles = profiles.filter(interests__in=interest_query)

        elif 'btnformsearch' in request.POST:
            form = FilterForm()
            s_form = SearchForm(request.POST)
            if s_form.is_valid():
                query = s_form.cleaned_data['query']
                profiles = profiles.filter(name__icontains=query)

    else:
        form = FilterForm()
        s_form = SearchForm()
    
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

    
    return render(request, 'home.html', {'context': context, 'partners': partners, 'req_received': req_received, 'form': form, 's_form': s_form})


#https://stackoverflow.com/questions/8000022/django-template-how-to-look-up-a-dictionary-value-with-a-variable
from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def index(request):
    return render(request, 'landing.html')