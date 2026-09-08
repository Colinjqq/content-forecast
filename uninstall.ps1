param([ValidateSet("codex", "claude", "all")][string]$Target = "codex")
$ErrorActionPreference = "Stop"
$SkillName = "content-forecast"
$Destinations = @()
if ($Target -eq "codex" -or $Target -eq "all") { $Destinations += Join-Path $HOME ".codex\\skills\\$SkillName" }
if ($Target -eq "claude" -or $Target -eq "all") { $Destinations += Join-Path $HOME ".claude\\skills\\$SkillName" }
foreach ($Destination in $Destinations) {
  if (Test-Path $Destination) {
    Remove-Item -Recurse -Force $Destination
    Write-Host "Removed: $Destination"
  } else { Write-Host "Not installed: $Destination" }
}
Write-Host "Your content-forecast-data directory was not touched."
