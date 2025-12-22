"""Example Frida helper (benign) - lists modules of a target process if frida is installed.

This is a defensive/research helper. It will refuse to run if the `frida` package
is not available. It does not modify process memory or inject scripts by default.
"""
import sys

try:
    import frida
except Exception:
    print('frida module not available. Install with `pip install frida` in an isolated env to run this example.')
    sys.exit(0)


def list_modules(process_name: str):
    session = None
    try:
        device = frida.get_usb_device(timeout=1)
    except Exception:
        try:
            device = frida.get_remote_device()
        except Exception:
            print('No frida device found (use emulator with frida-server).')
            return
    try:
        pid = device.spawn([process_name])
        device.resume(pid)
        session = device.attach(pid)
    except Exception:
        # try to attach to running process
        try:
            session = device.attach(process_name)
        except Exception as e:
            print('Failed to attach to process:', e)
            return
    try:
        modules = session.enumerate_modules()
        print(f'Found {len(modules)} modules in {process_name}')
        for m in modules[:20]:
            print(m.name)
    finally:
        try:
            session.detach()
        except Exception:
            pass


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python frida/example_list_modules.py <process_name>')
        sys.exit(0)
    list_modules(sys.argv[1])
