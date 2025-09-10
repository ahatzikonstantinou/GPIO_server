import socket
import threading
import json
import gpiod
import signal
import sys

HOST = 'localhost'
PORT = 65432
CHIP = gpiod.Chip('gpiochip0')
pin_registry = {}  # pin: {'direction': str, 'value': int, 'clients': set(), 'line': gpiod.Line}
lock = threading.Lock()

def handle_client(conn):
    with conn:
        while True:
            try:
                data = conn.recv(2048)
                if not data:
                    break
            except ConnectionResetError:
                print("Client disconnected abruptly")
                break
            try:
                req = json.loads(data.decode())
                # print(f"Received: {req}")
                response = process_request(req)
                conn.sendall(json.dumps(response).encode())
            except Exception as e:
                conn.sendall(json.dumps({"success": False, "message": str(e)}).encode())

def process_request(req):
    cmd = req.get("command")
    pin = req.get("pin")
    client_id = req.get("client_id")

    with lock:
        if cmd == "request":
            direction = req.get("direction")
            if pin not in pin_registry:
                line = CHIP.get_line(pin)
                try:
                    if direction == "in":
                        line.request(consumer="gpio_server", type=gpiod.LINE_REQ_DIR_IN)
                    elif direction == "out":
                        line.request(consumer="gpio_server", type=gpiod.LINE_REQ_DIR_OUT, default_val=0)
                    else:
                        print(f"Client {client_id} tried to request pin {pin} with invalid direction {direction}")
                        return {"success": False, "message": f"Invalid direction: {direction}"}
                    pin_registry[pin] = {"direction": direction, "clients": set(), "line": line}
                    print(f"Pin {pin} requested successfully for the first time by client {client_id} for {direction}")
                except Exception as e:
                    return {"success": False, "message": f"Failed to request pin {pin}: {e}"}
            pin_registry[pin]["clients"].add(client_id)
            print(f"Client {client_id} added to clients of pin {pin} ({direction})")
            return {"success": True, "message": f"Pin {pin} assigned"}

        elif cmd == "release":
            if pin in pin_registry and client_id in pin_registry[pin]["clients"]:
                pin_registry[pin]["clients"].remove(client_id)
                print(f"Client {client_id} released pin {pin}")
                if not pin_registry[pin]["clients"]:
                    pin_registry[pin]["line"].release()                    
                    del pin_registry[pin]
                    print(f"All clients have released pin {pin}. Pin is released.")
                return {"success": True, "message": f"Pin {pin} released"}
            return {"success": False, "message": "Pin not held"}

        elif cmd == "write":
            value = req.get("value")
            if pin in pin_registry and pin_registry[pin]["direction"] == "out":
                try:
                    pin_registry[pin]["line"].set_value(value)
                    pin_registry[pin]["value"] = value
                    print(f"Writing {value} to pin {pin}")
                    return {"success": True, "message": f"Pin {pin} set to {value}"}
                except Exception as e:
                    return {"success": False, "message": f"Failed to write to pin {pin}: {e}"}
            return {"success": False, "message": "Pin not output"}

        elif cmd == "read":
            if pin in pin_registry and pin_registry[pin]["direction"] == "in":
                try:
                    val = pin_registry[pin]["line"].get_value()
                    # print(f"Read {val} from pin {pin}")
                    pin_registry[pin]["value"] = val
                    return {"success": True, "value": val}
                except Exception as e:
                    return {"success": False, "message": f"Failed to read pin {pin}: {e}"}
            return {"success": False, "message": "Pin not input"}

        elif cmd == "check":
            available = pin not in pin_registry
            return {"success": True, "available": available}

        elif cmd == "getPinInfo":
            info = pin_registry.get(pin, {})
            clients = list(info.get("clients", []))
            direction = info.get("direction")
            value = info.get("value")

            return {
                "success": True,
                "clients": clients,
                "direction": direction,
                "value": value
            }

        elif cmd == "getAllPinsInfo":
            all_clients = {
                p: {
                    "clients": list(info["clients"]),
                    "direction": info.get("direction"),
                    "value": info.get("value")
                }
                for p, info in pin_registry.items()
            }
            return {"success": True, "clients_by_pin": all_clients}

    return {"success": False, "message": "Unknown command"}

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"GPIO Server running on {HOST}:{PORT}")

        def shutdown_handler(sig, frame):
            print("Shutting down server...")
            s.close()
            sys.exit(0)

        signal.signal(signal.SIGINT, shutdown_handler)

        while True:
            conn, _ = s.accept()
            threading.Thread(target=handle_client, args=(conn,), daemon=True).start()

if __name__ == "__main__":
    start_server()
