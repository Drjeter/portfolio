# Architecture Documentation

This document explains the architectural decisions, patterns, and rationale behind the Django portfolio application.

## Table of Contents
1. [High-Level Architecture](#high-level-architecture)
2. [Application Design](#application-design)
3. [Database Schema](#database-schema)
4. [Security Architecture](#security-architecture)
5. [Performance Considerations](#performance-considerations)
6. [Deployment Architecture](#deployment-architecture)

---

## High-Level Architecture

### Technology Choices

**Backend Framework: Django 5.0**
- Mature, battle-tested framework
- Built-in admin interface
- Excellent ORM for database operations
- Strong security features out of the box
- Large ecosystem and community

**Database: PostgreSQL**
- Production-grade reliability
- Advanced features (JSON fields, full-text search)
- Excellent Django integration
- Scalability for future growth
- ACID compliance

**Frontend: Bootstrap 5 + Minimal JS**
- Professional appearance without heavy JavaScript
- Responsive design built-in
- Fast page loads
- Easy to customize
- Accessibility features

**Deployment: Gunicorn + Whitenoise**
- Gunicorn: Production WSGI server
- Whitenoise: Efficient static file serving
- No separate web server needed
- Simplified deployment

---

## Application Design

### App Structure

The project follows Django's "app per feature" pattern:

```
portfolio_project/
├── config/          # Project-wide configuration
├── core/            # Homepage, contact, shared functionality
├── projects/        # Project portfolio
└── blog/            # Writing and articles
```

**Rationale:**
- Clear separation of concerns
- Each app is independently maintainable
- Easy to add new features
- Follows Django best practices

### Design Patterns

#### 1. Fat Models, Thin Views

Models contain business logic:

```python
class Project(models.Model):
    def get_case_study_html(self):
        """Convert markdown to safe HTML"""
        # Markdown conversion logic here
```

Views focus on request/response:

```python
class ProjectDetailView(DetailView):
    model = Project
    # Minimal logic, delegates to model
```

**Benefits:**
- Business logic is testable
- Views are simple and clear
- Logic is reusable across views

#### 2. Class-Based Views (CBVs)

Using Django's generic views:
- `ListView` for list pages
- `DetailView` for detail pages
- `CreateView` for forms

**Benefits:**
- Less boilerplate code
- Built-in pagination
- Consistent patterns
- Easy to override behavior

#### 3. Template Inheritance

Base template with shared layout:

```
base.html
├── core/home.html
├── projects/project_list.html
├── projects/project_detail.html
├── blog/post_list.html
└── blog/post_detail.html
```

**Benefits:**
- DRY (Don't Repeat Yourself)
- Consistent layout
- Easy global changes

---

## Database Schema

### Projects App

```
┌─────────────────┐
│   TechStack     │
├─────────────────┤
│ id (PK)         │
│ name            │
│ category        │
└─────────────────┘
         │
         │ many-to-many
         │
┌─────────────────────┐       ┌──────────────────┐
│     Project         │──────<│  ProjectImage    │
├─────────────────────┤  1:N  ├──────────────────┤
│ id (PK)             │       │ id (PK)          │
│ title               │       │ project_id (FK)  │
│ slug (unique)       │       │ image            │
│ short_description   │       │ caption          │
│ case_study_content  │       │ order            │
│ github_url          │       └──────────────────┘
│ live_url            │
│ featured            │
│ status              │
│ order               │
│ created_at          │
│ updated_at          │
└─────────────────────┘
```

**Design Decisions:**

1. **Slug Field:** SEO-friendly URLs
2. **Many-to-Many TechStack:** Projects can use multiple technologies
3. **Separate ProjectImage:** Multiple screenshots per project
4. **Order Field:** Control display sequence
5. **Status Field:** Draft/published workflow

### Blog App

```
┌──────────────┐
│   Category   │
├──────────────┤
│ id (PK)      │
│ name         │
│ slug         │
└──────────────┘
       │
       │ 1:N
       │
┌─────────────────────┐
│       Post          │
├─────────────────────┤
│ id (PK)             │
│ title               │
│ slug (unique)       │
│ author_id (FK)      │──> User
│ category_id (FK)    │
│ excerpt             │
│ content (markdown)  │
│ tags                │
│ featured_image      │
│ status              │
│ featured            │
│ created_at          │
│ updated_at          │
│ published_at        │
└─────────────────────┘
```

**Design Decisions:**

1. **Separate Category Model:** Enforces consistency
2. **Tags as CharField:** Simple implementation, flexible
3. **Markdown Content:** Writer-friendly, version-controllable
4. **Published Date:** Separate from created date for scheduling

### Core App

```
┌──────────────────┐
│ ContactMessage   │
├──────────────────┤
│ id (PK)          │
│ name             │
│ email            │
│ subject          │
│ message          │
│ read             │
│ created_at       │
└──────────────────┘
```

**Design Decisions:**

1. **Simple Structure:** Just stores messages
2. **Read Flag:** Track which messages have been reviewed
3. **No User FK:** Allow non-authenticated contact

### Indexing Strategy

```python
class Project(models.Model):
    slug = models.SlugField(unique=True)  # Automatic index
    status = models.CharField(...)         # Consider index
    
    class Meta:
        ordering = ['order', '-created_at']  # Index on these fields
```

**Indexes Created:**
- Primary keys (automatic)
- Unique fields (automatic)
- Foreign keys (automatic)
- Ordering fields (considered)

---

## Security Architecture

### 1. Authentication & Authorization

**Admin Only:**
```python
# All admin views require authentication
# Default Django admin login required
```

**Public Access:**
- Homepage
- Projects (published only)
- Blog (published only)
- Contact form

### 2. Input Validation

**Django Forms:**
```python
class ContactMessage(models.Model):
    email = models.EmailField()  # Validates email format
    # All fields have max_length constraints
```

**Markdown Sanitization:**
```python
def get_case_study_html(self):
    html = markdown.markdown(self.case_study_content)
    # Sanitize with bleach
    return bleach.clean(html, tags=ALLOWED_TAGS)
```

### 3. CSRF Protection

All forms include:
```html
<form method="post">
    {% csrf_token %}
    <!-- form fields -->
</form>
```

### 4. SQL Injection Prevention

Using Django ORM exclusively:
```python
# Safe - parameterized query
Project.objects.filter(slug=slug)

# Never raw SQL without parameters
```

### 5. XSS Prevention

**Template Auto-escaping:**
```html
{{ project.title }}  <!-- Auto-escaped -->
{{ project.get_case_study_html|safe }}  <!-- Sanitized before marked safe -->
```

### 6. Security Headers (Production)

```python
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    X_FRAME_OPTIONS = 'DENY'
```

### 7. Environment Variables

Sensitive data in environment:
```python
SECRET_KEY = config('SECRET_KEY')  # Never hardcoded
DATABASE_URL = config('DATABASE_URL')
```

---

## Performance Considerations

### 1. Database Query Optimization

**Select Related (1:1, FK):**
```python
Post.objects.select_related('author', 'category')
# Single query instead of N+1
```

**Prefetch Related (M2M):**
```python
Project.objects.prefetch_related('tech_stack', 'images')
# Two queries total instead of N+1
```

### 2. Static File Optimization

**Whitenoise:**
- Compresses static files
- Sets far-future cache headers
- Serves from CDN-like headers

**Configuration:**
```python
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### 3. Database Connection Pooling

```python
DATABASES = {
    'default': {
        'conn_max_age': 600,  # Persistent connections
        'conn_health_checks': True,  # Verify before use
    }
}
```

### 4. Template Fragment Caching (Future)

Can add:
```html
{% load cache %}
{% cache 500 sidebar %}
    <!-- expensive sidebar -->
{% endcache %}
```

### 5. Pagination

Automatic pagination:
```python
paginate_by = 10  # In list views
```

Prevents loading all records at once.

---

## Deployment Architecture

### Production Stack

```
┌─────────────────────────────────────┐
│         Internet Traffic            │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│      SSL/TLS Termination            │
│   (Render/Railway Managed)          │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│         Gunicorn Server             │
│    (WSGI Application Server)        │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│        Django Application           │
│                                     │
│  ┌──────────┐    ┌──────────┐     │
│  │  Views   │◄──►│  Models  │     │
│  └──────────┘    └─────┬────┘     │
│                         │          │
└─────────────────────────┼──────────┘
                          │
                          ▼
              ┌─────────────────────┐
              │    PostgreSQL DB    │
              └─────────────────────┘
                          
┌─────────────────────────────────────┐
│    Whitenoise (Static Files)        │
│         Serves CSS/JS/Images        │
└─────────────────────────────────────┘
```

### Scaling Strategy

**Vertical Scaling (Initial):**
- Upgrade database instance
- Increase web service resources

**Horizontal Scaling (Future):**
```
┌─────────────────┐
│  Load Balancer  │
└────────┬────────┘
         │
    ┌────┴─────┐
    │          │
    ▼          ▼
┌────────┐ ┌────────┐
│  Web   │ │  Web   │  (Multiple instances)
└───┬────┘ └───┬────┘
    │          │
    └────┬─────┘
         │
         ▼
   ┌──────────┐
   │ Database │
   └──────────┘
```

### Media Files Strategy

**Current:** Local filesystem (development)

**Production (Recommended):**
```python
# Use AWS S3 for media files
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

Benefits:
- CDN delivery
- Unlimited storage
- Backup/versioning

---

## Testing Strategy

### Unit Tests (Not Yet Implemented)

Recommended structure:
```python
# projects/tests.py
class ProjectModelTest(TestCase):
    def test_slug_generation(self):
        project = Project.objects.create(title="Test Project")
        self.assertEqual(project.slug, "test-project")
    
    def test_markdown_to_html(self):
        project = Project.objects.create(
            case_study_content="# Heading"
        )
        html = project.get_case_study_html()
        self.assertIn("<h1>", html)
```

### Integration Tests

Test view responses:
```python
class ProjectViewTest(TestCase):
    def test_project_list_view(self):
        response = self.client.get(reverse('projects:list'))
        self.assertEqual(response.status_code, 200)
```

---

## Future Enhancements

### 1. Search Functionality
- PostgreSQL full-text search
- Search projects by tech stack
- Search blog posts by content

### 2. API
- Django REST Framework
- Expose projects/blog as API
- Enable mobile app integration

### 3. Analytics
- Track project views
- Monitor contact form usage
- Popular blog posts

### 4. Internationalization
- Multi-language support
- Translation management
- Language detection

### 5. Comments
- Blog post comments
- Moderation queue
- Spam protection

---

## Maintenance & Monitoring

### Health Checks

Add endpoint:
```python
def health_check(request):
    return JsonResponse({'status': 'healthy'})
```

### Logging

```python
LOGGING = {
    'version': 1,
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    },
}
```

### Backup Strategy

1. **Database:** Daily automated backups
2. **Media Files:** Synced to S3
3. **Code:** Git repository (GitHub)
4. **Retention:** 30-day backup history

---

## Conclusion

This architecture provides:
- **Security:** Multiple layers of protection
- **Performance:** Optimized queries and caching
- **Scalability:** Ready for growth
- **Maintainability:** Clean, documented code
- **Reliability:** Production-tested patterns

The design follows Django best practices while remaining simple enough for a single developer to maintain.
