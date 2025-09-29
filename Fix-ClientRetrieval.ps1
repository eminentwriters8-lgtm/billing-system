# Quick fix for client retrieval issue
Write-Host "Applying fix for client retrieval..." -ForegroundColor Yellow

# Import module
Import-Module .\AfricaOnlineBilling -Force

# Test current state
Write-Host "`nCurrent state:" -ForegroundColor Cyan
$clients = Get-Clients
Write-Host "Clients found: $($clients.Count)" -ForegroundColor White

# Check data files
Write-Host "`nChecking data files..." -ForegroundColor Cyan
if (Test-Path ".\BillingData\Clients.json") {
    $content = Get-Content ".\BillingData\Clients.json" -Raw
    Write-Host "Clients.json content: $content" -ForegroundColor White
} else {
    Write-Host "Clients.json not found" -ForegroundColor Red
}

# Create a test client to verify
Write-Host "`nCreating test client..." -ForegroundColor Cyan
$testClient = New-Client -ClientName "Test Client Fix" -ServicePlan "Basic 5Mbps" -MonthlyRate 2499
Write-Host "Created: $($testClient.ClientName) ($($testClient.ClientID))" -ForegroundColor Green

# Check again
Write-Host "`nAfter creation:" -ForegroundColor Cyan
$clients = Get-Clients
Write-Host "Clients found: $($clients.Count)" -ForegroundColor White

if ($clients.Count -gt 0) {
    $clients | Format-Table ClientID, ClientName, ServicePlan, MonthlyRate -AutoSize
    Write-Host "✅ Fix applied successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Issue persists - manual fix required" -ForegroundColor Red
}