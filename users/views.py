from django.shortcuts import render, redirect, Http404, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from .models import Profile


def register(request):
    if request.method == 'POST':
        u_form = UserRegisterForm(request.POST)
        p_form = ProfileUpdateForm(request.POST)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            username = u_form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            p = Profile.objects.get(user=user)
            p_form = ProfileUpdateForm(request.POST, instance=p)
            p_form.save()
            messages.success(request, 'Your account has been created! You are now able to log in')
            return redirect('home')
    else:
        u_form = UserRegisterForm()
        p_form = ProfileUpdateForm()
    return render(request, 'users/register.html', {'u_form': u_form, 'p_form': p_form})


@login_required
def profile(request, username):
    try:
        this_user = User.objects.get(username=username)
    except:
        raise Http404

    # Flag that determines if we should show editable elements in template
    editable = False
    # Handling non authenticated user for obvious reasons
    if request.user.is_authenticated and request.user == this_user:
        editable = True

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=this_user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=this_user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile', this_user.username)

    else:
        u_form = UserUpdateForm(instance=this_user)
        p_form = ProfileUpdateForm(instance=this_user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'this_user': this_user,
        'editable': editable
    }

    return render(request, 'users/profile.html', context)