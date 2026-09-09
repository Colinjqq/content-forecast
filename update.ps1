param([ValidateSet("codex", "claude", "all")][string]$Target = "codex")
$ErrorActionPreference = "Stop"

$SkillName = "content-forecast"
$SourceDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Destinations = @()
if ($Target -eq "codex" -or $Target -eq "all") { $Destinations += Join-Path $HOME ".codex\skills\$SkillName" }
if ($Target -eq "claude" -or $Target -eq "all") { $Destinations += Join-Path $HOME ".claude\skills\$SkillName" }

if (Test-Path (Join-Path $SourceDir ".git")) {
  Write-Host "Fetching the latest version from GitHub..."
  git -C $SourceDir pull --ff-only
  if ($LASTEXITCODE -ne 0) { throw "Git could not fetch the latest version." }
} else {
  throw "This folder is not a Git clone. Download the latest release or clone the repository, then run update.ps1 again."
}

$Version = (Get-Content (Join-Path $SourceDir "VERSION") -ErrorAction SilentlyContinue | Select-Object -First 1)
if (-not $Version) { $Version = "unknown" }

foreach ($Destination in $Destinations) {
  if (-not (Test-Path $Destination)) { throw "Not installed: $Destination. Install first with .\install.ps1 -Target $Target" }

  $Parent = Split-Path -Parent $Destination
  $Staging = Join-Path $Parent (".content-forecast-update-" + [guid]::NewGuid().ToString("N"))
  $Backup = "$Destination.previous"
  New-Item -ItemType Directory -Force -Path $Staging | Out-Null

  Get-ChildItem -Force $SourceDir | Where-Object { $_.Name -notin @(".git", ".DS_Store") } | ForEach-Object {
    Copy-Item -Recurse -Force $_.FullName -Destination $Staging
  }

  if (Test-Path $Backup) { Remove-Item -Recurse -Force $Backup }
  Move-Item $Destination $Backup
  try {
    Move-Item $Staging $Destination
    Remove-Item -Recurse -Force $Backup
    Write-Host "Updated to v$Version`: $Destination"
  } catch {
    if (Test-Path $Destination) { Remove-Item -Recurse -Force $Destination }
    Move-Item $Backup $Destination
    throw "Update failed; the previous installation was restored."
  }
}

Write-Host "Your separate content-forecast-data directory was not touched."
Write-Host "Start a new Agent session to use the updated Skill."
