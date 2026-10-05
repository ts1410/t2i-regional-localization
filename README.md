# Regional Festival T2I Localization

A research application for evaluating how well Text-to-Image (T2I) image-generation models can localize the same commercial advertising campaign to culturally distinct Indian regional festival contexts.

## Research Question

**Can a T2I model adapt the same commercial campaign to culturally distinct Indian regional festival contexts without producing generic, culturally incoherent, or incorrectly localized imagery?**

## Project Overview

### Hypothesis

T2I models can learn to produce culturally coherent and region-specific advertising visuals when given:
- A clear commercial campaign brief
- A specific regional/festival context
- A product reference image
- An appropriate generation framework

### Pilot Scope

**Regions & Festivals:**
- Bihar — Makar Sankranti
- Gujarat — Uttarayan

**Campaign:**
- **Brand:** Amrit Foods
- **Product:** Sesame & Jaggery Bites
- **Message:** "A little sweetness brings everyone together."

**Required Models (Pilot):**
1. GPT Image 1
2. Gemini 2.5 Flash Image
3. Gemini 3.1 Flash Image Preview

### Project Status

**Current Phase:** Pilot / Exploratory Research

The pilot uses 1–2 generations per model-region combination. After review and feedback, the project will expand to formal human evaluation with 8–10 participants.

## Repository Structure

```
.
├── README.md                               # This file
├── .env.example                            # Environment variables template
├── .gitignore                              # Git ignore rules
│
├── framework/
│   └── T2I_ADVERTISING_CREATIVE_PROJECT_FRAMEWORK.md  # Reusable generation framework
│
├── campaigns/
│   └── REGIONAL_FESTIVAL_CAMPAIGN_PILOT.md  # Campaign brief & regional executions
│
├── references/
│   └── product_reference.jpeg              # Product image (source of truth)
│
├── docs/
│   ├── methodology.md                      # Research methodology explanation
│   ├── experiment-protocol.md              # Experiment execution protocol
│   └── evaluation-rubric.md                # [DRAFT] Evaluation dimensions
│
├── backend/                                # Python Flask API
│   ├── app.py                              # Main application
│   ├── config.py                           # Configuration
│   ├── models.py                           # Database models
│   ├── database.py                         # Database initialization
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── project.py                      # Project metadata endpoints
│   │   ├── experiments.py                  # Experiment CRUD
│   │   ├── generation.py                   # Generation orchestration
│   │   └── evaluation.py                   # Evaluation endpoints
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── prompt_builder.py               # Prompt construction from Markdown
│   │   ├── version_manager.py              # Framework/campaign versioning
│   │   └── experiment_logger.py            # Metadata logging
│   │
│   ├── providers/
│   │   ├── __init__.py
│   │   ├── base.py                         # Abstract provider interface
│   │   ├── openai_provider.py              # GPT Image 1 integration
│   │   └── google_provider.py              # Gemini models integration
│   │
│   └── utils/
│       ├── __init__.py
│       ├── file_utils.py                   # File reading helpers
│       └── error_messages.py               # User-friendly error strings
│
├── frontend/                               # React + TypeScript
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── index.tsx
│   │   ├── App.tsx
│   │   │
│   │   ├── pages/
│   │   │   ├── Overview.tsx                # Project overview
│   │   │   ├── Methodology.tsx             # Research methodology
│   │   │   ├── Campaign.tsx                # Campaign brief + reference
│   │   │   ├── ExperimentSetup.tsx         # Model/region selection
│   │   │   ├── Generate.tsx                # Generation interface
│   │   │   ├── Results.tsx                 # Results & comparison
│   │   │   ├── Evaluation.tsx              # Human evaluation interface
│   │   │   └── ExperimentLog.tsx           # Metadata viewer
│   │   │
│   │   ├── components/
│   │   │   ├── Navigation.tsx              # Main navigation
│   │   │   ├── ExperimentCard.tsx          # Result card component
│   │   │   ├── ComparisonView.tsx          # Image comparison
│   │   │   └── MetadataViewer.tsx          # Experiment details
│   │   │
│   │   ├── services/
│   │   │   └── api.ts                      # API client
│   │   │
│   │   ├── styles/
│   │   │   └── index.css                   # Global styles
│   │   │
│   │   └── types/
│   │       └── index.ts                    # TypeScript types
│   │
│   ├── package.json
│   ├── tsconfig.json
│   └── .env.example
│
├── experiments/                            # Experiment metadata & logs
│   └── .gitkeep
│
├── outputs/                                # Generated images (local, not committed)
│   └── .gitkeep
│
├── scripts/
│   ├── init_db.py                          # Initialize database
│   └── reset_db.py                         # Reset database (dev only)
│
└── requirements.txt                        # Python dependencies
```

## Quick Start

### Prerequisites

- Python 3.9+
- Node.js 16+ (for frontend)
- At least one of: OpenAI API key, Google API key

### Backend Setup

**1. Create virtual environment:**

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

**2. Install dependencies:**

```bash
pip install -r requirements.txt
```

**3. Configure environment variables:**

```bash
cp .env.example .env
# Edit .env and add your API keys
```

