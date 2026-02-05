# Django Developer Portfolio

A production-ready Django 5 portfolio application for showcasing software engineering projects, writing technical blog posts, and managing professional contacts.

## Architecture Overview

### Technology Stack
- **Backend**: Django 5.0 with PostgreSQL database
- **Frontend**: Bootstrap 5 with minimal JavaScript
- **Deployment**: Gunicorn + Whitenoise for static files
- **Security**: Django security best practices enabled

### Design Decisions

#### 1. **Clean Architecture**
The project follows Django's recommended structure with clear separation of concerns:
- `config/` - Project configuration (settings, URLs, WSGI)
- `core/` - Core functionality (homepage, contact)
- `projects/` - Project portfolio management
- `blog/` - Writing and article management

Each app is self-contained with its own models, views, URLs, and templates.

#### 2. **Database Design**
- **Projects**: Supports multiple tech stacks, images, and markdown case studies
- **Blog**: Category-based organization with tags and markdown content
- **Contact**: Message storage with read/unread tracking

#### 3. **Security First**
- CSRF protection enabled
- SQL injection prevention via ORM
- XSS protection with HTML sanitization (bleach)
- Secure password hashing
- Production security headers (HSTS, X-Frame-Options, etc.)
- Environment-based configuration (python-decouple)

#### 4. **Markdown Support**
Both projects and blog posts use markdown for content, converted safely to HTML with:
- Code syntax highlighting support
- Tables, lists, and blockquotes
- HTML sanitization to prevent XSS

#### 5. **Static Files Strategy**
- Whitenoise for efficient static file serving
- Compressed manifest storage in production
- Separate static and media directories

## Project Structure

```
portfolio_project/
├── config/                 # Django project settings
│   ├── settings.py        # Main settings (security, database, apps)
│   ├── urls.py            # Root URL configuration
│   ├── wsgi.py            # WSGI entry point
│   └── asgi.py            # ASGI entry point
├── core/                   # Core app (home, contact)
│   ├── models.py          # ContactMessage model
│   ├── views.py           # Home and contact views
│   ├── urls.py            # Core URLs
│   └── admin.py           # Contact admin
├── projects/               # Projects app
│   ├── models.py          # Project, TechStack, ProjectImage
│   ├── views.py           # List and detail views
│   ├── urls.py            # Project URLs
│   └── admin.py           # Project admin with inline images
├── blog/                   # Blog app
│   ├── models.py          # Post, Category models
│   ├── views.py           # List, category, detail views
│   ├── urls.py            # Blog URLs
│   └── admin.py           # Blog admin
├── templates/              # Django templates
│   ├── base.html          # Base template with nav/footer
│   ├── core/              # Core templates
│   ├── projects/          # Project templates
│   └── blog/              # Blog templates
├── static/                 # Static files (CSS, JS, images)
│   └── css/
│       └── style.css      # Custom styles
├── media/                  # User-uploaded files
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── manage.py              # Django management script
├── build.sh               # Render build script
├── render.yaml            # Render configuration
├── railway.json           # Railway configuration
└── Procfile               # Heroku-style process file
```

## Setup Instructions

### 1. Local Development

```bash
# Clone the repository
git clone <your-repo-url>
cd portfolio_project

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your settings

# Setup database
createdb portfolio_db  # PostgreSQL
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run development server
python manage.py runserver
```

Visit `http://localhost:8000` for the site and `http://localhost:8000/admin` for the admin panel.

### 2. Database Configuration

**PostgreSQL** (recommended for production):
```bash
# Install PostgreSQL
# Create database
createdb portfolio_db

# Update .env
DATABASE_URL=postgresql://username:password@localhost:5432/portfolio_db
```

### 3. Environment Variables

Required variables in `.env`:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://user:pass@localhost:5432/portfolio_db
```

Generate a secure secret key:
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Deployment

### Option 1: Render

1. **Push code to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo>
git push -u origin main
```

