$ErrorActionPreference = "Stop"

$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$StartScript = Join-Path $ProjectDir "start-selfdaily.ps1"

& $StartScript
Start-Process "http://localhost:5177/"
