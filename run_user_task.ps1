
$action = New-ScheduledTaskAction -Execute "C:\Program Files\Google\Chrome\Application\chrome.exe" -Argument "--new-window \"https://notebooklm.google.com/\""
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddSeconds(1)
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName "AntigravityUserTask" -Action $action -Trigger $trigger -Settings $settings -User "$env:USERNAME" -Force
Start-ScheduledTask -TaskName "AntigravityUserTask"
