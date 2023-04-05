from django.urls import path
from . import views

urlpatterns = [
    # /
    path('', views.landing, name='landing'),
    # /about_me/
    path('about_me/', views.about_me, name='about_me'),
]