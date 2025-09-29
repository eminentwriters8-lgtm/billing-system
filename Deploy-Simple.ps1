# Simple deployment script for Africa Online Networks Billing System
Write-Host "Deploying Africa Online Networks Billing System" -ForegroundColor Magenta
Write-Host "===============================================" -ForegroundColor Magenta

# Create module directory
$moduleDir = ".\AfricaOnlineBilling"
if (-not (Test-Path $moduleDir)) {
    New-Item -ItemType Directory -Path $moduleDir -Force
    Write-Host "Created module directory" -ForegroundColor Green
}

# Copy module file
if (Test-Path ".\AfricaOnlineBilling.psm1") {
    Copy-Item ".\AfricaOnlineBilling.psm1" -Destination $moduleDir -Force
    Write-Host "Copied module file" -ForegroundColor Green
} else {
    Write-Host "Module file not found. Please create AfricaOnlineBilling.psm1 first." -ForegroundColor Red
    exit 1
}

# Create module manifest
$manifestContent = @"
@{
    RootModule = 'AfricaOnlineBilling.psm1'
    ModuleVersion = '1.0.0'
    GUID = '$(New-Guid)'
    Author = 'Africa Online Networks'
    CompanyName = 'Africa Online Networks'
    Copyright = '(c) Africa Online Networks. All rights reserved.'
    Description = 'Billing system for Africa Online Networks'
    PowerShellVersion = '5.1'
    FunctionsToExport = @('Show-BillingDashboard', 'New-Client', 'Get-Clients', 'Get-ServicePlans')
    VariablesToExport = '*'
    AliasesToExport = @()
    PrivateData = @{
        PSData = @{
            Tags = @('Billing', 'AfricaOnline', 'Networks')
            ProjectUri = ''
            LicenseUri = ''
            ReleaseNotes = 'Initial release'
        }
    }
}
"@

$manifestContent | Out-File -FilePath "$moduleDir\AfricaOnlineBilling.psd1" -Encoding UTF8
Write-Host "Created module manifest" -ForegroundColor Green

# Initialize sample data
Write-Host "Initializing sample data..." -ForegroundColor Yellow

# Create data directory
$dataDir = ".\BillingData"
if (-not (Test-Path $dataDir)) {
    New-Item -ItemType Directory -Path $dataDir -Force
}

# Create empty data files
$dataFiles = @("Clients.json", "Invoices.json", "ServicePlans.json")
foreach ($file in $dataFiles) {
    $filePath = Join-Path $dataDir $file
    if (-not (Test-Path $filePath)) {
        "[]" | Out-File -FilePath $filePath -Encoding UTF8
    }
}

Write-Host "Sample data initialized" -ForegroundColor Green

Write-Host "`nDEPLOYMENT COMPLETED SUCCESSFULLY!" -ForegroundColor Green
Write-Host "You can now import the module using: Import-Module .\AfricaOnlineBilling" -ForegroundColor Cyan