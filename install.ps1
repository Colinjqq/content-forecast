param([ValidateSet("codex", "claude", "all")][string]$Target = "codex")
$ErrorActionPreference = "Stop"
$SkillName = "content-forecast"
$SourceDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Destinations = @()
if ($Target -eq "codex" -or $Target -eq "all") { $Destinations += Join-Path $HOME ".codex\\skills\\$SkillName" }
if ($Target -eq "claude" -or $Target -eq "all") { $Destinations += Join-Path $HOME ".claude\\skills\\$SkillName" }
foreach ($Destination in $Destinations) {
  if (Test-Path $Destination) { throw "Already installed: $Destination. Remove it first with .\\uninstall.ps1 -Target $Target" }
  New-Item -ItemType Directory -Force -Path (Split-Path -Parent $Destination) | Out-Null
  Copy-Item -Recurse -Path $SourceDir -Destination $Destination
  Write-Host "Installed: $Destination"
}
Write-Host "Start a new Agent session and say: Initialize Content Forecast"
