from PIL.ImImagePlugin import number
from django.contrib.auth import login as auth_login, authenticate, logout
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import  User
from django.template.defaultfilters import title
from django.views.generic import ListView

from .models import Userprofile, Post

# Create your views here.


def register(request):
    if request.method == "POST":
        username = request.POST.get('user')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        middle_name = request.POST.get('middle_name')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        avatar = request.FILES.get('avatar')

        if User.objects.filter(username = username).exists():
            return render(request, 'register.html', {'error' : 'Пользователь с таким именем уже существует'})

        if password != password2:
            return render(request, 'register.html', {'error' : 'Пароли не похожи'})

        try:
            profile = User.objects.create_user(username = username, password = password)

            Userprofile.objects.create(user = profile, first_name = first_name, last_name = last_name, middle_name = middle_name, avatar = avatar)
            return redirect('login')
        except IntegrityError:
            return render(request, 'register.html', {'error' : 'не получилось создать аккаунт'})

    return render(request, 'register.html')

def login_views(request):
    if request.method == 'POST':
        username = request.POST.get('user')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error' : 'ошибка авторизации'})

    return render(request, 'login.html')


def profile(request):

    if request.user.is_authenticated:
        try:
            user_profile = Userprofile.objects.get(user = request.user)

        except Userprofile.DoesNotExist:
            user_profile = None

        return render(request, 'profile.html', {'user_profile' : user_profile})
    return render(request, 'profile.html')


def home(request):
    query = request.GET.get('query', '')
    posts = Post.objects.all()

    if query:
        posts = posts.filter(title__icontains=query)



    return render(request, 'home.html', {'posts': posts, 'query' : query})

def logout_views(request):
    logout(request)
    return redirect('login')

def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        number = request.POST.get('number')
        date = request.POST.get('date')
        time = request.POST.get('time')

        if Post.objects.filter(title = title).exists():
            return render(request, 'create_post.html', {'error' : 'пост с таким названием уже существует'})

        try:

            Post.objects.create(title = title, description = description, number = number, date = date, time = time)

        except Post.DoesNotExist:
            return render(request, 'create_post.html', {'error' : 'Не получилось создать пост'})

    return render(request, 'create_post.html')

def post_detail(request, post_id):
    post = get_object_or_404(Post, id = post_id )
    return render(request, 'post_detail.html', {'post' : post})

def edit_profile(request):
    user = request.user

    # Проверяем, существует ли профиль для текущего пользователя
    try:
        user_profile = user.userprofile
    except Userprofile.DoesNotExist:
        return render(request, 'edit_profile.html', {'error': 'Профиль не найден. Пожалуйста, создайте профиль.'})

    if request.method == 'POST':
        user.username = request.POST.get('user')
        user_profile.first_name = request.POST.get('first_name')
        user_profile.last_name = request.POST.get('last_name')
        user_profile.middle_name = request.POST.get('middle_name')

        if request.FILES.get('avatar'):
            user_profile.avatar = request.FILES['avatar']

        user.save()
        user_profile.save()

        return redirect('profile')

    return render(request, 'edit_profile.html', {'user_profile': user_profile})







