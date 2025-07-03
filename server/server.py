import socket
import threading
import keyboard

clients = {}
keys = {}
clients_lock = threading.Lock()

def handle_keypress():
    if keyboard.is_pressed("ctrl+c"):
        raise KeyboardInterrupt

def handle_client(client_sock, client_addr):
    print(f"Client {client_addr} connected.")
    client_name = None
    try:
        while True:
            data = client_sock.recv(4096)
            if not data:
                print(f"Client {client_addr} disconnected.")
                break
            pro_data = data.decode()
            client_name = pro_data[1: int(pro_data[0]) + 1]
            if pro_data[-4:] == "init":
                # Extract public key from init message
                public_key = pro_data[int(pro_data[0]) + 1:-4]
                with clients_lock:
                    clients[client_name] = client_sock
                    keys[client_name] = public_key
                    # Send all known public keys to this client
                    all_keys = [(name, key) for name, key in keys.items()]
                    key_list = ';;'.join([f"{name}//{key}" for name, key in all_keys])
                    try:
                        client_sock.sendall(("KEYS:" + key_list).encode())
                        print(f"Sent all known public keys to {client_name}")
                    except Exception as e:
                        print(f"Error sending keys to {client_name}: {e}")
                    # Send updated key list to all clients
                    for c_name, c_sock in clients.items():
                        try:
                            c_sock.sendall(("KEYS:" + key_list).encode())
                            print(f"Sent updated public keys to {c_name}")
                        except Exception as e:
                            print(f"Error sending updated keys to {c_name}: {e}")
                print(f"Registered {client_name}")
                continue

            # Expecting multiple messages in the form: recipient//actual_message;;recipient2//actual_message2;;...
            msg_body = pro_data[int(pro_data[0]) + 1:]
            if ';;' in msg_body:
                messages = msg_body.split(';;')
            else:
                messages = [msg_body]
            with clients_lock:
                for msg in messages:
                    print(msg)
                    if '//' in msg:
                        recipient, actual_message = msg.split('//', 1)
                        recipient = recipient.strip()
                        recipient_sock = clients.get(recipient)
                        if recipient_sock:
                            try:
                                send_data = str(len(client_name)) + client_name + "//" + actual_message
                                recipient_sock.sendall(send_data.encode())
                                print(f"Forwarded message from {client_name} to {recipient}")
                            except Exception as e:
                                print(f"Error forwarding to {recipient}: {e}")
                        else:
                            print(f"Recipient {recipient} not found.")
                    else:
                        print(f"Malformed message from {client_name}: {msg}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        with clients_lock:
            if client_name and client_name in clients:
                del clients[client_name]
        client_sock.close()

def main():
    host = '0.0.0.0'
    port = 5000
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((host, port))
    server_sock.listen(10)
    server_sock.settimeout(1.0)
    print(f"Server listening on {host}:{port}")
    try:
        while True:
            try:
                client_sock, client_addr = server_sock.accept()
                t = threading.Thread(target=handle_client, args=(client_sock, client_addr), daemon=True)
                t.start()
            except socket.timeout:
                continue
    except KeyboardInterrupt:
        print("Shutting down server.")
    finally:
        server_sock.close()

if __name__ == "__main__":
    main()