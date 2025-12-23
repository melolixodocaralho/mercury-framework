# build-lite-release.ps1
<#
.SYNOPSIS
Builds a lightweight release ZIP of Mercury Framework containing only essential files.

.DESCRIPTION
Includes:
- Core Mercury framework (mercury/)
- Essential plugins (mercury_plugins/)
- Samples (samples/)
- Documentation (docs/, README.md, LICENSE, RESPONSIBLE_USE.md)
- Tools necessary for running

Excludes:
- CI workflows
- Tests
- Large optional binaries

.EXAMPLE
pwsh ./build-lite-release.ps1
#>

param (
    [string]$OutputDir = "release",
    [string]$ZipName = "mercury-framework-lite.zip"
)

# Resolve paths
$RootDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$OutputPath = Join-Path -Path $RootDir -ChildPath $OutputDir
$ZipPath = Join-Path -Path $OutputPath -ChildPath $ZipName

# Ensure output directory exists
if (-Not (Test-Path $OutputPath)) {
    New-Item -ItemType Directory -Path $OutputPath | Out-Null
}

# Files & directories to include
$IncludeItems = @(
    "mercury",
    "mercury_plugins",
    "samples",
    "docs",
    "README.md",
    "LICENSE",
    "RESPONSIBLE_USE.md"
)

# Clean up old ZIP if exists
if (Test-Path $ZipPath) {
    Remove-Item $ZipPath -Force
}

# Create ZIP (cross-platform)
Write-Host "Building lightweight ZIP..."
if ($IsWindows) {
    # Windows: Use Compress-Archive
    Compress-Archive -Path $IncludeItems -DestinationPath $ZipPath -Force
} else {
    # Linux / macOS: Use zip command if available
    if (Get-Command zip -ErrorAction SilentlyContinue) {
        Push-Location $RootDir
        zip -r $ZipPath $IncludeItems -x "*.git*" "*tests*" "*sandbox*" "*ci.yml*" -q
        Pop-Location
    } else {
        Write-Error "zip command not found on this system. Please install zip utility."
        exit 1
    }
}

Write-Host "Lite ZIP created at: $ZipPath"
