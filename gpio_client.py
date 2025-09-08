import socket
import json
from gpio_types import Direction, Command

class GPIOClient:
    def __init__(self, client_id: str, host: str = "localhost", port: int = 65432):
        self.client_id = client_id
        self.host = host
        self.port = port

    def _send(self, payload: dict) -> dict:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(json.dumps(payload).encode())
            return json.loads(s.recv(2048).decode())

    def request_pin(self, pin: int, direction: Direction) -> dict:
        return self._send({
            "command": Command.REQUEST,
            "pin": pin,
            "direction": direction.value,
            "client_id": self.client_id
        })

    def release_pin(self, pin: int) -> dict:
        return self._send({
            "command": Command.RELEASE,
            "pin": pin,
            "client_id": self.client_id
        })

    def write_pin(self, pin: int, value: int) -> dict:
        return self._send({
            "command": Command.WRITE,
            "pin": pin,
            "value": value,
            "client_id": self.client_id
        })

    def read_pin(self, pin: int) -> dict:
        return self._send({
            "command": Command.READ,
            "pin": pin,
            "client_id": self.client_id
        })

    def check_pin(self, pin: int) -> dict:
        return self._send({
            "command": Command.CHECK,
            "pin": pin
        })

    def get_clients_for_pin(self, pin: int) -> dict:
        return self._send({
            "command": Command.DEBUG_CLIENTS_FOR_PIN,
            "pin": pin
        })

    def get_all_clients(self) -> dict:
        return self._send({
            "command": Command.DEBUG_ALL_CLIENTS,
            "pin": None
        })
