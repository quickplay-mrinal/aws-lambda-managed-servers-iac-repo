# AWS Lambda Managed Instances - Deployment Script
# This script automates the deployment process

Write-Host "🚀 AWS Lambda Managed Instances Deployment" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
Write-Host "✓ Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "  Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Python not found. Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Check if Pulumi is installed
Write-Host "✓ Checking Pulumi installation..." -ForegroundColor Yellow
try {
    $pulumiVersion = pulumi version
    Write-Host "  Found: Pulumi $pulumiVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Pulumi not found. Please install Pulumi CLI" -ForegroundColor Red
    Write-Host "  Visit: https://www.pulumi.com/docs/install/" -ForegroundColor Yellow
    exit 1
}

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "✓ Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "  Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
}

# Activate virtual environment and install dependencies
Write-Host "✓ Installing dependencies..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"
pip install -r requirements.txt --quiet
Write-Host "  Dependencies installed" -ForegroundColor Green

# Check if Pulumi is logged in
Write-Host "✓ Checking Pulumi login status..." -ForegroundColor Yellow
try {
    pulumi whoami | Out-Null
    Write-Host "  Logged in to Pulumi" -ForegroundColor Green
} catch {
    Write-Host "  Not logged in. Running 'pulumi login'..." -ForegroundColor Yellow
    pulumi login
}

# Check if stack exists
Write-Host "✓ Checking Pulumi stack..." -ForegroundColor Yellow
$stackExists = pulumi stack ls 2>&1 | Select-String "dev"
if (-not $stackExists) {
    Write-Host "  Creating new stack 'dev'..." -ForegroundColor Yellow
    pulumi stack init dev
    pulumi config set aws:region us-east-1
    Write-Host "  Stack created and configured" -ForegroundColor Green
} else {
    Write-Host "  Stack 'dev' already exists" -ForegroundColor Green
}

# Preview deployment
Write-Host ""
Write-Host "📋 Previewing deployment..." -ForegroundColor Cyan
pulumi preview

# Ask for confirmation
Write-Host ""
$confirmation = Read-Host "Do you want to proceed with deployment? (yes/no)"
if ($confirmation -ne "yes") {
    Write-Host "Deployment cancelled" -ForegroundColor Yellow
    exit 0
}

# Deploy
Write-Host ""
Write-Host "🚀 Deploying infrastructure..." -ForegroundColor Cyan
pulumi up --yes

# Display outputs
Write-Host ""
Write-Host "✅ Deployment Complete!" -ForegroundColor Green
Write-Host "======================" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Outputs:" -ForegroundColor Cyan
pulumi stack output

Write-Host ""
Write-Host "🧪 Test Commands:" -ForegroundColor Cyan
Write-Host "  Data Processor (Small): curl `"$(pulumi stack output data_processor_url)?file_size=small`"" -ForegroundColor Yellow
Write-Host "  Data Processor (Large): curl `"$(pulumi stack output data_processor_url)?file_size=large`"" -ForegroundColor Yellow
Write-Host "  API Handler: curl $(pulumi stack output api_handler_url)" -ForegroundColor Yellow
Write-Host "  WebSocket Handler: curl $(pulumi stack output websocket_handler_url)" -ForegroundColor Yellow

Write-Host ""
Write-Host "📚 Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Test the endpoints using the commands above" -ForegroundColor White
Write-Host "  2. Check CloudWatch logs: aws logs tail /aws/lambda/data-processor --follow" -ForegroundColor White
Write-Host "  3. Review README.md for detailed documentation" -ForegroundColor White
Write-Host "  4. Post your experience on LinkedIn using LINKEDIN_POST.md" -ForegroundColor White

Write-Host ""
Write-Host "🎉 Happy coding!" -ForegroundColor Green
