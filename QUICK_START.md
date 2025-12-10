# AI Trend Analyzer - Quick Start Commands

## 🚀 Quick Deployment Commands

### 1. Remove Duplicate vercel.json (Important!)
```powershell
Remove-Item ai_trend_analyzer\vercel.json -Force
```

### 2. Generate Django SECRET_KEY
```powershell
cd ai_trend_analyzer
python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
cd ..
```

### 3. Test Locally (Optional)
```powershell
cd ai_trend_analyzer
python manage.py collectstatic --noinput
python manage.py runserver
# Visit: http://localhost:8000
cd ..
```

### 4. Commit and Push to GitHub
```powershell
git add .
git commit -m "Configure Django for Vercel serverless deployment"
git push origin main
```

### 5. Deploy on Vercel
```powershell
# Option A: Use Vercel CLI
npm install -g vercel
vercel --prod

# Option B: Deploy via Vercel Dashboard
# Go to vercel.com → Your Project → Deployments → Deploy
```

## 🔑 Required Environment Variables (Set in Vercel Dashboard)

Copy these to Vercel Project Settings → Environment Variables:

```
SECRET_KEY=<generate-using-command-above>
DEBUG=False
ALLOWED_HOSTS=.vercel.app
YOUTUBE_API_KEY=<your-youtube-api-key>
GOOGLE_CLIENT_ID=<your-google-oauth-client-id>
GOOGLE_CLIENT_SECRET=<your-google-oauth-secret>
DJANGO_SITE_ID=1
```

## ✅ Pre-Deployment Checklist

- [ ] Remove nested `ai_trend_analyzer/vercel.json`
- [ ] Generate and save SECRET_KEY securely
- [ ] Set all environment variables in Vercel dashboard
- [ ] Test `collectstatic` command locally
- [ ] Commit all changes to Git
- [ ] Push to GitHub main branch
- [ ] Deploy on Vercel
- [ ] Test homepage: `https://your-app.vercel.app/`
- [ ] Test admin: `https://your-app.vercel.app/admin/`

## 🐛 Quick Troubleshooting

### If you get 404 errors:
1. Check Vercel deployment logs
2. Verify `PYTHONPATH` in vercel.json
3. Ensure `wsgi.py` exports `app` variable

### If static files don't load:
1. Run `python manage.py collectstatic --noinput` locally
2. Check `STATIC_ROOT` path in settings.py
3. Verify WhiteNoise middleware is enabled

### If CSRF errors occur:
1. Add your domain to `CSRF_TRUSTED_ORIGINS`
2. Ensure `https://` prefix is included
3. Clear browser cookies and try again

## 📞 Need Help?

Check the full `DEPLOYMENT_GUIDE.md` for detailed explanations.
