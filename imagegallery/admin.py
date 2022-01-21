from django.contrib import admin
from .models import Category, Post, PostImages

class PostImagesAdmin(admin.StackedInline):
    model = PostImages

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=("id", "user", "name")
 
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostImagesAdmin]
    list_display=("id", "title", "category", "owner", "description")
 
    class Meta:
       model = Post   
    
 
@admin.register(PostImages)
class PostImagesAdmin(admin.ModelAdmin):
    list_display=("id", "post", "images")

    
# Admin's View Site link
admin.site.site_url = "/"
admin.site.site_header = "Gallery Admin"