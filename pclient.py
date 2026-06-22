import socket
import threading
import base64
import os
import random
import subprocess  # Added for Termux hardware bridge
import time        # Added for precise vibration timing
from datetime import datetime
from hashlib import sha256
from cryptography.fernet import Fernet

if os.name == 'nt':
    os.system('')
os.system("cls")
# Palettes with updated ultra-bright Neon Green and Light Gray
COLORS = [
    "\033[1;96m",  # Bold Cyan
    "\033[1;92m",  # Bold High-Intensity Bright Green (Updated)
    "\033[1;95m",  # Bold Soft Lavender
    "\033[1;91m",  # Bold Peach
    "\033[1;94m"   # Bold Sky Blue
]
LIGHT_GRAY = "\033[38;5;246m" # Light Gray for timestamps
YELLOW = "\033[1;93m"          # Minecraft style join/leave notice color
RESET = "\033[0m"

def get_color_for_name(name):
    clean_name = name.replace("[", "").replace("]", "")
    score = sum(ord(char) for char in clean_name)
    return COLORS[score % len(COLORS)]

def format_colored_message(raw_message):
    """Appends timestamps and maps local layout colors."""
    timestamp = datetime.now().strftime("%m/%d/%Y; %H:%M:%S")
    time_prefix = f"{LIGHT_GRAY}[{timestamp}]{RESET} "

    # Check for join/leave system banners
    if raw_message.endswith("has joined.") or raw_message.endswith("has left."):
        return f"{time_prefix}{YELLOW}{raw_message}{RESET}"
        
    # Chat message configuration
    if ": " in raw_message:
        sender_name, text = raw_message.split(": ", 1)
        color = get_color_for_name(sender_name)
        return f"{time_prefix}{color}{sender_name}{RESET}: {text}"
        
    return f"{time_prefix}{raw_message}"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def trigger_pager_vibration():
    """Triggers a distinct double-buzz like a real pager."""
    try:
        # First pulse (350 milliseconds)
        subprocess.run(["termux-vibrate", "-d", "350", "-f"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(0.18) # Gap between the double-buzz
        # Second pulse (350 milliseconds)
        subprocess.run(["termux-vibrate", "-d", "350", "-f"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        # Prevents the app from crashing if run outside of Termux (like on a PC)
        pass

# 1. Connection inputs
target_ip = input("Enter Server IP Address: ")
target_port = int(input("Enter Server Port: "))

random_id = random.randint(100, 999)
default_nickname = f"user{random_id}"

nickname = input(f"Choose your nickname [Press Enter for '{default_nickname}']: ")
if not nickname.strip():
    nickname = default_nickname

shared_password = input("Enter the secret chatroom password: ")

key = base64.urlsafe_b64encode(sha256(shared_password.encode()).digest())
cipher = Fernet(key)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((target_ip, target_port))

# --- HANDSHAKE ---
try:
    server_signal = client.recv(1024).decode('utf-8')
    if server_signal == "AUTH_REQUEST":
        client.send(shared_password.encode('utf-8'))
    
    server_signal = client.recv(1024).decode('utf-8')
    if server_signal == "NICKNAME_REQUEST":
        client.send(nickname.encode('utf-8'))
        
    count_signal = client.recv(1024).decode('utf-8')
    if count_signal.startswith("ONLINE_COUNT:"):
        online_users = int(count_signal.split(":")[1])
except Exception as e:
    print("Handshake failed.")
    client.close()
    exit()

clear_screen()
my_color = get_color_for_name(nickname)
print(f"--- Connected to the Chatroom as {my_color}{nickname}{RESET} ---")
if online_users == 1:
    print("✨ You are the only one here.")
else:
    print(f"👥 There are {online_users} members online.")
print("Type your message and press Enter.\n")

# Send encrypted join alert
join_alert = f"[{nickname}] has joined."
client.send(cipher.encrypt(join_alert.encode('utf-8')))

# 2. Chat logic threads
def receive_messages():
    while True:
        try:
            raw_data = client.recv(4096)
            if not raw_data:
                break
            
            # Catch server plain text leave signals
            try:
                decoded_msg = raw_data.decode('utf-8')
                if decoded_msg.startswith("SYSTEM_LEAVE_SIGNAL:"):
                    left_user = decoded_msg.split(":")[1]
                    raw_leave_text = f"[{left_user}] has left."
                    colored_msg = format_colored_message(raw_leave_text)
                    print(f"\r{colored_msg}")
                    print(f"{my_color}{nickname}{RESET}: ", end="", flush=True)
                    continue
            except:
                pass 

            # Standard chat decryption
            decrypted_message = cipher.decrypt(raw_data).decode('utf-8')
            colored_msg = format_colored_message(decrypted_message)
            
            print(f"\r{colored_msg}")
            print(f"{my_color}{nickname}{RESET}: ", end="", flush=True)
            
            # Check if incoming message is from someone else, then vibrate
            if ": " in decrypted_message:
                sender_name, _ = decrypted_message.split(": ", 1)
                if sender_name != nickname:
                    # Fire vibration in a separate background thread so the chat interface doesn't lag/freeze during pauses
                    threading.Thread(target=trigger_pager_vibration, daemon=True).start()
            
        except Exception as e:
            print("\n[Disconnected from server]")
            client.close()
            break

def send_messages():
    while True:
        try:
            text = input(f"{my_color}{nickname}{RESET}: ")
            
            if not text.strip():
                continue
                
            formatted_message = f"{nickname}: {text}"
            encrypted_message = cipher.encrypt(formatted_message.encode('utf-8'))
            client.send(encrypted_message)
            
            # Print your own sent message locally with fresh timestamp formatting above your input
            local_msg = format_colored_message(formatted_message)
            # \033[A moves cursor up line, \r clears line
            print(f"\033[A\r{local_msg}")
        except:
            break

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

send_thread = threading.Thread(target=send_messages)
send_thread.start()
