# setup_env.ps1
$ErrorActionPreference = "Stop"
$pythonVersionRequired = "3.12.13"
$venvDir = ".venv"

Write-Host "🔍 Checking for Python $pythonVersionRequired..."

# Check if python is installed
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Error "❌ Python is not installed or not in PATH."
    exit 1
}

# Verify version
$versionOutput = & python --version
if ($versionOutput -notmatch $pythonVersionRequired) {
    Write-Error "❌ Python version $pythonVersionRequired not found. Found: $versionOutput"
    exit 1
}

Write-Host "✅ Found Python $versionOutput"

# Create virtual environment
Write-Host "📦 Creating virtual environment at $venvDir"
python -m venv $venvDir

# Activate virtual environment
if ($IsWindows) {
    $activateScript = ".\$venvDir\Scripts\Activate.ps1"
} else {
    $activateScript = ". $venvDir/bin/activate"
}

Write-Host "🚀 Activating virtual environment"
Invoke-Expression $activateScript

# Upgrade pip and install requirements
Write-Host "📥 Installing requirements from requirements.txt"
pip install --upgrade pip
pip install -r requirements.txt

Write-Host "✅ Environment setup complete!"
