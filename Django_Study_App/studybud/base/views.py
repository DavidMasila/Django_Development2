from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from .models import *
from .forms import RoomForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome {username.capitalize()}')
            return redirect('/')
        else:
            messages.warning(request, 'Username or Password is incorrect')
            return redirect(request.path)

    context={'page':page}
    return render(request, 'base/login_register.html', context)


def register(request):
    form =UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            #freezes the saving to be able to clean the data
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            #login the user and send them to home
            login(request, user)
            messages.success(request, f'Account created successfully for {user.username.capitalize()}')
            return redirect('home')
        else:
            messages.warning(request, 'Please check your credentials')
            return redirect(request.path)
    else:
        form = UserCreationForm()

    context = {
        'form':form
    }
    return render(request, 'base/login_register.html', context)

def home(request):
    q = request.GET.get('q','')
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) | 
        Q(name__icontains = q) |
        Q(description__icontains = q)
        )
    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains = q))
    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'room_messages':room_messages
    }
    return render(request, 'base/home.html', context)

def room(request, pk):
    pk = int(pk)
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body'),
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {
        'room': room,
        'room_messages':room_messages,
        'participants': participants
    }
    return render(request, 'base/room.html', context)

@login_required(login_url='/login')
def create_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RoomForm

    context ={'form':form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='/login')
def update_room(request, pk):
    room =  Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("You need to own the room to edit!!")
    
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RoomForm(instance=room)

    context = {
        'form':form
    }
    return render(request, 'base/room_form.html', context)

@login_required(login_url='/login')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("You need to own the room to Delete!!")
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})
    
@login_required(login_url='/login')
def delete_message(request, pk):
    message = Message.objects.get(id=pk)
    room_id=message.room.id
    if request.user != message.user:
        return HttpResponse("You need to own the message to Delete!!")
    
    if request.method == 'POST':
        message.delete()
        return redirect(f'/room/{room_id}')
    return render(request, 'base/delete.html', {'obj':message})
    

def logoutPage(request):
    logout(request)
    return redirect('/login')