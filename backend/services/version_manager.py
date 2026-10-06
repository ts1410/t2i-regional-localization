import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def sha256_for_file(path):
    path = Path(path)
    if not path.exists():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def get_version_info():
    framework_path = ROOT / "framework" / "T2I_ADVERTISING_CREATIVE_PROJECT_FRAMEWORK.md"
    campaign_path = ROOT / "campaigns" / "REGIONAL_FESTIVAL_CAMPAIGN_PILOT.md"
    reference_path = ROOT / "Product_reference.jpeg"
    
    if not framework_path.exists():
        framework_path = ROOT / "Framework.md"
    if not campaign_path.exists():
        campaign_path = ROOT / "Campaign_pilot.md"
    if not reference_path.exists():
        reference_path = ROOT / "references" / "product_reference.png"

    return {
        "framework_version": "v1",
        "campaign_version": "v1",
        "reference_version": "v1",
        "framework_hash": sha256_for_file(framework_path),
        "campaign_hash": sha256_for_file(campaign_path),
        "reference_image_hash": sha256_for_file(reference_path),
    }