2. **Deploy on Render**
   - Go to [render.com](https://render.com) and sign up
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml`
   - Set environment variables in Render dashboard:
     - `SECRET_KEY` (generate a new one)
     - `ALLOWED_HOSTS` (add your Render URL)
     - `CONTACT_EMAIL` (your email)
   - Deploy!

3. **Post-deployment**
```bash
# Create superuser (via Render shell)
python manage.py createsuperuser
```

### Option 2: Railway

1. **Push code to GitHub** (same as above)

2. **Deploy on Railway**
   - Go to [railway.app](https://railway.app) and sign up
   - Click "New Project" → "Deploy from GitHub"
   - Select your repository
   - Railway will detect `railway.json`
   - Add PostgreSQL plugin
   - Set environment variables:
     - `SECRET_KEY`
     - `ALLOWED_HOSTS`
     - `CONTACT_EMAIL`
     - `DATABASE_URL` (automatically set by Railway)

3. **Create superuser**
```bash
railway run python manage.py createsuperuser
```

### Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Generate new `SECRET_KEY`
- [ ] Setup PostgreSQL database
- [ ] Configure email settings (SMTP)
- [ ] Setup SSL/HTTPS
- [ ] Run migrations
- [ ] Collect static files
- [ ] Create superuser
- [ ] Test all functionality

## Usage Guide

### Adding Projects

1. Login to admin panel (`/admin`)
2. Go to "Projects" → "Add Project"
3. Fill in basic information:
   - Title, description
   - Tech stack (select multiple)
   - GitHub/Live URLs
4. Write case study in Markdown
5. Upload project screenshots
6. Set as featured (optional)
7. Publish

**Example Markdown for Case Study:**
```markdown
## Problem Statement
Describe the challenge...

## Solution
Explain your approach...

### Technical Implementation
- Used Django REST Framework
- Implemented caching with Redis
- Deployed on AWS

## Results
Quantify the impact...
```

### Writing Blog Posts

1. Login to admin panel
2. Go to "Blog" → "Posts" → "Add Post"
3. Write content in Markdown
4. Add categories and tags
5. Upload featured image
6. Set publication date
7. Publish

### Managing Contact Messages

1. Go to "Contact Messages" in admin
2. View all submissions
3. Mark as read/unread
4. Emails are sent automatically (if configured)

## Customization

### Branding
Edit `templates/base.html`:
- Change "Your Name" in navbar
- Update footer links
- Modify social media links

### Styling
Edit `static/css/style.css`:
- Customize colors (`:root` variables)
- Adjust typography
- Modify component styles

### Homepage Content
Edit `templates/core/home.html`:
- Update hero section text
- Modify featured sections

## Advanced Features

### Email Configuration

For production email (contact form notifications):

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
CONTACT_EMAIL=your-email@gmail.com
```

### Custom Domain

1. Add domain to `ALLOWED_HOSTS` in settings
2. Configure DNS settings with your provider
3. Enable SSL (automatic on Render/Railway)

## Performance Optimization

The application includes several performance optimizations:
- `select_related` and `prefetch_related` for database queries
- Database connection pooling
- Static file compression (Whitenoise)
- Image optimization recommended for uploads

## Security Features

- CSRF protection on all forms
- SQL injection prevention via Django ORM
- XSS protection with HTML sanitization
- Secure password storage (PBKDF2)
- Security headers in production
- Admin panel protection (login required)

## Maintenance

### Database Backups
```bash
# Backup
pg_dump portfolio_db > backup.sql

# Restore
psql portfolio_db < backup.sql
```

### Updating Dependencies
```bash
pip install --upgrade -r requirements.txt
python manage.py migrate
```

## Troubleshooting

**Static files not loading:**
```bash
python manage.py collectstatic --clear
```

**Database errors:**
```bash
python manage.py migrate --run-syncdb
```

**Permission issues:**
```bash
chmod +x build.sh
```

## Contributing

This is a personal portfolio template. Feel free to fork and customize for your own use.

## License

MIT License - Feel free to use this for your own portfolio.

---

Built with Django 5, PostgreSQL, and Bootstrap 5.
