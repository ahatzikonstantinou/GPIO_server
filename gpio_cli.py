import argparse
from gpio_client import GPIOClient

def main():
    parser = argparse.ArgumentParser(description="GPIO Debug CLI")
    parser.add_argument("--client", type=str, default="debugger")
    parser.add_argument("--pin", type=int, help="Pin number")
    parser.add_argument("--all", action="store_true", help="List all clients for all pins")

    args = parser.parse_args()
    client = GPIOClient(args.client)

    if args.all:
        resp = client.get_all_clients()
        for pin, clients in resp.get("clients_by_pin", {}).items():
            print(f"Pin {pin}: {clients}")
    elif args.pin is not None:
        resp = client.get_clients_for_pin(args.pin)
        print(f"Clients for pin {args.pin}: {resp.get('clients', [])}")
    else:
        print("Specify --pin or --all")

if __name__ == "__main__":
    main()