**4. Initialize database:**

```bash
python scripts/init_db.py
```

**5. Start backend:**

```bash
python backend/app.py
```

Backend will run on `http://localhost:5000`

### Frontend Setup

**1. Navigate to frontend directory:**

```bash
cd frontend
```

**2. Install dependencies:**

```bash
npm install
```

**3. Configure environment (optional):**

```bash
cp .env.example .env.local
# Defaults to http://localhost:5000
```

**4. Start development server:**

```bash
npm start
```

Frontend will open at `http://localhost:3000`

## Application Workflow

### Research Workflow

1. **Overview** — Understand the project hypothesis and pilot scope
2. **Methodology** — Review research design and controlled variables
3. **Campaign** — Review the campaign brief and product reference image
4. **Experiment Setup** — Select model, region, and festival
5. **Generate** — Execute generation with logged metadata
6. **Results** — View outputs and compare regions/models
7. **Evaluation** — (Later) Collect participant ratings and feedback
8. **Experiment Log** — Review historical metadata and reproducibility

### Key Principles

**Experimental Control:**
- Framework, campaign brief, and product reference are identical across models
- Only the model and region/festival context change
- Every generation is tracked with reproducible metadata

**Separation of Concerns:**
- Generation instructions (framework) are separate from evaluation criteria
- Evaluation rubric does not appear in the generation prompt
- Pilot results are explicitly marked as exploratory, not conclusive

**No Fabricated Results:**
- If an API is not configured, the app shows "Provider not configured"
- No mock generations are produced
- No synthetic evaluation data is created
- The app truthfully reflects what was actually generated

## Project Documents

### Framework

See: `framework/T2I_ADVERTISING_CREATIVE_PROJECT_FRAMEWORK.md`

This is the reusable, model-independent instruction layer for creating commercial advertising images. It defines:
- Role (advertising production expert)
- Core objective (balancing campaign fidelity, reference fidelity, context, and quality)
- Creative interpretation guidelines
- Commercial photography standards
- Reference asset preservation
- Cultural context handling
- What not to do

### Campaign Brief

See: `campaigns/REGIONAL_FESTIVAL_CAMPAIGN_PILOT.md`

This specifies:
- Brand and product
- Campaign idea and objective
- Target audience
- Creative format
- Regional executions (Bihar/Gujarat)
- Festivals (Makar Sankranti/Uttarayan)
- Product reference

### Product Reference

See: `references/product_reference.jpeg`

This is the source-of-truth image for the product and packaging. The model must preserve its identity and visual characteristics.

## Backend API Reference

### Project Metadata

```
GET /api/project
```

Returns project overview, hypothesis, pilot scope, and current status.

### Framework & Campaign

```
GET /api/framework
GET /api/campaign
```

Returns the raw Markdown content and version hashes.

### Models & Regions

```
GET /api/models
GET /api/regions
```

Returns available models and regional configurations.

### Experiments

```
GET  /api/experiments                    # List all experiments
GET  /api/experiments/:id                # Get single experiment
POST /api/experiments                    # Create new experiment
GET  /api/results                        # List results with images
GET  /api/results/:id                    # Get single result
```

### Generation

```
POST /api/generate                       # Trigger generation
GET  /api/generate/:id/status            # Check generation status
```

Payload example:

```json
{
  "model": "gpt-image-1",
  "region": "bihar",
  "festival": "makar-sankranti",
  "experiment_id": "exp-001"
}
```

### Evaluation

```
GET  /api/evaluation/rubric              # Get evaluation criteria
POST /api/evaluation                     # Submit participant rating
GET  /api/evaluation/results             # Get aggregated results
```

## Experiment Metadata

Every generation records:

```json
{
  "experiment_id": "exp-20261005-001",
  "timestamp": "2026-10-05T14:30:00Z",
  "model": "gpt-image-1",
  "model_version": "1.0",
  "region": "bihar",
  "festival": "makar-sankranti",
  "framework_version": "1.0",
  "framework_hash": "sha256:...",
  "campaign_version": "1.0",
  "campaign_hash": "sha256:...",
  "reference_image_hash": "sha256:...",
  "prompt_version": "1.0",
  "generation_parameters": {
    "size": "1536x1024",
    "quality": "high"
  },
  "output_path": "outputs/gpt-image-1_bihar_20261005_143000.png",
  "status": "success",
  "error": null
}
```

This enables reproducibility: any historical experiment can be re-run with the exact same inputs and compare outputs.

## Human Evaluation

### Participant IDs

Participants are identified anonymously:

```
P01, P02, ..., P10
```

No personally identifiable information is collected unless explicitly consented.

### Evaluation Workflow (Future)

1. **Participant Login** — Enter participant ID (P01–P10)
2. **View Image** — See generated image with campaign/model/region context
3. **Rate Criteria** — Answer evaluation questions (to be finalized)
4. **Optional Comment** — Provide qualitative feedback
5. **Submit** — Record response with timestamp

### Evaluation Rubric

See: `docs/evaluation-rubric.md` (currently a DRAFT placeholder)

