"""
Example: Builder Mode - Environment-aware scoring with T+C+I axes.

This demonstrates how the same AI SOC product can score differently
depending on team maturity, organizational context, and asset criticality.

Framework by Andrei Cotaie, Cristian Miron & Filip Stojkovski
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from armm.scorer import BuilderAction, BuilderDomain, BuilderEvaluation

# ─────────────────────────────────────────────────────────────────────────────
# Scenario: Three organizations evaluating the same AI SOC product,
# scoring the Identity Response Plane with their own context.
# ─────────────────────────────────────────────────────────────────────────────

# Axis reference:
# T (Trust):      1=Enrichment only, 2=Validated (human confirms), 3=Autonomous
# C (Complexity): 1=Low (simple API), 2=Medium (multi-step), 3=High (complex)
# I (Impact):     1=Low (tagging), 2=Medium (disruption), 3=High (prod/critical)

IDENTITY_ACTIONS_ORG_A = [
    # Mature program, skilled team — high trust, low complexity, standard impact
    BuilderAction("reset_password_std",       "Reset Password (Std)",         T=3, C=1, I=2),
    BuilderAction("revoke_sessions",          "Revoke Sessions",              T=3, C=1, I=1),
    BuilderAction("disable_user",             "Disable User",                 T=3, C=1, I=2),
    BuilderAction("disable_service_principal","Disable Service Principals",   T=2, C=2, I=3),
    BuilderAction("remove_permissions",       "Remove Permissions",           T=2, C=2, I=3),
    BuilderAction("group_adherence",          "Group Adherence",              T=3, C=1, I=1),
    BuilderAction("group_creation",           "Group Creation",               T=3, C=2, I=2),
    BuilderAction("token_rotation",           "Token Rotation (Prod)",        T=2, C=3, I=3),
    BuilderAction("delete_sharing_perms",     "Delete Sharing Permissions",   T=2, C=2, I=2),
    BuilderAction("label_user",               "Label User (Tagging)",         T=3, C=1, I=1),
    BuilderAction("reset_password_vip",       "Reset Password (VIP)",         T=3, C=2, I=3),
]

IDENTITY_ACTIONS_ORG_B = [
    # New program, junior team — lower trust, higher complexity for same actions
    BuilderAction("reset_password_std",       "Reset Password (Std)",         T=1, C=2, I=2),
    BuilderAction("revoke_sessions",          "Revoke Sessions",              T=1, C=2, I=1),
    BuilderAction("disable_user",             "Disable User",                 T=1, C=2, I=2),
    BuilderAction("disable_service_principal","Disable Service Principals",   T=1, C=3, I=3),
    BuilderAction("remove_permissions",       "Remove Permissions",           T=1, C=3, I=3),
    BuilderAction("group_adherence",          "Group Adherence",              T=1, C=2, I=1),
    BuilderAction("group_creation",           "Group Creation",               T=1, C=3, I=2),
    BuilderAction("token_rotation",           "Token Rotation (Prod)",        T=1, C=3, I=3),
    BuilderAction("delete_sharing_perms",     "Delete Sharing Permissions",   T=1, C=2, I=2),
    BuilderAction("label_user",               "Label User (Tagging)",         T=2, C=1, I=1),
    BuilderAction("reset_password_vip",       "Reset Password (VIP)",         T=1, C=3, I=3),
]

IDENTITY_ACTIONS_ORG_C = [
    # High-risk environment, manual-first culture — conservative trust, elevated impact
    BuilderAction("reset_password_std",       "Reset Password (Std)",         T=2, C=1, I=3),
    BuilderAction("revoke_sessions",          "Revoke Sessions",              T=2, C=1, I=2),
    BuilderAction("disable_user",             "Disable User",                 T=2, C=1, I=3),
    BuilderAction("disable_service_principal","Disable Service Principals",   T=1, C=2, I=3),
    BuilderAction("remove_permissions",       "Remove Permissions",           T=1, C=2, I=3),
    BuilderAction("group_adherence",          "Group Adherence",              T=2, C=1, I=2),
    BuilderAction("group_creation",           "Group Creation",               T=2, C=2, I=3),
    BuilderAction("token_rotation",           "Token Rotation (Prod)",        T=1, C=3, I=3),
    BuilderAction("delete_sharing_perms",     "Delete Sharing Permissions",   T=1, C=2, I=3),
    BuilderAction("label_user",               "Label User (Tagging)",         T=3, C=1, I=1),
    BuilderAction("reset_password_vip",       "Reset Password (VIP)",         T=1, C=2, I=3),
]


def build_org_evaluation(name: str, identity_actions: list) -> BuilderEvaluation:
    ev = BuilderEvaluation(name=name)
    ev.add_domain(BuilderDomain("identity", "Identity Response Plane", actions=identity_actions))
    return ev


def print_builder_report(ev: BuilderEvaluation):
    r = ev.report()
    tier_icons = {"Explorer": "[Explorer]", "Entry": "[Entry]", "Advanced": "[Advanced]", "Expert": "[Expert]"}
    print(f"\n{'='*65}")
    print(f"  {r['evaluation_name']}")
    print(f"  Program Score : {r['program_score']:.2f}/9.00   "
          f"Composite: {tier_icons.get(r['composite_tier'], '')} {r['composite_tier']}")
    print()
    for d in r["domains"].values():
        print(f"  {d['name']}")
        print(f"  {'Action':<35} {'T':>3} {'C':>3} {'I':>3} {'Score':>6} {'Tier'}")
        print(f"  {'-'*60}")
        for a in d["actions"]:
            icon = tier_icons.get(a["tier"], "")
            print(
                f"  {a['name']:<35} {a['T']:>3} {a['C']:>3} {a['I']:>3} "
                f"{a['score']:>6}  {icon} {a['tier']}"
            )


if __name__ == "__main__":
    print("\nARMM Builder Mode - Context-Aware Scoring Demo")
    print("Framework by Andrei Cotaie, Cristian Miron & Filip Stojkovski")
    print("\nSame product, same capabilities, different organizational context:\n")
    print("  Org A: Mature program / Expert engineering team")
    print("  Org B: New program / Junior team")
    print("  Org C: High-risk environment / Manual-first culture")

    org_a = build_org_evaluation("Org A - Mature Program", IDENTITY_ACTIONS_ORG_A)
    org_b = build_org_evaluation("Org B - New Program (Junior Team)", IDENTITY_ACTIONS_ORG_B)
    org_c = build_org_evaluation("Org C - High-Risk / Manual-First", IDENTITY_ACTIONS_ORG_C)

    print_builder_report(org_a)
    print_builder_report(org_b)
    print_builder_report(org_c)

    print(f"\n{'='*65}")
    print("  CONCLUSION:")
    scores = [
        (org_a.name, org_a.domains["identity"].domain_score, org_a.domains["identity"].tier),
        (org_b.name, org_b.domains["identity"].domain_score, org_b.domains["identity"].tier),
        (org_c.name, org_c.domains["identity"].domain_score, org_c.domains["identity"].tier),
    ]
    tier_icons = {"Explorer": "[Explorer]", "Entry": "[Entry]", "Advanced": "[Advanced]", "Expert": "[Expert]"}
    for name, score, tier in scores:
        print(f"  {name}: {score:.2f} -> {tier_icons.get(tier, '')} {tier}")
    print()
    print("  The product capability is identical. The score reflects organizational reality.")
    print("  Builder Mode answers: 'Where should MY team invest to move up the maturity ladder?'")
