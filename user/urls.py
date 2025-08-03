from django.urls import path
from . import views

urlpatterns = [
    path('client/register/', views.register_client, name='c_register'),
    path('therapist/register/', views.register_therapist, name='t_register'),
    path('login/', views.user_login, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('client/dashboard/', views.client_dashboard, name='client_dashboard'),
    path('therapist/dashboard/', views.therapist_dashboard, name='therapist_dashboard'),
    path('profile/', views.profile, name='profile'),
    path('client/requests', views.client_requests, name='client_requests'),
    path('client/requests/delete', views.cancel_request, name='cancel_request'),
    path('therapist/dashboard/delete', views.decline_request, name='decline_request'),
    path('therapist/dashboard/accept', views.accept_request, name='accept_request'),
]
