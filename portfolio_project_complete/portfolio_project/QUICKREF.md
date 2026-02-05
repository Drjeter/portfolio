# Quick Reference Guide

## Essential Commands

### Initial Setup
```bash
# Run the setup script
./setup.sh

# Or manually:
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your settings
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```

### Development Server
```bash
python manage.py runserver
# Visit http://localhost:8000
# Admin: http://localhost:8000/admin
```

### Database Operations
```bash
# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Reset database (CAUTION: Deletes all data)
python manage.py flush

# Create database backup
pg_dump portfolio_db > backup.sql

# Restore from backup
psql portfolio_db < backup.sql
```

### Admin User Management
```bash
# Create superuser
python manage.py createsuperuser

# Change password
python manage.py changepassword username
```

### Static Files
```bash
# Collect all static files
python manage.py collectstatic

# Clear and recollect
python manage.py collectstatic --clear --no-input
```

### Shell Access
```bash
# Django shell
python manage.py shell

# Database shell
python manage.py dbshell
```

### Testing
```bash
# Run all tests
python manage.py test

# Test specific app
python manage.py test projects

# Test with coverage
coverage run --source='.' manage.py test
coverage report
```

## Git Commands

```bash
# Initialize repository
git init
git add .
git commit -m "Initial commit"

# Connect to GitHub
git remote add origin https://github.com/username/portfolio.git
git push -u origin main

# Daily workflow
git add .
git commit -m "Description of changes"
git push
```

## Deployment Commands

### Render
```bash
# After pushing to GitHub, Render deploys automatically
# To create superuser on Render:
# Go to Shell in Render dashboard, then:
python manage.py createsuperuser
```

### Railway
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link project
railway link

# Run commands
railway run python manage.py migrate
railway run python manage.py createsuperuser
```

## Common Tasks

### Add a New Project
1. Login to admin: `/admin`
2. Go to "Tech stack" → Add technologies
3. Go to "Projects" → "Add project"
4. Fill in details
5. Upload screenshots
6. Write case study in Markdown
7. Save and view on site

### Write a Blog Post
1. Login to admin
2. Go to "Categories" → Create categories (if needed)
3. Go to "Posts" → "Add post"
4. Write content in Markdown
5. Set status to "Published"
6. Save and view

### Check Contact Messages
1. Login to admin
2. Go to "Contact messages"
3. View submissions
4. Mark as read

## Environment Variables

### Development (.env)
```env
SECRET_KEY=dev-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://user:pass@localhost:5432/portfolio_db
```

### Production (.env on hosting platform)
```env
SECRET_KEY=<long-random-string>
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DATABASE_URL=<provided-by-platform>
CONTACT_EMAIL=your@email.com
```

## Troubleshooting

### "No module named config"
```bash
# Make sure you're in the project directory
cd portfolio_project
# Ensure virtual environment is activated
source venv/bin/activate
```

### Static files not loading
```bash
python manage.py collectstatic --clear
# Restart server
```

### Database connection error
```bash
# Check PostgreSQL is running
sudo service postgresql status

# Verify DATABASE_URL in .env
# Ensure database exists
createdb portfolio_db
```

### Admin CSS not loading
```bash
python manage.py collectstatic --no-input
# Make sure STATIC_ROOT is set correctly
```

### Permission denied on scripts
```bash
chmod +x setup.sh build.sh
```

## Useful Django Admin URLs

- `/admin/` - Main admin interface
- `/admin/projects/project/` - Manage projects
- `/admin/blog/post/` - Manage blog posts
- `/admin/core/contactmessage/` - View contact messages
- `/admin/auth/user/` - Manage users

## Project URLs

- `/` - Homepage
- `/projects/` - Project list
- `/projects/<slug>/` - Project detail
- `/blog/` - Blog post list
- `/blog/category/<slug>/` - Posts by category
- `/blog/<slug>/` - Blog post detail
- `/contact/` - Contact form

## Performance Tips

1. Use `select_related()` for foreign keys
2. Use `prefetch_related()` for many-to-many
3. Add database indexes for frequently queried fields
4. Enable caching in production
5. Use CDN for static/media files
6. Compress images before upload

## Security Checklist

- [x] DEBUG=False in production
- [x] Strong SECRET_KEY
- [x] HTTPS enabled
- [x] ALLOWED_HOSTS configured
- [x] CSRF protection enabled
- [x] SQL injection prevented (ORM)
- [x] XSS protection (template escaping)
- [x] Security headers enabled
- [ ] Regular dependency updates
- [ ] Database backups scheduled

## Useful Resources

- Django Docs: https://docs.djangoproject.com/
- PostgreSQL Docs: https://www.postgresql.org/docs/
- Bootstrap Docs: https://getbootstrap.com/docs/
- Markdown Guide: https://www.markdownguide.org/
- Render Docs: https://render.com/docs
- Railway Docs: https://docs.railway.app/

## Getting Help

1. Check error messages in terminal
2. Review Django debug page (in development)
3. Check deployment logs (in production)
4. Search Django documentation
5. Search Stack Overflow
6. Review this project's documentation

## Maintenance Schedule

**Daily:**
- Monitor error logs
- Check contact messages

**Weekly:**
- Review security updates
- Test backup restoration
- Check site performance

**Monthly:**
- Update dependencies
- Review and rotate credentials
- Audit user access

---

Keep this file handy during development and deployment!
