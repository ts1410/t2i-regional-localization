# Regional Festival T2I Localization

## Research Question

Can a T2I model adapt the same commercial campaign to culturally distinct Indian regional festival contexts without producing generic, culturally incoherent, or incorrectly localized imagery?

## Hypothesis

T2I models can learn to produce culturally coherent and region-specific advertising visuals when given a clear campaign brief, a specific regional/festival context, a product reference image, and a disciplined generation framework.

## Pilot Scope

This project is exploratory. The initial pilot compares two regional executions and keeps generation variables controlled.

- Bihar — Makar Sankranti
- Gujarat — Uttarayan

Required models for the formal evaluation are:

1. GPT Image 1
2. Gemini 2.5 Flash Image
3. Gemini 3.1 Flash Image Preview

Additional models may be explored only as optional comparators and must not silently enter the required evaluation set.

## Research Methodology

The application documents the separation between research design, generation instructions, and human evaluation. The pilot is exploratory, and the final human evaluation will use 8–10 participants.

Controlled variables:

- Same campaign brief
- Same product reference image
- Same prompt framework
- Same brand and campaign objective
- Same generation task structure

Variable regional context:

- Bihar / Makar Sankranti
- Gujarat / Uttarayan

Model comparison:

- Model is the primary variable for controlled comparison.
- Results should not be used as definitive rankings until evaluation data exists.

Reference-image usage:

- The product reference is treated as the source of truth for packaging and product identity.

Generation protocol:

- Prompt is constructed from the framework and campaign brief.
- Only regional execution changes between experiments.

Human evaluation:

- Separate from generation instructions.
- Evaluation rubric is stored in docs/evaluation-rubric.md as a draft and remains editable.

Limitations:

- This is a pilot and is not statistically conclusive.
- Full formal evaluation is deferred until the method is reviewed.

## Campaign Summary

Brand: Amrit Foods
Product: Sesame & Jaggery Bites
Campaign idea: “A little sweetness brings everyone together.”
Campaign objective: Create a warm, festive advertising visual that connects the product with sharing, family, community, and celebration.
Target audience: Indian families and young adults.
