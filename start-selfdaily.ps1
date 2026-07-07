$ErrorActionPreference = "Stop"

$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Port = 5177

$listener = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue |
  Where-Object { $_.OwningProcess -ne 0 } |
  Select-Object -First 1

if (-not $listener) {
  Start-Process -WindowStyle Hidden -FilePath python -ArgumentList "selfdaily-server.py" -WorkingDirectory $ProjectDir
  Start-Sleep -Milliseconds 900
}
