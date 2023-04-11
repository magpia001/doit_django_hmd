from django.urls import path
from . import views

urlpatterns = [
    # /blog/
    path('', views.PostList.as_view(), name='post_list'),
    # /blog/1/
    path('<int:pk>/', views.PostDetail.as_view(), name='post_etail'),
    # /blog/category/{self.slug}
    # /blog/category/파이썬
    path('category/<str:slug>/', views.category_page, name='category_fiter'),
    # /blog/tag/{self.slug}
    # /blog/tag/프로그래밍
    path('tag/<str:slug>/', views.tag_page, name='tag_filter'),
    # /blog/create_post
    path('create_post', views.PostCreate.as_view(), name='create_post'),
    # new comment
    path('<int:pk>/new_comment/', views.new_comment, name='new_comment'),

]
