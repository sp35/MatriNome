from django.shortcuts import render, redirect, Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Your account has been created! You are now able to log in')
            return redirect('profile', username)
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


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