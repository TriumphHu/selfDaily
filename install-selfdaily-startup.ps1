$ErrorActionPreference = "Stop"

$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$StartupDir = [Environment]::GetFolderPath("Startup")
$ShortcutPath = Join-Path $StartupDir "SelfDaily Server.lnk"
$Target = "powershell.exe"
$ScriptPath = Join-Path $ProjectDir "start-selfdaily.ps1"
$Arguments = "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$ScriptPath`""

$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($ShortcutPath)
$shortcut.TargetPath = $Target
$shortcut.Arguments = $Arguments
$shortcut.WorkingDirectory = $ProjectDir
$shortcut.WindowStyle = 7
$shortcut.Description = "Start SelfDaily local journal server"
$shortcut.Save()

Write-Host "Installed startup shortcut:"
Write-Host $ShortcutPath
