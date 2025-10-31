# app/errors.py
# Centralized JSON error handling + minimal structured request/response logging.

from __future__ import annotations
import time
import uuid
import logging
from typing import Optional

from flask import jsonify, request, g
from werkzeug.exceptions import HTTPException, BadRequest
from pydantic import ValidationError


# --- minimal JSON logger setup (uses root logger) ---
# You can enhance formatters later; this is intentionally simple for a fresher project.
logger = logging.getLogger("flask-ml-api")
if not logger.handlers:
    logger.setLevel(logging.INFO)
    _h = logging.StreamHandler()
    _h.setLevel(logging.INFO)
    # Very small, JSON-ish line format to keep it reviewer-friendly
    _fmt = logging.Formatter('%(message)s')
    _h.setFormatter(_fmt)
    logger.addHandler(_h)


def _json_error(code: int, message: str, details: Optional[str] = None):
    """Return a consistent JSON error body."""
    body = {"error": message, "code": code}
    if details:
        body["details"] = details
    return jsonify(body), code


def register_request_logging(app):
    """
    Registers before/after hooks to log each request and response in a structured way.
    Covers part of requirement #6: structured logs.
    """
    @app.before_request
    def _start_timer_and_request_id():
        g._start_time = time.time()
        # simple per-request id (useful when scanning logs)
        g.request_id = str(uuid.uuid4())

    @app.after_request
    def _log_response(response):
        try:
            duration_ms = int((time.time() - getattr(g, "_start_time", time.time())) * 1000)
            client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
            method = request.method
            path = request.path
            status = response.status_code
            content_type = response.headers.get("Content-Type", "")
            # Keep it one-line JSON-ish for easy grep; real JSON logger can be added if you want.
            log_line = {
                "event": "http_request",
                "request_id": getattr(g, "request_id", None),
                "method": method,
                "path": path,
                "status": status,
                "duration_ms": duration_ms,
                "client_ip": client_ip,
                "content_type": content_type,
            }
            # Note: Do NOT log request/response bodies here to avoid PII/noise.
            logger.info(str(log_line))
        except Exception:
            # Never let logging break the response path
            pass
        return response


def register_error_handlers(app):
    """
    Registers global error handlers (requirement #5).
    Returns JSON for common failures with proper HTTP codes.
    """

    @app.errorhandler(ValidationError)
    def handle_pydantic_validation(err: ValidationError):
        # Pydantic v2 ValidationError
        try:
            detail = "; ".join([e.get("msg", "") for e in err.errors()])
        except Exception:
            detail = str(err)
        return _json_error(400, "Invalid input", detail)

    @app.errorhandler(BadRequest)
    def handle_bad_request(err: BadRequest):
        # Missing/invalid JSON body, etc.
        detail = getattr(err, "description", None) or "Bad request"
        return _json_error(400, "Bad Request", detail)

    @app.errorhandler(HTTPException)
    def handle_http_exception(err: HTTPException):
        # Any other HTTPException: 404 Not Found, 405 Method Not Allowed, etc.
        code = err.code or 500
        message = err.name or "HTTP Error"
        detail = getattr(err, "description", None)
        return _json_error(code, message, detail)

    @app.errorhandler(Exception)
    def handle_generic_exception(err: Exception):
        # Catch-all safety net; don't leak internals
        return _json_error(500, "Internal Server Error", "An unexpected error occurred")
