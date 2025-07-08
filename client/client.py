import pygame
import sys
import os
import socket
import threading
import sys
import base64
import nacl.public 
import random


pygame.init()


min_size = 900, 650
screen = pygame.display.set_mode(min_size, pygame.RESIZABLE)
screen_size = pygame.display.get_window_size()
clock = pygame.time.Clock()

class pfp():
    def __init__(self, name):
        self.initial = name[0].upper()
        self.rect = pygame.Rect(20,37,50,50)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(base_dir, 'assets', 'font', 'ggsans-Normal.ttf')
        self.font = pygame.font.Font(font_path, 30)
        self.txt_surface = self.font.render(self.initial, True, (255,255,255))
        self.text_coord = (230,42)
        self.rand1 = random.randint(100, 200)
        self.rand2 = random.randint(100, 200)
        self.rand3 = random.randint(100, 200)
    
    def update(self, offset):
        self.rect[1] = self.rect[1] + offset
        self.text_coord = (35,42 + offset)


    def draw(self):
        pygame.draw.rect(screen, (self.rand1,self.rand2,self.rand3), self.rect, border_radius= 40)
        pygame.draw.rect(screen, (150,150,150), self.rect,width=2, border_radius= 40)
        pygame.draw.rect(screen, (40,40,40), pygame.Rect(90, 32, 2, screen_size[1]))
        screen.blit(self.txt_surface, self.text_coord)
        self.reset()

    def reset(self):
        self.rect = pygame.Rect(20,37,50,50)
        self.text_coord = (35,42)


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(base_dir, 'assets', 'font', 'ggsans-Normal.ttf')
        self.font = pygame.font.Font(font_path, 20)
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (61,61,61)
        self.text = [""]
        self.index = 0
        self.text_color = (150,150,150)
        self.txt_surface = self.font.render(text, True, self.text_color)
        self.surfaces = [self.txt_surface]
        self.active = False
        self.text_total = [0]
        self.send_arrow_image = os.path.join(base_dir, 'assets', 'send_arrow.png')
        self.send_image_rect = pygame.rect.Rect(screen_size[0] - 60, screen_size[1] - 62.5, screen_size[1]* 0.059, screen_size[1] - 10)

    def handle_event(self, event):
        COLOR_INACTIVE = (61,61,61)
        COLOR_ACTIVE = (79,79,79)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        elif event.type == pygame.MOUSEBUTTONUP and self.send_image_rect.collidepoint(event.pos):
                    if self.text == [""]:
                        pass
                    else:
                        message = Message(text="".join(self.text), slide=5)
                        self.text = [""]
                        self.text_total = [0]
                        self.surfaces = [self.txt_surface]
                        return message
                    
        elif event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    if self.text == [""]:
                        pass
                    else:
                        message = Message(text="".join(self.text), slide=5)
                        self.text = [""]
                        self.text_total = [0]
                        self.surfaces = [self.txt_surface]
                        return message
                elif event.key == pygame.K_BACKSPACE:
                    if len(self.text[self.index]) == 0 and len(self.text) > 1:
                        self.text.pop()
                        self.text_total.pop()
                        self.surfaces.pop()
                        self.index -= 1

                    if self.text[self.index][:-1] != "":
                        self.text_total[self.index]  -= self.font.size(self.text[self.index][-1])[0]
                    self.text[self.index] = self.text[self.index][:-1]

                else:
                    self.text[self.index] += event.unicode 
                    self.text_total[self.index] += self.font.size(event.unicode)[0]
                for i, line in enumerate(self.text):
                    self.surfaces[i] = self.font.render(line, True, self.text_color)

    def update(self):
        self.check_line_split_increase()
        self.check_line_split_decrease()
        self.rect = pygame.Rect(4.5, 
                                screen_size[1] - 60.0 - (20 * len(self.text)-1), 
                                screen_size[0] - 9, 
                                50 + (20 * len(self.text)-1))
        self.text_total = []
        for i, line in enumerate(self.text):
            self.text_total.append(0)
            for char in line:
                self.text_total[i] += self.font.size(char)[0]

        for i, line in enumerate(self.text):
            self.surfaces[i] = self.font.render(line, True, self.text_color)

    def draw(self, screen):
        pygame.draw.rect(screen, (31,31,31), pygame.rect.Rect(0, 0, screen_size[0], 32))
        pygame.draw.rect(screen, (31,31,31), pygame.rect.Rect(0, 
                                                          screen_size[1] - 60 - (20 * len(self.text)-1),
                                                          screen_size[0], 
                                                          screen_size[1]))
        for i, surface in enumerate(self.surfaces):
            screen.blit(surface, (13.5, 
                                  self.rect[1]+ 23 + (i * 20)))
        pygame.draw.rect(screen, self.color, (self.rect[0], self.rect[1] + 5, self.rect[2], self.rect[3]), 2, 20)

        self.draw_send_button()
    
    def draw_send_button(self):
        send_arrow = pygame.image.load(self.send_arrow_image)
        self.send_image_rect = pygame.rect.Rect(screen_size[0] - 60, screen_size[1] - 62.5, screen_size[1]* 0.059, screen_size[1] - 10)
        n_image = pygame.surface.Surface((40, 40))
        pygame.transform.scale(send_arrow, (40, 40), n_image)
        pygame.Surface.blit(screen, n_image, self.send_image_rect)
        
    
    def get_rect(self):
        return self.rect

    def get_current_total(self):
        return self.text_total[self.index]

    def check_line_split_decrease(self):
        for i, line in enumerate(self.text):
            temp_string = ""
            temp_total = 0
            total = self.text_total[i]
            y = len(line) - 1
            while total > screen_size[0] - 65 and len(self.text[i]) > 0:
                self.text_total[i] -= self.font.size(line[y])[0]
                temp_total += self.font.size(line[y])[0]
                temp_string += line[y]
                self.text[i] = self.text[i][:-1]
                y -= 1
                total = self.text_total[i]
            if temp_string != "":
                if i+1 > len(self.text)-1:
                    self.text.append("")
                    self.text_total.append(0)
                self.text[i+1] = temp_string[::-1] + self.text[i+1]
                self.text_total[i+1] += temp_total
                self.surfaces.append(self.txt_surface)
        self.index = len(self.text) -1

    def check_line_split_increase(self):
        if len(self.text) > 1:
            i = 1
            while i < len(self.text):
                temp_string = ""
                temp_total = 0
                total = self.text_total[i-1]
                y = 0
                while total <= screen_size[0] - 6 and len(self.text[i]) > 0:
                    self.text_total[i] -= self.font.size(self.text[i][y])[0]
                    temp_total += self.font.size(self.text[i][y])[0]
                    temp_string += self.text[i][y]
                    self.text[i] = self.text[i][1:]
                    total = self.text_total[i-1]

                if temp_string != "":
                    self.text[i-1] = self.text[i-1] + temp_string
                    self.text_total[i-1] += temp_total
                i += 1
            x = len(self.text) -1
            while "" in self.text and x +1 == len(self.text):
                if self.text[x] == "":
                    self.text.pop(x)
                    self.surfaces.pop(x)
                    self.text_total.pop(x)


