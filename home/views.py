from django.shortcuts import render, redirect

from user.models import User, Post, Comment


def add_comment(request, post_id):
    if request.method == 'POST':
        if 'user-id' not in request.session:
            return redirect('user:user_login')

        try:
            user = User.objects.get(id=request.session.get('user-id'))
            post = Post.objects.get(id=post_id)
            content = request.POST.get('content')

            if content:
                comment = Comment(post=post, user=user, content=content)
                comment.save()

            return redirect('home:home-page')
        except (User.DoesNotExist, Post.DoesNotExist):
            return redirect('user:user_login')

    return redirect('home:home-page')


# Create your views here.
def home_page(request):
    user_id = request.session.get('user-id')
    if not user_id:
        return redirect('user:user_login')

    user = None
    try:
        user = User.objects.get(id = user_id)
    except User.DoesNotExist:
        return redirect('user:user_login')

    followed_users = User.objects.filter(followed_by__user=user)
    posts = Post.objects.filter(user__in=followed_users).order_by('-created_at')

    return render(request, 'home/home_page.html', {'username': user.username, 'posts': posts})
