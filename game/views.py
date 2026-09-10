from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import PlayerProfile
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def save_score(request):
    if request.method == 'POST' and request.user.is_authenticated:
        data = json.loads(request.body)
        score = data.get('score', 0)
        profile = PlayerProfile.objects.get(user=request.user)
        if score > profile.high_score:
            profile.high_score = score
            profile.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'})

@csrf_exempt
def login_view(request):
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            error = 'Invalid username or password'
    return render(request, 'login.html', {'error': error})

def register_view(request):
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm')
        if password != confirm:
            error = 'Passwords do not match'
        elif User.objects.filter(username=username).exists():
            error = 'Username already taken'
        else:
            user = User.objects.create_user(username=username, password=password)
            PlayerProfile.objects.create(user=user)
            login(request, user)
            return redirect('home')
    return render(request, 'register.html', {'error': error})

def logout_view(request):
    logout(request)
    return redirect('login')

def home_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'home.html')

def level_select_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'level_select.html')

def leaderboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    players = PlayerProfile.objects.order_by('-high_score')[:10]
    return render(request, 'leaderboard.html', {'players': players})

def game_view(request, level):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'game.html', {'level': level})

def leaderboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    players = PlayerProfile.objects.order_by('-high_score')[:10]
    my_profile = PlayerProfile.objects.get(user=request.user)
    return render(request, 'leaderboard.html', {
        'players': players,
        'my_score': my_profile.high_score
    })