import bcrypt
from django.shortcuts import render, redirect
from django.http import HttpResponse

from user.forms import LoginForm
from user.models import User, Post, Comment, Follow


# Create your views here.

def user_page(request, username):
    if request.method == 'POST':
        if 'user-id' not in request.session:
            return redirect('user:user_login')

        user = User.objects.get(id = request.session.get('user-id'))

        if not user:
            return redirect('user:user_login')

        if request.POST.get('form_type') == 'post_form':
            content = request.POST.get('content')
            if content:
                post = Post(user=user, content=content)
                post.save()
        elif request.POST.get('form_type') == 'follow_form':
            user_on_page = User.objects.get(username=username)
            follow = Follow.objects.filter(user=user, followed=user_on_page).first()
            if follow:
                follow.delete()
            else:
                follow = Follow(user=user, followed=user_on_page)
                follow.save()
        else:
            post_id = request.POST.get('post_id')
            content = request.POST.get('content')
            post = Post.objects.get(id=post_id)
            new_comment = Comment(post=post, user=user, content=content)
            new_comment.save()

    is_page_of_logged_user = False

    try:
        user = User.objects.get(username = username)
        if user.id == request.session.get('user-id'):
            is_page_of_logged_user = True
    except User.DoesNotExist:
        return render(request, 'user/user_notfound.html', {'username': username})

    is_following = None
    if not is_page_of_logged_user and request.session.get('user-id'):
        logged_user = User.objects.get(id=request.session.get('user-id'))
        is_following = Follow.objects.filter(user=logged_user, followed=user).exists()

    return render(request, 'user/user_page.html', {
        'user': user,
        'is_page_of_logged_user': is_page_of_logged_user,
        'is_following': is_following,
    })

def user_create(request):
    warning = ''

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        r_password = request.POST.get('repeat_password')

        try:
            possible_user = User.objects.get(username=username)
            warning = f'User with username {username} already exists'
        except User.DoesNotExist:
            if password != r_password:
                warning = 'Passwords does not match'
            else:
                hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                new_user = User.objects.create(username=username, password_hash=hashed.decode('utf-8'))
                new_user.save()
                warning = ''
                return redirect('user:user_login')


    return render(request, 'user/user_create.html', {'warning': warning})

def user_login(request):
    message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            if bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
                request.session['user-id'] = user.id
                return redirect('home:home-page')  # username is stored in session
            else:
                message = 'Invalid password'
        except User.DoesNotExist:
            message = 'User not found'

    return render(request, 'user/user_login.html', {
        'warning': message,
        'form': LoginForm
    })

def user_logout(request):
    if 'user-id' in request.session:
        del request.session['user-id']
    return redirect('user:user_login')

def user_me(request):
    user_id = request.session.get('user-id')
    if user_id:
        try:
            user = User.objects.get(id=user_id)
            return redirect('user:user_page', user.username)
        except User.DoesNotExist:
            return redirect('user:user_login')
    else:
        return redirect('user:user_login')
