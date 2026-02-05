# Django Portfolio - Complete File Structure

```
portfolio_project/
│
├── config/                          # Django project configuration
│   ├── __init__.py
│   ├── settings.py                  # Main settings file
│   ├── urls.py                      # Root URL configuration
│   ├── wsgi.py                      # WSGI application
│   └── asgi.py                      # ASGI application
│
├── core/                            # Core app (homepage, contact)
│   ├── __init__.py
│   ├── apps.py                      # App configuration
│   ├── models.py                    # ContactMessage model
│   ├── views.py                     # HomeView, ContactView
│   ├── urls.py                      # Core URL patterns
│   ├── admin.py                     # Contact admin
│   └── tests.py                     # Unit tests
│
├── projects/                        # Projects portfolio app
│   ├── __init__.py
│   ├── apps.py                      # App configuration
│   ├── models.py                    # Project, TechStack, ProjectImage
│   ├── views.py                     # List and detail views
│   ├── urls.py                      # Project URL patterns
│   ├── admin.py                     # Project admin with inlines
│   └── tests.py                     # Unit tests
│
├── blog/                            # Blog/writing app
│   ├── __init__.py
│   ├── apps.py                      # App configuration
│   ├── models.py                    # Post, Category models
│   ├── views.py                     # Blog views
│   ├── urls.py                      # Blog URL patterns
│   ├── admin.py                     # Blog admin
│   └── tests.py                     # Unit tests
│
├── templates/                       # Django templates
│   ├── base.html                    # Base template with nav/footer
│   ├── core/
│   │   ├── home.html               # Homepage
│   │   └── contact.html            # Contact form
│   ├── projects/
│   │   ├── project_list.html       # Project listing
│   │   └── project_detail.html     # Project case study
│   └── blog/
│       ├── post_list.html          # Blog post listing
│       └── post_detail.html        # Individual post
│
├── static/                          # Static files (CSS, JS)
│   ├── css/
│   │   └── style.css               # Custom styles
│   ├── js/
│   └── images/
│
├── media/                           # User-uploaded files (created at runtime)
│   ├── projects/
│   └── blog/
│
├── staticfiles/                     # Collected static files (created at runtime)
│
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment variables template
├── .gitignore                       # Git ignore rules
├── manage.py                        # Django management script
│
├── build.sh                         # Render build script
├── setup.sh                         # Local setup script
├── Procfile                         # Process file for deployments
├── runtime.txt                      # Python version specification
├── render.yaml                      # Render configuration
├── railway.json                     # Railway configuration
│
├── README.md                        # Main documentation
├── ARCHITECTURE.md                  # Architecture decisions
└── DEPLOYMENT.md                    # Deployment guide
```

## Key Files Explained

### Configuration Files

**config/settings.py**
- Database configuration
- Security settings
- Installed apps
- Middleware
- Static/media file settings
- Email configuration

**config/urls.py**
- Routes requests to appropriate apps
- Admin panel configuration

### Application Files

**models.py** (each app)
- Database schema definitions
- Business logic methods
- Meta options (ordering, indexes)

**views.py** (each app)
- Request handling
- Template rendering
- Form processing

**admin.py** (each app)
- Admin panel customization
- Inline models
- List display options

**urls.py** (each app)
- App-specific URL patterns
- Named URLs for reverse lookups

### Templates

**base.html**
- Site-wide navigation
- Footer
- Common HTML structure
- Bootstrap integration

**App Templates**
- Extend base.html
- App-specific content
- Forms and lists

### Static Files

**static/css/style.css**
- Custom styling
- Bootstrap overrides
- Responsive adjustments

### Deployment Files

**requirements.txt**
- All Python dependencies
- Pinned versions for reproducibility

**build.sh**
- Automated build script
- Runs migrations
- Collects static files

**render.yaml / railway.json**
- Platform-specific configuration
- Service definitions
- Environment variables

**.env.example**
- Template for environment variables
- Required settings documentation

## File Count Summary

- Python files: 24
- Templates: 7
- Configuration files: 8
- Documentation: 3
- Total: ~42 files

## Important Notes

1. **Never commit .env** - Contains sensitive data
2. **media/ is gitignored** - User uploads, not in version control
3. **staticfiles/ is gitignored** - Generated at deployment
4. **__pycache__/ is gitignored** - Python bytecode

## Database Files

Not in file structure (managed by PostgreSQL):
- User data
- Projects
- Blog posts
- Contact messages

## Generated Directories

These are created automatically:
```
media/
├── projects/
│   ├── 2024/
│   │   ├── 01/
│   │   └── 02/
└── blog/
    └── 2024/

staticfiles/
├── css/
├── js/
├── admin/
└── ...
```

## Development vs Production

**Development** (DEBUG=True):
- Uses Django development server
- Serves media files automatically
- Detailed error pages
- No security headers

**Production** (DEBUG=False):
- Uses Gunicorn
- Whitenoise serves static files
- Generic error pages
- Full security headers enabled

## Adding New Features

To add a new app:
```bash
python manage.py startapp app_name
```

Then update:
1. config/settings.py - Add to INSTALLED_APPS
2. config/urls.py - Include app URLs
3. Create models, views, templates
4. Run migrations
