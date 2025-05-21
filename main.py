from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Azure!"

if __name__ == "__main__":
    # Make sure it's listening on 0.0.0.0 for external access
    app.run(host="0.0.0.0", port=80)
