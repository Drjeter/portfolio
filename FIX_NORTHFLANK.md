# Fix Northflank Build - Quick Steps

## ✅ What's Fixed
- Pinned `psycopg2-binary==2.9.9`
- Pinned `Pillow==10.2.0`
- Code is on GitHub

## 🚀 Steps to Get It Working

### Step 1: Redeploy on Northflank

1. Go to your service in Northflank
2. Click **"Redeploy"** button (top right)
3. Watch the build logs

### Step 2: Check Build Logs

1. Go to **"Logs"** tab
2. Select **"Build logs"** (not runtime logs)
3. Watch for errors

### Step 3: Verify Environment Variables

Make sure these are set in **Environment** tab:

**Required:**
- `SECRET_KEY` - from your secret group or added manually
- `DATABASE_URL` - linked to PostgreSQL addon
- `DEBUG` - set to `False`
- `ALLOWED_HOSTS` - set to `.northflank.app`

### Step 4: Check Build Settings

In your service settings:

**Build:**
- Should auto-detect Python buildpack
- No custom build command needed

**Deploy:**
- **Run command**: `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --log-file -`
- **Release command** (optional): `python manage.py migrate && python manage.py collectstatic --noinput`

### Step 5: If Build Still Fails

**Common Issues:**

#### Issue 1: "No module named 'django'"
- Check that `requirements.txt` is in the root directory ✅
- Verify buildpack detected Python ✅

#### Issue 2: Database connection error during build
- This is OK! Database isn't needed during build
- Only needed at runtime

#### Issue 3: "Pillow requires..." or system dependencies
**Fix:** Add a `packages.txt` file (if needed):
```
libjpeg-dev
zlib1g-dev
```

#### Issue 4: Port binding error
- Make sure run command uses `$PORT` variable ✅
- Port should be 8080 in service settings

#### Issue 5: `DATABASE_URL` or `SECRET_KEY` not found during build
If your build fails with `decouple.UndefinedValueError: DATABASE_URL not found`, it means the secrets are not accessible during the **Build Phase**.

**How to fix on Northflank:**
1. Go to your **Secret Group** in Northflank.
2. In the **Linked Services** section, ensure your **Build Service** is selected (not just the deployment service).
3. If you haven't linked it yet:
   - Go to your Service -> **Environment** tab.
   - Click **"Link Secret Group"**.
   - Select your secret group and make sure to check the box for **"Link to Build"**.
4. Redeploy.

### Step 6: After Successful Build

1. Service should show **"Running"** status
2. Click on the service URL to view your site
3. If you get a Django error page, check:
   - `ALLOWED_HOSTS` includes your Northflank domain
   - Database migrations ran
   - Static files collected

### Step 7: Run Migrations

Once deployed, open the **Terminal** tab:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

## 🆘 Still Not Working?

**Share the exact error message from the build logs** and I'll help you fix it!

Look for lines that say:
- `ERROR:`
- `Failed to build`
- `Could not find...`
- `No module named...`

Copy the full error and we'll troubleshoot!
