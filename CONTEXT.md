# ARMM Toolkit — Project Context

This file provides context for AI assistants working on this codebase.

## What This Project Is

A Python toolkit that implements the **AI Response Maturity Model (ARMM)** — a framework for scoring and comparing AI SOC (Security Operations Center) solutions by their actual response capabilities and automation depth.

**Framework authors:** Andrei Cotaie, Cristian Miron & Filip Stojkovski
**Original article:** https://www.cybersec-automation.com/p/ai-response-maturity-model
**Official app:** https://armm.secops-unpacked.ai
**Framework version implemented:** 0.1

## What This Toolkit Does

It does NOT evaluate specific vendor products by name. It provides:
1. A scoring engine (Python) that implements ARMM's two scoring modes
2. Pre-populated templates with all 80+ capabilities ready to score
3. A CLI for running evaluations from JSON files
4. Example evaluations using hypothetical products

## Core Concepts

### Two Scoring Modes

**Evaluator Mode** — for comparing products side-by-side:
- Each capability scored: `0` / `1C` / `1G` / `1A` / `2`
- Output: Coverage Rate %, Full Automation Rate %, per-domain tier

**Builder Mode** — for environment-aware roadmapping:
- Each capability scored on 3 axes: T (Trust 1-3) + C (Complexity 1-3) + I (Impact 1-3)
- Action score = T + C + I (range 3-9)
- Same product can score differently based on team maturity and organizational context

### Maturity Tiers
- **Explorer** (3.00–5.99): foundational, low-risk quick wins
- **Entry** (6.00–6.99): stabilized, moderate effort/impact
- **Advanced** (7.00–7.99): mature, high-fidelity reasoning required
- **Expert** (8.00–9.00): critical, VIP/production-critical actions

### Composite Label Logic
Sequential gating: highest tier where ≥4/6 planes qualify, with unbroken chain from Explorer upward.

### Six Domains (planes)
1. Identity (11 actions)
2. Network (13 actions)
3. Endpoint (23 actions)
4. Cloud (15 actions)
5. SaaS (10 actions)
6. General / Usability (22 capabilities)

Equal plane weighting: each contributes exactly 1/6 of the program score.

## File Structure

```
armm/
  capabilities.json   — master data: all actions with IDs, descriptions, reference T/C/I scores
  scorer.py           — scoring engine; EvaluatorEvaluation and BuilderEvaluation classes
  cli.py              — argparse CLI; commands: evaluator, builder, compare
  __init__.py

templates/
  evaluator_template.json   — all actions pre-loaded with score "0", ready to fill
  builder_template.json     — all actions pre-loaded with T=1,C=1,I=1, ready to fill

examples/
  evaluator_example.py      — two hypothetical products compared (BrainBox AI vs AutoSOC Pro)
  builder_example.py        — same product scored by 3 orgs with different context
```

## Design Decisions

- **No external dependencies** — pure Python 3.8+ stdlib only
- **JSON-first** — input/output via JSON for interoperability with other tools
- **Equal plane weighting** is deliberate (matches ARMM spec): prevents high-action-count planes (Endpoint=23) from dominating
- **Composite tier uses sequential gating**, not average score — matches the spec exactly
- **General domain** in Evaluator Mode maps 0/1/2 to the same numeric weights as other domains (0.0, 0.75, 2.0 via 1A approximation) since it uses a slightly different scale in the original framework (0=not available, 1=limited, 2=fully available)

## What to Keep in Mind

- The Full Automation Rate is the KEY metric — high coverage with low automation = guided workflow tool, not autonomous AI
- Builder Mode scores reflect team context, not just product capability
- The framework is v0.1 — capability lists are not exhaustive by design
- Do not add vendor comparisons with real product names without explicit user request
- Always preserve credits to Andrei Cotaie, Cristian Miron & Filip Stojkovski
