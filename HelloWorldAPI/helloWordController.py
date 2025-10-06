from flask import Blueprint, request

__all__ = ['hello_controller']

hello_controller = Blueprint('hello', __name__)


@hello_controller.route("/hello", methods=['GET'])
def say_hello():
    return dict(message="Hello World!")