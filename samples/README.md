Samples and benign app templates

This folder contains harmless sample projects and build notes for testing in
isolated labs and emulators. These are NOT backdoors and contain no exploit
code — they are intended for detection testing and training only.

- `python_http_server/` - a tiny Python HTTP server sample used to demonstrate local network flows.
- `android_template/` - notes and placeholder files for building a benign Android app in an emulator.

Build and test guidance

- Python server: run `python samples/python_http_server/server.py` in an isolated environment.
- Android: follow the README in `android_template/` to build a minimal apk with Android Studio or `gradle` in an emulator.
