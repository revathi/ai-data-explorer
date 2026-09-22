# Lovable pitch package — version 5

Upload `LOVABLE_PITCH_SCRIPT.md` and diagrams **01, 03 and 04** from `assets/` to Lovable. Diagram 01 also has an animated GIF. Use the existing **66-second prototype video** from 00:57 to 02:03. The total target is 178 seconds, following the workshop's seven-section order. Older 40-second timing instructions are superseded.

Suggested instruction to Lovable:

> Create the remaining pitch around the existing 66-second prototype video, following LOVABLE_PITCH_SCRIPT.md. Preserve the demo at normal speed from 00:57 to 02:03; do not rebuild it or invent results. Follow the seven sections: hook, problem and value, solution and innovation, demonstration, impact, credibility/risks/safeguards, and close. Use the supplied diagrams with animated highlights. Keep the total at 2:58, including transitions. Preserve navy/orange styling, professional English narration and subtle music. Inspect the demo's audio before mixing so narration and music do not overlap. If the demo file is not yet available, prepare the surrounding 112 seconds and reserve its exact 66-second slot. Use diagrams 01, 03 and 04; do not add a second safeguards slide or product owner section.

## Files

- `LOVABLE_PITCH_SCRIPT.md`: fresh 178-second script and complete production instructions.
- `assets/01-system-architecture.png` and `.svg`: simplified four-layer design with user question/response loop; read-only execution appears in the Data & Audit layer.
- `assets/01-system-architecture-animated.gif`: 16.8-second looping walkthrough. Retime its stages to fit the architecture narration in the video.
- `assets/02-trust-boundaries.png` and `.svg`: earlier reference; use diagram 04 instead in the pitch.
- `assets/03-portability-and-extensions.png` and `.svg`: portable core, replaceable adapters and future schema RAG/agent/prediction extensions.
- `assets/04-human-oversight-and-guardrails.png` and `.svg`: the current Credibility, Risks & Safeguards visual, distinguishing routine, exceptional and unsafe queries.
- `create_guardrails_image.py`: generates diagram 04.
- `generate_diagrams.py`: base drawing source using Pillow, with editable vector output. Run `animate_simple_architecture.py` afterwards to apply the simplified architecture and generate its GIF.

These are original code-drawn diagrams retaining the layer and symbol approach discussed with the project owner. They are not edits of the video creator's screenshot. No new video is included in this package.
