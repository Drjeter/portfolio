# Northflank Deployment Guide

This guide walks you through deploying your Django portfolio to Northflank securely.

## Prerequisites

- [x] GitHub account with repository access
- [x] Northflank account (free tier available)
- [x] Code pushed to GitHub

## Step 1: Generate Production SECRET_KEY

Before deploying, generate a secure SECRET_KEY:

```bash
python generate_secret_key.py
```

**IMPORTANT**: Copy the generated key - you'll need it for Northflank environment variables.

## Step 2: Create Northflank Project

1. Log in to [Northflank](https://northflank.com)
2. Click **"Create Project"**
3. Name your project (e.g., "Portfolio")
4. Click **"Create"**

## Step 3: Add PostgreSQL Database

1. In your project, click **"Add Addon"**
2. Select **"PostgreSQL"**
3. Choose a name (e.g., "portfolio-db")
4. Select the **Free tier** (or your preferred plan)
5. Click **"Create Addon"**
6. Wait for the database to be ready (status: Running)
7. **Copy the connection string** - you'll need this for environment variables

## Step 4: Create Service from GitHub

1. Click **"Add Service"** → **"Combined Service"**
2. Select **"GitHub"** as the source
3. Authorize Northflank to access your GitHub account
4. Select your **portfolio repository**
5. Select the **main** branch (or your default branch)
6. Configure the service:
   - **Name**: portfolio-web
   - **Build Type**: Buildpack
   - **Port**: 8080

## Step 5: Configure Environment Variables

In the service settings, go to **"Environment"** tab and add these variables:

### Required Variables

| Variable | Value | Notes |
|----------|-------|-------|
| `SECRET_KEY` | *[Generated key from Step 1]* | Never share this! |
| `DEBUG` | `False` | Always False in production |
| `ALLOWED_HOSTS` | `your-app.northflank.app` | Update with your actual domain |
| `DATABASE_URL` | *[From PostgreSQL addon]* | Click "Link" to auto-populate |

### Optional Email Variables (for contact form)

| Variable | Value |
|----------|-------|
| `EMAIL_BACKEND` | `django.core.mail.backends.smtp.EmailBackend` |
| `EMAIL_HOST` | `smtp.gmail.com` |
| `EMAIL_PORT` | `587` |
| `EMAIL_USE_TLS` | `True` |
| `EMAIL_HOST_USER` | `your-email@gmail.com` |
| `EMAIL_HOST_PASSWORD` | `your-app-password` |
| `CONTACT_EMAIL` | `your-email@example.com` |

> **Note**: For Gmail, you need to use an [App Password](https://support.google.com/accounts/answer/185833), not your regular password.

## Step 6: Configure Build & Deploy

1. Go to **"Build Settings"** tab
2. Verify **Build Command** (should auto-detect):
   ```
   pip install -r requirements.txt
   ```

3. Go to **"Deploy"** tab
4. Set **Run Command**:
   ```
   gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --log-file -
   ```

5. Add **Release Command** (runs before each deployment):
   ```
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```

## Step 7: Deploy

1. Click **"Deploy"** or **"Redeploy"**
2. Monitor the build logs for any errors
3. Wait for deployment to complete (status: Running)

## Step 8: Update ALLOWED_HOSTS

1. Once deployed, copy your Northflank URL (e.g., `portfolio-web-abc123.northflank.app`)
2. Update the `ALLOWED_HOSTS` environment variable with your actual domain
3. Redeploy the service

## Step 9: Create Django Superuser

To access the Django admin panel:

1. Go to your service in Northflank
2. Click **"Terminal"** tab
3. Click **"Connect"**
4. Run:
   ```bash
   python manage.py createsuperuser
   ```
5. Follow the prompts to create your admin account

## Step 10: Verify Deployment

Visit your site and verify:

- [ ] Homepage loads correctly
- [ ] Static files (CSS, JS, images) are working
- [ ] Projects page displays properly
- [ ] Blog page works
- [ ] Contact form functions (if configured)
- [ ] Admin panel accessible at `/admin`
- [ ] HTTPS is enabled (should be automatic)

## Custom Domain (Optional)

To use your own domain:

1. In Northflank, go to **"Networking"** tab
2. Click **"Add Domain"**
3. Enter your domain name
4. Add the provided DNS records to your domain registrar
5. Update `ALLOWED_HOSTS` environment variable to include your domain
6. Redeploy

## Troubleshooting

### Build Fails

- Check build logs for missing dependencies
- Verify `requirements.txt` is correct
- Ensure Python version is compatible (check `runtime.txt`)

### Database Connection Errors

- Verify `DATABASE_URL` is correctly set
- Check PostgreSQL addon is running
- Ensure database migrations ran successfully

### Static Files Not Loading

- Verify `collectstatic` ran in release command
- Check `STATIC_ROOT` and `STATIC_URL` in settings
- Confirm WhiteNoise is in `MIDDLEWARE`

### 500 Internal Server Error

- Check application logs in Northflank
- Verify all environment variables are set
- Ensure `DEBUG=False` and `ALLOWED_HOSTS` includes your domain

## Security Checklist

- [x] `DEBUG=False` in production
- [x] Strong `SECRET_KEY` generated and set
- [x] `ALLOWED_HOSTS` properly configured
- [x] Database credentials secured (not in code)
- [x] `.env` file not committed to Git
- [x] HTTPS enabled (automatic on Northflank)
- [x] Security middleware enabled in settings
- [ ] Regular dependency updates
- [ ] Database backups configured

## Monitoring & Maintenance

### View Logs

1. Go to your service in Northflank
2. Click **"Logs"** tab
3. Monitor for errors or issues

### Update Code

1. Push changes to GitHub
2. Northflank will auto-deploy (if enabled)
3. Or manually click **"Redeploy"**

### Database Backups

1. Go to PostgreSQL addon
2. Click **"Backups"** tab
3. Configure automatic backups (recommended)

## Cost Optimization

- **Free Tier**: Northflank offers free tier for small projects
- **Sleep Mode**: Enable sleep mode for development environments
- **Resource Limits**: Adjust CPU/memory based on actual usage

## Support Resources

- [Northflank Documentation](https://northflank.com/docs)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Northflank Community](https://community.northflank.com)

---

**Deployment Complete!** 🎉

Your portfolio is now live and accessible to the world. Remember to keep your dependencies updated and monitor your application logs regularly.
