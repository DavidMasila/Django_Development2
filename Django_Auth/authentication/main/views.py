from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from .forms import RegistrationForm, PostForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from .models import Post

# Create your views here.
@login_required(login_url= "/login")
@permission_required("main.view_post", login_url='/login', raise_exception=True)
def home(request):
    posts_made = Post.objects.all()

    if request.method == "POST":
        post_id = request.POST.get('post-id')
        user_id = request.POST.get('user-id')

        if post_id:
            post = Post.objects.get(id=post_id)
            if post and (post.author == request.user or request.user.has_perm("main.delete_post")):
                post.delete()
        elif user_id:
            user = User.objects.get(id=user_id)
            if user and request.user.is_staff:
                group = Group.objects.get(name='default')
                group.user_set.remove(user)
                group = Group.objects.get(name='mod')
                group.user_set.remove(user)
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
@permission_required("main.add_post", login_url="/login", raise_exception=True)
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

