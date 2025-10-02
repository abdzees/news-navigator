param(
    [string]$mode = "setup"  # 'setup' (default) does full venv/create/install; 'start' just activates and runs
)

$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$venv = Join-Path $root '.venv'

Write-Host "Frontend run helper starting in: $root (mode=$mode)"

function Activate-VenvAndRunStreamlit {
    param(
        [string]$streamlitArgs = "app.py"
    )

    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process -Force | Out-Null
    $activate = Join-Path $venv 'Scripts\Activate.ps1'
    if (-not (Test-Path $activate)) {
        return $false
    }

    Write-Host "Activating venv..."
    . $activate

    # Load .env if present (streamlit will pick up API_URL from environment if set)
    $envFile = Join-Path $root '.env'
    if (Test-Path $envFile) {
        Get-Content $envFile | ForEach-Object {
            if ($_ -and ($_ -notmatch "^\s*#")) {
                $parts = $_ -split "=", 2
                if ($parts.Length -eq 2) {
                    $name = $parts[0].Trim()
                    $value = $parts[1].Trim()
                    if ($name) {
                        # Use Set-Item for dynamic environment variable names
                        Set-Item -Path ("Env:" + $name) -Value $value -Force
                    }
                }
            }
        }
    } else {
        Write-Warning "No .env file found in frontend. The app may fail to find API_URL."
    }

    Write-Host "Starting Streamlit (app.py)..."
    streamlit run $streamlitArgs
    return $true
}

# Quick-start mode: try activate and run
if ($mode -eq 'start') {
    $ok = Activate-VenvAndRunStreamlit
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

# Activate venv
$activate = Join-Path $venv 'Scripts\Activate.ps1'
if (-not (Test-Path $activate)) {
    Write-Error "Activation script not found at $activate"
    exit 1
}

Write-Host "Activating venv..."
. $activate

# Upgrade pip and install frontend requirements
Write-Host "Upgrading pip and installing frontend dependencies..."
python -m pip install --upgrade pip
if (Test-Path (Join-Path $root 'requirements.txt')) {
    pip install -r (Join-Path $root 'requirements.txt') python-dotenv
} else {
    Write-Host "No requirements.txt found; installing minimal deps..."
    pip install streamlit requests pandas plotly python-dotenv
}

# Ensure .env exists
$envFile = Join-Path $root '.env'
if (-not (Test-Path $envFile)) {
    Write-Host "No .env file found in frontend. Created .env with placeholders. Please add your API_URL if different and restart the script."
    "# Local frontend config. Do NOT commit real secrets.`nAPI_URL=http://127.0.0.1:8000/api`n" | Out-File -FilePath $envFile -Encoding utf8
    Write-Host "Created $envFile"
    Write-Host "Exiting so you can edit .env. Re-run the script after updating .env."
    exit 0
}

# Load .env into environment for this process
Get-Content $envFile | ForEach-Object {
    if ($_ -and ($_ -notmatch "^\s*#")) {
        $parts = $_ -split "=", 2
        if ($parts.Length -eq 2) {
            $name = $parts[0].Trim()
            $value = $parts[1].Trim()
            if ($name) {
                Set-Item -Path ("Env:" + $name) -Value $value -Force
            }
        }
    }
}

# Start Streamlit
Write-Host "Starting Streamlit (app.py)..."
streamlit run app.py
