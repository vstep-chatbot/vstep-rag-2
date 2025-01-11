import argparse
import logging

from dotenv import load_dotenv
from flask import Flask
from routes import setup_routes
from utils.database import clear_database
from utils.setup_chroma_db import setup_chroma_db

app = Flask(__name__)

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def handle_arguments():
    args = parse_arguments()

    if args.clear:
        if not clear_database():
            logger.error("Database could not be cleared.")


def parse_arguments():
    parser = argparse.ArgumentParser(description="Manage the Flask app and database.")
    parser.add_argument("--clear", action="store_true", help="Clear the database.")

    return parser.parse_args()


if __name__ == "__main__":
    handle_arguments()
    setup_chroma_db()
    setup_routes(app)
    logger.info("Setting up routes...")
    app.run(host="0.0.0.0", port=5000)
