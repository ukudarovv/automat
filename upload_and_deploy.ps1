# PowerShell script to upload files and deploy to server
# Usage: .\upload_and_deploy.ps1

$serverIP = "194.110.54.230"
$serverUser = "ubuntu"
$serverPassword = "LPrMf+G+9F3JcwFxntRLIHE="
$localPath = "C:\Users\Umar\Desktop\avtomat"
$remotePath = "~/avtomat"

Write-Host "📤 Uploading files to server..." -ForegroundColor Cyan

# Install PSCP if not available (part of PuTTY)
# For now, we'll use SCP through OpenSSH if available

# Create deployment package
Write-Host "📦 Creating deployment package..." -ForegroundColor Yellow

# Note: This script requires SSH/SCP access
# Alternative: Use WinSCP or manual file transfer

Write-Host ""
Write-Host "To deploy manually:" -ForegroundColor Yellow
Write-Host "1. Use WinSCP or FileZilla to upload project folder to ~/avtomat" -ForegroundColor White
Write-Host "2. Or use: scp -r $localPath $serverUser@$serverIP`:~/avtomat" -ForegroundColor White
Write-Host "3. SSH to server: ssh $serverUser@$serverIP" -ForegroundColor White
Write-Host "4. Run: cd ~/avtomat && chmod +x setup_server.sh && ./setup_server.sh" -ForegroundColor White
Write-Host "5. Create .env.production file" -ForegroundColor White
Write-Host "6. Run: ./deploy.sh" -ForegroundColor White

