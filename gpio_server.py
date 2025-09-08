import socket
import threading
import json
import gpiod

HOST = 'localhost'
PORT = 65432
CHIP = gpiod.Chip('gpiochip0')
pin_registry = {}  # pin: {'direction': str, 'clients': set(), 'line': gpiod.Line}
lock = threading.Lock()

def handle_client(conn):
    with conn:
        while True:
            data = conn.recv(2048)
            if not data:
                break
            req = json.loads(data.decode())
            response = process_request(req)
            conn.sendall(json.dumps(response).encode())

def process_request(req):
    cmd = req.get("command")
    pin = req.get("pin")
    client_id = req.get("client_id")

    with lock:
        if cmd == "request":
            direction = req["direction"]
            if pin not in pin_registry:
                line = CHIP.get_line(pin)
                config = gpiod.LineRequest()
                config.consumer = "gpio_server"
                config.request_type = gpiod.LineRequest.DIRECTION_INPUT if direction == "in" else gpiod.LineRequest.DIRECTION_OUTPUT
                line.request(config)
                pin_registry[pin] = {"direction": direction, "clients": set(), "line": line}
            pin_registry[pin]["clients"].add(client_id)
            return {"success": True, "message": f"Pin {pin} assigned"}

        elif cmd == "release":
            if pin in pin_registry and client_id in pin_registry[pin]["clients"]:
                pin_registry[pin]["clients"].remove(client_id)
                if not pin_registry[pin]["clients"]:
                    pin_registry[pin]["line"].release()
                    del pin_registry[pin]
                return {"success": True, "message": f"Pin {pin} released"}
            return {"success": False, "message": "Pin not held"}

        elif cmd == "write":
            value = req["value"]
            if pin in pin_registry and pin_registry[pin]["direction"] == "out":
                pin_registry[pin]["line"].set_value(value)
                return {"success": True, "message": f"Pin {pin} set to {value}"}
            return {"success": False, "message": "Pin not output"}

        elif cmd == "read":
            if pin in pin_registry and pin_registry[pin]["direction"] == "in":
                val = pin_registry[pin]["line"].get_value()
                return {"success": True, "value": val}
            return {"success": False, "message": "Pin not input"}

        elif cmd == "check":
            available = pin not in pin_registry
            return {"success": True, "available": available}

        elif cmd == "getNamesOfAllClientsForPin":
            clients = list(pin_registry.get(pin, {}).get("clients", []))
            return {"success": True, "clients": clients}

        elif cmd == "getNamesOfAllClientsForAllPins":
            all_clients = {p: list(info["clients"]) for p, info in pin_registry.items()}
            return {"success": True, "clients_by_pin": all_clients}

    return {"success": False, "message": "Unknown command"}

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"GPIO Server running on {HOST}:{PORT}")
        while True:
            conn, _ = s.accept()
            threading.Thread(target=handle_client, args=(conn,), daemon=True).start()

if __name__ == "__main__":
    start_server()
