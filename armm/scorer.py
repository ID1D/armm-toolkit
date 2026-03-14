"""
ARMM Scoring Engine - Evaluator Mode and Builder Mode.

Framework by Andrei Cotaie, Cristian Miron & Filip Stojkovski
Reference: https://www.cybersec-automation.com/p/ai-response-maturity-model
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal
from statistics import mean

# ── Tier thresholds (Builder Mode action scores, range 3–9) ─────────────────
TIERS = {
    "Explorer":  (3.0, 5.99),
    "Entry":     (6.0, 6.99),
    "Advanced":  (7.0, 7.99),
    "Expert":    (8.0, 9.0),
}

TIER_ORDER = ["Explorer", "Entry", "Advanced", "Expert"]

# Evaluator Mode sub-level numeric weights (for optional score aggregation)
EVALUATOR_WEIGHTS = {
    "0":  0.0,
    "1":  1.0,   # General domain uses plain "1" (available but limited)
    "1C": 0.5,
    "1G": 1.0,
    "1A": 1.5,
    "2":  2.0,
}

EvaluatorScore = Literal["0", "1", "1C", "1G", "1A", "2"]


def score_to_tier(score: float) -> str:
    for tier, (lo, hi) in TIERS.items():
        if lo <= score <= hi:
            return tier
    return "Unscored"


# ── Builder Mode ─────────────────────────────────────────────────────────────

@dataclass
class BuilderAction:
    action_id: str
    name: str
    T: int  # Trust:      1-3
    C: int  # Complexity: 1-3
    I: int  # Impact:     1-3

    @property
    def score(self) -> int:
        return self.T + self.C + self.I

    @property
    def tier(self) -> str:
        return score_to_tier(self.score)

    def to_dict(self) -> dict:
        return {
            "action_id": self.action_id,
            "name": self.name,
            "T": self.T,
            "C": self.C,
            "I": self.I,
            "score": self.score,
            "tier": self.tier,
        }


@dataclass
class BuilderDomain:
    domain_id: str
    name: str
    actions: list[BuilderAction] = field(default_factory=list)

    @property
    def domain_score(self) -> float:
        if not self.actions:
            return 0.0
        return mean(a.score for a in self.actions)

    @property
    def tier(self) -> str:
        return score_to_tier(self.domain_score)

    def to_dict(self) -> dict:
        return {
            "domain_id": self.domain_id,
            "name": self.name,
            "domain_score": round(self.domain_score, 2),
            "tier": self.tier,
            "actions": [a.to_dict() for a in self.actions],
        }


class BuilderEvaluation:
    """Builder Mode: environment-aware scoring (T + C + I per action)."""

    def __init__(self, name: str = "My Evaluation"):
        self.name = name
        self.domains: dict[str, BuilderDomain] = {}

    def add_domain(self, domain: BuilderDomain):
        self.domains[domain.domain_id] = domain

    @property
    def program_score(self) -> float:
        """Arithmetic mean of all domain scores (equal plane weighting)."""
        if not self.domains:
            return 0.0
        return mean(d.domain_score for d in self.domains.values())

    @property
    def composite_tier(self) -> str:
        """
        Sequential gating: highest tier where >= 4 of 6 planes qualify,
        with unbroken chain from Explorer upward.
        """
        domain_tiers = [d.tier for d in self.domains.values()]
        composite = "Explorer"
        for tier in TIER_ORDER:
            tier_idx = TIER_ORDER.index(tier)
            qualifying = sum(
                1 for t in domain_tiers
                if TIER_ORDER.index(t) >= tier_idx
            )
            if qualifying >= 4:
                composite = tier
            else:
                break
        return composite

    def report(self) -> dict:
        return {
            "evaluation_name": self.name,
            "mode": "Builder",
            "program_score": round(self.program_score, 2),
            "composite_tier": self.composite_tier,
            "domains": {k: v.to_dict() for k, v in self.domains.items()},
        }


# ── Evaluator Mode ───────────────────────────────────────────────────────────

@dataclass
class EvaluatorAction:
    action_id: str
    name: str
    score: EvaluatorScore  # "0", "1C", "1G", "1A", "2"

    @property
    def is_covered(self) -> bool:
        return self.score != "0"

    @property
    def is_fully_automated(self) -> bool:
        return self.score == "2"

    @property
    def numeric(self) -> float:
        return EVALUATOR_WEIGHTS[self.score]

    def to_dict(self) -> dict:
        return {
            "action_id": self.action_id,
            "name": self.name,
            "score": self.score,
            "covered": self.is_covered,
            "fully_automated": self.is_fully_automated,
        }


@dataclass
class EvaluatorDomain:
    domain_id: str
    name: str
    actions: list[EvaluatorAction] = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.actions)

    @property
    def covered(self) -> int:
        return sum(1 for a in self.actions if a.is_covered)

    @property
    def fully_automated(self) -> int:
        return sum(1 for a in self.actions if a.is_fully_automated)

    @property
    def coverage_rate(self) -> float:
        return (self.covered / self.total * 100) if self.total else 0.0

    @property
    def automation_rate(self) -> float:
        return (self.fully_automated / self.total * 100) if self.total else 0.0

    @property
    def weighted_score(self) -> float:
        """Normalized score 0–100 based on numeric weights."""
        if not self.actions:
            return 0.0
        return mean(a.numeric for a in self.actions) / 2.0 * 100

    @property
    def tier(self) -> str:
        """Map coverage/automation to tier for cross-product comparison."""
        ws = self.weighted_score
        if ws >= 80:
            return "Expert"
        elif ws >= 65:
            return "Advanced"
        elif ws >= 40:
            return "Entry"
        else:
            return "Explorer"

    def to_dict(self) -> dict:
        return {
            "domain_id": self.domain_id,
            "name": self.name,
            "total_actions": self.total,
            "covered": self.covered,
            "fully_automated": self.fully_automated,
            "coverage_rate_pct": round(self.coverage_rate, 1),
            "automation_rate_pct": round(self.automation_rate, 1),
            "weighted_score_pct": round(self.weighted_score, 1),
            "tier": self.tier,
            "actions": [a.to_dict() for a in self.actions],
        }


class EvaluatorEvaluation:
    """Evaluator Mode: side-by-side product comparison on 0/1C/1G/1A/2 scale."""

    def __init__(self, name: str = "Product Evaluation"):
        self.name = name
        self.domains: dict[str, EvaluatorDomain] = {}

    def add_domain(self, domain: EvaluatorDomain):
        self.domains[domain.domain_id] = domain

    @property
    def total_actions(self) -> int:
        return sum(d.total for d in self.domains.values())

    @property
    def total_covered(self) -> int:
        return sum(d.covered for d in self.domains.values())

    @property
    def total_automated(self) -> int:
        return sum(d.fully_automated for d in self.domains.values())

    @property
    def overall_coverage_pct(self) -> float:
        return (self.total_covered / self.total_actions * 100) if self.total_actions else 0.0

    @property
    def overall_automation_pct(self) -> float:
        return (self.total_automated / self.total_actions * 100) if self.total_actions else 0.0

    @property
    def overall_score_pct(self) -> float:
        """Equal plane-weighted score."""
        if not self.domains:
            return 0.0
        return mean(d.weighted_score for d in self.domains.values())

    @property
    def composite_tier(self) -> str:
        domain_tiers = [d.tier for d in self.domains.values()]
        composite = "Explorer"
        for tier in TIER_ORDER:
            tier_idx = TIER_ORDER.index(tier)
            qualifying = sum(
                1 for t in domain_tiers
                if TIER_ORDER.index(t) >= tier_idx
            )
            if qualifying >= 4:
                composite = tier
            else:
                break
        return composite

    def report(self) -> dict:
        return {
            "evaluation_name": self.name,
            "mode": "Evaluator",
            "overall_score_pct": round(self.overall_score_pct, 1),
            "overall_coverage_pct": round(self.overall_coverage_pct, 1),
            "overall_automation_pct": round(self.overall_automation_pct, 1),
            "composite_tier": self.composite_tier,
            "total_actions": self.total_actions,
            "total_covered": self.total_covered,
            "total_fully_automated": self.total_automated,
            "domains": {k: v.to_dict() for k, v in self.domains.items()},
        }


# ── Convenience: compare multiple Evaluator reports ─────────────────────────

class ARMMScorer:
    """
    Top-level comparison helper.

    Usage:
        scorer = ARMMScorer()
        scorer.add(eval_a)
        scorer.add(eval_b)
        print(scorer.compare())
    """

    def __init__(self):
        self.evaluations: list[EvaluatorEvaluation | BuilderEvaluation] = []

    def add(self, evaluation: EvaluatorEvaluation | BuilderEvaluation):
        self.evaluations.append(evaluation)

    def compare(self) -> list[dict]:
        rows = []
        for ev in self.evaluations:
            report = ev.report()
            row = {
                "name": report["evaluation_name"],
                "mode": report["mode"],
                "composite_tier": report["composite_tier"],
            }
            if report["mode"] == "Evaluator":
                row["overall_score_pct"] = report["overall_score_pct"]
                row["coverage_pct"] = report["overall_coverage_pct"]
                row["automation_pct"] = report["overall_automation_pct"]
            else:
                row["program_score"] = report["program_score"]
            rows.append(row)
        return rows