class Message():
    def __init__(self, name=None, text=None, slide=0):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(base_dir, 'assets', 'font', 'ggsans-Normal.ttf')
        if name:
            self.text = [name+":"]
        else:
            self.text = [text]
        self.sender = name
        self.text_total = [0]
        self.font = pygame.font.Font(font_path, 20)
        self.text_color = (150,150,150)
        self.txt_surface = self.font.render(None, True, self.text_color)
        self.surfaces = [self.txt_surface]
        self.get_total()
        self.height = 0
        self.rect = pygame.Rect(110, 32, screen_size[0] - 210, 50 + (20 * self.height))
        self.slide = slide
    
    def get_total(self):
        for i, line in enumerate(self.text):
            for char in line:
                self.text_total[i] += self.font.size(char)[0]

    def update(self):
        self.update_text()
        self.height = len(self.text) - 1
        self.rect = pygame.Rect(110, self.rect[1], screen_size[0] - 210, self.rect[3])
        for i, line in enumerate(self.text):
            self.surfaces[i] = self.font.render(line, True, self.text_color)
        self.draw()
    
    def update_text(self):
        self.check_line_split_increase()
        self.check_line_split_decrease()
    
    def draw(self):
        for i, surface in enumerate(self.surfaces):
            screen.blit(surface, (self.rect[0]+self.slide, self.rect[1]+ 18 + (i * 20)))
    
    def translate(self, direction, spacing, offset):
        self.rect[1] = 32 + offset
        self.rect[1] -=  15 * direction 
        self.rect[1] += spacing
        self.update()

    def check_line_split_decrease(self):
        for i, line in enumerate(self.text):
            temp_string = ""
            temp_total = 0
            total = self.text_total[i]
            y = len(line) - 1
            while total > screen_size[0] - 120 and len(self.text[i]) > 0:
                self.text_total[i] -= self.font.size(line[y])[0]
                temp_total += self.font.size(line[y])[0]
                temp_string += line[y]
                self.text[i] = self.text[i][:-1]
                y -= 1
                total = self.text_total[i]
            if temp_string != "":
                if i+1 > len(self.text)-1:
                    self.text.append("")
                    self.text_total.append(0)
                    self.surfaces.append(self.txt_surface)
                self.text[i+1] = temp_string[::-1] + self.text[i+1]
                self.text_total[i+1] += temp_total
        self.index = len(self.text) -1

    def check_line_split_increase(self):
        if len(self.text) > 1:
            i = 1
            while i < len(self.text):
                temp_string = ""
                temp_total = 0
                total = self.text_total[i-1]
                y = 0
                while total <= screen_size[0] - 120 and len(self.text[i]) > 0:
                    self.text_total[i] -= self.font.size(self.text[i][y])[0]
                    temp_total += self.font.size(self.text[i][y])[0]
                    temp_string += self.text[i][y]
                    self.text[i] = self.text[i][1:]
                    total = self.text_total[i-1]

                if temp_string != "":
                    self.text[i-1] = self.text[i-1] + temp_string
                    self.text_total[i-1] += temp_total
                i += 1
            x = len(self.text) -1
            while "" in self.text:
                if self.text[x] == "":
                    self.text.pop(x)
                    self.surfaces.pop(x)
                    self.text_total.pop(x)
    

