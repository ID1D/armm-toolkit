"""
Example: Evaluator Mode - Compare two hypothetical AI SOC products.

This shows how to use the ARMM toolkit programmatically to compare
products on the 0/1C/1G/1A/2 scale.

Framework by Andrei Cotaie, Cristian Miron & Filip Stojkovski
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from armm.scorer import EvaluatorAction, EvaluatorDomain, EvaluatorEvaluation

TIER_ICONS = {"Explorer": "[Explorer]", "Entry": "[Entry]", "Advanced": "[Advanced]", "Expert": "[Expert]"}

# ── Product A: "BrainBox AI" - Strong analysis, weak execution ───────────────

product_a = EvaluatorEvaluation(name="BrainBox AI")

product_a.add_domain(EvaluatorDomain("identity", "Identity Response Plane", actions=[
    EvaluatorAction("reset_password_std",       "Reset Password (Std)",         "1A"),
    EvaluatorAction("revoke_sessions",          "Revoke Sessions",              "2"),
    EvaluatorAction("disable_user",             "Disable User",                 "1A"),
    EvaluatorAction("disable_service_principal","Disable Service Principals",   "1G"),
    EvaluatorAction("remove_permissions",       "Remove Permissions",           "1G"),
    EvaluatorAction("group_adherence",          "Group Adherence",              "2"),
    EvaluatorAction("group_creation",           "Group Creation",               "1A"),
    EvaluatorAction("token_rotation",           "Token Rotation (Prod)",        "1C"),
    EvaluatorAction("delete_sharing_perms",     "Delete Sharing Permissions",   "1G"),
    EvaluatorAction("label_user",               "Label User (Tagging)",         "2"),
    EvaluatorAction("reset_password_vip",       "Reset Password (VIP)",         "1C"),
]))

product_a.add_domain(EvaluatorDomain("network", "Network Response Plane", actions=[
    EvaluatorAction("acl_creation",             "ACL Creation",                 "1G"),
    EvaluatorAction("vlan_creation",            "VLAN Creation",                "0"),
    EvaluatorAction("firewall_rule_creation",   "Firewall Rule Creation",       "1A"),
    EvaluatorAction("ips_rule_creation",        "IPS Rule Creation",            "1C"),
    EvaluatorAction("network_connection_reset", "Network Connection Reset",     "2"),
    EvaluatorAction("dns_entry_change",         "DNS Entry Change",             "1G"),
    EvaluatorAction("routing_table_change",     "Routing Table Change",         "0"),
    EvaluatorAction("sinkhole_traffic",         "Sinkhole Traffic",             "1A"),
    EvaluatorAction("rate_limit_traffic",       "Rate Limit Traffic",           "1A"),
    EvaluatorAction("vlan_modification",        "VLAN Modification",            "0"),
    EvaluatorAction("quarantine_device_net",    "Quarantine Device",            "1A"),
    EvaluatorAction("quarantine_server",        "Quarantine Server",            "1C"),
    EvaluatorAction("modify_nat_rules",         "Modify NAT Rules",             "0"),
]))

product_a.add_domain(EvaluatorDomain("endpoint", "Endpoint Response Plane", actions=[
    EvaluatorAction("isolate_device",           "Isolate Device",               "1A"),
    EvaluatorAction("initiate_malware_scan",    "Initiate Malware Scan",        "2"),
    EvaluatorAction("grab_file",               "Grab File from Device",         "2"),
    EvaluatorAction("submit_to_sandbox",        "Submit File to Sandbox",       "2"),
    EvaluatorAction("lock_out_user",            "Lock Out User",                "1G"),
    EvaluatorAction("remove_user_from_device",  "Remove User from Device",      "1C"),
    EvaluatorAction("delete_files",             "Delete Files",                 "1G"),
    EvaluatorAction("kill_processes",           "Kill Processes",               "1A"),
    EvaluatorAction("remove_application",       "Remove Application",           "1C"),
    EvaluatorAction("remove_browser_ext",       "Remove Browser Extension",     "1A"),
    EvaluatorAction("modify_browser_settings",  "Modify Browser Settings",      "1G"),
    EvaluatorAction("remove_scheduled_task",    "Remove Scheduled Task",        "1G"),
    EvaluatorAction("remove_startup_items",     "Remove Startup Items",         "1G"),
    EvaluatorAction("remove_library",           "Remove Library / Package",     "0"),
    EvaluatorAction("upgrade_application",      "Upgrade Application",          "0"),
    EvaluatorAction("upgrade_os",               "Upgrade OS",                   "0"),
    EvaluatorAction("deploy_script",            "Deploy Script",                "1C"),
    EvaluatorAction("modify_registry_key",      "Modify Registry Key",          "1C"),
    EvaluatorAction("disable_service",          "Disable Service",              "1G"),
    EvaluatorAction("collect_memory_dump",      "Collect Memory Dump",          "1A"),
    EvaluatorAction("clear_browser_cache",      "Clear Browser Cache",          "2"),
    EvaluatorAction("remove_device_from_domain","Remove Device from Domain",    "0"),
    EvaluatorAction("block_file_hash",          "Block File (via Hash)",        "1A"),
]))

product_a.add_domain(EvaluatorDomain("cloud", "Cloud Response Plane", actions=[
    EvaluatorAction("modify_security_group",    "Modify Security Group Rules",  "1A"),
    EvaluatorAction("create_security_group",    "Create Security Group",        "1G"),
    EvaluatorAction("isolate_resource",         "Isolate Resource",             "1A"),
    EvaluatorAction("modify_access_type",       "Modify Access Type",           "1G"),
    EvaluatorAction("remove_resource_perms",    "Remove Permissions to Resource","1G"),
    EvaluatorAction("delete_resource",          "Delete Resource",              "1C"),
    EvaluatorAction("stop_resource",            "Stop Resource",                "1A"),
    EvaluatorAction("modify_keyvault",          "Modify KeyVault Entries",      "0"),
    EvaluatorAction("use_breakglass",           "Use Breakglass Account",       "0"),
    EvaluatorAction("remove_files_storage",     "Remove Files from Storage",    "1G"),
    EvaluatorAction("copy_storage_device",      "Copy Storage Device",          "1A"),
    EvaluatorAction("mount_storage_device",     "Mount Storage Device",         "1G"),
    EvaluatorAction("snapshot_vm",              "Snapshot VM",                  "2"),
    EvaluatorAction("enable_diagnostic",        "Enable Diagnostic Settings",   "2"),
    EvaluatorAction("apply_resource_lock",      "Apply Resource Lock",          "1A"),
]))

product_a.add_domain(EvaluatorDomain("saas", "SaaS Response Plane", actions=[
    EvaluatorAction("delete_email",             "Delete Email",                 "2"),
    EvaluatorAction("quarantine_email",         "Quarantine Email",             "2"),
    EvaluatorAction("create_routing_rules",     "Create Routing Rules",         "1A"),
    EvaluatorAction("grab_email_sample",        "Grab Email Sample",            "2"),
    EvaluatorAction("grab_email_link",          "Grab Email Link",              "2"),
    EvaluatorAction("add_remove_meeting",       "Add / Remove Meeting Invite",  "1G"),
    EvaluatorAction("read_modify_user_status",  "Read / Modify User Status",    "1G"),
    EvaluatorAction("disable_inbox_rule",       "Disable Malicious Inbox Rule", "1A"),
    EvaluatorAction("block_sender",             "Block Sender",                 "2"),
    EvaluatorAction("modify_hr_records",        "Modify HR Records",            "1C"),
]))

product_a.add_domain(EvaluatorDomain("general", "General Options / Usability", actions=[
    EvaluatorAction("close_alerts_siem",        "Close Alerts in SIEM",         "2"),
    EvaluatorAction("logging",                  "Logging",                      "2"),
    EvaluatorAction("reasoning_logging",        "Reasoning Logging",            "2"),
    EvaluatorAction("api_development",          "API Development",              "1"),
    EvaluatorAction("support_level",            "Support Level",                "2"),
    EvaluatorAction("account_management",       "Account Management",           "2"),
    EvaluatorAction("roles_rbac",               "Roles and Responsibility",     "1A"),
    EvaluatorAction("ease_of_use",              "Ease of Use (GUI)",            "2"),
    EvaluatorAction("native_chat_integration",  "Native Chat Integration",      "1A"),
    EvaluatorAction("alerting",                 "Alerting",                     "1A"),
    EvaluatorAction("stats_dashboards",         "Stats / Health Dashboards",    "2"),
    EvaluatorAction("byom",                     "Bring Your Own Model",         "0"),
    EvaluatorAction("context_grounding",        "Context Grounding",            "1A"),
    EvaluatorAction("autonomous_thresholds",    "Autonomous Action Thresholds", "1A"),
    EvaluatorAction("investigation_audit",      "Investigation Audit Trail",    "2"),
    EvaluatorAction("ir_metrics",               "IR Metrics Tracking",          "1A"),
    EvaluatorAction("feedback_loop",            "Feedback Loop Mechanism",      "1A"),
    EvaluatorAction("auto_close_reversal",      "Auto-Close Reversal Tracking", "1A"),
    EvaluatorAction("explainability",           "Explainability",               "2"),
    EvaluatorAction("ai_accuracy_reporting",    "AI Decision Accuracy Reporting","1A"),
    EvaluatorAction("model_drift",              "Model Drift Detection",        "0"),
    EvaluatorAction("adversarial_robustness",   "Adversarial Robustness Testing","0"),
]))

# ── Product B: "AutoSOC Pro" - Narrower but highly automated ─────────────────

product_b = EvaluatorEvaluation(name="AutoSOC Pro")

product_b.add_domain(EvaluatorDomain("identity", "Identity Response Plane", actions=[
    EvaluatorAction("reset_password_std",       "Reset Password (Std)",         "2"),
    EvaluatorAction("revoke_sessions",          "Revoke Sessions",              "2"),
    EvaluatorAction("disable_user",             "Disable User",                 "2"),
    EvaluatorAction("disable_service_principal","Disable Service Principals",   "1A"),
    EvaluatorAction("remove_permissions",       "Remove Permissions",           "1A"),
    EvaluatorAction("group_adherence",          "Group Adherence",              "2"),
    EvaluatorAction("group_creation",           "Group Creation",               "1A"),
    EvaluatorAction("token_rotation",           "Token Rotation (Prod)",        "1A"),
    EvaluatorAction("delete_sharing_perms",     "Delete Sharing Permissions",   "1G"),
    EvaluatorAction("label_user",               "Label User (Tagging)",         "2"),
    EvaluatorAction("reset_password_vip",       "Reset Password (VIP)",         "1A"),
]))

product_b.add_domain(EvaluatorDomain("network", "Network Response Plane", actions=[
    EvaluatorAction("acl_creation",             "ACL Creation",                 "1A"),
    EvaluatorAction("vlan_creation",            "VLAN Creation",                "1G"),
    EvaluatorAction("firewall_rule_creation",   "Firewall Rule Creation",       "2"),
    EvaluatorAction("ips_rule_creation",        "IPS Rule Creation",            "1A"),
    EvaluatorAction("network_connection_reset", "Network Connection Reset",     "2"),
    EvaluatorAction("dns_entry_change",         "DNS Entry Change",             "1A"),
    EvaluatorAction("routing_table_change",     "Routing Table Change",         "1C"),
    EvaluatorAction("sinkhole_traffic",         "Sinkhole Traffic",             "2"),
    EvaluatorAction("rate_limit_traffic",       "Rate Limit Traffic",           "2"),
    EvaluatorAction("vlan_modification",        "VLAN Modification",            "1A"),
    EvaluatorAction("quarantine_device_net",    "Quarantine Device",            "2"),
    EvaluatorAction("quarantine_server",        "Quarantine Server",            "1A"),
    EvaluatorAction("modify_nat_rules",         "Modify NAT Rules",             "1G"),
]))

product_b.add_domain(EvaluatorDomain("endpoint", "Endpoint Response Plane", actions=[
    EvaluatorAction("isolate_device",           "Isolate Device",               "2"),
    EvaluatorAction("initiate_malware_scan",    "Initiate Malware Scan",        "2"),
    EvaluatorAction("grab_file",               "Grab File from Device",         "2"),
    EvaluatorAction("submit_to_sandbox",        "Submit File to Sandbox",       "2"),
    EvaluatorAction("lock_out_user",            "Lock Out User",                "1A"),
    EvaluatorAction("remove_user_from_device",  "Remove User from Device",      "1A"),
    EvaluatorAction("delete_files",             "Delete Files",                 "1A"),
    EvaluatorAction("kill_processes",           "Kill Processes",               "2"),
    EvaluatorAction("remove_application",       "Remove Application",           "1A"),
    EvaluatorAction("remove_browser_ext",       "Remove Browser Extension",     "2"),
    EvaluatorAction("modify_browser_settings",  "Modify Browser Settings",      "1A"),
    EvaluatorAction("remove_scheduled_task",    "Remove Scheduled Task",        "1A"),
    EvaluatorAction("remove_startup_items",     "Remove Startup Items",         "1A"),
    EvaluatorAction("remove_library",           "Remove Library / Package",     "1G"),
    EvaluatorAction("upgrade_application",      "Upgrade Application",          "1G"),
    EvaluatorAction("upgrade_os",               "Upgrade OS",                   "1C"),
    EvaluatorAction("deploy_script",            "Deploy Script",                "1A"),
    EvaluatorAction("modify_registry_key",      "Modify Registry Key",          "1A"),
    EvaluatorAction("disable_service",          "Disable Service",              "1A"),
    EvaluatorAction("collect_memory_dump",      "Collect Memory Dump",          "2"),
    EvaluatorAction("clear_browser_cache",      "Clear Browser Cache",          "2"),
    EvaluatorAction("remove_device_from_domain","Remove Device from Domain",    "1A"),
    EvaluatorAction("block_file_hash",          "Block File (via Hash)",        "2"),
]))

product_b.add_domain(EvaluatorDomain("cloud", "Cloud Response Plane", actions=[
    EvaluatorAction("modify_security_group",    "Modify Security Group Rules",  "1A"),
    EvaluatorAction("create_security_group",    "Create Security Group",        "1A"),
    EvaluatorAction("isolate_resource",         "Isolate Resource",             "1A"),
    EvaluatorAction("modify_access_type",       "Modify Access Type",           "1A"),
    EvaluatorAction("remove_resource_perms",    "Remove Permissions to Resource","1A"),
    EvaluatorAction("delete_resource",          "Delete Resource",              "1C"),
    EvaluatorAction("stop_resource",            "Stop Resource",                "1A"),
    EvaluatorAction("modify_keyvault",          "Modify KeyVault Entries",      "1C"),
    EvaluatorAction("use_breakglass",           "Use Breakglass Account",       "0"),
    EvaluatorAction("remove_files_storage",     "Remove Files from Storage",    "1A"),
    EvaluatorAction("copy_storage_device",      "Copy Storage Device",          "1A"),
    EvaluatorAction("mount_storage_device",     "Mount Storage Device",         "1A"),
    EvaluatorAction("snapshot_vm",              "Snapshot VM",                  "2"),
    EvaluatorAction("enable_diagnostic",        "Enable Diagnostic Settings",   "2"),
    EvaluatorAction("apply_resource_lock",      "Apply Resource Lock",          "2"),
]))

product_b.add_domain(EvaluatorDomain("saas", "SaaS Response Plane", actions=[
    EvaluatorAction("delete_email",             "Delete Email",                 "2"),
    EvaluatorAction("quarantine_email",         "Quarantine Email",             "2"),
    EvaluatorAction("create_routing_rules",     "Create Routing Rules",         "1A"),
    EvaluatorAction("grab_email_sample",        "Grab Email Sample",            "2"),
    EvaluatorAction("grab_email_link",          "Grab Email Link",              "2"),
    EvaluatorAction("add_remove_meeting",       "Add / Remove Meeting Invite",  "0"),
    EvaluatorAction("read_modify_user_status",  "Read / Modify User Status",    "1A"),
    EvaluatorAction("disable_inbox_rule",       "Disable Malicious Inbox Rule", "2"),
    EvaluatorAction("block_sender",             "Block Sender",                 "2"),
    EvaluatorAction("modify_hr_records",        "Modify HR Records",            "0"),
]))

product_b.add_domain(EvaluatorDomain("general", "General Options / Usability", actions=[
    EvaluatorAction("close_alerts_siem",        "Close Alerts in SIEM",         "2"),
    EvaluatorAction("logging",                  "Logging",                      "2"),
    EvaluatorAction("reasoning_logging",        "Reasoning Logging",            "1A"),
    EvaluatorAction("api_development",          "API Development",              "2"),
    EvaluatorAction("support_level",            "Support Level",                "1A"),
    EvaluatorAction("account_management",       "Account Management",           "2"),
    EvaluatorAction("roles_rbac",               "Roles and Responsibility",     "2"),
    EvaluatorAction("ease_of_use",              "Ease of Use (GUI)",            "1A"),
    EvaluatorAction("native_chat_integration",  "Native Chat Integration",      "2"),
    EvaluatorAction("alerting",                 "Alerting",                     "2"),
    EvaluatorAction("stats_dashboards",         "Stats / Health Dashboards",    "2"),
    EvaluatorAction("byom",                     "Bring Your Own Model",         "1A"),
    EvaluatorAction("context_grounding",        "Context Grounding",            "1A"),
    EvaluatorAction("autonomous_thresholds",    "Autonomous Action Thresholds", "2"),
    EvaluatorAction("investigation_audit",      "Investigation Audit Trail",    "2"),
    EvaluatorAction("ir_metrics",               "IR Metrics Tracking",          "2"),
    EvaluatorAction("feedback_loop",            "Feedback Loop Mechanism",      "1A"),
    EvaluatorAction("auto_close_reversal",      "Auto-Close Reversal Tracking", "2"),
    EvaluatorAction("explainability",           "Explainability",               "1A"),
    EvaluatorAction("ai_accuracy_reporting",    "AI Decision Accuracy Reporting","1A"),
    EvaluatorAction("model_drift",              "Model Drift Detection",        "1A"),
    EvaluatorAction("adversarial_robustness",   "Adversarial Robustness Testing","1C"),
]))

# ── Run comparison ────────────────────────────────────────────────────────────

def print_report(ev: EvaluatorEvaluation):
    r = ev.report()
    print(f"\n{'='*60}")
    print(f"  {r['evaluation_name']}")
    print(f"  Composite : {TIER_ICONS.get(r['composite_tier'], r['composite_tier'])}")
    print(f"  Score     : {r['overall_score_pct']}%  Coverage: {r['overall_coverage_pct']}%  Automation: {r['overall_automation_pct']}%")
    print(f"  {'Domain':<30} {'Coverage':>9} {'Auto':>6} {'Tier'}")
    print(f"  {'-'*55}")
    for d in r["domains"].values():
        icon = TIER_ICONS.get(d["tier"], d["tier"])
        print(f"  {d['name']:<30} {d['coverage_rate_pct']:>7.1f}%  {d['automation_rate_pct']:>4.1f}%  {icon}")


if __name__ == "__main__":
    print("\nARMM Evaluator Mode - Hypothetical Product Comparison")
    print("Framework by Andrei Cotaie, Cristian Miron & Filip Stojkovski")

    print_report(product_a)
    print_report(product_b)

    print(f"\n{'='*60}")
    print("  KEY INSIGHT:")
    ra = product_a.report()
    rb = product_b.report()
    print(f"  {product_a.name}: {ra['overall_coverage_pct']}% coverage / {ra['overall_automation_pct']}% automated")
    print(f"  {product_b.name}: {rb['overall_coverage_pct']}% coverage / {rb['overall_automation_pct']}% automated")
    print()
    print("  BrainBox AI covers more capabilities but relies heavily on human approvals.")
    print("  AutoSOC Pro is narrower but operates with higher actual automation.")
    print("  These are different products for different buyers.")
