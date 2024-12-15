import os
import json
from datetime import datetime

CHAT_BASE_DIR = "chat_sessions/"

def save_conversation_history(chat_folder, messages):
    """Save the conversation history to a JSON file."""
    history_file = os.path.join(chat_folder, "history.json")
    with open(history_file, "w") as f:
        json.dump(messages, f)

def load_conversation_history(chat_folder):
    """Load the conversation history from a JSON file."""
    history_file = os.path.join(chat_folder, "history.json")
    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            return json.load(f)
    return []
