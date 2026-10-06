from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def build_prompt(region: str, festival: str, model: str, custom_task: str = None):
    framework_path = ROOT / "framework" / "T2I_ADVERTISING_CREATIVE_PROJECT_FRAMEWORK.md"
    campaign_path = ROOT / "campaigns" / "REGIONAL_FESTIVAL_CAMPAIGN_PILOT.md"
    
    if not framework_path.exists():
        framework_path = ROOT / "Framework.md"
    if not campaign_path.exists():
        campaign_path = ROOT / "Campaign_pilot.md"
    
    framework_text = framework_path.read_text(encoding="utf-8")
    campaign_text = campaign_path.read_text(encoding="utf-8")

    task = custom_task or (
        f"Generate one final advertising image for the {region.title()} — {festival.title()} execution. "
        "Use the supplied product reference image as the source of truth for product identity and packaging. "
        "Preserve the campaign objective and create a coherent regional commercial image without turning the brief into a checklist."
    )

    prompt = f"""PROJECT FRAMEWORK

{framework_text}

CAMPAIGN BRIEF

{campaign_text}

CURRENT REGIONAL EXECUTION

- Region: {region.title()}
- Festival: {festival.title()}
- Model: {model}

GENERATION TASK

{task}

Do not include the evaluation rubric in the generation prompt. Keep the prompt separate from human evaluation criteria. Generate one final image only.
"""
    return prompt
