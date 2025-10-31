# app/routes.py
# Flask routes for health check, single predict, and batch predict.

from __future__ import annotations
from flask import Blueprint,request,jsonify, current_app
from app.auth import require_api_key
from app.schemas import PredictRequest, BatchRequest, PredictResponse

bp=Blueprint("api",__name__)

@bp.get("/health")
def health():
    """
    Lightweight readiness/liveness endpoint.
    Returns model name and version so reviewers know what is running.
    """
    cfg = current_app.config["APP_CONFIG"]
    model =current_app.config.get("MODEL")
    return jsonify({
        "status": "ok",
        "model" : cfg.model_name,
        "model_version":getattr(model, "version", cfg.model_version)
    }), 200

@bp.post("/predict")
@require_api_key
def predict():
    data = request.get_json(silent=True)
    if data is None:
        # 400 explicitly for non-JSON body
        return jsonify({"error": "Bad Request", "code": 400, "details": "Body must be JSON"}), 400

    # Let pydantic raise ValidationError (handled globally as 400)
    req = PredictRequest.model_validate(data)

    model = current_app.config["MODEL"]
    label, prob = model.predict_one(req.features)

    resp = PredictResponse(
        id=req.id,
        label=label,
        probability=float(round(prob, 6)),
        model_version=model.version
    )
    return jsonify(resp.model_dump()), 200


@bp.post("/batch_predict")
@require_api_key
def batch_predict():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Bad Request", "code": 400, "details": "Body must be JSON"}), 400

    req = BatchRequest.model_validate(data)

    features_list = [item.features for item in req.items]
    ids = [item.id for item in req.items]

    model = current_app.config["MODEL"]
    results = model.predict_many(features_list)

    out = []
    for _id, (label, prob) in zip(ids, results):
        out.append(PredictResponse(
            id=_id,
            label=label,
            probability=float(round(prob, 6)),
            model_version=model.version
        ).model_dump())

    return jsonify({"results": out}), 200


