from flask import Flask, render_template, request, jsonify
from qa_engine import answer_question
import traceback, os, subprocess

app = Flask(__name__, static_folder='static', template_folder='templates')

EXAMPLE_FILE = "example_input.txt"

def load_examples():
    try:
        with open(EXAMPLE_FILE, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        return [
            "Compare production of Rice and Wheat",
            "Show trend of Rice",
            "Average annual rainfall for the last 5 years"
        ]

examples = load_examples()

@app.route("/")
def index():
    return render_template("index.html", examples=examples)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json() or {}
    query = data.get("question", "")
    try:
        result = answer_question(query)
        return jsonify(result)
    except Exception as e:
        # print traceback to server console and return JSON error
        traceback.print_exc()
        return jsonify({"text": f"Internal server error: {e}", "sources": []}), 500

if __name__ == "__main__":
    # optional: auto-run DB load if data present and DB missing tables? we keep explicit step
    app.run(debug=True)
