# Lovable pitch package — version 5

Upload `LOVABLE_PITCH_SCRIPT.md` and diagrams **01, 03 and 04** from `assets/` to Lovable. Diagram 01 also has an animated GIF. Add your silent 40-second prototype clip when ready. SVG versions are included for editing and animation. The total target is 178 seconds, including the impact section for customer experience and productivity.

Suggested instruction to Lovable:

> Create the complete pitch video following the attached LOVABLE_PITCH_SCRIPT.md. First capture the existing prototype's business conversation and query-history flow as a 40-second demo for 00:29–01:09. Use the actual question and answer, followed by authorised DevOps query history. Do not rebuild the prototype or invent results. Use the attached architecture diagrams as separate scene assets and animate their highlights. Follow the script's narration, order and timing, adjusting the spoken result only to match the actual captured answer. Preserve the navy/orange style, use one professional British English narration voice and subtle music, and keep the final export below three minutes. Do not add product owner or business-overview scenes, vendor branding or unverified functionality. If recording the prototype is unavailable, prepare the other scenes and ask me to supply a silent 40-second screen recording.

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
