from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return {"message": "OK"}

if __name__ == "__main__":
    app.run(threaded=True, debug=True)