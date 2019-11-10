from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Partner, RelationshipRequest


@login_required
def send_match_request(request, username):
    try:
        to_user = get_object_or_404(User, username=username)
    except:
        messages.warning(request, 'Error')
        return redirect('home')

    if Partner.objects.filter(
        current_user=request.user,
        its_partner=to_user).exists():
        messages.success(request, 'You both are already matched')
    elif RelationshipRequest.objects.filter(
        from_user=request.user,
        to_user =to_user).exists():
        messages.warning(request, 'Request Already Sent!')
    else:
        RelationshipRequest.objects.create(
                    from_user=request.user,                     # The sender
                    to_user =to_user,                           # The recipient
                    message='Hi! I would like to add you')      # This message is optional
        messages.success(request, 'Match request sent!')
        
    return redirect('home')


@login_required
def accept_match_request(request, username):
    try:
        to_user = get_object_or_404(User, username=username)
    except:
        messages.warning(request, 'Error')
        return redirect('home')
    if Partner.objects.filter(current_user=request.user, its_partner=to_user).exists():
        messages.success(request, 'You both are already matched')
    else:
        Partner.objects.create(
                    current_user = request.user,                               
                    its_partner = to_user,                                    
                    )
        # creating a reverse relation
        Partner.objects.create(
                    current_user = to_user,                               
                    its_partner = request.user,                                    
                    )
        RelationshipRequest.objects.filter(from_user=to_user,
                                                to_user =request.user).delete()
        messages.success(request, 'Successfully added')

    return redirect('home')

@login_required
def reject_match_request(request, username):
    try:
        to_user = get_object_or_404(User, username=username)
        RelationshipRequest.objects.filter(from_user=to_user,
                                                to_user =request.user).delete()
        messages.success(request, 'Declined!')
    
    except:
        messages.warning(request, 'Error')

    return redirect('home')


@login_required
def view_matches(request):
    partner_objects = Partner.objects.filter(current_user=request.user)
    partners = []
    for partner_object in partner_objects:
        partners.append(partner_object.its_partner)

    return render(request, 'matching/partners_list.html', {'partners': partners})


@login_required
def view_requests(request):
    requests = RelationshipRequest.objects.filter(to_user=request.user)

    return render(request, 'matching/requests_list.html', {'requests': requests})


@login_required
def view_request_details(
    request, relationship_request_id):
    """ View a particular relationship request """
    r_request = get_object_or_404(RelationshipRequest, id=relationship_request_id)

    return render(request, 'matching/request.html', {"relationship_request": r_request})