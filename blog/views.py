from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from .models import Post, Category, Tag, Comment
from .forms import PostForm, CommentForm

# Create your views here.


class PostList(ListView):
    model = Post
    ordering = '-pk'

    # 한페이지 보여줄 post 갯수 정하기
    paginate_by = 3
    
    # post_list.html : class이름_list.html 내부적으로 정의가 되어있기 때문에 생략가능
    # 파일명을 위에 있는 규칙으로 하지 않을 경우 명시해줘야함.
    # template_name = 'blog/post_list.html'

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()

        # Post 테이블에서 category 필드를 선택안 한 포스트의 갯수
        context['no_category_post_cnt'] = Post.objects.filter(
            category=None).count()
        return context


class PostDetail(DetailView):
    model = Post
    # template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        # Post 테이블에서 category 필드를 선택안 한 포스트의 갯수
        context['no_category_post_cnt'] = Post.objects.filter(
            category=None).count()
        context['comment_form'] = CommentForm
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

# from django.db.models import Q
# 방법2 : 카테고리 필터 FBV 함수 정의


def category_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        # 선택한 슬러그의 해당하는 Category테이블의 레코드
        category = Category.objects.get(slug=slug)
        # print(category)
        post_list = Post.objects.filter(category=category)
        # Post 테이블에서 선택한 category의 레코드만 필터링

    context = {
        'post_list': post_list,
        'categories': Category.objects.all(),
        'no_category_post_cnt': Post.objects.filter(category=None).count(),
        'category': category
    }
    # print(context)
    return render(request, 'blog/post_list.html', context)

# tag 필터 페이지 FBV로 정의


def tag_page(request, slug):
    # Tag테이블에서 클릭한 tag의 레코드를 가져옴
    tag = Tag.objects.get(slug=slug)
    # tag와 연결된 post들 모두 가져옴
    post_list = tag.post_set.all()

    # 아래 부분은 side weget을 실행하기 위한 부분임
    # 모든 Category 가져옴
    cotegories = Category.objects.all()
    no_category_post_cnt = Post.objects.filter(category=None).count()

    # dict로 만들기
    context = {
        'post_list': post_list,
        'tag': tag,
        'cotegories': cotegories,
        'no_category_post_cnt': no_category_post_cnt,
    }
    # dict type으로 구성한 데이터를 html템플릿으로 랜더링후, response
    return render(request, 'blog/post_list.html', context)

# post Create


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    # fields = ['title', 'hook_text', 'content',
    #           'head_image', 'file_upload', 'category']

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/blog/')
        
from django.shortcuts import get_object_or_404

def new_comment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else:
            return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied
    
class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def dispathc(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).displatch(request, *args, **kwargs)
        else:
            raise PermissionDenied