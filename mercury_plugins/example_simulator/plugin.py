import sys

if __name__ == "__main__":
    if "--setup" in sys.argv:
        print("Setup: initializing example simulator plugin...")
        sys.exit(0)
    elif "--run" in sys.argv:
        print("Run: running safe example plugin...")
        sys.exit(0)
    elif "--cleanup" in sys.argv:
        print("Cleanup: cleaning up example simulator plugin...")
        sys.exit(0)
    else:
        print("Unknown command")
        sys.exit(1)
