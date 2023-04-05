from django.urls import path, include
from . import views

urlpatterns = [
    # /blog/
    path('', views.index, name='index'),

]