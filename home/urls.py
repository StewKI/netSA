from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home_page, name='home-page'),
    path('add_comment/<post_id>', views.add_comment, name='add_comment'),
]