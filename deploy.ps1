# Quick Deployment Script for Vercel
# Run this script from the project root directory

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "Django to Vercel Deployment Script" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Remove duplicate vercel.json
Write-Host "[1/6] Removing duplicate vercel.json..." -ForegroundColor Yellow
if (Test-Path "ai_trend_analyzer\vercel.json") {
    Remove-Item -Path "ai_trend_analyzer\vercel.json" -Force
    Write-Host "[OK] Removed duplicate vercel.json" -ForegroundColor Green
} else {
    Write-Host "[OK] No duplicate vercel.json found" -ForegroundColor Green
}
Write-Host ""

# Step 2: Check if Git is initialized
Write-Host "[2/6] Checking Git repository..." -ForegroundColor Yellow
if (-not (Test-Path ".git")) {
    Write-Host "Initializing Git repository..." -ForegroundColor Gray
    git init
    Write-Host "[OK] Git repository initialized" -ForegroundColor Green
} else {
    Write-Host "[OK] Git repository already exists" -ForegroundColor Green
}
Write-Host ""

# Step 3: Stage and commit changes
Write-Host "[3/6] Staging changes for Git..." -ForegroundColor Yellow
git add .
Write-Host "[OK] Files staged" -ForegroundColor Green
Write-Host ""

Write-Host "[4/6] Committing changes..." -ForegroundColor Yellow
git commit -m "Configure Django project for Vercel deployment" 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Changes committed" -ForegroundColor Green
} else {
    Write-Host "[INFO] No changes to commit (already committed)" -ForegroundColor Cyan
}
Write-Host ""

# Step 4: Check if Vercel CLI is installed
Write-Host "[5/6] Checking Vercel CLI..." -ForegroundColor Yellow
$vercelInstalled = Get-Command vercel -ErrorAction SilentlyContinue
if (-not $vercelInstalled) {
    Write-Host "[ERROR] Vercel CLI not found" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Vercel CLI first:" -ForegroundColor Yellow
    Write-Host "  npm install -g vercel" -ForegroundColor Cyan
    Write-Host ""
    exit 1
} else {
    Write-Host "[OK] Vercel CLI is installed" -ForegroundColor Green
}
Write-Host ""

# Step 5: Display deployment instructions
Write-Host "[6/6] Ready to deploy!" -ForegroundColor Yellow
Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Login to Vercel (if not already logged in):" -ForegroundColor White
Write-Host "   vercel login" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. Deploy to Vercel (development):" -ForegroundColor White
Write-Host "   vercel" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. Set environment variables in Vercel Dashboard:" -ForegroundColor White
Write-Host "   - SECRET_KEY" -ForegroundColor Gray
Write-Host "   - DEBUG=False" -ForegroundColor Gray
Write-Host "   - ALLOWED_HOSTS=.vercel.app" -ForegroundColor Gray
Write-Host "   - CSRF_TRUSTED_ORIGINS=https://*.vercel.app" -ForegroundColor Gray
Write-Host "   - YOUTUBE_API_KEY (if applicable)" -ForegroundColor Gray
Write-Host "   - GOOGLE_CLIENT_ID (if applicable)" -ForegroundColor Gray
Write-Host "   - GOOGLE_CLIENT_SECRET (if applicable)" -ForegroundColor Gray
Write-Host "   - DJANGO_SITE_ID=1" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Deploy to production:" -ForegroundColor White
Write-Host "   vercel --prod" -ForegroundColor Cyan
Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "Documentation" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "For detailed instructions, see:" -ForegroundColor White
Write-Host "  - VERCEL_DEPLOYMENT_GUIDE.md" -ForegroundColor Cyan
Write-Host "  - DEPLOYMENT_SUMMARY.md" -ForegroundColor Cyan
Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "Good luck with your deployment!" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Cyan
