# Complete Test Script for Africa Online Networks Billing System
Write-Host "COMPLETE TEST: Africa Online Networks Billing System" -ForegroundColor Magenta
Write-Host "====================================================" -ForegroundColor Magenta

try {
    # Import the module
    Write-Host "Importing module..." -ForegroundColor Yellow
    Import-Module .\AfricaOnlineBilling.psm1 -Force
    Write-Host "Module imported successfully" -ForegroundColor Green
    
    # Test 1: Dashboard
    Write-Host "`n1. Testing Dashboard..." -ForegroundColor Cyan
    Show-BillingDashboard
    
    # Test 2: Service Plans
    Write-Host "`n2. Testing Service Plans..." -ForegroundColor Cyan
    $plans = Get-ServicePlans
    Write-Host "Available service plans:" -ForegroundColor Green
    $plans | Format-Table PlanName, MonthlyRate, Bandwidth -AutoSize
    
    # Test 3: Client Management
    Write-Host "`n3. Testing Client Management..." -ForegroundColor Cyan
    $testClient = New-Client -ClientName "John Doe" -Email "john@example.com" -Phone "0712345678" -ServicePlan "Basic 5Mbps" -MonthlyRate 2499
    Write-Host "Created client: $($testClient.ClientName) (ID: $($testClient.ClientID))" -ForegroundColor Green
    
    # Test 4: Invoice Generation
    Write-Host "`n4. Testing Invoice Generation..." -ForegroundColor Cyan
    $invoice = New-Invoice -ClientID $testClient.ClientID
    Write-Host "Generated invoice: $($invoice.InvoiceID) for KES $($invoice.Total)" -ForegroundColor Green
    
    # Test 5: Client Retrieval
    Write-Host "`n5. Testing Client Retrieval..." -ForegroundColor Cyan
    $clients = Get-Clients
    Write-Host "Total clients in system: $($clients.Count)" -ForegroundColor Green
    $clients | Format-Table ClientID, ClientName, ServicePlan, MonthlyRate -AutoSize
    
    # Test 6: Invoice Retrieval
    Write-Host "`n6. Testing Invoice Retrieval..." -ForegroundColor Cyan
    $invoices = Get-Invoices
    Write-Host "Total invoices in system: $($invoices.Count)" -ForegroundColor Green
    $invoices | Format-Table InvoiceID, ClientName, Total, DueDate, Status -AutoSize
    
    # Test 7: Financial Report
    Write-Host "`n7. Testing Financial Report..." -ForegroundColor Cyan
    $report = Get-FinancialReport
    Write-Host "Financial Summary:" -ForegroundColor Green
    $report | Format-List
    
    # Test 8: Update Invoice Status
    Write-Host "`n8. Testing Invoice Status Update..." -ForegroundColor Cyan
    $updateResult = Update-InvoiceStatus -InvoiceID $invoice.InvoiceID -NewStatus "Paid"
    if ($updateResult) {
        Write-Host "Invoice status updated to Paid" -ForegroundColor Green
    }
    
    Write-Host "`n" + "="*50 -ForegroundColor Green
    Write-Host "🎉 ALL TESTS COMPLETED SUCCESSFULLY!" -ForegroundColor Green
    Write-Host "="*50 -ForegroundColor Green
    
} catch {
    Write-Host "`n❌ TEST FAILED: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Error at: $($_.InvocationInfo.ScriptName):$($_.InvocationInfo.ScriptLineNumber)" -ForegroundColor Red
}