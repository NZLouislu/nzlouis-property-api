# PowerShell alias for running pytest with correct Python version
function Run-Pytest {
    python -m pytest $args
}

Set-Alias -Name pyt -Value Run-Pytest

Write-Host "✅ PowerShell aliases loaded!" -ForegroundColor Green
Write-Host "Use 'pyt' to run pytest with correct Python version" -ForegroundColor Cyan
