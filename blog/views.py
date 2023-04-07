from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Category

# Create your views here.

class PostList(ListView):
  model = Post
  # post_list.html : class이름_list.html 내부적으로 정의가 되어있기 때문에 생략가능
  # 파일명을 위에 있는 규칙으로 하지 않을 경우 명시해줘야함. 
  # template_name = 'blog/post_list.html'
  ordering = '-pk'

  def get_context_data(self, **kwargs):
    context = super(PostList, self).get_context_data()
    context['categories'] = Category.objects.all()
    # Post 테이블에서 category 필드를 선택안 한 포스트의 갯수
    context['no_category_post_cnt'] = Post.objects.filter(category=None).count()
    return context


class PostDetail(DetailView):
  model = Post
  # template_name = 'blog/post_detail.html'
