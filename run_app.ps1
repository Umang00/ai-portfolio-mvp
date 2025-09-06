# AI Portfolio Assistant Launcher
Write-Host "🚀 Starting AI Portfolio Assistant..." -ForegroundColor Green
Write-Host ""

# Kill any existing Python processes
Write-Host "🔄 Cleaning up existing processes..." -ForegroundColor Yellow
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

# Wait for ports to be released
Start-Sleep -Seconds 3

# Activate virtual environment and run app
Write-Host "📦 Activating virtual environment..." -ForegroundColor Blue
& ".\\.venv\\Scripts\\Activate.ps1"

Write-Host "🎯 Launching AI Portfolio Assistant..." -ForegroundColor Green
python app.py

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
