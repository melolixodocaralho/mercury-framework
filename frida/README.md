Frida instrumentation examples (emulator only)

This folder contains guidance and a minimal example showing how researchers can
use Frida to instrument a benign sample app running in an emulator. Do not use
these techniques against devices without explicit authorization.

Requirements

- `frida` Python package (optional, used for examples)
- A running Android emulator or device with `frida-server` installed (emulator preferred for testing)

Example usage (high-level)

1) Start emulator and run a benign sample app.
2) Optionally start `frida-server` on the emulator (only in controlled lab).
3) Use the example script to attach to a process name and list modules.

Note: the example script `example_list_modules.py` will only run if `frida` is installed.
It is intentionally conservative and prints guidance rather than performing invasive actions.
