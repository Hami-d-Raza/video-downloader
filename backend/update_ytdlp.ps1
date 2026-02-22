# Update yt-dlp to latest version
# This script updates yt-dlp to fix Instagram and other platform issues

Write-Host "Updating yt-dlp to latest version..." -ForegroundColor Green

# Update yt-dlp
pip install --upgrade yt-dlp

# Check version
Write-Host "`nInstalled yt-dlp version:" -ForegroundColor Cyan
python -c "import yt_dlp; print(yt_dlp.version.__version__)"

Write-Host "`nyt-dlp has been updated successfully!" -ForegroundColor Green
Write-Host "Instagram downloads should now work properly." -ForegroundColor Green
