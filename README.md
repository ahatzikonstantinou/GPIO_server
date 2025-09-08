# 🧠 Raspberry Pi GPIO TCP Server

A lightweight, type-safe GPIO server for Raspberry Pi using `libgpiod` and raw TCP. Designed for multi-client access with shared pin state, introspection tools, and a clean Python client library.

---

## 📦 Dependencies

### System Packages

Make sure your Raspberry Pi has the following installed:

```bash
sudo apt update
sudo apt install libgpiod-dev python3-pip
```

### Python Packages

Install via pip:

```bash
pip install gpiod
```

---

## 🛠️ Installation

### 🔧 Option 1: System-Wide Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourname/gpio_server.git
   cd gpio_server
   ```

2. Install Python dependencies:

   ```bash
   pip3 install gpiod
   ```

3. Install the systemd service:

   ```bash
   sudo cp gpio-server.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable gpio-server
   sudo systemctl start gpio-server
   ```

4. Check status:

   ```bash
   sudo systemctl status gpio-server
   ```

---

### 🧪 Option 2: Virtual Environment Setup

1. Clone and enter the project:

   ```bash
   git clone https://github.com/yourname/gpio_server.git
   cd gpio_server
   ```

2. Create and activate virtualenv:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install gpiod
   ```

4. Run the server manually:

   ```bash
   python gpio_server.py
   ```

> ⚠️ Note: If using a virtualenv, systemd won’t automatically activate it. You’ll need to wrap the server in a shell script that sources the venv before launching.

---

## 🧰 Python Client Library

Use the provided `gpio_client.py` and `gpio_types.py` for type-safe access.

### Example:

```python
from gpio_client import GPIOClient
from gpio_types import Direction

client = GPIOClient("my_app")

# Request pin 17 for output
client.request_pin(17, Direction.OUT)
client.write_pin(17, 1)
client.release_pin(17)

# Request pin 27 for input
client.request_pin(27, Direction.IN)
value = client.read_pin(27)
print("Read:", value)
client.release_pin(27)
```

---

## 🖥️ Command-Line Interface

Use `gpio_cli.py` to inspect active clients.

### List clients for a specific pin:

```bash
python gpio_cli.py --pin 17
```

### List all clients for all pins:

```bash
python gpio_cli.py --all
```

---

## 🔧 Systemd Service File

Located in `gpio-server.service`. Example contents:

```ini
[Unit]
Description=GPIO TCP Server using libgpiod
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/gpio_server/gpio_server.py
WorkingDirectory=/home/pi/gpio_server
Restart=always
User=pi
Group=pi
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

> ✅ Adjust paths and Python location as needed (`which python3`).

---

## 📁 Project Structure

```
gpio_server/
├── gpio_server.py         # TCP server
├── gpio_client.py         # Python client library
├── gpio_types.py          # Enums and type hints
├── gpio_cli.py            # Command-line debug tool
├── gpio-server.service    # systemd service file
└── README.md              # This file
```

---

## 🧼 Uninstall

To remove the systemd service:

```bash
sudo systemctl stop gpio-server
sudo systemctl disable gpio-server
sudo rm /etc/systemd/system/gpio-server.service
sudo systemctl daemon-reload
```

---

## 🧠 Notes

- Pins are held until **all clients** release them.
- Server runs on `localhost:65432` by default.
- Debug methods available:
  - `getNamesOfAllClientsForPin`
  - `getNamesOfAllClientsForAllPins`

---

## 📬 License

MIT (or your preferred license)
