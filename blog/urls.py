from django.urls import path, include
from . import views

urlpatterns = [
    # /blog/
    path('', views.index, name='index'),
    path('<int:pk>/', views.single_post_page, name='sing_post_page'),

]