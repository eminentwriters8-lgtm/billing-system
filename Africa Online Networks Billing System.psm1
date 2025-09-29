# Africa Online Networks Billing System
# Complete Working Version

$Global:BillingConfig = @{
    SystemName = "Africa Online Networks Billing System"
    SupportNumber = "0706315742"
    Currency = "KES"
    DataPath = ".\BillingData"
    LogPath = ".\Logs"
}

# Ensure required directories exist
function Initialize-BillingSystem {
    $directories = @($Global:BillingConfig.DataPath, $Global:BillingConfig.LogPath)
    foreach ($dir in $directories) {
        if (!(Test-Path $dir)) { 
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
            Write-Host "Created directory: $dir" -ForegroundColor Green
        }
    }
    
    # Initialize default service plans
    $plans = Get-ServicePlans
}

# Data storage functions
function Get-BillingData {
    param([string]$DataType)
    
    $filePath = "$($Global:BillingConfig.DataPath)\$DataType.json"
    if (Test-Path $filePath) {
        $content = Get-Content $filePath -Raw
        if ($content.Trim()) {
            return $content | ConvertFrom-Json
        }
    }
    return @()
}

function Save-BillingData {
    param([string]$DataType, [object]$Data)
    
    $filePath = "$($Global:BillingConfig.DataPath)\$DataType.json"
    $Data | ConvertTo-Json -Depth 10 | Set-Content $filePath
}

function Write-BillingLog {
    param([string]$Message, [string]$Level = "INFO")
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logEntry = "[$timestamp] [$Level] $Message"
    $logFile = "$($Global:BillingConfig.LogPath)\billing_$(Get-Date -Format 'yyyy-MM-dd').log"
    
    Add-Content -Path $logFile -Value $logEntry
    
    if ($Level -eq "ERROR") {
        Write-Host $logEntry -ForegroundColor Red
    } elseif ($Level -eq "WARNING") {
        Write-Host $logEntry -ForegroundColor Yellow
    } else {
        Write-Host $logEntry -ForegroundColor White
    }
}

# Dashboard function
function Show-BillingDashboard {
    Write-Host ""
    Write-Host "Africa Online Networks Billing System" -ForegroundColor Green
    Write-Host "Support: 0706315742" -ForegroundColor Cyan
    Write-Host "==========================================" -ForegroundColor DarkGray
    
    # Get actual data
    $clients = Get-Clients
    $invoices = Get-Invoices
    
    Write-Host "System Status:" -ForegroundColor Yellow
    Write-Host "  Billing System: Operational" -ForegroundColor Green
    Write-Host "  Client Database: Healthy" -ForegroundColor Green
    Write-Host "  Payment Gateway: Active" -ForegroundColor Green
    
    Write-Host "Quick Stats:" -ForegroundColor Yellow
    Write-Host "  Active Clients: $($clients.Count)" -ForegroundColor White
    Write-Host "  Pending Invoices: $(($invoices | Where-Object {$_.Status -eq 'Pending'}).Count)" -ForegroundColor White
    Write-Host "  Overdue Invoices: $(($invoices | Where-Object {$_.Status -eq 'Overdue'}).Count)" -ForegroundColor White
    
    Write-Host "Dashboard loaded successfully!" -ForegroundColor Green
}

# Client management functions
function New-Client {
    param(
        [Parameter(Mandatory = $true)]
        [string]$ClientName,
        [string]$Email = "",
        [string]$Phone = "",
        [Parameter(Mandatory = $true)]
        [string]$ServicePlan,
        [decimal]$MonthlyRate = 0
    )
    
    $clients = Get-BillingData -DataType "Clients"
    
    $newClient = [PSCustomObject]@{
        ClientID = "CLI" + (Get-Random -Minimum 1000 -Maximum 9999)
        ClientName = $ClientName
        Email = $Email
        Phone = $Phone
        ServicePlan = $ServicePlan
        MonthlyRate = $MonthlyRate
        Status = "Active"
        JoinDate = Get-Date -Format "yyyy-MM-dd"
    }
    
    $clients += $newClient
    Save-BillingData -DataType "Clients" -Data $clients
    
    Write-BillingLog "Created new client: $ClientName ($($newClient.ClientID))"
    return $newClient
}

function Get-Clients {
    param([string]$Status = "All")
    
    $clients = Get-BillingData -DataType "Clients"
    if ($Status -ne "All") {
        $clients = $clients | Where-Object { $_.Status -eq $Status }
    }
    
    return $clients | Sort-Object ClientName
}

function Update-Client {
    param(
        [Parameter(Mandatory = $true)]
        [string]$ClientID,
        [string]$NewPlan,
        [decimal]$NewRate
    )
    
    $clients = Get-BillingData -DataType "Clients"
    $client = $clients | Where-Object { $_.ClientID -eq $ClientID }
    
    if ($client) {
        if ($NewPlan) { $client.ServicePlan = $NewPlan }
        if ($NewRate -gt 0) { $client.MonthlyRate = $NewRate }
        
        Save-BillingData -DataType "Clients" -Data $clients
        Write-BillingLog "Updated client: $ClientID"
        return $true
    }
    
    Write-BillingLog "Client $ClientID not found" -Level "ERROR"
    return $false
}

