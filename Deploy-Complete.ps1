# Complete Deployment Script for Africa Online Networks Billing System
Write-Host "DEPLOYING: Africa Online Networks Billing System" -ForegroundColor Magenta
Write-Host "=================================================" -ForegroundColor Magenta

# Step 1: Check if module file exists
if (-not (Test-Path ".\AfricaOnlineBilling.psm1")) {
    Write-Host "ERROR: AfricaOnlineBilling.psm1 not found!" -ForegroundColor Red
    Write-Host "Please create the module file first." -ForegroundColor Yellow
    exit 1
}

# Step 2: Create module directory
$moduleDir = ".\AfricaOnlineBilling"
if (-not (Test-Path $moduleDir)) {
    New-Item -ItemType Directory -Path $moduleDir -Force
    Write-Host "✅ Created module directory: $moduleDir" -ForegroundColor Green
}

# Step 3: Copy module file
Copy-Item ".\AfricaOnlineBilling.psm1" -Destination "$moduleDir\AfricaOnlineBilling.psm1" -Force
Write-Host "✅ Copied module file" -ForegroundColor Green

# Step 4: Create module manifest
$manifest = @{
    RootModule = 'AfricaOnlineBilling.psm1'
    ModuleVersion = '1.0.0'
    GUID = (New-Guid)
    Author = 'Africa Online Networks'
    CompanyName = 'Africa Online Networks'
    Copyright = '(c) Africa Online Networks. All rights reserved.'
    Description = 'Complete billing system for Africa Online Networks'
    PowerShellVersion = '5.1'
    FunctionsToExport = @(
        'Show-BillingDashboard',
        'New-Client', 'Get-Clients', 'Update-Client',
        'New-Invoice', 'Get-Invoices', 'Update-InvoiceStatus', 
        'Get-ServicePlans', 'New-ServicePlan',
        'Get-FinancialReport',
        'Write-BillingLog'
    )
    VariablesToExport = '*'
    AliasesToExport = @()
}

New-ModuleManifest -Path "$moduleDir\AfricaOnlineBilling.psd1" @manifest
Write-Host "✅ Created module manifest" -ForegroundColor Green

# Step 5: Initialize data directories
$dataDir = ".\BillingData"
$logDir = ".\Logs"

if (-not (Test-Path $dataDir)) {
    New-Item -ItemType Directory -Path $dataDir -Force
    Write-Host "✅ Created data directory: $dataDir" -ForegroundColor Green
}

if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force
    Write-Host "✅ Created log directory: $logDir" -ForegroundColor Green
}

# Step 6: Test the deployment
Write-Host "`nTesting deployment..." -ForegroundColor Yellow
try {
    Import-Module .\AfricaOnlineBilling -Force
    Write-Host "✅ Module imported successfully" -ForegroundColor Green
    
    # Test basic functions
    Show-BillingDashboard
    $plans = Get-ServicePlans
    Write-Host "✅ Service plans loaded: $($plans.Count)" -ForegroundColor Green
    
    Write-Host "`n" + "="*50 -ForegroundColor Green
    Write-Host "🎉 DEPLOYMENT COMPLETED SUCCESSFULLY!" -ForegroundColor Green
    Write-Host "="*50 -ForegroundColor Green
    Write-Host "`nUsage examples:" -ForegroundColor Cyan
    Write-Host "  Import-Module .\AfricaOnlineBilling" -ForegroundColor White
    Write-Host "  Show-BillingDashboard" -ForegroundColor White
    Write-Host "  New-Client -ClientName 'Test Client' -ServicePlan 'Basic 5Mbps' -MonthlyRate 2499" -ForegroundColor White
    Write-Host "  Get-Clients" -ForegroundColor White
    
} catch {
    Write-Host "❌ Deployment test failed: $($_.Exception.Message)" -ForegroundColor Red
}