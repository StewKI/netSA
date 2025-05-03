from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('page/<str:username>/', views.user_page, name='user_page'),
    path('create/', views.user_create, name='user_create'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('me/', views.user_me, name='user_me')
]
