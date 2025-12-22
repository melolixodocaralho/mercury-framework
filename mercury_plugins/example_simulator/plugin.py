import argparse

def setup():
    print("Setup complete for example_simulator")

def run():
    print("Running safe example plugin")

def cleanup():
    print("Cleanup done for example_simulator")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--setup", action="store_true")
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--cleanup", action="store_true")
    args = parser.parse_args()

    if args.setup:
        setup()
    elif args.run:
        run()
    elif args.cleanup:
        cleanup()
    else:
        print("No action specified")
