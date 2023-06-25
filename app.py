import json
import random
import time
from http import HTTPStatus

from flask import Flask, Response, request

from clients.postgress.errors import DataBaseQueryIsEmpty
from routes.orders_route import orders_blueprint

app = Flask(__name__)
app.register_blueprint(orders_blueprint)


@app.errorhandler(Exception)
def general_error(err):
    return {"status": "fail", "error": str(err)}, 500


@app.errorhandler(DataBaseQueryIsEmpty)
def empty_search(err: DataBaseQueryIsEmpty):
    return dict(code=404, message=f"not found {err.args}"), 404


@app.errorhandler(422)
@app.errorhandler(400)
def handle_error(err):
    messages = err.data.get("messages", ["Invalid request."])
    return json.dumps({"errors": messages}), err.code


@app.before_request
def wait_random_time():
    if request.method != 'OPTIONS':
        if request.path not in ["/healthcheck"]:
            time.sleep(random.randint(1, 10) / 10)


@app.route("/healthcheck", methods=["GET"])
def health_check():
    return Response(status=HTTPStatus.OK)


if __name__ == '__main__':
    app.run(debug=False)
