from django.shortcuts import render, redirect, Http404, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.models import User
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, AddInterestForm
from .models import Profile,InterestChoice
from matching.models import Partner, RelationshipRequest


def register(request):
    if request.method == 'POST':
        u_form = UserRegisterForm(request.POST)
        p_form = ProfileUpdateForm(request.POST)
        a_form = AddInterestForm(request.POST)

        if u_form.is_valid() and p_form.is_valid() and a_form.is_valid():
            u_form.save()
            username = u_form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            p = Profile.objects.get(user=user)
            p_form = ProfileUpdateForm(request.POST, instance=p)
            p_obj = p_form.save()

            extra_interest = a_form.cleaned_data.get('add_interest')
            if extra_interest.rstrip().lstrip() != '':
                choice = InterestChoice.objects.create(interest = extra_interest)
                p_obj.interests.add(choice)
                p_obj.save()
            
            messages.success(request, 'Your account has been created! You are now able to log in')
            return redirect('home')
    else:
        u_form = UserRegisterForm()
        p_form = ProfileUpdateForm()
        a_form = AddInterestForm()
    return render(request, 'register.html', {'u_form': u_form, 'p_form': p_form, 'a_form':a_form})


@login_required
def profile(request, username):
    try:
        this_user = User.objects.get(username=username)
    except:
        raise Http404

    # Flag that determines if we should show editable elements in template
    editable = False
    # Flag that determines if we should show otherwise abstracted details
    show = False
    req_received = False
    req_sent = False
    # Handling non authenticated user for obvious reasons
    if request.user.is_authenticated:
        if request.user == this_user:
            editable = True
        # for abstracting some details from non-matched users
        else:
            show = Partner.objects.filter(current_user=request.user,
                                         its_partner=this_user).exists()
            req_received = RelationshipRequest.objects.filter(from_user=this_user,
                                                         to_user=request.user).exists()
            req_sent = RelationshipRequest.objects.filter(from_user=request.user,
                                                         to_user=this_user).exists()

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=this_user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=this_user.profile)
        a_form = AddInterestForm(request.POST)
        

        if u_form.is_valid() and p_form.is_valid() and a_form.is_valid():
            u_form.save()
            p_obj = p_form.save()
            extra_interest = a_form.cleaned_data.get('add_interest')
            if extra_interest.rstrip().lstrip() != '':
                choice = InterestChoice.objects.create(interest=extra_interest)
                p_obj.interests.add(choice)
                p_obj.save()

            messages.success(request, 'Your account has been updated!')
            return redirect('profile', this_user.username)

    else:
        u_form = UserUpdateForm(instance=this_user)
        p_form = ProfileUpdateForm(instance=this_user.profile)
        a_form = AddInterestForm()

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'a_form': a_form,
        'this_user': this_user,
        'editable': editable,
        'show': show,
        'req_received': req_received,
        'req_sent': req_sent,
    }

    return render(request, 'profile.html', context)
