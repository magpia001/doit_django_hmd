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

  def get_context_data(self, **kwargs):
    context = super(PostDetail, self).get_context_data()
    context['categories'] = Category.objects.all()
    # Post 테이블에서 category 필드를 선택안 한 포스트의 갯수
    context['no_category_post_cnt'] = Post.objects.filter(category=None).count()
    return context
  
# 방법1 : 카테고리 필더터 FBV 함수 정의
# def category_page(request, slug):
#   context = {}
#   # 선택한 슬러그의 해당하는 Category테이블의 레코드
#   category = Category.objects.get(slug=slug)
#   print(category)
#   # Post 테이블에서 선택한 category의 레코드만 필터링
#   context['post_list'] = Post.objects.filter(category=category)
#   # Category 테이블의 목록 모두 가져옴
#   context['categories'] = Category.objects.all()
#   # Post 테이블에서 category 필드를 선택안 한 포스트의 갯수
#   context['no_category_post_cnt'] = Post.objects.filter(category=None).count()
#   # 선택한 카테고리의 레코드
#   context['category'] = category
#   # print(context)
#   return render(request, 'blog/post_list.html', context)


# 방법2 : 카테고리 필터 FBV 함수 정의
def category_page(request, slug):
  if slug == 'no_category':
    category = '미분류'
    post_list = Post.objects.filter(category=None)
  else:
    # 선택한 슬러그의 해당하는 Category테이블의 레코드
    category = Category.objects.get(slug=slug)
    post_list = Post.objects.filter(category=category)
    # Post 테이블에서 선택한 category의 레코드만 필터링

  context = {
    'post_list': post_list,
    'categories': Category.objects.all(),
    'no_category_post_cnt': Post.objects.filter(category=None).count(),
    'category': category
  }
  # print(context)
  return render(request,'blog/post_list.html', context)