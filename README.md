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
   git clone https://github.com/ahatzikonstantinou/gpio_server.git
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
ExecStart=/usr/bin/python3 /opt/GPIO_server/gpio_server.py
WorkingDirectory=/opt/GPIO_server/
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
GPIO_server/
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


## 🔧 Making the GPIO Client Library Globally Available

If you want all applications and users on your Raspberry Pi to access the `gpio_client.py` and `gpio_types.py` library from a shared location (e.g. `/opt/GPIO_server`), you can set the `PYTHONPATH` environment variable system-wide.

### 📁 Step 1: Place the Library

Move or copy the library files to a shared directory:

```bash
mkdir -p /opt/gpio_lib
cp gpio_client.py gpio_types.py /opt/gpio_lib/
```

(Optional) Add an `__init__.py` file to make it a proper Python module:

```bash
touch /opt/gpio_lib/__init__.py
```

---

### 🛠️ Step 2: Set PYTHONPATH System-Wide

To make this path available to all users and apps:

#### Option A: Add to `/etc/profile` (login shells)

```bash
sudo nano /etc/profile
```

Add this line at the end:

```bash
export PYTHONPATH=/opt/gpio_lib${PYTHONPATH:+:$PYTHONPATH}
```

#### Option B: Add to `/etc/bash.bashrc` (non-login shells)

```bash
sudo nano /etc/bash.bashrc
```

Add the same line:

```bash
export PYTHONPATH=/opt/gpio_lib${PYTHONPATH:+:$PYTHONPATH}
```

---

### 🔄 Step 3: Apply Changes

To apply the changes immediately:

```bash
source /etc/profile
```

Or reboot the system:

```bash
sudo reboot
```

Verify the path is active:

```bash
echo $PYTHONPATH
```

You should see `/opt/gpio_lib` included.

---

### 🧪 Step 4: Import from Anywhere

Now any Python script can import the library:

```python
from gpio_client import GPIOClient
from gpio_types import Direction
```

---

### 🧼 Optional: Use a Wrapper Script for Apps

If you're launching apps via systemd or shell scripts, you can create a wrapper that sets the path before execution:

```bash
#!/bin/bash
export PYTHONPATH=/opt/gpio_lib${PYTHONPATH:+:$PYTHONPATH}
exec python3 /opt/gpio_lib/gpio_server.py
```

Then point your systemd service to this script.

