# Placeholder PowerShell script to start an emulator AVD
param(
    [string]$name = "mercury_avd"
)

Write-Host "To start the emulator, run (ensure emulator is on PATH):"
Write-Host "    emulator -avd $name -netdelay none -netspeed full"
Write-Host "Use adb to install sample APKs: adb install -r path/to/app-debug.apk"
