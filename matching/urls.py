from django.urls import path
from . import views as matching_views

urlpatterns = [
    path('send_match_request/<username>', matching_views.send_match_request, name='send_match_request'),
    path('accept_match_request/<username>', matching_views.accept_match_request, name='accept_match_request'),
    path('reject_match_request/<username>', matching_views.reject_match_request, name='reject_match_request'),
    path('view_matches', matching_views.view_matches, name='view_matches'),
    path('view_requests', matching_views.view_requests, name='view_requests'),
    path('view_request_details/<int:relationship_request_id>', matching_views.view_request_details, name='view_request_details'),
]