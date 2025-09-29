# PowerShell Syntax Validator for Africa Online Networks Billing System
# Save this as Test-Syntax.ps1 and run it

param(
    [string]$ScriptPath = ".",
    [switch]$Detailed,
    [switch]$FixErrors
)

Write-Host "🔍 Starting PowerShell Syntax Validation..." -ForegroundColor Cyan
Write-Host "Scanning path: $ScriptPath" -ForegroundColor Gray

$ErrorFiles = @()
$WarningFiles = @()
$TotalErrors = 0
$TotalWarnings = 0

function Test-PowerShellSyntax {
    param([string]$FilePath)
    
    $errors = @()
    $warnings = @()
    
    if (-not (Test-Path $FilePath)) {
        return @{Errors = @("File not found: $FilePath"); Warnings = @()}
    }
    
    $content = Get-Content $FilePath -Raw
    
    # Common syntax patterns to check
    $commonIssues = @(
        @{Pattern = 'switch\s*\([^)]+\)\s*\{[^}]*"[\w\s]+"="[\w\s]+"[^}]*\}'; Description = "Incorrect switch statement syntax - use {Value { Code }} instead of {Value=Code}"}
        @{Pattern = 'if\s*\([^)]+\)\s*\{'; Description = "Missing closing brace in if statement"}
        @{Pattern = 'foreach\s*\([^)]+\)\s*\{'; Description = "Missing closing brace in foreach statement"}
        @{Pattern = 'function\s+\w+\s*\{'; Description = "Function missing proper parameter block"}
        @{Pattern = '\$[a-zA-Z_]\w*\s*='; Description = "Variable assignment issues"}
    )
    
    foreach ($issue in $commonIssues) {
        if ($content -match $issue.Pattern) {
            $warnings += "Potential issue: $($issue.Description)"
        }
    }
    
    # Test actual PowerShell parsing
    $tokens = @()
    $parseErrors = @()
    
    try {
        [System.Management.Automation.PSParser]::Tokenize($content, [ref]$tokens) | Out-Null
        
        # Check for unclosed blocks
        $braceCount = 0
        $parenCount = 0
        $bracketCount = 0
        
        foreach ($token in $tokens) {
            switch ($token.Type) {
                "GroupStart" { 
                    switch ($token.Content) {
                        "{" { $braceCount++ }
                        "(" { $parenCount++ }
                        "[" { $bracketCount++ }
                    }
                }
                "GroupEnd" { 
                    switch ($token.Content) {
                        "}" { $braceCount-- }
                        ")" { $parenCount-- }
                        "]" { $bracketCount-- }
                    }
                }
            }
        }
        
        if ($braceCount -ne 0) { $errors += "Unbalanced braces: $braceCount unmatched" }
        if ($parenCount -ne 0) { $errors += "Unbalanced parentheses: $parenCount unmatched" }
        if ($bracketCount -ne 0) { $errors += "Unbalanced brackets: $bracketCount unmatched" }
        
    } catch {
        $errors += "Tokenization failed: $($_.Exception.Message)"
    }
    
    # Try to parse as script block
    try {
        $scriptBlock = [scriptblock]::Create($content)
        $scriptBlock.CheckRestrictedLanguage($tokens, $null, $false)
    } catch {
        $errors += "Script parsing failed: $($_.Exception.Message)"
    }
    
    return @{Errors = $errors; Warnings = $warnings}
}

function Test-SwitchStatements {
    param([string]$FilePath, [string]$Content)
    
    $issues = @()
    
    # Find all switch statements
    $switchPattern = 'switch\s*\([^)]+\)\s*\{([^}]+)\}'
    $matches = [regex]::Matches($Content, $switchPattern, [System.Text.RegularExpressions.RegexOptions]::Singleline)
    
    foreach ($match in $matches) {
        $switchContent = $match.Groups[1].Value
        
        # Check for incorrect syntax: "Value"="Color"
        $incorrectSyntax = '"[^"]+"\s*=\s*"[^"]+"'
        if ($switchContent -match $incorrectSyntax) {
            $issues += "Incorrect switch syntax found: $($match.Value.Trim())"
        }
        
        # Check for missing braces
        $casePattern = '"[^"]+"\s*\{[^}]+\}'
        $caseMatches = [regex]::Matches($switchContent, $casePattern)
        if ($caseMatches.Count -eq 0 -and $switchContent.Trim() -ne "") {
            $issues += "Switch statement may have incorrect case syntax"
        }
    }
    
    return $issues
}

