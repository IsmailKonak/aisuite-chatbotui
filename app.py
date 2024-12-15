from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
from chatbot.chat_manager import save_conversation_history, load_conversation_history
from chatbot.file_handler import extract_text_with_tika
from chatbot.aisuite_handler import get_model_response
from chatbot.conversation import crop_conversation
import json
import os
import uuid

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads/"

chat_folder = None  # To store the current session folder

# Load pricing configuration
with open("config/pricing_config.json") as f:
    pricing_config = json.load(f)

# Route for the chatbot UI
@app.route("/")
def index():
    """Create a new chat session and redirect to its page."""
    global chat_folder
    session_id = str(uuid.uuid4())  # Generate a unique session ID
    chat_folder = os.path.join("chat_sessions", session_id)
    os.makedirs(chat_folder, exist_ok=True)

    # Initialize an empty history file
    with open(os.path.join(chat_folder, "history.json"), "w") as f:
        json.dump([], f)

    return redirect(url_for("chat_page", session_id=session_id))

@app.route("/new_chat", methods=["GET"])
def new_chat():
    """Create a new chat session and redirect to its page."""
    global chat_folder
    session_id = str(uuid.uuid4())  # Generate a unique session ID
    chat_folder = os.path.join("chat_sessions", session_id)
    os.makedirs(chat_folder, exist_ok=True)

    # Initialize an empty history file
    with open(os.path.join(chat_folder, "history.json"), "w") as f:
        json.dump([], f)

    return redirect(url_for("chat_page", session_id=session_id))

@app.route("/chat/<session_id>", methods=["GET", "POST"])
def chat_page(session_id):
    """Handle chat session based on the session ID."""
    global chat_folder
    chat_folder = os.path.join("chat_sessions", session_id)
    return render_template("index.html", session_id=session_id)

@app.route("/upload_file", methods=["POST"])
def upload_file():
    """Handle file uploads and extract text."""
    global chat_folder
    if chat_folder is None:
        return jsonify({"error": "Chat session not initialized"}), 400

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    # Save file to chat folder
    file_path = os.path.join(chat_folder, file.filename)
    file.save(file_path)

    # Extract text using Tika
    extracted_text = extract_text_with_tika(file_path)
    return jsonify({"message": "File uploaded successfully.", "text": extracted_text})

@app.route("/chat", methods=["POST"])
def chat():
    """Handle chat messages."""
    global chat_folder
    if chat_folder is None:
        return jsonify({"error": "Chat session not initialized"}), 400

    data = request.json
    model = data.get("model")
    user_message = data.get("message")
    max_tokens = data.get("max_tokens", 2048)

    # Load existing history
    messages = load_conversation_history(chat_folder)

    # Add user message
    next_message = {"role": "user", "content": user_message}
    cropped_messages = crop_conversation(max_tokens, messages, next_message)

    # Get model response
    bot_response = get_model_response(model, cropped_messages)
    cropped_messages.append({"role": "assistant", "content": bot_response})

    # Save updated history
    save_conversation_history(chat_folder, cropped_messages)

    # Calculate total tokens and cost
    total_tokens = sum(len(message["content"].split()) for message in cropped_messages)
    total_cost = calculate_total_cost(cropped_messages, model)

    return jsonify({"response": bot_response, "total_tokens": total_tokens, "total_cost": total_cost, "model": model})

def calculate_total_cost(messages, model):
    with open("config/pricing_config.json") as f:
        pricing = json.load(f)

    model_pricing = pricing.get(model, {})
    if not model_pricing:
        return 0  # If model is not found in pricing config, return 0 cost

    prompt_cost_per_token = model_pricing.get("prompt_tokens", 0)
    completion_cost_per_token = model_pricing.get("completion_tokens", 0)

    total_prompt_tokens = 0
    total_completion_tokens = 0
    total_cost = 0

    for message in messages:
        tokens = len(message["content"].split())
        if message["role"] == "user":
            total_prompt_tokens += tokens
        else:
            total_completion_tokens += tokens

        total_cost += (total_prompt_tokens * prompt_cost_per_token + total_completion_tokens * completion_cost_per_token) / 1_000_000

    return total_cost

@app.route("/calculate_cost", methods=["POST"])
def calculate_cost():
    data = request.json
    messages = data.get("messages", [])
    model = data.get("model")

    with open("config/model_config.json") as f:
        models = json.load(f)["models"]

    # Check if the model is local
    is_local = any(m["id"] == model and m["local"] for m in models)

    if is_local:
        return jsonify({"total_cost": "FREE"})

    total_cost = calculate_total_cost(messages, model)
    return jsonify({"total_cost": total_cost})

@app.route("/get_models", methods=["POST"])
def get_models():
    data = request.json  # Expecting { "mode": "API" or "Local" }
    mode = data.get("mode")

    # Load JSON data
    with open("config/model_config.json") as f:
        models = json.load(f)["models"]

    # Set the environment variables based on keywords in the model names
    for model in models:
        model_name = model['name']
        api_key = model['api_key']
        
        if "openai" in model_name.lower():
            print("Setting OpenAI API Key")
            os.environ['OPENAI_API_KEY'] = api_key
        elif "anthropic" in model_name.lower():
            print("Setting Anthropic API Key")
            os.environ['ANTHROPIC_API_KEY'] = api_key
        elif "groq" in model_name.lower():
            print("Setting GROQ API Key")
            os.environ['GROQ_API_KEY'] = api_key

    # Filter models based on mode
    is_local = mode == "Local"
    filtered_models = [model for model in models if model["local"] == is_local]

    return jsonify(filtered_models)

@app.route("/chat/<session_id>/history", methods=["GET"])
def get_chat_history(session_id):
    """Serve chat history for a given session."""
    chat_folder = os.path.join("chat_sessions", session_id)
    history_file = os.path.join(chat_folder, "history.json")

    if not os.path.exists(history_file):
        return jsonify([])

    with open(history_file, "r") as f:
        history = json.load(f)

    return jsonify(history)

@app.route("/previous_chats", methods=["GET"])
def previous_chats():
    """List previous chat sessions with their first message."""
    chat_sessions_dir = "chat_sessions"
    previous_chats = []

    if not os.path.exists(chat_sessions_dir):
        return jsonify(previous_chats)

    for session_id in os.listdir(chat_sessions_dir):
        history_file = os.path.join(chat_sessions_dir, session_id, "history.json")
        if os.path.exists(history_file):
            with open(history_file, "r") as f:
                history = json.load(f)
                if history:
                    first_message = history[0]["content"][:30]  # Get first 30 characters of the first message
                    previous_chats.append({
                        "session_id": session_id,
                        "first_message": first_message
                    })

    return jsonify(previous_chats)

if __name__ == "__main__":
    app.run(debug=True)