"""
Projects app models
Stores portfolio projects with case studies
"""
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
import markdown
import bleach


class TechStack(models.Model):
    """Technology/Tool used in projects"""
    name = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=50, blank=True, help_text="e.g., Backend, Frontend, Database")
    
    class Meta:
        ordering = ['name']
        verbose_name = "Tech Stack Item"
        verbose_name_plural = "Tech Stack"
    
    def __str__(self):
        return self.name


class Project(models.Model):
    """Portfolio project with detailed information"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    short_description = models.TextField(max_length=300, help_text="Brief description for project cards")
    tech_stack = models.ManyToManyField(TechStack, related_name='projects')
    
    # Links
    github_url = models.URLField(blank=True, null=True)
    live_url = models.URLField(blank=True, null=True)
    
    # Case study content (markdown)
    case_study_content = models.TextField(
        blank=True,
        help_text="Detailed case study in Markdown format"
    )
    
    # Metadata
    featured = models.BooleanField(default=False, help_text="Show on homepage")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    order = models.IntegerField(default=0, help_text="Display order (lower numbers first)")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('projects:detail', kwargs={'slug': self.slug})
    
    def get_case_study_html(self):
        """Convert markdown to safe HTML"""
        html = markdown.markdown(
            self.case_study_content,
            extensions=['fenced_code', 'codehilite', 'tables', 'toc']
        )
        # Sanitize HTML to prevent XSS
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
    
    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    """Screenshots/images for projects"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/%Y/%m/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.project.title} - Image {self.order}"
