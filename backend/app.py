import base64
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, jsonify, request, send_file, send_from_directory
from flask_cors import CORS

from backend.config import APP_CONFIG, EVALUATION_QUESTIONS, PROJECT_META, REQUIRED_MODELS, REGIONS, get_reference_path
from backend.database import get_experiment, init_db, list_evaluations, list_experiments, save_evaluation, save_experiment
from backend.providers.google_provider import GoogleImageProvider
from backend.providers.openai_provider import OpenAIImageProvider
from backend.services.prompt_builder import build_prompt
from backend.services.version_manager import get_version_info

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS_DIR = ROOT / "outputs"
FRONTEND_DIR = ROOT / "frontend"

app = Flask(__name__, static_folder=str(FRONTEND_DIR), static_url_path="/static")
CORS(app)


@app.route("/")
def index():
    return send_file(FRONTEND_DIR / "index.html")


@app.route("/styles.css")
def styles():
    return send_file(FRONTEND_DIR / "styles.css")


@app.route("/app.js")
def app_js():
    return send_file(FRONTEND_DIR / "app.js")


@app.route("/api/project", methods=["GET"])
def api_project():
    return jsonify(PROJECT_META)


@app.route("/api/framework", methods=["GET"])
def api_framework():
    framework_path = APP_CONFIG["framework_path"]
    if not framework_path.exists():
        framework_path = ROOT / "Framework.md"
    content = framework_path.read_text(encoding="utf-8")
    versions = get_version_info()
    return jsonify({
        "content": content,
        "version": versions["framework_version"],
        "hash": versions["framework_hash"],
    })


@app.route("/api/campaign", methods=["GET"])
def api_campaign():
    campaign_path = APP_CONFIG["campaign_path"]
    if not campaign_path.exists():
        campaign_path = ROOT / "Campaign_pilot.md"
    content = campaign_path.read_text(encoding="utf-8")
    versions = get_version_info()
    return jsonify({
        "content": content,
        "version": versions["campaign_version"],
        "hash": versions["campaign_hash"],
    })


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
    experiment = get_experiment(experiment_id)
    if experiment is None:
        return jsonify({"error": "Experiment not found."}), 404
    return jsonify({"experiment": experiment})


@app.route("/api/results", methods=["GET"])
def api_results():
    experiments = list_experiments()
    results = [entry for entry in experiments if entry.get("output_path")]
    return jsonify({"results": results})


@app.route("/api/results/<experiment_id>", methods=["GET"])
def api_result(experiment_id):
    experiment = get_experiment(experiment_id)
    if experiment is None:
        return jsonify({"error": "Experiment not found."}), 404
    output_path = ROOT / experiment["output_path"]
    if not output_path.exists():
        return jsonify({"error": "Result file not found."}), 404
    return send_file(output_path, mimetype="image/png")


@app.route("/api/evaluation/rubric", methods=["GET"])
def api_evaluation_rubric():
    rubric_path = ROOT / "docs" / "evaluation-rubric.md"
    if not rubric_path.exists():
        rubric_content = "# Draft Evaluation Rubric\n\nNo rubric available yet."
    else:
        rubric_content = rubric_path.read_text(encoding="utf-8")
    return jsonify({
        "rubric": rubric_content,
        "questions": EVALUATION_QUESTIONS,
    })


@app.route("/api/evaluation", methods=["GET"])
def api_evaluation():
    return jsonify({"evaluations": list_evaluations()})


@app.route("/api/evaluation", methods=["POST"])
def submit_evaluation():
    payload = request.get_json(silent=True) or {}
    participant_id = payload.get("participant_id")
    experiment_id = payload.get("experiment_id")
    if not participant_id or not experiment_id:
        return jsonify({"error": "Participant ID and experiment ID are required."}), 400

    record = {
        "id": str(uuid.uuid4()),
        "participant_id": participant_id,
        "experiment_id": experiment_id,
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
    model_id = payload.get("model")
    region_id = payload.get("region")
    festival_id = payload.get("festival")
    if not model_id or not region_id or not festival_id:
        return jsonify({"error": "Model, region, and festival are required."}), 400

    model = next((item for item in REQUIRED_MODELS if item["id"] == model_id), None)
    region = next((item for item in REGIONS if item["id"] == region_id), None)
    if model is None:
        return jsonify({"error": "Invalid experiment configuration."}), 400
    if region is None:
        return jsonify({"error": "Invalid experiment configuration."}), 400

    api_key_name = model.get("requires_api_key")
    if not os.getenv(api_key_name):
        return jsonify({"error": f"{api_key_name.replace('_', ' ').title()} is not configured."}), 400

    try:
        prompt = build_prompt(region=region_id, festival=festival_id, model=model_id)
        versions = get_version_info()
        params = model.get("default_params", {})
        provider_name = model["provider"]

        if provider_name == "openai":
            provider = OpenAIImageProvider(api_key=os.getenv(api_key_name))
        elif provider_name == "google":
            provider = GoogleImageProvider(api_key=os.getenv(api_key_name))
        else:
            return jsonify({"error": "Model is unavailable."}), 400

        reference_path = str(get_reference_path())
        result = provider.generate(prompt=prompt, model=model_id, parameters=params, reference_image=reference_path)

        OUTPUTS_DIR.mkdir(exist_ok=True)
        output_name = f"{model_id}_{region_id}_{festival_id}_{uuid.uuid4().hex[:8]}.png"
        output_path = OUTPUTS_DIR / output_name
        with output_path.open("wb") as handle:
            handle.write(base64.b64decode(result["image_b64"]))

        experiment_id = f"exp-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6]}"
        metadata = {
            "output_name": output_name,
            "prompt": prompt,
            "provider": provider_name,
            "reference_path": reference_path,
        }
        record = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "model": model_id,
            "model_version": "v1",
            "region": region_id,
            "festival": festival_id,
            "experiment_id": experiment_id,
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
            "metadata": metadata,
        }
        save_experiment(record)
        return jsonify({"ok": True, "experiment": record})

    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except FileNotFoundError:
        return jsonify({"error": "Reference image could not be loaded."}), 400
    except Exception as exc:
        return jsonify({"error": "Generation failed.", "details": str(exc)}), 500


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
