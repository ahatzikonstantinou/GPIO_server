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
            # print(f"Sending '{payload}'")
            s.connect((self.host, self.port))
            s.sendall(json.dumps(payload).encode())

            raw = s.recv(2048).decode().strip()
            if not raw:
                raise ValueError("Received empty response from server")
            
            # print(f"Received #{raw}#")
            return json.loads(raw)

    def request_pin(self, pin: int, direction: Direction) -> dict:
        return self._send({
            "command": Command.REQUEST.value,
            "pin": pin,
            "direction": direction.value,
            "client_id": self.client_id
        })

    def release_pin(self, pin: int) -> dict:
        return self._send({
            "command": Command.RELEASE.value,
            "pin": pin,
            "client_id": self.client_id
        })

    def write_pin(self, pin: int, value: int) -> dict:
        return self._send({
            "command": Command.WRITE.value,
            "pin": pin,
            "value": value,
            "client_id": self.client_id
        })

    def read_pin(self, pin: int) -> dict:
        return self._send({
            "command": Command.READ.value,
            "pin": pin,
            "client_id": self.client_id
        })

    def check_pin(self, pin: int) -> dict:
        return self._send({
            "command": Command.CHECK.value,
            "pin": pin
        })

    def get_pin_info(self, pin: int) -> dict:
        return self._send({
            "command": Command.PIN_INFO.value,
            "pin": pin
        })

    def get_all_pins(self) -> dict:
        return self._send({
            "command": Command.ALL_PINS_INFO.value,
            "pin": None
        })
