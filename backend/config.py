import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_MODELS = [
    {
        "id": "gpt-image-1",
        "name": "GPT Image 1",
        "provider": "openai",
        "requires_api_key": "OPENAI_API_KEY",
        "default_params": {"quality": "high", "size": "1536x1024"},
    },
    {
        "id": "gemini-2.5-flash-image",
        "name": "Gemini 2.5 Flash Image",
        "provider": "google",
        "requires_api_key": "GOOGLE_API_KEY",
        "default_params": {"temperature": 0.7},
    },
    {
        "id": "gemini-3.1-flash-image-preview",
        "name": "Gemini 3.1 Flash Image Preview",
        "provider": "google",
        "requires_api_key": "GOOGLE_API_KEY",
        "default_params": {"temperature": 0.7},
    },
]

REGIONS = [
    {
        "id": "bihar",
        "name": "Bihar",
        "festival": "Makar Sankranti",
        "festival_id": "makar-sankranti",
        "status": "pilot",
    },
    {
        "id": "gujarat",
        "name": "Gujarat",
        "festival": "Uttarayan",
        "festival_id": "uttarayan",
        "status": "pilot",
    },
]

PROJECT_META = {
    "title": "Regional Festival T2I Localization",
    "research_question": "Can a T2I model adapt the same commercial campaign to culturally distinct Indian regional festival contexts without producing generic, culturally incoherent, or incorrectly localized imagery?",
    "hypothesis": "T2I models can learn to produce culturally coherent and region-specific advertising visuals when given a clear campaign brief, a specific regional/festival context, a product reference image, and a disciplined generation framework.",
    "status": "Pilot / exploratory research",
}

APP_CONFIG = {
    "framework_path": ROOT / "framework" / "T2I_ADVERTISING_CREATIVE_PROJECT_FRAMEWORK.md",
    "campaign_path": ROOT / "campaigns" / "REGIONAL_FESTIVAL_CAMPAIGN_PILOT.md",
    "reference_path": ROOT / "references" / "product_reference.png",
    "fallback_reference_path": ROOT / "Product_reference.jpeg",
    "outputs_dir": ROOT / "outputs",
    "experiments_db": ROOT / "experiments" / "t2i_research.db",
}

EVALUATION_QUESTIONS = [
    {"id": "regional_specificity", "label": "Regional cultural specificity"},
    {"id": "cultural_coherence", "label": "Cultural coherence"},
    {"id": "campaign_fidelity", "label": "Campaign objective/message"},
    {"id": "product_fidelity", "label": "Product fidelity"},
    {"id": "commercial_quality", "label": "Commercial advertising quality"},
    {"id": "overall_usefulness", "label": "Overall usefulness"},
]


def get_reference_path():
    if APP_CONFIG["reference_path"].exists():
        return APP_CONFIG["reference_path"]
    if APP_CONFIG["fallback_reference_path"].exists():
        return APP_CONFIG["fallback_reference_path"]
    return APP_CONFIG["reference_path"]
