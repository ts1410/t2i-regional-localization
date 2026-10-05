import base64
from openai import OpenAI

client = OpenAI()

# Read framework
with open("Framework.md", "r", encoding="utf-8") as f:
    framework = f.read()

# Read campaign brief
with open("Campaign_pilot.md", "r", encoding="utf-8") as f:
    campaign = f.read()

# Read product image
with open("Product_reference.jpeg", "rb") as f:
    image_data = base64.b64encode(f.read()).decode("utf-8")

prompt = f"""
PROJECT FRAMEWORK:
{framework}

CAMPAIGN BRIEF:
{campaign}

TASK:
Generate the Bihar — Makar Sankranti execution described in the campaign brief.

Use the supplied product reference image as the reference for the product and packaging.

Generate one final photorealistic commercial advertising image.
"""

result = client.images.generate(
    model="gpt-image-1",
    prompt=prompt,
    size="1536x1024",
    quality="high",
)

image_base64 = result.data[0].b64_json

with open("outputs/gpt-image-1_bihar.png", "wb") as f:
    f.write(base64.b64decode(image_base64))