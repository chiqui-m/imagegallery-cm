from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_image_file_extension

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=50, null=False, blank=False)
    user=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class Post(models.Model):        
    title       = models.CharField(max_length=30, blank=False)
    description = models.TextField(max_length=300)
    category    = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    owner       = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}: {self.title} - {self.category} by ({self.owner})"
 
class PostImages(models.Model):
    post    = models.ForeignKey(Post, default=None, on_delete=models.CASCADE)
    images  = models.ImageField(upload_to = 'images/', validators=[validate_image_file_extension])
 
    def __str__(self):
        return f"{self.id}.{self.post.id} : {self.post.category} - {self.post.title}"