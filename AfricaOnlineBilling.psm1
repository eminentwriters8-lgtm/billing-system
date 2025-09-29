# Africa Online Networks Billing System
# ULTRA-SIMPLE WORKING VERSION

# Configuration
$Global:BillingConfig = @{
    SystemName = "Africa Online Networks Billing System"
    SupportNumber = "0706315742"
    Currency = "KES"
    DataPath = ".\BillingData"
    LogPath = ".\Logs"
}

# Initialize system
function Initialize-System {
    # Create directories
    $dirs = @($Global:BillingConfig.DataPath, $Global:BillingConfig.LogPath)
    foreach ($dir in $dirs) {
        if (!(Test-Path $dir)) { 
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
        }
    }
    
    # Initialize service plans if empty
    $plans = Get-ServicePlans
}

# Data functions
function Get-BillingData {
    param([string]$DataType)
    
    $filePath = "$($Global:BillingConfig.DataPath)\$DataType.json"
    if (Test-Path $filePath) {
        $content = Get-Content $filePath -Raw
        if ($content.Trim() -ne "" -and $content.Trim() -ne "[]") {
            try {
                $data = $content | ConvertFrom-Json
                if ($data -is [array]) {
                    return $data
                } else {
                    return @($data)
                }
            } catch {
                return @()
            }
        }
    }
    return @()
}

function Save-BillingData {
    param([string]$DataType, [object]$Data)
    
    $filePath = "$($Global:BillingConfig.DataPath)\$DataType.json"
    $Data | ConvertTo-Json -Depth 5 | Set-Content $filePath
}

# Logging
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
        Write-Host $logEntry -ForegroundColor Gray
    }
}

# Dashboard
function Show-BillingDashboard {
    Write-Host ""
    Write-Host "=== Africa Online Networks Billing System ===" -ForegroundColor Green
    Write-Host "Support: 0706315742" -ForegroundColor Cyan
    Write-Host "=============================================" -ForegroundColor DarkGray
    
    $clients = Get-Clients
    $invoices = Get-Invoices
    
    Write-Host "Quick Stats:" -ForegroundColor Yellow
    Write-Host "  Active Clients: $($clients.Count)" -ForegroundColor White
    Write-Host "  Total Invoices: $($invoices.Count)" -ForegroundColor White
    Write-Host "  Pending Invoices: $(($invoices | Where-Object Status -eq 'Pending').Count)" -ForegroundColor White
    
    Write-Host "`nSystem Status: OPERATIONAL" -ForegroundColor Green
}

# Client Management
function New-Client {
    param(
        [Parameter(Mandatory=$true)]
        [string]$ClientName,
        [string]$Email = "",
        [string]$Phone = "",
        [Parameter(Mandatory=$true)]
        [string]$ServicePlan,
        [decimal]$MonthlyRate = 0
    )
    
    $clients = Get-BillingData -DataType "Clients"
    
    $newClient = @{
        ClientID = "CLI" + (Get-Random -Minimum 1000 -Maximum 9999)
        ClientName = $ClientName
        Email = $Email
        Phone = $Phone
        ServicePlan = $ServicePlan
        MonthlyRate = $MonthlyRate
        Status = "Active"
        JoinDate = Get-Date -Format "yyyy-MM-dd"
    }
    
    # Convert to array and add new client
    $clientsArray = @($clients) + $newClient
    Save-BillingData -DataType "Clients" -Data $clientsArray
    
    Write-BillingLog "Created client: $ClientName ($($newClient.ClientID))"
    return $newClient
}

function Get-Clients {
    $clients = Get-BillingData -DataType "Clients"
    return $clients
}

# Invoice Management
function New-Invoice {
    param(
        [Parameter(Mandatory=$true)]
        [string]$ClientID
    )
    
    $clients = Get-BillingData -DataType "Clients"
    $client = $clients | Where-Object { $_.ClientID -eq $ClientID }
    
    if (-not $client) {
        Write-BillingLog "Client $ClientID not found" -Level "ERROR"
        return $null
    }
    
    $invoiceID = "INV" + (Get-Date -Format "yyyyMMddHHmmss")
    $amount = $client.MonthlyRate
    $tax = [math]::Round($amount * 0.16, 2)
    $total = $amount + $tax
    
    $invoice = @{
        InvoiceID = $invoiceID
        ClientID = $ClientID
        ClientName = $client.ClientName
        BillingDate = Get-Date -Format "yyyy-MM-dd"
        DueDate = (Get-Date).AddDays(30).ToString("yyyy-MM-dd")
        Amount = $amount
        Tax = $tax
        Total = $total
        Status = "Pending"
    }
    
    $invoices = Get-BillingData -DataType "Invoices"
    $invoicesArray = @($invoices) + $invoice
    Save-BillingData -DataType "Invoices" -Data $invoicesArray
    
    Write-BillingLog "Created invoice: $invoiceID for $($client.ClientName)"
    return $invoice
}

function Get-Invoices {
    $invoices = Get-BillingData -DataType "Invoices"
    return $invoices
}

# Service Plans
function Get-ServicePlans {
    $plans = Get-BillingData -DataType "ServicePlans"
    
    if ($plans.Count -eq 0) {
        # Create default plans
        $plans = @(
            @{PlanID="BASIC"; PlanName="Basic 5Mbps"; MonthlyRate=2499; Bandwidth="5Mbps"},
            @{PlanID="STANDARD"; PlanName="Standard 10Mbps"; MonthlyRate=3999; Bandwidth="10Mbps"},
            @{PlanID="PREMIUM"; PlanName="Premium 20Mbps"; MonthlyRate=6499; Bandwidth="20Mbps"}
        )
        Save-BillingData -DataType "ServicePlans" -Data $plans
        Write-BillingLog "Initialized default service plans"
    }
    
    return $plans
}

# Initialize on import
Initialize-System

# Export functions
Export-ModuleMember -Function Show-BillingDashboard
Export-ModuleMember -Function New-Client, Get-Clients
Export-ModuleMember -Function New-Invoice, Get-Invoices
Export-ModuleMember -Function Get-ServicePlans
Export-ModuleMember -Function Write-BillingLog