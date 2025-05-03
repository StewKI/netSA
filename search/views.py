from django.shortcuts import render
from django.db.models import Q
from user.models import User


# Create your views here.

def search_page(request):
    query = request.GET.get('q', '')
    users = []

    if query:
        users = User.objects.filter(
            Q(username__icontains=query)
        )

    context = {
        'users': users
    }
    return render(request, 'search/search_page.html', context)
