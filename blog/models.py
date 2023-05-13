from django.db import models
from user.models import User
from django.utils.text import slugify


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=150,unique=True)
    slug = models.SlugField(null=True,blank=True)
    created = models.DateField(auto_now_add=True) 

    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Tag(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(null=True,blank=True)
    created = models.DateField(auto_now_add=True) 

    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Blog(models.Model):
    user = models.ForeignKey(User, related_name="user_blogs",on_delete=models.CASCADE)
    category = models.ForeignKey(Category,related_name="category_blogs",on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag,related_name="tag_blogs",blank=True)
    likes = models.ManyToManyField(User,related_name="user_likes", blank=True)
    title = models.CharField(max_length=140)
    slug = models.SlugField(null=True,blank=True)
    blog_image = models.ImageField(upload_to="blog_images")
    description = models.TextField()
    created = models.DateField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Comment(models.Model):
    user = models.ForeignKey(User, related_name="user_comments", on_delete= models.CASCADE)
    blog_comment = models.ForeignKey(Blog, related_name="blog_comments",on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.text
    
class Reply(models.Model):
    user = models.ForeignKey(User, related_name="user_replies", on_delete= models.CASCADE)
    blog_reply = models.ForeignKey(Comment, related_name="comment_replies",on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.text