class message_canvas():
    def __init__(self):
        self.rect = pygame.rect.Rect(90, 32, screen_size[0] - 180, screen_size[1] - 110)
        self.messages = []
        self.spacing = 0
        self.offset = 0
        self.total_spacing = 0

    def draw(self):
        self.update_size()

    def translate(self, direction):
        translated = False
        print(self.rect, textbox.rect, direction)
        if direction < 0 and self.rect[1] + self.rect[3] > textbox.rect[1]:
            self.rect[1] -= 20 * -direction
            self.offset -= 20 * -direction
            translated = True
        elif direction > 0 and self.rect[1] < 22:
            print(True)
            self.rect[1] += 20 * direction
            self.offset += 20 * direction
            translated = True

        if translated:
            self.update_messages(direction)
            self.update_size()
         
    def update_size(self):
        self.rect = pygame.rect.Rect(90, self.rect[1], screen_size[0] - 180, self.total_spacing)
    
    def populate(self, message):
        self.messages.append(message)
        gap = 20
        if self.total_spacing + gap >= screen_size[1]:
            self.rect[3] += gap
            self.offset -= gap
            self.rect[1] -= gap 

    def update_messages(self, direction=0):
        self.spacing = 0
        for message in self.messages:
            message.translate(direction= direction, spacing = self.spacing, offset = self.offset)
            self.spacing += (len(message.text) * 20)
            message.update()
        self.total_spacing = self.spacing


def draw_screen():
    screen_size = pygame.display.get_window_size()
    background = pygame.rect.Rect(0,0, screen_size[0], screen_size[1])
    background_color = (20,20,20)

    # draw solid background colour
    pygame.draw.rect(screen, background_color, background)

    canvas.draw()

    textbox.draw(screen)
    

def entry_message():
    min_size = 900, 650
    entry_screen = pygame.display.set_mode(min_size)
    entry_screen_size = pygame.display.get_window_size()
    clock = pygame.time.Clock()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(base_dir, 'assets', 'font', 'ggsans-Normal.ttf')
    font = pygame.font.Font(font_path, 20)
    name = ""
    background_rect = pygame.Rect(0,0,entry_screen_size[0], entry_screen_size[1])
    
    textfield = InputBox(4.5, entry_screen_size[1] - 65.0, entry_screen_size[0] - 9, entry_screen_size[1]- 5)

    text = font.render("Please enter your name: ", True, (150, 150, 150))

    name = None

    running = True
    while running:

        background_rect = pygame.Rect(0,0,entry_screen_size[0], entry_screen_size[1])
        textfield.update()
        
        pygame.draw.rect(entry_screen, (31,31,31) ,background_rect)
        entry_screen.blit(text, (4.5, entry_screen_size[1]-110))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return name
            message = textfield.handle_event(event)
            if message:
                return"".join(message.text)
        textfield.draw(entry_screen)
        clock.tick(500)
        pygame.display.update()
    return name

