# Month12 L10：治理与风险文档  （对应 docs/12-capstone/governance-risk-doc.mdx）
# 目标：为助手产出模型卡 + 威胁摘要 + 简化说明，体现负责任的风险判断
# 用法：python labs/month12/m12l10_risk/test_risk.py


def model_card(name, intended_use, limitations, training_data):
    return {"name": name, "intended_use": intended_use,
            "limitations": limitations, "training_data": training_data}


def threat_summary(threats):
    return sorted(threats, key=lambda t: -t["severity"])[:3]    # top 3


def validate_governance(card, threats):
    return bool(card.get("limitations")) and len(threats) > 0   # 必须写清局限 + 有威胁分析


def run():
    card = model_card("assistant", "架构评审", ["不保证100%准确"], "公开文档")
    threats = [{"name": "injection", "severity": 3}, {"name": "leak", "severity": 2}]
    assert validate_governance(card, threats)
    assert not validate_governance({"limitations": []}, threats)   # 没写局限 -> 不合格
    assert threat_summary(threats)[0]["name"] == "injection"
    print("✅ 全部通过: 治理文档（模型卡+威胁摘要+局限）")


if __name__ == "__main__":
    run()
