import csv
import logging
import os

import click
# Load the specific libraries
from flask import Flask, request
from loguru import logger
from pydantic import BaseModel

# Initiate the web server
app = Flask(__name__)


# User class
class User(BaseModel):
    uid: int
    first_name: str
    last_name: str
    department: str


# Get the current path of the file "user.csv"
filepath = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "user.csv"
)

# Load the user from the CSV file in local memory
users = []
with open(filepath, "r") as f:
    titles = ["uid", "first_name", "last_name", "department"]
    with open(filepath, "r") as file:
        reader = csv.DictReader(file, titles)
        next(reader)  # skip header
        for csv_user in reader:
            users.append(User(**csv_user))


# Create a custom handler
class InterceptHandler(logging.Handler):
    def emit(self, record):
        pass


# 1. Add CLI arguments
# Initiate the web server
@logger.catch
@click.command()
@click.option("--ip", default="127.0.0.1", help="Server IP Address")
@click.option("--tcp", default=9000, help="Server port")
@click.option("--log_level", default="INFO", help="Level of the debugger")
def main(ip, tcp, log_level):
    # Se the debug if log level is on DEBUG
    debug = False
    if log_level == "DEBUG":
        debug = True

    # 2. Track the server usage
    logger.start(
        "server.log",
        level=log_level,
        format="{time} {level} {message}",
        backtrace=debug,
    )

    # Register Loguru as handler
    app.logger.addHandler(InterceptHandler())

    logger.info("Server starting")

    # Main function to run the server
    app.run(debug=debug, port=tcp, host=ip)


# Route (path of the URL) declaration
@app.route("/")
def root():
    # Print hello world HTML web page
    logger.debug(f"{request.method} - / - {request.args.__dict__}")

    return "<html><title>Hello world</title><body><p>Hello world</p></body></html>"


@app.route("/user/<int:uid>", methods=["GET"])
def get_user_by_id(uid):
    # Get a user by it's Id
    logger.debug(f"{request.method} - /user/<int> - {request.args.__dict__}")

    return users[uid - 1].__dict__


@app.route("/user", methods=["POST"])
def create_user():
    # Insert a new user
    logger.debug(f"{request.method} - /user/<int> - {request.args.__dict__}")

    users.append(
        User(
            **{
                "uid": len(users) + 1,
                "first_name": request.args.get("first_name"),
                "last_name": request.args.get("last_name"),
                "department": request.args.get("department"),
            }
        )
    )
    return users[-1].__dict__


@app.route("/user/<int:uid>", methods=["PUT"])
def update_user_by_id(uid):
    # Update a user by it's Id
    logger.debug(f"{request.method} - /user/<int> - {request.args.__dict__}")

    users[uid - 1] = User(
        **{
            "uid": uid,
            "first_name": request.args.get("first_name"),
            "last_name": request.args.get("last_name"),
            "department": request.args.get("department"),
        }
    )
    return users[uid - 1].__dict__


@app.route("/user/<int:uid>", methods=["DELETE"])
def delete_user(uid):
    # Delete a user
    logger.debug(f"{request.method} - /user/<int> - {request.args.__dict__}")

    users.pop(uid - 1)
    return "ok"


@app.route("/users")
def list_user():
    # Get the list of user
    logger.debug(f"{request.method} - /users - {request.args.__dict__}")

    return [usr.__dict__ for usr in users]


if __name__ == "__main__":
    # Run the server with te help of the arguments given in the CLI
    print(main(standalone_mode=False))
