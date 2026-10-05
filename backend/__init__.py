from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_MODELS = [
    {
        "id": "gpt-image-1",
        "name": "GPT Image 1",
        "provider": "openai",
        "requires_api_key": "OPENAI_API_KEY",
        "status": "active",
        "description": "Required evaluation model"
    },
    {
        "id": "gemini-2.5-flash-image",
        "name": "Gemini 2.5 Flash Image",
        "provider": "google",
        "requires_api_key": "GOOGLE_API_KEY",
        "status": "planned",
        "description": "Required evaluation model"
    },
    {
        "id": "gemini-3.1-flash-image-preview",
        "name": "Gemini 3.1 Flash Image Preview",
        "provider": "google",
        "requires_api_key": "GOOGLE_API_KEY",
        "status": "planned",
        "description": "Required evaluation model"
    }
]

REGIONS = [
    {
        "id": "bihar",
        "name": "Bihar",
        "festival": "Makar Sankranti",
        "festival_id": "makar-sankranti",
        "status": "pilot"
    },
    {
        "id": "gujarat",
        "name": "Gujarat",
        "festival": "Uttarayan",
        "festival_id": "uttarayan",
        "status": "pilot"
    }
]

APP_TITLE = "Regional Festival T2I Localization"
APP_RESEARCH_QUESTION = "Can a T2I model adapt the same commercial campaign to culturally distinct Indian regional festival contexts without producing generic, culturally incoherent, or incorrectly localized imagery?"
APP_HYPOTHESIS = "T2I models can learn to produce culturally coherent and region-specific advertising visuals when given a clear campaign brief, a specific regional/festival context, a product reference image, and a disciplined generation framework."
APP_STATUS = "Pilot / exploratory research"

EVALUATION_QUESTIONS = [
    {"id": "regional_specificity", "label": "Regional cultural specificity", "type": "scale", "min": 1, "max": 5},
    {"id": "cultural_coherence", "label": "Cultural coherence", "type": "scale", "min": 1, "max": 5},
    {"id": "campaign_fidelity", "label": "Campaign objective/message", "type": "scale", "min": 1, "max": 5},
    {"id": "product_fidelity", "label": "Product fidelity", "type": "scale", "min": 1, "max": 5},
    {"id": "commercial_quality", "label": "Commercial advertising quality", "type": "scale", "min": 1, "max": 5},
    {"id": "overall_usefulness", "label": "Overall usefulness", "type": "scale", "min": 1, "max": 5}
]

PROJECT_DOCUMENTS = {
    "framework": ROOT / "framework" / "T2I_ADVERTISING_CREATIVE_PROJECT_FRAMEWORK.md",
    "campaign": ROOT / "campaigns" / "REGIONAL_FESTIVAL_CAMPAIGN_PILOT.md",
    "reference": ROOT / "references" / "product_reference.png",
    "methodology": ROOT / "docs" / "methodology.md",
    "protocol": ROOT / "docs" / "experiment-protocol.md",
    "rubric": ROOT / "docs" / "evaluation-rubric.md"
}
