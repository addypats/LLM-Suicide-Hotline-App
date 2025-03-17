from flask import Flask, request, jsonify

app = Flask(__name__)

# Temporary in-memory storage for conversations
conversations = {}

@app.route('/')
def home():
    return "Suicide Hotline API is running."

# Endpoint to start a call session
@app.route('/start_call', methods=['POST'])
def start_call():
    data = request.json
    call_id = data.get("call_id")
    if not call_id:
        return jsonify({"error": "Missing call ID"}), 400

    conversations[call_id] = {"messages": []}  # Initialize conversation log
    return jsonify({"message": f"Call {call_id} started."})

# Endpoint to receive text from STT
@app.route('/receive_text', methods=['POST'])
def receive_text():
    data = request.json
    call_id = data.get("call_id")
    user_text = data.get("text")

    if not call_id or not user_text:
        return jsonify({"error": "Missing call ID or text"}), 400

    # Save user message
    conversations[call_id]["messages"].append({"role": "user", "text": user_text})

    # Placeholder response (later we'll use LLM)
    ai_response = "I'm here for you. Can you tell me more about what you're feeling?"

    # Save AI response
    conversations[call_id]["messages"].append({"role": "ai", "text": ai_response})

    return jsonify({"response": ai_response})

# Endpoint to end the call and save logs
@app.route('/end_call', methods=['POST'])
def end_call():
    data = request.json
    call_id = data.get("call_id")
    if not call_id or call_id not in conversations:
        return jsonify({"error": "Invalid call ID"}), 400

    # Save conversation (later to database)
    conversation_log = conversations.pop(call_id, {})

    return jsonify({"message": f"Call {call_id} ended.", "conversation": conversation_log})

if __name__ == '__main__':
    app.run(debug=True)
