from django.db import models

import os

# Create your models here.
class Post(models.Model):
  title = models.CharField(max_length=30)
  hook_text = models.CharField(max_length=100, blank=True)
  content = models.TextField()
  head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d', blank=True)
  file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d', blank=True)

  created_at = models.DateField(auto_now_add=True)
  updated_at = models.DateField(auto_now=True)

  def __str__(self):
    return f'[{self.id}] {self.title}'
  
  def get_absolute_url(self):
    return f'/blog/{self.pk}/'
  
  # upload 파일 이름 가져오기
  def get_file_name(self):
    f_name = os.path.basename(self.file_upload.name)
    # print(f_name)
    return f_name
  
  # upload 파일 확장자 가져오기
  def get_file_ext(self):
    f_ext = self.get_file_name().split(".")[-1]
    # print(f_ext)
    return f_ext
  
