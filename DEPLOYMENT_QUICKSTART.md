# 🚀 Northflank Deployment - Step by Step

Your code is on GitHub! Now let's deploy to Northflank.

## ✅ What's Already Done

- ✅ Code pushed to: https://github.com/Drjeter/portfolio.git
- ✅ `.env` excluded from Git (verified)
- ✅ All deployment files created
- ✅ SECRET_KEY generator ready

---

## 📋 Deployment Steps

### Step 1: Generate Your SECRET_KEY

Run this command **right now** and save the output:

```bash
python generate_secret_key.py
```

**Copy the generated key** - you'll paste it into Northflank in a moment.

---

### Step 2: Log into Northflank

1. Go to https://northflank.com
2. Log in to your account
3. Click **"Create Project"**
4. Name it: `Portfolio` (or your choice)
5. Click **"Create"**

---

### Step 3: Add PostgreSQL Database

1. In your project, click **"Add Addon"**
2. Select **"PostgreSQL"**
3. Name: `portfolio-db`
4. Plan: **Free tier** (or your choice)
5. Click **"Create Addon"**
6. ⏳ Wait for status: **Running** (takes ~1 minute)

---

### Step 4: Create Service from GitHub

1. Click **"Add Service"** → **"Combined Service"**
2. Source: **"GitHub"**
3. Authorize Northflank (if first time)
4. Repository: **`Drjeter/portfolio`**
5. Branch: **`main`**
6. Service name: `portfolio-web`
7. Build type: **Buildpack** (auto-detected)
8. Port: **8080**

---

### Step 5: Configure Environment Variables

Click **"Environment"** tab and add these:

#### Required Variables

| Variable | Value | Where to Get It |
|----------|-------|-----------------|
| `SECRET_KEY` | *[Your generated key]* | From Step 1 |
| `DEBUG` | `False` | Type exactly: False |
| `ALLOWED_HOSTS` | `.northflank.app` | Type exactly as shown |
| `DATABASE_URL` | *[Auto-filled]* | Click "Link" → Select `portfolio-db` |

**How to link DATABASE_URL:**
1. Click the **"Link"** button next to DATABASE_URL
2. Select your `portfolio-db` addon
3. It will auto-populate the connection string

---

### Step 6: Configure Build Commands

1. Go to **"Deploy"** tab
2. Set **Release Command** (runs before each deploy):
   ```bash
   python manage.py migrate && python manage.py collectstatic --noinput
   ```

3. Verify **Run Command** (should be auto-detected):
   ```bash
   gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --log-file -
   ```

---

### Step 7: Deploy! 🚀

1. Click **"Deploy"** button
2. Watch the build logs
3. ⏳ Wait for status: **Running** (takes 2-3 minutes)
4. Copy your app URL (e.g., `portfolio-web-abc123.northflank.app`)

---

### Step 8: Update ALLOWED_HOSTS

1. Copy your Northflank URL from Step 7
2. Go back to **"Environment"** tab
3. Update `ALLOWED_HOSTS` to your actual URL:
   ```
   portfolio-web-abc123.northflank.app
   ```
4. Click **"Redeploy"**

---

### Step 9: Create Django Superuser

1. Go to your service
2. Click **"Terminal"** tab
3. Click **"Connect"**
4. Run this command:
   ```bash
   python manage.py createsuperuser
   ```
5. Follow prompts to create your admin account

---

### Step 10: Verify Everything Works ✅

Visit your site and check:

- [ ] Homepage loads
- [ ] Static files work (CSS/images)
- [ ] Projects page displays
- [ ] Blog page works
- [ ] Admin panel: `https://your-url/admin`
- [ ] HTTPS is enabled (🔒 in browser)

---

## 🎉 You're Live!

Your portfolio is now deployed at: `https://your-northflank-url`

---

## 🔧 Optional: Email Configuration

To enable the contact form, add these environment variables:

```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
CONTACT_EMAIL=your-email@example.com
```

**For Gmail:** Use an [App Password](https://support.google.com/accounts/answer/185833), not your regular password.

---

## 🆘 Troubleshooting

### Build Fails
- Check build logs for errors
- Verify `requirements.txt` is correct
- Ensure Python version matches `runtime.txt`

### Database Connection Error
- Verify `DATABASE_URL` is linked to PostgreSQL addon
- Check addon status is "Running"
- Ensure migrations ran successfully

### Static Files Not Loading
- Verify `collectstatic` ran in release command
- Check `STATIC_ROOT` in settings.py
- Confirm WhiteNoise is in MIDDLEWARE

### 500 Error
- Check application logs in Northflank
- Verify all environment variables are set
- Ensure `ALLOWED_HOSTS` includes your domain

---

## 📚 Additional Resources

- **Full Guide**: See `NORTHFLANK_DEPLOYMENT.md` in your project
- **Northflank Docs**: https://northflank.com/docs
- **Django Deployment**: https://docs.djangoproject.com/en/stable/howto/deployment/

---

## 🔄 Updating Your Site

To deploy changes:

1. Make changes locally
2. Commit: `git commit -am "Your message"`
3. Push: `git push`
4. Northflank auto-deploys (if enabled) or click "Redeploy"

---

**Need help?** Check the troubleshooting section or the full deployment guide!
