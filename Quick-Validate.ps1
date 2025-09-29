# Quick Validation Script - Run this first!
Write-Host "Quick PowerShell Syntax Check" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# Test the corrected billing system files
$filesToCheck = @("AfricaOnlineBilling.psm1", "Deploy-BillingSystem.ps1")

foreach ($file in $filesToCheck) {
    if (Test-Path $file) {
        Write-Host "Found: $file" -ForegroundColor Green
        
        # Quick syntax test
        try {
            $content = Get-Content $file -Raw
            $scriptBlock = [scriptblock]::Create($content)
            Write-Host "   Syntax OK" -ForegroundColor Green
        } catch {
            Write-Host "   Syntax Error: $($_.Exception.Message)" -ForegroundColor Red
        }
    } else {
        Write-Host "Missing: $file" -ForegroundColor Yellow
    }
}

# Check for common issues
Write-Host "Checking for common issues..." -ForegroundColor Yellow

# Check switch statements in the main module
if (Test-Path "AfricaOnlineBilling.psm1") {
    $content = Get-Content "AfricaOnlineBilling.psm1" -Raw
    
    # Check for incorrect switch syntax
    if ($content -match 'switch.*{.*".*"=.*".*".*}') {
        Write-Host "Found incorrect switch statement syntax" -ForegroundColor Red
        Write-Host "   Fix: Use 'Value' { 'Code' } instead of 'Value' = 'Code'" -ForegroundColor Yellow
    } else {
        Write-Host "Switch statements look correct" -ForegroundColor Green
    }
    
    # Check for balanced braces
    $openBraces = ($content | Select-String -Pattern "{" -AllMatches).Matches.Count
    $closeBraces = ($content | Select-String -Pattern "}" -AllMatches).Matches.Count
    if ($openBraces -eq $closeBraces) {
        Write-Host "Braces are balanced" -ForegroundColor Green
    } else {
        Write-Host "Unbalanced braces: $openBraces { vs $closeBraces }" -ForegroundColor Red
    }
}

Write-Host "Quick validation complete!" -ForegroundColor Green