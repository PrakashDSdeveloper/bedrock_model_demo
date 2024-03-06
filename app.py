from flask import Flask, request, jsonify, render_template
from test import demo_memory, demo_conversation  # Import from app.py instead of test

app = Flask(__name__)

memory = demo_memory()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    input_text = request.json.get('input_text')
    chat_response = demo_conversation(input_text=input_text, memory=memory)
    return jsonify({'response': chat_response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
