from flask import Flask
from time import sleep

app = Flask(__name__)

@app.route("/wait")
def wait():
    sleep(1)
    return "<p>Hello, world!</p>"

if __name__ == "__main__":
    app.run(threaded=False, processes=3, port=8000)
