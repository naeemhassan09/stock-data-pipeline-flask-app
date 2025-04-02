from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from Flask on Google Cloud!"

if __name__ == '__main__':
    # Running on 0.0.0.0 makes the app accessible from any external IP
    app.run(host='0.0.0.0', port=8080, debug=True)