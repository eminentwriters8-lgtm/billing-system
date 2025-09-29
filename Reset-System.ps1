# Reset System - Clean start for testing
Write-Host "Resetting Africa Online Networks Billing System..." -ForegroundColor Yellow

# Remove module from memory
Remove-Module AfricaOnlineBilling -ErrorAction SilentlyContinue
Write-Host "✅ Module removed from memory" -ForegroundColor Green

# Remove data files
$dataDir = ".\BillingData"
if (Test-Path $dataDir) {
    $dataFiles = Get-ChildItem -Path $dataDir -Filter "*.json" -File
    foreach ($file in $dataFiles) {
        Remove-Item $file.FullName -Force
        Write-Host "✅ Removed: $($file.Name)" -ForegroundColor Green
    }
} else {
    New-Item -ItemType Directory -Path $dataDir -Force | Out-Null
    Write-Host "✅ Created data directory" -ForegroundColor Green
}

# Create empty data files
$emptyData = "[]"
$dataFiles = @("Clients.json", "Invoices.json", "ServicePlans.json")
foreach ($file in $dataFiles) {
    $filePath = Join-Path $dataDir $file
    $emptyData | Set-Content -Path $filePath -Encoding UTF8
    Write-Host "✅ Reset: $file" -ForegroundColor Green
}

Write-Host "`n🎉 System reset complete! Ready for fresh test." -ForegroundColor Cyan
Write-Host "Run: .\Test-Fixed.ps1 to test the system" -ForegroundColor White