# PowerShell helper to create/activate a venv, install dependencies and run the FastAPI app
# Usage: from the repo root (or the backend folder) run: .\backend\run.ps1

param(
    [string]$mode = "setup"  # 'setup' (default) does full venv/create/install; 'start' just activates and runs
)

$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$venv = Join-Path $root '.venv'

Write-Host "Backend run helper starting in: $root (mode=$mode)"

function Activate-VenvAndRunUvicorn {
    param(
        [string]$uvicornArgs = "--reload --host 127.0.0.1 --port 8000"
    )

    # Allow activation script for this process
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force | Out-Null
    $activate = Join-Path $venv 'Scripts\Activate.ps1'
    if (-not (Test-Path $activate)) {
        return $false
    }

    Write-Host "Activating venv..."
    . $activate

    # Ensure PYTHONPATH so uvicorn can import the backend.app package when run from repo root
    $env:PYTHONPATH = $root

    # Warn if .env missing
    $envFile = Join-Path $root '.env'
    if (-not (Test-Path $envFile)) {
        Write-Warning "No .env file found in backend. The app may fail to find required secrets."
    }

    Write-Host "Starting uvicorn (app.main:app) on 127.0.0.1:8000..."
    python -m uvicorn app.main:app $uvicornArgs
    return $true
}

# If user asked for quick start, try to activate existing venv first; if not possible, fall back to setup
if ($mode -eq 'start') {
    $ok = Activate-VenvAndRunUvicorn
    if ($ok) { exit 0 }
    Write-Host "Venv activation failed or venv not present; falling back to full setup..."
}

# Ensure Python is available
try {
    python --version > $null
} catch {
    Write-Error "Python is not available on PATH. Please install Python 3.8+ and try again."
    exit 1
}

# Create venv if missing
if (-not (Test-Path $venv)) {
    Write-Host "Creating venv at $venv..."
    python -m venv $venv
}

# Allow activation script for this process
Write-Host "Setting execution policy for this process..."
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force

# Activate venv (should exist now)
$activate = Join-Path $venv 'Scripts\Activate.ps1'
if (-not (Test-Path $activate)) {
    Write-Error "Activation script not found at $activate"
    exit 1
}

Write-Host "Activating venv..."
. $activate

# Upgrade pip and install requirements
Write-Host "Upgrading pip and installing dependencies..."
python -m pip install --upgrade pip
if (Test-Path (Join-Path $root 'requirements.txt')) {
    pip install -r (Join-Path $root 'requirements.txt') python-dotenv
} else {
    Write-Host "No requirements.txt found; installing minimal deps..."
    pip install fastapi "uvicorn[standard]" requests python-dotenv
}

# Ensure .env exists
$envFile = Join-Path $root '.env'
if (-not (Test-Path $envFile)) {
    Write-Host "No .env file found in backend. Created .env with placeholders. Please add your NEWSAPI_KEY and restart the script."
    "# Local secrets for the backend. Do NOT commit this file to source control.`nNEWSAPI_KEY=`nDATABASE_URL=sqlite+aiosqlite:///./data/news.db`n" | Out-File -FilePath $envFile -Encoding utf8
    Write-Host "Created $envFile"
    Write-Host "Exiting so you can add your NEWSAPI_KEY to .env. Re-run the script after updating .env."
    exit 0
}

# Ensure PYTHONPATH so uvicorn can import the backend.app package when run from repo root
$env:PYTHONPATH = $root

# Start the FastAPI app
Write-Host "Starting uvicorn (app.main:app) on 127.0.0.1:8000..."
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
