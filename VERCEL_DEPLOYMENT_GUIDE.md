# 🚀 Vercel Deployment Guide for Django AI Trend Analyzer

This guide will help you deploy your Django application to Vercel successfully.

---

## 📋 Pre-Deployment Checklist

### 1. **Remove Duplicate vercel.json**
You have two `vercel.json` files. Keep only the one at the **root** level:
```powershell
Remove-Item -Path "ai_trend_analyzer\vercel.json" -Force
```

### 2. **Verify Project Structure**
Your project should look like this:
```
ai_trend_analyzer/               # Root directory
├── vercel.json                  # ✅ Main Vercel config (at root)
├── build_files.sh               # ✅ Build script
├── requirements.txt             # ✅ Python dependencies
├── .vercelignore                # ✅ Files to exclude from deployment
├── ai_trend_analyzer/           # Django project folder
│   ├── manage.py
│   ├── db.sqlite3               # (excluded via .vercelignore)
│   ├── viralbrain/
│   │   ├── settings.py          # ✅ Updated for Vercel
│   │   ├── wsgi.py              # ✅ Updated for Vercel
│   │   └── urls.py
│   └── trends/
│       ├── views.py
│       └── ...
```

---

## 🔧 Configuration Files Explained

### **1. vercel.json** (Root Level)
```json
{
  "version": 2,
  "builds": [
    {
      "src": "ai_trend_analyzer/viralbrain/wsgi.py",  // WSGI entry point
      "use": "@vercel/python",                         // Python runtime
      "config": {
        "maxLambdaSize": "15mb",                       // Lambda size limit
        "runtime": "python3.9"                         // Python version
      }
    },
    {
      "src": "build_files.sh",                         // Build script
      "use": "@vercel/static-build",                   // Run collectstatic
      "config": {
        "distDir": "ai_trend_analyzer/staticfiles"     // Static files output
      }
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",                           // Static files route
      "dest": "/static/$1"
    },
    {
      "src": "/(.*)",                                  // All other routes → WSGI
      "dest": "ai_trend_analyzer/viralbrain/wsgi.py"
    }
  ],
  "env": {
    // Environment variables (set these in Vercel dashboard)
    "SECRET_KEY": "",
    "DEBUG": "False",
    "ALLOWED_HOSTS": ".vercel.app,localhost,127.0.0.1",
    "CSRF_TRUSTED_ORIGINS": "https://*.vercel.app",
    "YOUTUBE_API_KEY": "",
    "GOOGLE_CLIENT_ID": "",
    "GOOGLE_CLIENT_SECRET": "",
    "DJANGO_SITE_ID": "1",
    "DJANGO_SETTINGS_MODULE": "viralbrain.settings",
    "PYTHONPATH": "/var/task/ai_trend_analyzer"
  }
}
```

### **2. build_files.sh**
This script runs during Vercel's build phase:
- Installs Python dependencies (`pip install -r requirements.txt`)
- Collects static files (`python manage.py collectstatic`)
- Runs database migrations (`python manage.py migrate`)

⚠️ **Important**: SQLite is not suitable for production on Vercel (serverless). Consider using PostgreSQL or another managed database.

### **3. settings.py Updates**
- **ALLOWED_HOSTS**: Now accepts `.vercel.app` subdomains
- **CSRF_TRUSTED_ORIGINS**: Allows HTTPS Vercel URLs
- **STATIC_ROOT**: Set to `staticfiles/` for collectstatic
- **STATICFILES_STORAGE**: Uses WhiteNoise for efficient static file serving

### **4. wsgi.py**
- Exposes the WSGI application as both `application` and `app`
- Vercel's serverless functions require the `app` variable

---

## 🌐 Deploy to Vercel

### **Step 1: Install Vercel CLI (if not already installed)**
```powershell
npm install -g vercel
```

### **Step 2: Login to Vercel**
```powershell
vercel login
```

### **Step 3: Remove Duplicate vercel.json**
```powershell
Remove-Item -Path "ai_trend_analyzer\vercel.json" -Force
```

### **Step 4: Initialize Git Repository (if not already done)**
```powershell
git init
git add .
git commit -m "Configure Django project for Vercel deployment"
```

### **Step 5: Deploy to Vercel**
Navigate to your project root and run:
```powershell
vercel
```

Follow the prompts:
- **Set up and deploy**: Yes
- **Which scope**: Select your account
- **Link to existing project**: No (first time) or Yes (redeployment)
- **Project name**: `ai-trend-analyzer` (or your preferred name)
- **Directory**: `.` (current directory)

### **Step 6: Set Environment Variables**
After deployment, go to the Vercel Dashboard:
1. Open your project
2. Navigate to **Settings** → **Environment Variables**
3. Add the following variables:

