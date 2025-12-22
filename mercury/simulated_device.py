"""Simulated Device - Harmless stubs for educational testing.

All functions return fake data and explicitly warn the user. These are intended
for use in emulators and isolated labs only.
"""
from dataclasses import dataclass
from typing import List
import datetime


@dataclass
class SimulatedDevice:
    device_id: str = "mercury-sim-0001"
    model: str = "MercuryOS Emulator"
    os_version: str = "SimOS 1.0"

    def device_info(self) -> str:
        return (
            f"Device ID: {self.device_id}\n"
            f"Model: {self.model}\n"
            f"OS Version: {self.os_version}\n"
            f"Note: This is a simulated device. No real device data is accessed."
        )

    def fake_sms(self) -> List[str]:
        """Return a list of fake SMS message strings."""
        now = datetime.datetime.utcnow().isoformat() + "Z"
        return [
            f"{now} - Alice: Hey, this is a test message (simulated)",
            f"{now} - Bob: Reminder: meeting at 10:00 (simulated)",
        ]

    def fake_gallery(self) -> List[str]:
        """Return a list of fake gallery entries (filenames)."""
        return [
            "IMG_0001_simulated.jpg",
            "IMG_0002_simulated.png",
            "holiday_photo_simulated.jpg",
        ]

    def fake_camera_frame(self) -> str:
        """Return an ASCII-art 'camera frame' for demo purposes."""
        ascii_frame = (
            "+----------------------+\n"
            "| /////////\\\\\\ \\|\n"
            "| |||||||||||||||||| |\n"
            "| \\\\\\\\/////// |\n"
            "+----------------------+\n"
            "(Simulated camera frame — no real camera used)"
        )
        return ascii_frame
