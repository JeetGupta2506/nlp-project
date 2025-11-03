# Deployment Preparation Script for Windows PowerShell

Write-Host "🚀 Social Media Rewriter - Deployment Preparation" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is initialized
if (Test-Path .git) {
    Write-Host "✅ Git repository found" -ForegroundColor Green
} else {
    Write-Host "⚠️  Git not initialized. Initializing..." -ForegroundColor Yellow
    git init
    Write-Host "✅ Git initialized" -ForegroundColor Green
}

Write-Host ""
Write-Host "📋 Checking required files..." -ForegroundColor Cyan

# Check for required files
$requiredFiles = @(
    "backend\requirements.txt",
    "backend\main.py",
    "backend\Procfile",
    "backend\render.yaml",
    "package.json",
    "vercel.json",
    ".gitignore"
)

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  ✅ $file" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $file missing!" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "🔐 Environment Variables Checklist:" -ForegroundColor Cyan
Write-Host "  Backend (Render):" -ForegroundColor Yellow
Write-Host "    • GEMINI_API_KEY"
Write-Host "    • REDDIT_CLIENT_ID"
Write-Host "    • REDDIT_CLIENT_SECRET"
Write-Host "    • REDDIT_USER_AGENT"
Write-Host "    • YOUTUBE_API_KEY"
Write-Host ""
Write-Host "  Frontend (Vercel):" -ForegroundColor Yellow
Write-Host "    • VITE_API_URL (add after backend deployment)"

Write-Host ""
Write-Host "📝 Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Commit your changes:"
Write-Host "     git add ."
Write-Host "     git commit -m `"Prepare for deployment`""
Write-Host ""
Write-Host "  2. Push to GitHub:"
Write-Host "     git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git"
Write-Host "     git branch -M main"
Write-Host "     git push -u origin main"
Write-Host ""
Write-Host "  3. Deploy Backend to Render:"
Write-Host "     https://dashboard.render.com"
Write-Host ""
Write-Host "  4. Deploy Frontend to Vercel:"
Write-Host "     https://vercel.com/new"
Write-Host ""
Write-Host "📖 Full guide: See DEPLOYMENT.md" -ForegroundColor Green
Write-Host ""
