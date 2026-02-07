import datetime
import os

LOG_FILE = os.path.join(os.path.dirname(__file__), '..', 'database', 'chat_logs.txt')

def log_message(user_msg, bot_reply):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{timestamp}] USER: {user_msg}\nBOT: {bot_reply}\n\n")