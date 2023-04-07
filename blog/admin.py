from django.contrib import admin
from .models import Post, Category

# Register your models here.
admin.site.register(Post)

class CategoryAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('name', )}

class TagAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug': ('name', )}

# admin site 등록
admin.site.register(Category, CategoryAdmin)
admin.site.register(Category, TagAdmin)

