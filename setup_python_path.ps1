$pyDir = "C:\Users\User\AppData\Roaming\uv\python\cpython-3.11.16-windows-x86_64-none"
$pyScripts = "C:\Users\User\AppData\Roaming\uv\python\cpython-3.11.16-windows-x86_64-none\Scripts"

$userPath = [Environment]::GetEnvironmentVariable("PATH", "User")
if (-not $userPath) { $userPath = "" }

$newEntries = @()
if ($userPath -notlike "*$pyDir*") {
    $newEntries += $pyDir
}
if ($userPath -notlike "*$pyScripts*") {
    $newEntries += $pyScripts
}

if ($newEntries.Count -gt 0) {
    $finalPath = ($newEntries -join ";") + ";" + $userPath
    [Environment]::SetEnvironmentVariable("PATH", $finalPath, "User")
    Write-Host "SUCCESS: Added Python and Scripts to User PATH:" -ForegroundColor Green
    Write-Host "  -> $pyDir" -ForegroundColor Cyan
    Write-Host "  -> $pyScripts" -ForegroundColor Cyan
} else {
    Write-Host "Python paths already exist in User PATH." -ForegroundColor Green
}