function Get-FileEncoding {
    param([string]$FilePath)
    
    $bytes = [System.IO.File]::ReadAllBytes($FilePath)
    if ($bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
        return "UTF-8 with BOM"
    } elseif ($bytes[0] -eq 0xFF -and $bytes[1] -eq 0xFE) {
        return "UTF-16 LE"
    } elseif ($bytes[0] -eq 0xFE -and $bytes[1] -eq 0xFF) {
        return "UTF-16 BE"
    } else {
        return "ANSI/UTF-8 without BOM"
    }
}

# Main validation logic
$files = Get-ChildItem -Path $ScriptPath -Include "*.ps1", "*.psm1", "*.psd1" -Recurse

foreach ($file in $files) {
    Write-Host "`n📄 Testing: $($file.Name)" -ForegroundColor White
    
    $result = Test-PowerShellSyntax -FilePath $file.FullName
    $switchIssues = Test-SwitchStatements -FilePath $file.FullName -Content (Get-Content $file.FullName -Raw)
    $encoding = Get-FileEncoding -FilePath $file.FullName
    
    $fileErrors = $result.Errors + $switchIssues
    $fileWarnings = $result.Warnings
    
    # Check encoding
    if ($encoding -ne "UTF-8 with BOM" -and $encoding -ne "ANSI/UTF-8 without BOM") {
        $fileWarnings += "Unusual file encoding: $encoding (recommended: UTF-8 with BOM)"
    }
    
    if ($fileErrors.Count -gt 0) {
        Write-Host "  ❌ ERRORS: $($fileErrors.Count)" -ForegroundColor Red
        $ErrorFiles += $file.Name
        $TotalErrors += $fileErrors.Count
        
        # FIXED: Use a different variable name instead of $error
        foreach ($err in $fileErrors) {
            Write-Host "    - $err" -ForegroundColor Red
        }
    } else {
        Write-Host "  ✅ No critical errors" -ForegroundColor Green
    }
    
    if ($fileWarnings.Count -gt 0) {
        Write-Host "  ⚠️  WARNINGS: $($fileWarnings.Count)" -ForegroundColor Yellow
        $WarningFiles += $file.Name
        $TotalWarnings += $fileWarnings.Count
        
        foreach ($warning in $fileWarnings) {
            Write-Host "    - $warning" -ForegroundColor Yellow
        }
    }
    
    if ($Detailed) {
        Write-Host "  📝 Encoding: $encoding" -ForegroundColor Gray
        Write-Host "  📊 Lines: $(($content -split "`r`n" | Measure-Object).Count)" -ForegroundColor Gray
    }
}

# Summary Report
Write-Host "`n" + "="*60 -ForegroundColor Cyan
Write-Host "📊 VALIDATION SUMMARY" -ForegroundColor Cyan
Write-Host "="*60 -ForegroundColor Cyan

Write-Host "Files scanned: $($files.Count)" -ForegroundColor White
Write-Host "Total errors: $TotalErrors" -ForegroundColor $(if ($TotalErrors -gt 0) { "Red" } else { "Green" })
Write-Host "Total warnings: $TotalWarnings" -ForegroundColor $(if ($TotalWarnings -gt 0) { "Yellow" } else { "Green" })

if ($ErrorFiles.Count -eq 0) {
    Write-Host "`n🎉 All files passed syntax validation!" -ForegroundColor Green
} else {
    Write-Host "`n❌ Files with errors:" -ForegroundColor Red
    $ErrorFiles | ForEach-Object { Write-Host "  - $_" -ForegroundColor Red }
}

if ($WarningFiles.Count -gt 0) {
    Write-Host "`n⚠️  Files with warnings:" -ForegroundColor Yellow
    $WarningFiles | ForEach-Object { Write-Host "  - $_" -ForegroundColor Yellow }
}

# Exit code for CI/CD
if ($TotalErrors -gt 0) {
    exit 1
} else {
    exit 0
}