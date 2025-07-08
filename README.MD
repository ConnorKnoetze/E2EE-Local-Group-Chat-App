# End-to-End Encrypted Local Group Chat Application

## Overview
This project is a secure, peer-to-peer group chat application designed for local area networks (LAN). It features end-to-end encryption (E2EE) using Curve25519 (via PyNaCl) and supports both CLI and GUI clients. The application is ideal for private communication within a local network.

## Features
- **End-to-End Encryption (E2EE):** Messages are encrypted using Curve25519 keys, ensuring secure communication.
- **Multi-Client Support:** Run multiple clients on the same device or across devices on a LAN.
- **LAN Connectivity:** Easily connect devices within the same network.
- **Cross-Platform:** Compatible with Windows and other platforms supporting Python and PyNaCl.
- **Customizable GUI:** Includes a pygame-based graphical user interface for sending and receiving messages.

## Installation
### Dependencies
Ensure the following Python packages are installed:
- `PyGame`
- `PyNaCl`
- `keyboard`

You can install them manually:
```bash
pip install pynacl keyboard pygame
```
Alternatively, run `client_launcher.py` to automatically install dependencies.

## Usage
### Running Multiple Clients on the Same Device
1. Open `client_launcher.py`.
2. Edit the range of the `for` loop to specify the desired number of clients (default is 2).
3. Run `client_launcher.py`.

### Connecting Multiple Devices on LAN
1. Open `client.py`.
2. Locate the line near the bottom: `server = "127.0.0.1"`.
3. Replace `127.0.0.1` with the IPv4 address of the device hosting the server. You can find this address by running `ipconfig` in the command prompt.
4. Start the server:
   - Run `client_launcher.py`, or
   - Run `server.py` directly from the command prompt or PowerShell, and
   - Run `client.py` on all devices you wish to connect.

### Stopping the Server
To stop the server:
- Press `Ctrl + C` in the terminal, or
- Close the terminal window.

## Notes
- If running the server independently, ensure `client.py` is executed on all devices to establish communication.
- The application is designed for local networks and does not support internet-based communication.

## License
This project is licensed under the MIT License.

## Contact
For questions or support, please contact connorknoetze@gmail.com.
