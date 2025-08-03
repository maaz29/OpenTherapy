from .forms import CustomUserCreationForm, CustomLoginForm
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth import login, logout
from .models import User, TherapyRequest


def register_client(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                email=form.data['email'],
                username=form.data['username'],
                password=form.data['password1'],
                first_name=form.data['first_name'],
                last_name=form.data['last_name'],
                is_client=True,
                is_online=False,
            )
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'user/register.html', {'form': form})


def register_therapist(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                email=form.data['email'],
                username=form.data['username'],
                password=form.data['password1'],
                first_name=form.data['first_name'],
                last_name=form.data['last_name'],
                is_client=False,
                is_online=False,
            )
            return redirect('login')
        else:
            print("invalid")
    else:
        form = CustomUserCreationForm()
    return render(request, 'user/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            login_user = User.objects.get(username=user.username)
            if not user.is_client:
                login_user.is_online = True
            login_user.save()
            if user.is_client:
                return redirect('/user/client/dashboard')
            else:
                return redirect('/user/therapist/dashboard')
    else:
        form = CustomLoginForm()
    return render(request, 'user/login.html', {'form': form})


@login_required(login_url="/user/login/")
def client_dashboard(request):
    if not request.user.is_client:
        return Http404("Access Denied")
    active_therapists = User.objects.filter(is_online=True)

    requests_by_client = TherapyRequest.objects.filter(client=request.user.username)
    if requests_by_client:
        list_of_requested_therapists = requests_by_client.values_list('therapist', flat=True)
        requested_therapists = list(list_of_requested_therapists)
    else:
        requested_therapists = []
    context = {
        'therapists': active_therapists,
        'requested_therapists': requested_therapists
    }
    return render(request, 'user/client_dashboard.html', context=context)


@login_required(login_url="/user/login/")
def therapist_dashboard(request):
    if request.user.is_client:
        raise Http404("Access Denied")
    all_requesting_clients = TherapyRequest.objects.filter(therapist=request.user.username).exclude(status='declined')
    requests_from_clients = []
    for req in all_requesting_clients:
        client = User.objects.get(username=req.client)
        requests_from_clients.append(client)
    return render(request, 'user/therapist_dashboard.html', context={'clients': requests_from_clients})


@login_required(login_url="/user/login/")
def profile(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user.username)
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        if request.POST.get('age'):
            user.age = request.POST.get('age')
        else:
            user.age = None
        user.gender = request.POST.get('gender')
        user.city = request.POST.get('city')
        user.country = request.POST.get('country')
        user.reason = request.POST.get('reason')
        user.experience = request.POST.get('experience')
        user.qualifications = request.POST.get('qualifications')
        if request.POST.get('years_of_experience'):
            user.years_of_experience = request.POST.get('years_of_experience')
        else:
            user.years_of_experience = None
        if request.FILES.get('profile_image'):
            user.profile_image = request.FILES.get('profile_image')
        user.save()
        messages.success(request, "Profile Updated!")
        return redirect('profile')
    if request.user.is_client:
        return render(request, 'user/client_profile.html')
    else:
        return render(request, 'user/therapist_profile.html')


@login_required(login_url="/user/login/")
def client_requests(request):
    if request.method == 'POST':
        new_request = TherapyRequest(
            client=request.user.username,
            therapist=request.POST.get('therapist_username'),
            status='pending'
        )
        new_request.save()
        return redirect('/user/client/dashboard')
    all_requests = TherapyRequest.objects.filter(client=request.user.username)
    therapists_requested = []
    for req in all_requests:
        therapist = User.objects.get(username=req.therapist)
        session = TherapyRequest.objects.get(client=request.user.username, therapist=therapist.username)
        therapists_requested.append({'data': therapist, 'status': session.status, 'duration': session.duration})
    context = {
        'therapists': therapists_requested
    }
    return render(request, 'user/requests.html', context=context)


@login_required(login_url="/user/login/")
def cancel_request(request):
    if request.method == 'POST':
        request_to_delete = TherapyRequest.objects.get(client=request.user.username,
                                                       therapist=request.POST.get('therapist_username'))
        request_to_delete.delete()
        return redirect('/user/client/requests')
    return render(request, 'user/requests.html')


@login_required(login_url="/user/login/")
def decline_request(request):
    if request.method == 'POST':
        declined_request = TherapyRequest.objects.get(therapist=request.user.username,
                                                      client=request.POST.get('client_username'))
        declined_request.status = 'declined'
        declined_request.save()
        return redirect('/user/therapist/dashboard')
    return render(request, 'user/therapist_dashboard.html')


@login_required(login_url="/user/login/")
def accept_request(request):
    session_duration = request.POST.get('session_duration')

    if request.method == 'POST':
        accepted_request = TherapyRequest.objects.get(therapist=request.user.username,
                                                      client=request.POST.get('client_username'))
        accepted_request.status = 'accepted'
        if session_duration:
            accepted_request.duration = session_duration
        else:
            accepted_request.duration = 30
        accepted_request.save()
        chat_url = reverse('chat-page', args=[f"{request.POST.get('client_username')}-{request.user.username}"])
        chat_url += f"?session_duration={session_duration}"
        return redirect(chat_url)
    return render(request, 'chat/chat_page.html')


@login_required(login_url="/user/login/")
def logout_user(request):
    if not request.user.is_client:
        inactive_therapist = request.user
        inactive_therapist.is_online = False
        inactive_therapist.save()
    logout(request)
    return redirect('/user/login/')
