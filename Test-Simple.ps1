# Simple test script for the billing system
Write-Host "Testing Africa Online Networks Billing System" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan

try {
    # Import the module
    Import-Module .\AfricaOnlineBilling.psm1 -Force
    Write-Host "Module imported successfully" -ForegroundColor Green
    
    # Test dashboard
    Write-Host "`nTesting Dashboard..." -ForegroundColor Yellow
    Show-BillingDashboard
    
    # Test client creation
    Write-Host "`nTesting Client Creation..." -ForegroundColor Yellow
    $testClient = New-Client -ClientName "John Doe" -ServicePlan "Basic 5Mbps" -MonthlyRate 2499
    Write-Host "Created client: $($testClient.ClientName) with ID: $($testClient.ClientID)" -ForegroundColor Green
    
    # Test getting clients
    Write-Host "`nTesting Client Retrieval..." -ForegroundColor Yellow
    $clients = Get-Clients
    Write-Host "Total clients: $($clients.Count)" -ForegroundColor Green
    
    # Test service plans
    Write-Host "`nTesting Service Plans..." -ForegroundColor Yellow
    $plans = Get-ServicePlans
    Write-Host "Available plans: $($plans.Count)" -ForegroundColor Green
    foreach ($plan in $plans) {
        Write-Host "  - $($plan.PlanName): KES $($plan.MonthlyRate)" -ForegroundColor White
    }
    
    Write-Host "`nALL TESTS PASSED SUCCESSFULLY!" -ForegroundColor Green
    
} catch {
    Write-Host "TEST FAILED: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Error details: $($_.ScriptStackTrace)" -ForegroundColor Red
}