### Network Infrastructure ###
class Port:
    def __init__(self, host='0.0.0.0', port=5000):
        self.host = host
        self.port = port
        self.sock = None

    def connect(self, target_host, target_port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((target_host, target_port))
        return self.sock

keys = {}
pfps = {}
recv_messages = []
def receive_messages(sock, private_key):
    import traceback
    while True:
        try:
            data = sock.recv(4096)
            if not data:
                print("Connection closed by server.")
                break
            pro_data = data.decode()
            if pro_data.startswith("KEYS:"):
                key_list = pro_data[5:]
                if key_list:
                    for entry in key_list.split(';;'):
                        if not entry.strip():
                            continue  # skip empty entries
                        try:
                            peer, pubkey = entry.split('//', 1)
                            keys[peer] = nacl.public.PublicKey(bytes.fromhex(pubkey))
                            if peer not in pfps.keys():
                                pfps[peer] = pfp(peer)
                        except Exception as e:
                            print(f"[ERROR] Malformed key entry: '{entry}' - {e}")
                    print("[Updated] Available peers:", ', '.join(keys.keys()))
                continue
            # If message is encrypted, decode base64 before decrypting
            try:
                name = pro_data[1:int(pro_data[0]) + 1]
                msg_body = pro_data[int(pro_data[0]) + 1:]
                if '//' in msg_body:
                    _, ciphertext_b64 = msg_body.split('//', 1)
                    ciphertext = base64.b64decode(ciphertext_b64)
                    box = nacl.public.Box(private_key, keys[name])
                    message = box.decrypt(ciphertext).decode()
                    recv_messages.append((name, message))
                else:
                    print(pro_data)
            except Exception as e:
                print(f"[ERROR] Failed to parse or decrypt message: {e}\n{traceback.format_exc()}")
        except Exception as e:
            print(f"[ERROR] Exception in receive_messages: {e}\n{traceback.format_exc()}")
            break

def send_message(message, private_key, sock, name):
    message_to_send = ""
    for recipient in keys:
        if recipient != name:
            box = nacl.public.Box(private_key, keys[recipient])
            ciphertext = box.encrypt(message.encode())
            # Encode ciphertext as base64 for safe transport
            ciphertext_b64 = base64.b64encode(ciphertext).decode()
            message_to_send += ";;" + recipient + '//' + ciphertext_b64
    message_to_send = str(len(name))+ name + message_to_send[2:]
    print(message_to_send)
    sock.sendall(message_to_send.encode())


# Initialize program
base_dir = os.path.dirname(os.path.abspath(__file__))
send_arrow_path = os.path.join(base_dir, 'assets', 'send_arrow.png')
send_arrow = pygame.image.load(send_arrow_path)
text_field_color = (61,61,61)
running = True
mouse_direction = 0
canvas = message_canvas()
textbox = InputBox(4.5, screen_size[1] - 65.0, screen_size[0] - 9, screen_size[1]- 5)
name = entry_message()
message = None

private_key = nacl.public.PrivateKey.generate()
public_key = private_key.public_key
pub_key = public_key.encode().hex()

###################################################################################################

server = "127.0.0.1" # change to current device ip address to let all devices on LAN connect

###################################################################################################

entered = False
try:
    port = Port()
    sock = port.connect(server, 5000)
    sock.sendall(f"{len(name)}{name}{pub_key}init".encode())
except ConnectionRefusedError:
    print("Error: Server either refused connection or is currently down.")
    sys.exit(1)

# Start thread for recveiving messages from the server in parallel with main loop execution
recv_thread = threading.Thread(target=receive_messages, args=(sock, private_key), daemon=True)
recv_thread.start()


pygame.display.set_mode(min_size, pygame.RESIZABLE)

while running:
    n_image_rect = draw_screen()  # Draw the main UI and get the send button rect
    textbox.update()              # Update the input box (handle resizing, line splits)
    canvas.update_messages()      # Update message positions and layout
    clock.tick(60)                # Limit to 60 FPS
    offset = 0
    pygame.draw.rect(screen, (30,30,30), pygame.Rect(0, 32, 90, screen_size[1]))
    for p in pfps:
        pfps[p].update(offset)
        pfps[p].draw()
        offset += 55
    textbox.draw(screen)          # Draw the input box
    pygame.draw.rect(screen, (40,40,40), pygame.rect.Rect(90, 30, screen_size[0], 2))
    pygame.display.update()       # Refresh the display

    # Handle window resizing
    if screen_size != pygame.display.get_window_size():
        if (
            pygame.display.get_window_size()[0] < min_size[0]
            or pygame.display.get_window_size()[1] < min_size[1]
        ):
            pygame.display.set_mode(min_size, pygame.RESIZABLE)
        else:
            screen_size = pygame.display.get_window_size()

    # Handle all pygame events (keyboard, mouse, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # User closed the window
        message = textbox.handle_event(event)  # Handle input box events
        if message:
            # User pressed Enter: add message to canvas and send to peers
            canvas.populate(Message(name))      # Show sender name
            canvas.populate(message)            # Show message text
            canvas.populate(Message(text="")) # Add spacing
            canvas.translate(direction=0)      # Scroll to bottom
            if keys:
                send_message("".join(message.text), private_key, sock, name)  # Send encrypted message to all peers
        if event.type == pygame.MOUSEWHEEL:
            mouse_direction = event.y
            canvas.translate(mouse_direction)  # Scroll message canvas
            mouse_direction = 0

    # Display received messages from the receive thread
    while recv_messages:
        recv_name, recv_message = recv_messages.pop(0)
        canvas.populate(Message(recv_name))         # Show sender name
        canvas.populate(Message(text=recv_message, slide=5)) # Show message text
        canvas.populate(Message(text=""))         # Add spacing
        canvas.translate(direction=0)              # Scroll to bottom
    message = None

# quit pygame after closing window
sock.close()
pygame.quit()