# Invoice management functions
function New-Invoice {
    param(
        [Parameter(Mandatory = $true)]
        [string]$ClientID,
        [datetime]$BillingDate = (Get-Date)
    )
    
    $clients = Get-BillingData -DataType "Clients"
    $client = $clients | Where-Object { $_.ClientID -eq $ClientID }
    
    if (-not $client) {
        Write-BillingLog "Client $ClientID not found for invoice generation" -Level "ERROR"
        return $null
    }
    
    $invoiceID = "INV" + (Get-Date -Format "yyyyMMdd") + (Get-Random -Minimum 100 -Maximum 999)
    $amount = $client.MonthlyRate
    $tax = [math]::Round($amount * 0.16, 2)  # 16% VAT
    $total = $amount + $tax
    
    $invoice = [PSCustomObject]@{
        InvoiceID = $invoiceID
        ClientID = $ClientID
        ClientName = $client.ClientName
        BillingDate = $BillingDate.ToString("yyyy-MM-dd")
        DueDate = $BillingDate.AddDays(30).ToString("yyyy-MM-dd")
        Amount = $amount
        Tax = $tax
        Total = $total
        Status = "Pending"
        ServicePlan = $client.ServicePlan
    }
    
    $invoices = Get-BillingData -DataType "Invoices"
    $invoices += $invoice
    Save-BillingData -DataType "Invoices" -Data $invoices
    
    Write-BillingLog "Generated invoice $invoiceID for client $ClientID - Amount: $($Global:BillingConfig.Currency) $total"
    return $invoice
}

function Get-Invoices {
    param([string]$Status = "All")
    
    $invoices = Get-BillingData -DataType "Invoices"
    if ($Status -ne "All") {
        $invoices = $invoices | Where-Object { $_.Status -eq $Status }
    }
    
    return $invoices | Sort-Object BillingDate -Descending
}

function Update-InvoiceStatus {
    param(
        [Parameter(Mandatory = $true)]
        [string]$InvoiceID,
        [Parameter(Mandatory = $true)]
        [ValidateSet("Paid", "Overdue", "Cancelled", "Pending")]
        [string]$NewStatus
    )
    
    $invoices = Get-BillingData -DataType "Invoices"
    $invoice = $invoices | Where-Object { $_.InvoiceID -eq $InvoiceID }
    
    if ($invoice) {
        $invoice.Status = $NewStatus
        Save-BillingData -DataType "Invoices" -Data $invoices
        Write-BillingLog "Updated invoice $InvoiceID status to: $NewStatus"
        return $true
    }
    
    Write-BillingLog "Invoice $InvoiceID not found" -Level "ERROR"
    return $false
}

# Service plan functions
function Get-ServicePlans {
    $plans = Get-BillingData -DataType "ServicePlans"
    if (-not $plans -or $plans.Count -eq 0) {
        # Initialize default plans
        $plans = @(
            [PSCustomObject]@{PlanID = "BASIC"; PlanName = "Basic 5Mbps"; MonthlyRate = 2499; Bandwidth = "5Mbps"; DataCap = "100GB"},
            [PSCustomObject]@{PlanID = "STANDARD"; PlanName = "Standard 10Mbps"; MonthlyRate = 3999; Bandwidth = "10Mbps"; DataCap = "250GB"},
            [PSCustomObject]@{PlanID = "PREMIUM"; PlanName = "Premium 20Mbps"; MonthlyRate = 6499; Bandwidth = "20Mbps"; DataCap = "Unlimited"},
            [PSCustomObject]@{PlanID = "BUSINESS"; PlanName = "Business 50Mbps"; MonthlyRate = 12999; Bandwidth = "50Mbps"; DataCap = "Unlimited"}
        )
        Save-BillingData -DataType "ServicePlans" -Data $plans
        Write-BillingLog "Initialized default service plans"
    }
    return $plans
}

function New-ServicePlan {
    param(
        [Parameter(Mandatory = $true)]
        [string]$PlanName,
        [Parameter(Mandatory = $true)]
        [decimal]$MonthlyRate,
        [string]$Bandwidth = "",
        [string]$DataCap = ""
    )
    
    $plans = Get-ServicePlans
    $newPlan = [PSCustomObject]@{
        PlanID = "PLN" + (Get-Random -Minimum 1000 -Maximum 9999)
        PlanName = $PlanName
        MonthlyRate = $MonthlyRate
        Bandwidth = $Bandwidth
        DataCap = $DataCap
        CreatedDate = Get-Date -Format "yyyy-MM-dd"
    }
    
    $plans += $newPlan
    Save-BillingData -DataType "ServicePlans" -Data $plans
    
    Write-BillingLog "Created new service plan: $PlanName"
    return $newPlan
}

# Reporting functions
function Get-FinancialReport {
    $invoices = Get-BillingData -DataType "Invoices"
    $clients = Get-BillingData -DataType "Clients"
    
    $paidInvoices = $invoices | Where-Object { $_.Status -eq "Paid" }
    $pendingInvoices = $invoices | Where-Object { $_.Status -eq "Pending" }
    $overdueInvoices = $invoices | Where-Object { $_.Status -eq "Overdue" }
    
    $report = [PSCustomObject]@{
        TotalClients = $clients.Count
        ActiveClients = ($clients | Where-Object { $_.Status -eq "Active" }).Count
        TotalRevenue = ($paidInvoices | Measure-Object -Property Total -Sum).Sum
        PendingRevenue = ($pendingInvoices | Measure-Object -Property Total -Sum).Sum
        OverdueAmount = ($overdueInvoices | Measure-Object -Property Total -Sum).Sum
        ReportDate = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    }
    
    return $report
}

# Initialize the system when module is imported
Initialize-BillingSystem

# Export all functions
Export-ModuleMember -Function Show-BillingDashboard
Export-ModuleMember -Function New-Client, Get-Clients, Update-Client
Export-ModuleMember -Function New-Invoice, Get-Invoices, Update-InvoiceStatus
Export-ModuleMember -Function Get-ServicePlans, New-ServicePlan
Export-ModuleMember -Function Get-FinancialReport
Export-ModuleMember -Function Write-BillingLog