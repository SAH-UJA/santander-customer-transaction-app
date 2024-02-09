"""Main flask app server module"""

from flask import Flask

flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    """Home route"""
    return {"message": "OK"}


if __name__ == "__main__":
    flask_app.run(threaded=True, debug=True)