from django.shortcuts import render
from .models import Post
# Create your views here.
def index(request):
  posts = Post.objects.all().order_by('-id')
  print(posts)
  return render(request, 'blog/index.html', {'posts':posts})