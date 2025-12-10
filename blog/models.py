from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse 
from ckeditor.fields import RichTextField

# --- 1. MANAGERS ---
class PostManager(models.Manager):
    def active(self):
        return self.filter(status='published')

# --- 2. CATEGORY MODEL ---
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

# --- 3. TAG MODEL ---
class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# --- 4. MAIN POST MODEL ---
class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts')
    tags = models.ManyToManyField(Tag, blank=True)
    
    image = models.ImageField(upload_to='uploads/%Y/%m/', blank=True, null=True)
    content = RichTextField()
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager() 
    published = PostManager() 

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
    def reading_time(self):
        words = len(self.content.split())
        minutes = words / 200
        return f"{int(minutes) + 1} min read"

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.slug])

# --- 5. CONTACT MODEL ---
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"
    










# blog/models.py ke end mein

class Subscriber(models.Model):
    email = models.EmailField(unique=True) # Duplicate emails nahi aayenge
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    





# blog/models.py ke end mein

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True) # Admin chahe toh comment hide kar sakta hai

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'