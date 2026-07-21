from flask import Flask, request
import requests

load_balancer = Flask(__name__)

targets = [
    "http://127.0.0.1:5000",
    "http://127.0.0.1:5001",
    "http://127.0.0.1:5002",
    "http://127.0.0.1:5003"
]

current_index = 0


@load_balancer.route("/", methods=["GET", "POST"])
def balance():
    global current_index

    target = targets[current_index]
    current_index = (current_index + 1) % len(targets)

    try:
        response = requests.request(
            method=request.method,
            url=target,
            data=request.get_data(),
            timeout=5
        )

        return response.content, response.status_code

    except requests.RequestException:
        return f"Unable to reach {target}", 503


if __name__ == "__main__":
    load_balancer.run(
        host="0.0.0.0",
        port=8000
    )
