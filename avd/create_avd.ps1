# Placeholder PowerShell script to create an Android AVD (requires Android SDK tools)
# This script is a convenience wrapper and will print the commands to run.

param(
    [string]$name = "mercury_avd",
    [string]$api = "30",
    [string]$abi = "x86"
)

Write-Host "This script expects Android SDK tools (sdkmanager, avdmanager) to be installed and on PATH."
Write-Host "Example commands (execute in an environment with Android SDK installed):"
Write-Host "    sdkmanager \"platforms;android-$api\" \"system-images;android-$api;default;$abi\""
Write-Host "    avdmanager create avd -n $name -k \"system-images;android-$api;default;$abi\" --force"

Write-Host "Created AVD name will be: $name (run emulator -avd $name to start)"
