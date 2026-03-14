#!/usr/bin/env python3
"""
ARMM CLI - Score AI SOC products using the AI Response Maturity Model.

Usage:
    python -m armm.cli evaluator --input templates/evaluator_template.json
    python -m armm.cli builder   --input templates/builder_template.json
    python -m armm.cli compare   --inputs product_a.json product_b.json

Framework by Andrei Cotaie, Cristian Miron & Filip Stojkovski
"""

import argparse
import json
import sys
from pathlib import Path

from .scorer import (
    BuilderAction, BuilderDomain, BuilderEvaluation,
    EvaluatorAction, EvaluatorDomain, EvaluatorEvaluation,
    ARMMScorer, TIER_ORDER,
)

BANNER = """
╔══════════════════════════════════════════════════════════════╗
║       AI Response Maturity Model (ARMM) - Toolkit v0.1      ║
║  Framework by Andrei Cotaie, Cristian Miron, Filip Stojkovski║
║  https://www.cybersec-automation.com/p/ai-response-maturity-model ║
╚══════════════════════════════════════════════════════════════╝
"""

TIER_ICONS = {
    "Explorer": "🔵",
    "Entry":    "🟡",
    "Advanced": "🟠",
    "Expert":   "🔴",
}


VALID_EVALUATOR_SCORES = {"0", "1", "1C", "1G", "1A", "2"}
VALID_AXIS_RANGE = range(1, 4)  # 1, 2, 3


