# Deployment Guide

This guide covers deploying your Django portfolio to production on Render or Railway.

## Pre-Deployment Checklist

- [ ] All code committed to Git
- [ ] `.env` file NOT committed (in `.gitignore`)
- [ ] `requirements.txt` is up to date
- [ ] Database migrations created and tested
- [ ] Static files collected locally
- [ ] Admin account created and tested

## Render Deployment (Recommended)

### Step 1: Prepare Your Repository

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/portfolio.git
git push -u origin main
```

### Step 2: Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Authorize Render to access your repositories

### Step 3: Deploy via Blueprint

1. Click **"New +"** → **"Blueprint"**
2. Connect your repository
3. Render detects `render.yaml` automatically
4. Review the configuration:
   - Web service named "portfolio"
   - PostgreSQL database named "portfolio_db"
5. Click **"Apply"**

### Step 4: Configure Environment Variables

Render automatically creates some variables. Add these manually:

1. Go to your web service dashboard
2. Click **"Environment"**
3. Add these variables:
   ```
   SECRET_KEY = <generate-new-secret-key>
   ALLOWED_HOSTS = your-app-name.onrender.com
   DEBUG = False
   CONTACT_EMAIL = your-email@example.com
   ```

To generate `SECRET_KEY`:
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 5: Deploy

1. Render automatically builds and deploys
2. Monitor the build logs
3. Wait for "Live" status (5-10 minutes first time)

### Step 6: Create Superuser

1. Go to your service dashboard
2. Click **"Shell"**
3. Run:
   ```bash
   python manage.py createsuperuser
   ```
4. Follow prompts to create admin account

### Step 7: Verify Deployment

1. Visit `https://your-app-name.onrender.com`
2. Check all pages load correctly
3. Login to admin at `/admin`
4. Test creating a project and blog post

### Step 8: Custom Domain (Optional)

1. Go to service **"Settings"**
2. Click **"Custom Domain"**
3. Add your domain
4. Update DNS records as instructed
5. Update `ALLOWED_HOSTS` environment variable

---

## Railway Deployment

### Step 1: Prepare Repository

Same as Render (see above).

### Step 2: Create Railway Account

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub

### Step 3: Create New Project

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your repository
4. Railway detects `railway.json`

### Step 4: Add Database

1. Click **"+ New"** in your project
2. Select **"Database"** → **"Add PostgreSQL"**
3. Railway automatically sets `DATABASE_URL`

### Step 5: Configure Environment Variables

1. Click on your web service
2. Go to **"Variables"** tab
3. Add:
   ```
   SECRET_KEY = <generate-new-key>
   ALLOWED_HOSTS = your-app.up.railway.app
   DEBUG = False
   CONTACT_EMAIL = your-email@example.com
   ```

### Step 6: Deploy

1. Railway automatically deploys on push
2. Click **"Deploy"** if needed
3. Monitor deployment logs

### Step 7: Create Superuser

1. Click **"..."** → **"Run a command"**
2. Enter:
   ```bash
   python manage.py createsuperuser
   ```

### Step 8: Custom Domain (Optional)

1. Go to **"Settings"** → **"Domains"**
2. Add custom domain
3. Update DNS records
4. Update `ALLOWED_HOSTS`

---

## Post-Deployment Tasks

### 1. Setup Email

Configure SMTP for contact form:

**Gmail:**
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

**SendGrid:**
```env
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
```

### 2. Add Content

1. Login to admin panel
2. Create tech stack items
3. Add 2-3 projects
4. Write 1-2 blog posts
5. Test contact form

### 3. Setup Monitoring

**Render:**
- Automatically includes basic monitoring
- Check dashboard for uptime and logs

**Railway:**
- Includes deployment history
- Monitor resource usage in dashboard

### 4. Backup Strategy

**Database Backups:**

Render:
```bash
# Download backup from Render dashboard
# Database → Backups → Download
```

Railway:
```bash
# Use Railway CLI
railway connect postgres
pg_dump > backup.sql
```

### 5. SSL/HTTPS

Both Render and Railway provide automatic SSL certificates. Verify:
- Site loads with `https://`
- No mixed content warnings
- Security headers active

---

## Troubleshooting

### Build Fails

**Issue:** Build script fails
```
Error: No such file or directory: build.sh
```

**Solution:**
```bash
chmod +x build.sh
git add build.sh
git commit -m "Make build script executable"
git push
```

### Static Files Not Loading

**Issue:** CSS/images not displaying

**Solution:**
1. Check `STATIC_ROOT` in settings
2. Run locally: `python manage.py collectstatic`
3. Verify `whitenoise` in `INSTALLED_APPS`
4. Check build logs for errors

### Database Connection Errors

**Issue:** Database not connecting

**Solution:**
1. Verify `DATABASE_URL` environment variable
2. Check database is running (Render/Railway dashboard)
3. Ensure `psycopg2-binary` in requirements.txt
4. Check database credentials

### 500 Internal Server Error

**Issue:** Site returns 500 errors

**Solution:**
1. Check deployment logs
2. Verify all environment variables set
3. Run migrations: `python manage.py migrate`
4. Check `ALLOWED_HOSTS` includes your domain

### Admin Media Files Not Displaying

**Issue:** Uploaded images don't show

**Solution:**
1. Configure media file storage (use AWS S3 for production)
2. Install `django-storages` and `boto3`
3. Update settings for S3 backend

---

## Production Optimization

### 1. Enable Caching

Add Redis for caching (optional):

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': config('REDIS_URL'),
    }
}
```

### 2. Optimize Database Queries

Already implemented:
- `select_related()` for foreign keys
- `prefetch_related()` for many-to-many
- Database indexes on frequently queried fields

### 3. Image Optimization

Recommended: Use a CDN for images
- Cloudinary
- AWS S3 + CloudFront
- ImageKit

### 4. Monitoring

Setup error tracking:
- Sentry (recommended)
- Rollbar
- Bugsnag

Add to `requirements.txt`:
```
sentry-sdk==1.40.0
```

Configure in `settings.py`:
```python
import sentry_sdk

sentry_sdk.init(
    dsn=config('SENTRY_DSN'),
    traces_sample_rate=1.0,
)
```

---

## Maintenance

### Regular Updates

```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Create and run migrations
python manage.py makemigrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input

# Commit and push
git add .
git commit -m "Update dependencies"
git push
```

### Database Backups

Schedule regular backups:
- Weekly full backups
- Daily incremental backups
- Store offsite (S3, Google Cloud Storage)

### Security Updates

- Monitor Django security announcements
- Update Django when patches released
- Review and rotate `SECRET_KEY` annually
- Audit admin user accounts quarterly

---

## Scaling Considerations

When your portfolio grows:

1. **Database:** Upgrade to larger instance
2. **Web Service:** Scale to multiple instances
3. **CDN:** Use for static/media files
4. **Caching:** Add Redis for database query caching
5. **Monitoring:** Implement comprehensive monitoring

---

## Support Resources

- **Django Documentation:** https://docs.djangoproject.com/
- **Render Documentation:** https://render.com/docs
- **Railway Documentation:** https://docs.railway.app/
- **PostgreSQL Documentation:** https://www.postgresql.org/docs/

---

**Deployment Complete!** 🎉

Your portfolio is now live and ready to showcase your work.
