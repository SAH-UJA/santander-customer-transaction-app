"""Main flask app server module"""

from datetime import datetime
from flask import Flask

flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    """Home route"""
    return {
        "message": "OK",
        "timestamp": datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    }


if __name__ == "__main__":
    flask_app.run(threaded=True, debug=True)