| Variable Name           | Example Value                          | Description                     |
|------------------------|----------------------------------------|---------------------------------|
| `SECRET_KEY`           | `your-django-secret-key-here`          | Django secret key               |
| `DEBUG`                | `False`                                | Disable debug mode              |
| `ALLOWED_HOSTS`        | `.vercel.app,yourdomain.com`           | Allowed hostnames               |
| `CSRF_TRUSTED_ORIGINS` | `https://*.vercel.app`                 | CSRF trusted origins            |
| `YOUTUBE_API_KEY`      | `your-youtube-api-key`                 | YouTube Data API key            |
| `GOOGLE_CLIENT_ID`     | `your-google-client-id`                | Google OAuth Client ID          |
| `GOOGLE_CLIENT_SECRET` | `your-google-client-secret`            | Google OAuth Client Secret      |
| `DJANGO_SITE_ID`       | `1`                                    | Django Site ID for allauth      |

### **Step 7: Redeploy After Setting Environment Variables**
```powershell
vercel --prod
```

---

## ✅ Verify Deployment

1. **Open Your Vercel URL** (e.g., `https://ai-trend-analyzer.vercel.app`)
2. **Check Homepage**: You should see your homepage without 404 errors
3. **Test Static Files**: CSS/JS should load correctly
4. **Test Routes**: Navigate to `/dashboard/`, `/login/`, etc.

---

## 🐛 Troubleshooting

### **Issue: 404 NOT_FOUND Error**
- **Cause**: Incorrect routing in `vercel.json` or WSGI not properly configured
- **Solution**: Ensure `vercel.json` routes point to `ai_trend_analyzer/viralbrain/wsgi.py`

### **Issue: Static Files Not Loading**
- **Cause**: `collectstatic` didn't run or WhiteNoise not configured
- **Solution**: 
  - Check `build_files.sh` runs successfully
  - Verify `STATIC_ROOT` in `settings.py`
  - Ensure WhiteNoise middleware is in `MIDDLEWARE`

### **Issue: DisallowedHost Error**
- **Cause**: Your Vercel URL is not in `ALLOWED_HOSTS`
- **Solution**: 
  - Add `.vercel.app` to `ALLOWED_HOSTS` in Vercel environment variables
  - Or update `settings.py` to include your custom domain

### **Issue: Database Not Persisting**
- **Cause**: SQLite doesn't work with serverless (Vercel)
- **Solution**: 
  - Use **PostgreSQL** (Vercel Postgres, Supabase, Railway)
  - Update `DATABASES` in `settings.py` to use external database
  - Install `psycopg2-binary` in `requirements.txt`

### **Issue: Build Failed**
- **Cause**: Dependency issues or Python version mismatch
- **Solution**: 
  - Check Vercel build logs
  - Ensure all dependencies are in `requirements.txt`
  - Verify Python version compatibility

---

## 📊 Post-Deployment Steps

### **1. Set Up Production Database**
SQLite is not suitable for production. Consider:
- **Vercel Postgres** (built-in, easy setup)
- **Supabase** (PostgreSQL, free tier)
- **Railway** (PostgreSQL, free tier)
- **AWS RDS** (managed PostgreSQL/MySQL)

Update `settings.py`:
```python
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600
    )
}
```

Add to `requirements.txt`:
```
psycopg2-binary==2.9.9
dj-database-url==2.1.0
```

### **2. Configure Custom Domain (Optional)**
1. Go to Vercel Dashboard → **Settings** → **Domains**
2. Add your custom domain
3. Update `ALLOWED_HOSTS` to include your domain

### **3. Set Up CI/CD (Optional)**
Connect your GitHub repository to Vercel for automatic deployments:
1. Push your code to GitHub
2. Import the repository in Vercel
3. Vercel will automatically deploy on every push

---

## 📝 Quick Commands Reference

```powershell
# Remove duplicate vercel.json
Remove-Item -Path "ai_trend_analyzer\vercel.json" -Force

# Deploy to Vercel (development)
vercel

# Deploy to Vercel (production)
vercel --prod

# View deployment logs
vercel logs

# Open Vercel dashboard
vercel open
```

---

## 🎉 Success!

Your Django application should now be live on Vercel! 

**Example URL**: `https://ai-trend-analyzer.vercel.app`

If you encounter any issues, check the Vercel deployment logs for detailed error messages.

---

## 📚 Additional Resources

- [Vercel Python Documentation](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [WhiteNoise Documentation](http://whitenoise.evans.io/)
- [Vercel Environment Variables](https://vercel.com/docs/projects/environment-variables)

---

**Need Help?** Check the Vercel logs or open an issue on GitHub.
