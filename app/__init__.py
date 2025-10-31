# app/__init__.py
# App factory: wires config, model, CORS, and routes together.

from __future__ import annotations
from flask import Flask
from flask_cors import CORS

from app.config import load_config
from app.model import IrisModel
from app.routes import bp as api_bp          # use api_bp consistently
from app.errors import register_error_handlers, register_request_logging


def create_app() -> Flask:
    """
    Create and configure the Flask application.
    - Loads YAML settings
    - Enables CORS
    - Loads the trained Iris model (joblib artifact) at startup
    - Registers API routes
    """
    app = Flask(__name__)

    # 1) Load configuration from config/settings.yaml
    cfg = load_config()
    app.config["APP_CONFIG"] = cfg

    # 2) Enable CORS for allowed origins
    CORS(app, resources={r"/*": {"origins": cfg.cors_origins}})

    # 3) Load the trained model (fail fast if artifact missing)
    #    Requirement: load a small pre-trained model at startup via a config file.
    model = IrisModel(cfg.model_path)
    app.config["MODEL"] = model

    # 4) Register blueprint and global hooks
    app.register_blueprint(api_bp)
    register_request_logging(app)   # structured request/response logs
    register_error_handlers(app)    # global JSON errors

    return app
