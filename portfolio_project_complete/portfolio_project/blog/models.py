"""
Blog app models
Writing/articles with markdown support
"""
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User
import markdown
import bleach


class Category(models.Model):
    """Blog post categories"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Post(models.Model):
    """Blog post with markdown content"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    
    excerpt = models.TextField(max_length=300, help_text="Brief summary for post listings")
    content = models.TextField(help_text="Full post content in Markdown")
    
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")
    
    featured_image = models.ImageField(upload_to='blog/%Y/%m/', blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    featured = models.BooleanField(default=False, help_text="Feature on homepage")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-published_at', '-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})
    
    def get_content_html(self):
        """Convert markdown to safe HTML"""
        html = markdown.markdown(
            self.content,
            extensions=['fenced_code', 'codehilite', 'tables', 'toc']
        )
        allowed_tags = [
            'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'strong', 'em', 'a', 'ul', 'ol', 'li',
            'blockquote', 'code', 'pre', 'hr', 'br',
            'table', 'thead', 'tbody', 'tr', 'th', 'td',
            'img', 'div', 'span'
        ]
        allowed_attrs = {
            'a': ['href', 'title'],
            'img': ['src', 'alt', 'title'],
            'code': ['class'],
            'div': ['class'],
            'span': ['class'],
        }
        return bleach.clean(html, tags=allowed_tags, attributes=allowed_attrs)
    
    def get_tags_list(self):
        """Return tags as a list"""
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    def __str__(self):
        return self.title
