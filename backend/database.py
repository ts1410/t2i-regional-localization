from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from pathlib import Path
import os
import uuid
import json
from datetime import datetime, timezone

from backend.config import APP_CONFIG, PROJECT_META, REQUIRED_MODELS, REGIONS, EVALUATION_QUESTIONS
from backend.database import init_db, list_experiments, get_experiment, save_experiment, list_evaluations, save_evaluation
from backend.services.prompt_builder import build_prompt
from backend.services.version_manager import get_version_info
from backend.services import sha256_file
from backend.providers.openai_provider import OpenAIImageProvider
from backend.providers.google_provider import GoogleImageProvider

ROOT = Path(__file__).resolve().parents[1]
FRONTEND_DIR = ROOT / "frontend"
OUTPUTS_DIR = ROOT / "outputs"

app = Flask(__name__, static_folder=str(FRONTEND_DIR), static_url_path="")
CORS(app)


@app.route("/")
def index():
    return send_file(FRONTEND_DIR / "index.html")


@app.route("/api/project", methods=["GET"])
def api_project():
    return jsonify({
        "title": PROJECT_META["title"],
        "research_question": PROJECT_META["research_question"],
        "hypothesis": PROJECT_META["hypothesis"],
        "status": PROJECT_META["status"],
    })


@app.route("/api/framework", methods=["GET"])
def api_framework():
    path = APP_CONFIG["framework_path"]
    content = path.read_text(encoding="utf-8")
    version = get_version_info()
    return jsonify({"content": content, "path": str(path), "hash": version["framework_hash"], "version": version["framework_version"]})


@app.route("/api/campaign", methods=["GET"])
def api_campaign():
    path = APP_CONFIG["campaign_path"]
    content = path.read_text(encoding="utf-8")
    version = get_version_info()
    return jsonify({"content": content, "path": str(path), "hash": version["campaign_hash"], "version": version["campaign_version"]})


@app.route("/api/methodology", methods=["GET"])
def api_methodology():
    path = ROOT / "docs" / "methodology.md"
    return jsonify({"content": path.read_text(encoding="utf-8")})


@app.route("/api/experiment-protocol", methods=["GET"])
def api_protocol():
    path = ROOT / "docs" / "experiment-protocol.md"
    return jsonify({"content": path.read_text(encoding="utf-8")})


@app.route("/api/models", methods=["GET"])
def api_models():
    return jsonify({"models": REQUIRED_MODELS})


@app.route("/api/regions", methods=["GET"])
def api_regions():
    return jsonify({"regions": REGIONS})


@app.route("/api/experiments", methods=["GET"])
def api_experiments():
    return jsonify({"experiments": list_experiments()})


@app.route("/api/experiments/<experiment_id>", methods=["GET"])
def api_experiment(experiment_id):
    item = get_experiment(experiment_id)
    if item is None:
        return jsonify({"error": "Experiment not found."}), 404
    return jsonify({"experiment": item})


@app.route("/api/results", methods=["GET"])
def api_results():
    items = list_experiments()
    results = [item for item in items if item.get("output_path")]
    return jsonify({"results": results})


@app.route("/api/results/<experiment_id>", methods=["GET"])
def api_result(experiment_id):
    item = get_experiment(experiment_id)
    if item is None:
        return jsonify({"error": "Experiment not found."}), 404
    if not item.get("output_path"):
        return jsonify({"error": "No result file for that experiment."}), 404
    path = ROOT / item["output_path"]
    return send_file(path, mimetype="image/png")


@app.route("/api/evaluation/rubric", methods=["GET"])
def api_evaluation_rubric():
    content = (ROOT / "docs" / "evaluation-rubric.md").read_text(encoding="utf-8")
    return jsonify({"rubric": content, "questions": EVALUATION_QUESTIONS})


@app.route("/api/evaluation", methods=["GET"])
def api_evaluations():
    return jsonify({"evaluations": list_evaluations()})


@app.route("/api/evaluation", methods=["POST"])
def submit_evaluation():
    payload = request.get_json(silent=True) or {}
    if not payload.get("participant_id") or not payload.get("experiment_id"):
        return jsonify({"error": "Participant ID and experiment ID are required."}), 400
    record = {
        "id": str(uuid.uuid4()),
        "participant_id": payload["participant_id"],
        "experiment_id": payload["experiment_id"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "responses": payload.get("responses", {}),
        "comment": payload.get("comment"),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    save_evaluation(record)
    return jsonify({"ok": True, "evaluation": record})


@app.route("/api/generate", methods=["POST"])
def generate_image():
    payload = request.get_json(silent=True) or {}
    model = payload.get("model")
    region = payload.get("region")
    festival = payload.get("festival")
    if not model or not region or not festival:
        return jsonify({"error": "Model, region, and festival are required."}), 400

    valid_model = next((m for m in REQUIRED_MODELS if m["id"] == model), None)
    valid_region = next((r for r in REGIONS if r["id"] == region), None)
    if not valid_model:
        return jsonify({"error": "Invalid model configuration."}), 400
    if not valid_region:
        return jsonify({"error": "Invalid region configuration."}), 400

    try:
        prompt = build_prompt(region=region, festival=festival, model=model)
        versions = get_version_info()
        params = {
            "size": "1536x1024",
            "quality": "high",
            "temperature": 0.7,
        }
        provider_name = valid_model["provider"]
        api_key_name = valid_model["requires_api_key"]
        if not os.getenv(api_key_name):
            return jsonify({"error": f"{api_key_name.replace('_', ' ').title()} is not configured."}), 400

        if provider_name == "openai":
            provider = OpenAIImageProvider(api_key=os.getenv(api_key_name))
        elif provider_name == "google":
            provider = GoogleImageProvider(api_key=os.getenv(api_key_name))
        else:
            return jsonify({"error": "Model provider is unavailable."}), 400

        result = provider.generate(prompt=prompt, model=model, parameters=params, reference_image=str(APP_CONFIG["reference_path"]))
        output_name = f"{model}_{region}_{festival}_{uuid.uuid4().hex[:8]}.png"
        output_path = OUTPUTS_DIR / output_name
        OUTPUTS_DIR.mkdir(exist_ok=True)
        with open(output_path, "wb") as fh:
            fh.write(base64_decode(result["image_b64"]))

        exp_id = str(uuid.uuid4())
        experiment_record = {
            "id": exp_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "model": model,
            "model_version": "v1",
            "region": region,
            "festival": festival,
            "experiment_id": f"exp-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6]}",
            "framework_version": versions["framework_version"],
            "framework_hash": versions["framework_hash"],
            "campaign_version": versions["campaign_version"],
            "campaign_hash": versions["campaign_hash"],
            "reference_image_hash": versions["reference_image_hash"],
            "prompt_version": "v1",
            "generation_parameters": params,
            "output_path": f"outputs/{output_name}",
            "status": "success",
            "error": None,
            "provider": provider_name,
            "api_key_present": True,
            "metadata": {
                "region_name": valid_region["name"],
                "festival_name": valid_region["festival"],
                "prompt": prompt,
                "framework_path": str(APP_CONFIG["framework_path"]),
                "campaign_path": str(APP_CONFIG["campaign_path"]),
            },
        }
        save_experiment(experiment_record)
        return jsonify({"ok": True, "experiment": experiment_record, "result": {"image_path": experiment_record["output_path"]}})
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except FileNotFoundError as exc:
        return jsonify({"error": "Reference image could not be loaded."}), 400
    except Exception as exc:
        return jsonify({"error": "Generation failed.", "details": str(exc)}), 500


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
