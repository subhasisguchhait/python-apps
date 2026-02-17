# app/__init__.py
from flask import Flask
from flask_smorest import Api

from app.db import init_engine, init_session_factory, register_session_handlers
from app.resources import users_blp
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file


def create_app():
    app = Flask(__name__)

    # --- OpenAPI / Swagger ---
    app.config["API_TITLE"] = "Simple CRUD API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.json.sort_keys = False

    # --- DB URL (DBA-managed schema; no migrations here) ---
    DATABASE_URL = os.getenv("DATABASE_URL")

    # Engine + Session factory stored on app
    app.engine = init_engine(DATABASE_URL)
    app.SessionLocal = init_session_factory(app.engine)

    # Ensure sessions are always rollback/closed
    register_session_handlers(app)

    # Smorest API + routes
    api = Api(app)
    api.register_blueprint(users_blp)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app
