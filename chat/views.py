from django.shortcuts import render, redirect
from user.models import TherapyRequest


def chat_page(request, room_name):
    names = room_name.split('-')
    if not request.user.is_authenticated \
            or request.user.username not in [names[0], names[1]]:
        return redirect("login")
    if request.user.is_client:
        session_duration = TherapyRequest.objects.get(client=names[0], therapist=names[1]).duration
    else:
        session_duration = request.GET.get('session_duration')

    context = {
        'room_name': room_name,
        'duration': session_duration,
        'client': names[0]
    }
    return render(request, "chat/chat_page.html", context)


def end_session(request):
    client_username = request.GET.get('client')
    completed_session = TherapyRequest.objects.get(therapist=request.user.username, client=client_username)
    if completed_session:
        completed_session.delete()
    return redirect('/user/therapist/dashboard')
