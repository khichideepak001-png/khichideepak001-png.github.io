Write-Host "====================================="
Write-Host "ErgoElite Amazon Affiliate Bot System"
Write-Host "====================================="
Write-Host "Starting the autonomous background loop..."
Write-Host "Press Ctrl+C to stop the bot at any time."
Write-Host ""

while ($true) {
    $currentTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$currentTime] Triggering hourly sweep..."
    
    # Run the master python bot script
    python bot/bot_loop.py
    
    $nextRun = (Get-Date).AddHours(1).ToString("HH:mm:ss")
    Write-Host "`nSweep complete. Sleeping for 1 hour to avoid rate limits."
    Write-Host "Next run scheduled for: $nextRun`n"
    
    # Sleep for 1 hour (3600 seconds)
    Start-Sleep -Seconds 3600
}