Potential dimensions:
- **Regional Cultural Specificity** — How much does the image reflect the specific region/festival?
- **Cultural Coherence** — Do all visual elements make sense together culturally?
- **Campaign Fidelity** — Does the image communicate the campaign message?
- **Product Fidelity** — Is the product accurate and recognizable?
- **Commercial Quality** — Is it suitable for use as advertising?
- **Overall Usefulness** — Would this image work for the advertiser?

These are **placeholders only** and will be finalized based on researcher feedback.

## Version Control & Reproducibility

### Hashing Strategy

The application calculates SHA-256 hashes for:
- Framework Markdown file
- Campaign brief Markdown file
- Product reference image

These hashes are stored with each experiment.

**Why?** If any source document changes, the hash changes. This makes it clear that subsequent experiments used a new version.

### Historical Preservation

Experiment metadata is never overwritten. Each run creates a new record with a unique experiment ID and timestamp.

**Query Example:**

"Show me all generations using framework v1.0 and campaign v1.0 for Bihar"

## Configuration

### Adding a New Model

1. Create a provider in `backend/providers/` (e.g., `anthropic_provider.py`)
2. Implement the `ImageGenerationProvider` interface
3. Add configuration to `backend/config.py`
4. Update `/api/models` endpoint
5. **Do not** hardcode model names throughout the app

### Adding a New Region/Festival

1. Update `campaigns/REGIONAL_FESTIVAL_CAMPAIGN_PILOT.md` with the regional execution
2. The frontend dynamically reads regions from campaign data
3. Update `/api/regions` endpoint if needed

## Security & Best Practices

### API Keys

✅ **Do:** Store API keys in `.env` file (never committed)
✅ **Do:** Pass API keys only to backend, never expose to browser
✅ **Do:** Show "Provider not configured" if key is missing

❌ **Don't:** Hardcode API keys in code
❌ **Don't:** Log or print API keys
❌ **Don't:** Send API keys to frontend

### Generated Images

✅ **Do:** Store in `outputs/` directory
✅ **Do:** Track paths in experiment metadata
✅ **Do:** Allow local export/download

❌ **Don't:** Commit generated images to Git (use `.gitignore`)
❌ **Don't:** Assume cloud storage without explicit configuration

### Research Integrity

✅ **Do:** Keep generation instructions separate from evaluation rubric
✅ **Do:** Preserve experiment versions for reproducibility
✅ **Do:** Mark pilot results as exploratory (not conclusive)
✅ **Do:** Show honest results (no fabricated generations)

❌ **Don't:** Optimize prompts after seeing output (without versioning)
❌ **Don't:** Claim one model is "better" without evaluation data
❌ **Don't:** Generate synthetic findings or mock results

## Troubleshooting

### "Provider not configured"

**Cause:** API key not set in `.env`

**Solution:**
1. Copy `.env.example` to `.env`
2. Add your API key
3. Restart backend: `python backend/app.py`

### Database locked (SQLite)

**Cause:** Multiple processes accessing database simultaneously

**Solution:** Only run one backend instance. Use `scripts/reset_db.py` if needed (development only).

### CORS errors

**Cause:** Frontend and backend not aligned

**Solution:** Ensure backend runs on `:5000` and frontend on `:3000`

### "Reference image not found"

**Cause:** `references/product_reference.jpeg` missing or moved

**Solution:** Ensure the file exists at the expected path.

## Development Notes

### Testing the Generation Workflow

```bash
# 1. Ensure .env has OPENAI_API_KEY or GOOGLE_API_KEY set
# 2. Start backend
python backend/app.py

# 3. In another terminal, start frontend
cd frontend
npm start

# 4. Navigate to http://localhost:3000
# 5. Go through: Overview → Methodology → Campaign → Experiment Setup → Generate
```

### Database Schema

The application uses SQLite with these main tables:

- **experiments** — Experiment metadata
- **results** — Generated images and outputs
- **evaluations** — Participant ratings and feedback
- **versions** — Version hashes for framework/campaign/references

Schema is auto-created on first run by `scripts/init_db.py`.

### Logging

Backend logs are written to `backend.log`. Check this file for:
- API call details
- Generation status
- Error tracebacks
- Prompt construction debug info

### Extending the Rubric

1. Edit `docs/evaluation-rubric.md`
2. Update evaluation questions in `backend/config.py`
3. Modify `/api/evaluation/rubric` endpoint
4. Update frontend evaluation form (`Evaluation.tsx`)

## Future Roadmap

- [ ] Finalize human evaluation rubric
- [ ] Recruit 8–10 evaluation participants
- [ ] Collect and aggregate participant ratings
- [ ] Add statistical analysis dashboard
- [ ] Expand to 4 regions (Uttar Pradesh, Tamil Nadu)
- [ ] Compare all required models (GPT, Gemini 2.5, Gemini 3.1)
- [ ] Export findings as research report
- [ ] Optional cloud storage integration

## License

This research application is provided as-is for academic and commercial use. Research findings should be cited appropriately.

## Contact

For questions about the research methodology, contact the project lead.

---

**This application is designed to support reproducible, transparent research on T2I model localization. Use it to preserve experimental control, maintain version history, and separate research generation from evaluation.**
