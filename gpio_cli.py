import argparse
from gpio_client import GPIOClient

def main():
    parser = argparse.ArgumentParser(description="GPIO Debug CLI")
    parser.add_argument("--client", type=str, default="debugger")
    parser.add_argument("--pin", type=int, help="Pin number")
    parser.add_argument("--all", action="store_true", help="List all pins")

    args = parser.parse_args()
    client = GPIOClient(args.client)

    if args.all:
        resp = client.get_all_pins()
        print(f"{'Pin':<6} {'Direction':<10} {'Value':<6} Clients")
        print("-" * 50)
        for pin, info in resp.get("clients_by_pin", {}).items():
            direction = info.get("direction", "")
            value = info.get("value", "")
            clients = ", ".join(info.get("clients", []))
            print(f"{str(pin):<6} {direction:<10} {str(value):<6} {clients}")
    elif args.pin is not None:
        resp = client.get_pin_info(args.pin)
        direction = resp.get("direction", "")
        value = resp.get("value", "")
        clients = ", ".join(resp.get("clients", []))

        print(f"{'Pin':<6} {'Direction':<10} {'Value':<6} Clients")
        print("-" * 50)
        print(f"{str(args.pin):<6} {direction:<10} {str(value):<6} {clients}")

    else:
        print("Specify --pin or --all")

if __name__ == "__main__":
    main()
