# PowerShell script to run tests with correct Python version
$python = "C:\Users\Administrator\.pyenv\pyenv-win\versions\3.11.7\python.exe"

Write-Host "🐍 Using Python 3.11.7" -ForegroundColor Green

& $python -m pytest $args
