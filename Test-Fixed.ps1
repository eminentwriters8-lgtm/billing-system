# Simple Test Script for Africa Online Networks Billing System
Write-Host "TEST: Africa Online Networks Billing System" -ForegroundColor Magenta
Write-Host "============================================" -ForegroundColor Magenta

try {
    # Import module
    Write-Host "Importing module..." -ForegroundColor Yellow
    Import-Module .\AfricaOnlineBilling.psm1 -Force
    Write-Host "✅ Module imported" -ForegroundColor Green

    # Test 1: Dashboard
    Write-Host "`n1. Testing Dashboard..." -ForegroundColor Cyan
    Show-BillingDashboard

    # Test 2: Service Plans
    Write-Host "`n2. Testing Service Plans..." -ForegroundColor Cyan
    $plans = Get-ServicePlans
    Write-Host "✅ Service Plans: $($plans.Count)" -ForegroundColor Green
    $plans | Format-Table PlanName, MonthlyRate, Bandwidth -AutoSize

    # Test 3: Create Client
    Write-Host "`n3. Creating Client..." -ForegroundColor Cyan
    $client = New-Client -ClientName "John Doe" -ServicePlan "Basic 5Mbps" -MonthlyRate 2499
    Write-Host "✅ Client Created: $($client.ClientName)" -ForegroundColor Green
    Write-Host "   Client ID: $($client.ClientID)" -ForegroundColor White

    # Test 4: Get Clients
    Write-Host "`n4. Getting Clients..." -ForegroundColor Cyan
    $clients = Get-Clients
    Write-Host "✅ Total Clients: $($clients.Count)" -ForegroundColor Green

    # Test 5: Create Invoice
    Write-Host "`n5. Creating Invoice..." -ForegroundColor Cyan
    $invoice = New-Invoice -ClientID $client.ClientID
    Write-Host "✅ Invoice Created: $($invoice.InvoiceID)" -ForegroundColor Green
    Write-Host "   Amount: KES $($invoice.Total)" -ForegroundColor White

    # Test 6: Get Invoices
    Write-Host "`n6. Getting Invoices..." -ForegroundColor Cyan
    $invoices = Get-Invoices
    Write-Host "✅ Total Invoices: $($clients.Count)" -ForegroundColor Green

    Write-Host "`n" + "="*50 -ForegroundColor Green
    Write-Host "🎉 ALL TESTS PASSED!" -ForegroundColor Green
    Write-Host "="*50 -ForegroundColor Green

} catch {
    Write-Host "`n❌ TEST FAILED: $($_.Exception.Message)" -ForegroundColor Red
}