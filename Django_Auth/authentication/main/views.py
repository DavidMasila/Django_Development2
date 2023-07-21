from django.shortcuts import render, redirect
from .forms import RegistrationForm, PostForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Post

# Create your views here.
@login_required(login_url= "/login")
def home(request):
    posts_made = Post.objects.all()

    if request.method == "POST":
        post_id = request.POST.get('post-id')
        post = Post.objects.get(id=post_id)
        if post and post.author == request.user:
            post.delete()
    return render(request, 'main/home.html', {"posts":posts_made})


def sign_up(request):
    if request.method == "POST":
        #get the date and assign it to variable form
        form = RegistrationForm(request.POST)
        #check if data is valid
        if form.is_valid():
            # here we can save commmit = True (default) because the form data is 
            # complete with the model fields
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegistrationForm()

    return render(request, 'registration/sign_up.html', {"form": form})

@login_required(login_url="/login")
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # set commit = False so it doesn't save automatically save because of incomplete info
            post = form.save(commit=False)
            #assign the author of the post to the current logged in acc user
            post.author = request.user
            post.save() #effect that to the database
            return redirect("/home")
    else:
        form = PostForm()

    return render(request, 'main/create_post.html',  {"form":form})