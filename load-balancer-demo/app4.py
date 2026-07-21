from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Response from Flask App 4"


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5003
    )