def load_json(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


def _validate_evaluator_score(score: str, action_id: str) -> str:
    if score not in VALID_EVALUATOR_SCORES:
        raise ValueError(
            f"Invalid score '{score}' for action '{action_id}'. "
            f"Must be one of: {sorted(VALID_EVALUATOR_SCORES)}"
        )
    return score


def _validate_axis(value: int, axis: str, action_id: str) -> int:
    if not isinstance(value, int) or value not in VALID_AXIS_RANGE:
        raise ValueError(
            f"Invalid {axis}={value!r} for action '{action_id}'. Must be an integer 1, 2, or 3."
        )
    return value


def build_evaluator(data: dict) -> EvaluatorEvaluation:
    ev = EvaluatorEvaluation(name=data.get("name", "Unnamed Evaluation"))
    for domain_id, domain_data in data["domains"].items():
        domain = EvaluatorDomain(
            domain_id=domain_id,
            name=domain_data["name"],
        )
        for action_data in domain_data["actions"]:
            action_id = action_data["action_id"]
            domain.actions.append(EvaluatorAction(
                action_id=action_id,
                name=action_data["name"],
                score=_validate_evaluator_score(action_data["score"], action_id),
            ))
        ev.add_domain(domain)
    return ev


def build_builder(data: dict) -> BuilderEvaluation:
    ev = BuilderEvaluation(name=data.get("name", "Unnamed Evaluation"))
    for domain_id, domain_data in data["domains"].items():
        domain = BuilderDomain(
            domain_id=domain_id,
            name=domain_data["name"],
        )
        for action_data in domain_data["actions"]:
            action_id = action_data["action_id"]
            domain.actions.append(BuilderAction(
                action_id=action_id,
                name=action_data["name"],
                T=_validate_axis(action_data["T"], "T", action_id),
                C=_validate_axis(action_data["C"], "C", action_id),
                I=_validate_axis(action_data["I"], "I", action_id),
            ))
        ev.add_domain(domain)
    return ev


def print_evaluator_report(report: dict):
    print(BANNER)
    print(f"  Evaluation : {report['evaluation_name']}")
    print(f"  Mode       : Evaluator")
    print(f"  Composite  : {TIER_ICONS.get(report['composite_tier'], '')} {report['composite_tier']}")
    print(f"  Coverage   : {report['overall_coverage_pct']}%  ({report['total_covered']}/{report['total_actions']} capabilities)")
    print(f"  Automation : {report['overall_automation_pct']}% fully automated")
    print(f"  Score      : {report['overall_score_pct']}% (equal plane-weighted)\n")

    print(f"  {'Domain':<30} {'Covered':>8} {'Auto':>6} {'Score':>8} {'Tier':<12}")
    print(f"  {'-'*30} {'-'*8} {'-'*6} {'-'*8} {'-'*12}")
    for d in report["domains"].values():
        icon = TIER_ICONS.get(d["tier"], "")
        print(
            f"  {d['name']:<30} "
            f"{d['coverage_rate_pct']:>7.1f}% "
            f"{d['automation_rate_pct']:>5.1f}% "
            f"{d['weighted_score_pct']:>7.1f}% "
            f"{icon} {d['tier']}"
        )


def print_builder_report(report: dict):
    print(BANNER)
    print(f"  Evaluation : {report['evaluation_name']}")
    print(f"  Mode       : Builder")
    print(f"  Program    : {report['program_score']:.2f} / 9.00")
    print(f"  Composite  : {TIER_ICONS.get(report['composite_tier'], '')} {report['composite_tier']}\n")

    print(f"  {'Domain':<30} {'Avg Score':>10} {'Tier':<12}")
    print(f"  {'-'*30} {'-'*10} {'-'*12}")
    for d in report["domains"].values():
        icon = TIER_ICONS.get(d["tier"], "")
        print(f"  {d['name']:<30} {d['domain_score']:>9.2f}  {icon} {d['tier']}")


def print_comparison(rows: list[dict]):
    print(BANNER)
    print("  COMPARISON\n")
    for row in rows:
        icon = TIER_ICONS.get(row["composite_tier"], "")
        print(f"  {row['name']}")
        print(f"    Tier  : {icon} {row['composite_tier']}")
        if row["mode"] == "Evaluator":
            print(f"    Score : {row['overall_score_pct']}%  Coverage: {row['coverage_pct']}%  Automation: {row['automation_pct']}%")
        else:
            print(f"    Score : {row['program_score']:.2f}/9.00")
        print()


def cmd_evaluator(args):
    data = load_json(args.input)
    ev = build_evaluator(data)
    report = ev.report()
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_evaluator_report(report)
    if args.output:
        Path(args.output).write_text(json.dumps(report, indent=2))
        print(f"\n  Saved to {args.output}")


def cmd_builder(args):
    data = load_json(args.input)
    ev = build_builder(data)
    report = ev.report()
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_builder_report(report)
    if args.output:
        Path(args.output).write_text(json.dumps(report, indent=2))
        print(f"\n  Saved to {args.output}")


def cmd_compare(args):
    scorer = ARMMScorer()
    for path in args.inputs:
        data = load_json(path)
        mode = data.get("mode", "evaluator").lower()
        if mode == "builder":
            scorer.add(build_builder(data))
        else:
            scorer.add(build_evaluator(data))
    rows = scorer.compare()
    if args.json:
        print(json.dumps(rows, indent=2))
    else:
        print_comparison(rows)


def main():
    parser = argparse.ArgumentParser(
        description="ARMM Toolkit - AI Response Maturity Model scorer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # evaluator
    p_eval = sub.add_parser("evaluator", help="Score a product (0/1C/1G/1A/2 scale)")
    p_eval.add_argument("--input", required=True, help="Path to JSON evaluation file")
    p_eval.add_argument("--output", help="Save report as JSON to this path")
    p_eval.add_argument("--json", action="store_true", help="Print raw JSON output")
    p_eval.set_defaults(func=cmd_evaluator)

    # builder
    p_build = sub.add_parser("builder", help="Score with T+C+I axes (environment-aware)")
    p_build.add_argument("--input", required=True, help="Path to JSON evaluation file")
    p_build.add_argument("--output", help="Save report as JSON to this path")
    p_build.add_argument("--json", action="store_true", help="Print raw JSON output")
    p_build.set_defaults(func=cmd_builder)

    # compare
    p_cmp = sub.add_parser("compare", help="Compare multiple evaluations side-by-side")
    p_cmp.add_argument("--inputs", nargs="+", required=True, help="Paths to evaluation JSON files")
    p_cmp.add_argument("--json", action="store_true", help="Print raw JSON output")
    p_cmp.set_defaults(func=cmd_compare)

    args = parser.parse_args()
    try:
        args.func(args)
    except (KeyError, TypeError, ValueError) as exc:
        print(f"\n  [ERROR] Invalid input: {exc}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError as exc:
        print(f"\n  [ERROR] File not found: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
