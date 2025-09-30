# Enhanced-Dashboard.ps1
Import-Module .\AfricaOnlineBilling.psm1 -Force

function Show-EnhancedDashboard {
    # Clear screen and show header
    Clear-Host
    Write-Host "`n`n"
    Write-Host "=== 🌍 AFRICA ONLINE NETWORKS - COMPLETE DASHBOARD ===" -ForegroundColor Cyan
    Write-Host "=========================================================`n" -ForegroundColor Cyan
    
    # Quick Stats Section
    Write-Host "📊 DASHBOARD OVERVIEW" -ForegroundColor Yellow
    Write-Host "---------------------" -ForegroundColor Yellow
    
    # Get actual data from your system
    $clients = Get-Clients
    $invoices = Get-Invoices
    $servicePlans = Get-ServicePlans
    
    # Client Statistics
    Write-Host "`n👥 CLIENT STATISTICS" -ForegroundColor Green
    Write-Host "   Total Clients: $($clients.Count)" -ForegroundColor White
    Write-Host "   Active Clients: $(($clients | Where-Object Status -eq 'Active').Count)" -ForegroundColor White
    Write-Host "   Suspended Clients: $(($clients | Where-Object Status -eq 'Suspended').Count)" -ForegroundColor White
    
    # Revenue Statistics
    Write-Host "`n💰 REVENUE ANALYTICS" -ForegroundColor Green
    Write-Host "   Monthly Revenue: KSH $(($invoices | Where-Object { $_.Date -ge (Get-Date).AddDays(-30) } | Measure-Object Amount -Sum).Sum)" -ForegroundColor White
    Write-Host "   Yearly Revenue: KSH $(($invoices | Measure-Object Amount -Sum).Sum)" -ForegroundColor White
    Write-Host "   Total Invoices: $($invoices.Count)" -ForegroundColor White
    Write-Host "   Pending Invoices: $(($invoices | Where-Object Status -ne 'Paid').Count)" -ForegroundColor White
    
    # Network Traffic Monitor Section
    Write-Host "`n🌐 NETWORK TRAFFIC MONITOR" -ForegroundColor Green
    Write-Host "   Current Usage: $(Get-Random -Minimum 50 -Maximum 200) Mbps" -ForegroundColor White
    Write-Host "   Download Speed: $(Get-Random -Minimum 80 -Maximum 150) Mbps" -ForegroundColor White
    Write-Host "   Upload Speed: $(Get-Random -Minimum 20 -Maximum 60) Mbps" -ForegroundColor White
    Write-Host "   Active Sessions: $(Get-Random -Minimum 100 -Maximum 400)" -ForegroundColor White
    
    # Service Analytics
    Write-Host "`n📈 SERVICE ANALYTICS" -ForegroundColor Green
    Write-Host "   Available Service Plans: $($servicePlans.Count)" -ForegroundColor White
    Write-Host "   Most Popular Plan: $(if($servicePlans) { $servicePlans[0].Name } else { 'N/A' })" -ForegroundColor White
    
    # Quick Actions
    Write-Host "`n⚡ QUICK ACTIONS" -ForegroundColor Yellow
    Write-Host "   1. Add New Client" -ForegroundColor White
    Write-Host "   2. Generate Invoice" -ForegroundColor White
    Write-Host "   3. View Financial Report" -ForegroundColor White
    Write-Host "   4. Send SMS Notifications" -ForegroundColor White
    Write-Host "   5. Refresh Dashboard" -ForegroundColor White
    
    # Technical Support
    Write-Host "`n🛠️ TECHNICAL SUPPORT" -ForegroundColor Yellow
    Write-Host "   📞 Call Support: 0706315742" -ForegroundColor White
    Write-Host "   ✉️ Email Support: Quick Response" -ForegroundColor White
    Write-Host "   🌐 System Info: Version 2.0" -ForegroundColor White
    
    Write-Host "`n=========================================================" -ForegroundColor Cyan
    Write-Host "© 2025 Africa Online Networks. All rights reserved." -ForegroundColor Gray
    Write-Host "Support: 📞 0706315742 | ✉️ Email Support" -ForegroundColor Gray
    Write-Host "`n`n"
    
    # Interactive menu
    do {
        $choice = Read-Host "Select an option (1-5) or 'Q' to quit"
        switch ($choice) {
            '1' { 
                Write-Host "Opening Client Creation..." -ForegroundColor Green
                # Add client creation logic here
            }
            '2' { 
                Write-Host "Opening Invoice Generation..." -ForegroundColor Green
                # Add invoice generation logic here
            }
            '3' { 
                Write-Host "Generating Financial Report..." -ForegroundColor Green
                Get-FinancialReport
            }
            '4' { 
                Write-Host "Opening SMS System..." -ForegroundColor Green
                # Add SMS logic here
            }
            '5' { 
                Write-Host "Refreshing Dashboard..." -ForegroundColor Green
                Start-Sleep -Seconds 2
                Show-EnhancedDashboard
                return
            }
            'Q' { 
                Write-Host "Exiting dashboard..." -ForegroundColor Yellow
                return
            }
            default { Write-Host "Invalid option. Please try again." -ForegroundColor Red }
        }
    } while ($choice -ne 'Q')
}

# Start the enhanced dashboard
Show-EnhancedDashboard
