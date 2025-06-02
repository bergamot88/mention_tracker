try {
    $pythonVersion = python --version
    Write-Host "Python has been found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Python was not found. Install Python and add it to the PATH." -ForegroundColor Red
    exit 1
}

if (-not (Test-Path "configs\requirements.txt")) {
    Write-Host "Error: File configs\requirements.txt not found in the current directory." -ForegroundColor Red
    exit 1
}

Write-Host "I'm creating a virtual environment..." -ForegroundColor Cyan
python -m venv venv

if (-not (Test-Path "venv")) {
    Write-Host "Error when creating a virtual environment." -ForegroundColor Red
    exit 1
}

Write-Host "Activating the virtual environment..." -ForegroundColor Cyan
$activateScript = Join-Path (Get-Location) "venv\Scripts\Activate.ps1"
if (Test-Path $activateScript) {
    . $activateScript
} else {
    Write-Host "Error: The activation script could not be found." -ForegroundColor Red
    exit 1
}

Write-Host "I install dependencies from configs\requirements.txt..." -ForegroundColor Cyan
pip install -r configs\requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error when installing dependencies." -ForegroundColor Red
    exit 1
}

Write-Host "The virtual environment has been successfully created and the dependencies are installed!" -ForegroundColor Green
Write-Host "To activate the environment in the future, do:" -ForegroundColor Yellow
Write-Host ".\venv\Scripts\Activate.ps1" -ForegroundColor White
