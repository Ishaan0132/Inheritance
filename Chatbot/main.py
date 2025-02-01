from flask import Flask, render_template, request, jsonify
import os
from google.generativeai import GenerativeModel
import markdown

app = Flask(__name__)

os.environ["GOOGLE_API_KEY"] = "API_KEY"

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

gemini = GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="You are a cybersecurity expert",)


def get_gemini_response(prompt):
    try:
        response = gemini.generate_content(
            prompt
        )
        return response.text
    except Exception as e:
        print(f"Error communicating with Gemini API: {e}")
        return "I'm currently experiencing issues. Please try again later."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    user_input = request.form.get("message")
    if user_input:
        bot_response = get_gemini_response(user_input)
        html_response = markdown.markdown(bot_response)
        return jsonify({"bot_response": html_response})
    return jsonify({"error": "No message provided"})


if __name__ == "__main__":
    app.run(debug=True)
