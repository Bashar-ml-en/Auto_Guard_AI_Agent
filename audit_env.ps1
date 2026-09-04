Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "       AI & ML DEVELOPER ENVIRONMENT AUDIT       " -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan

function Test-Executable ($title, $cmdStr) {
    try {
        $result = Invoke-Expression $cmdStr 2>$null
        if ($result) {
            Write-Host "[INSTALLED] $title : $result" -ForegroundColor Green
        } else {
            Write-Host "[MISSING]   $title" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "[MISSING]   $title" -ForegroundColor Yellow
    }
}

Write-Host "`n--- 1. Python & Package Managers ---" -ForegroundColor White
Test-Executable "python (Global)" "python --version"
Test-Executable "py (Windows Launcher)" "py --version"
Test-Executable "uv (Ultra-fast Manager)" "uv --version"
Test-Executable "pip" "pip --version"
Test-Executable "conda / mamba" "conda --version"
Test-Executable "poetry" "poetry --version"

Write-Host "`n--- 2. Python Binary Paths Found on System ---" -ForegroundColor White
$searchLocations = @(
    "$env:LOCALAPPDATA\Programs\Python",
    "$env:APPDATA\uv\python",
    "C:\Program Files\Python*",
    "C:\Google_Hackathon\.venv"
)
foreach ($loc in $searchLocations) {
    if (Test-Path $loc) {
        Get-ChildItem -Path $loc -Recurse -Depth 2 -Filter "python.exe" -ErrorAction SilentlyContinue | ForEach-Object {
            Write-Host "  -> $($_.FullName)" -ForegroundColor Cyan
        }
    }
}

Write-Host "`n--- 3. Version Control & Web/Cloud Tooling ---" -ForegroundColor White
Test-Executable "git" "git --version"
Test-Executable "gh (GitHub CLI)" "gh --version"
Test-Executable "node.js" "node --version"
Test-Executable "npm" "npm --version"
Test-Executable "vercel CLI" "vercel --version"
Test-Executable "docker" "docker --version"
Test-Executable "gcloud CLI" "gcloud --version"
Test-Executable "terraform" "terraform --version"

Write-Host "`n--- 4. GPU & ML Acceleration ---" -ForegroundColor White
try {
    $gpu = Get-WmiObject Win32_VideoController | Select-Object -ExpandProperty Name
    Write-Host "Graphics Card(s): $gpu" -ForegroundColor Cyan
} catch {}
Test-Executable "nvidia-smi (CUDA)" "nvidia-smi"

Write-Host "`n--- 5. Current PATH Check ---" -ForegroundColor White
$env:PATH -split ';' | Where-Object { $_ -match 'python|uv|node|git|cuda' } | ForEach-Object {
    Write-Host "  PATH: $_" -ForegroundColor DarkGray
}
