# Month11 L7：风险治理框架  （对应 docs/11-production-ai-platform/risk-governance-frameworks.mdx）
# 目标：按风险分级的治理要求 + 就绪检查 + 审计追溯——可执行制度
# 用法：python labs/month11/m11l7_governance/test_governance.py


def risk_tier(system):
    if system.get("affects_safety") or system.get("affects_finance"):
        return "high"
    if system.get("external_users"):
        return "medium"
    return "low"


REQUIREMENTS = {
    "high": ["eval", "red_team", "human_signoff", "audit_log"],
    "medium": ["eval", "audit_log"],
    "low": ["eval"],
}


def readiness(system, completed):
    tier = risk_tier(system)
    missing = [r for r in REQUIREMENTS[tier] if r not in completed]
    return {"tier": tier, "ready": len(missing) == 0, "missing": missing}


def run():
    r = readiness({"affects_finance": True}, completed={"eval", "audit_log"})
    assert r["tier"] == "high" and not r["ready"] and "human_signoff" in r["missing"]
    r2 = readiness({"external_users": True}, {"eval", "audit_log"})
    assert r2["tier"] == "medium" and r2["ready"]
    print("✅ 全部通过: 风险分级治理+就绪检查+审计")


if __name__ == "__main__":
    run()
