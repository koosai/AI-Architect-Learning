# Month2 L6：CAP 取舍  （对应 docs/02-system-design-bridge/cap-consistency.mdx）
# 目标：分区发生时二选一；按业务选 CP（保一致）或 AP（保可用）
# 用法：python labs/month02/m2l6_cap/test_cap.py


def decide(partitioned, prefer):
    # 无分区：既一致又可用。有分区：只能保 prefer 之一。
    if not partitioned:
        return {"consistent": True, "available": True}
    if prefer == "C":   # CP：如银行转账，宁可拒绝服务也要一致
        return {"consistent": True, "available": False}
    if prefer == "A":   # AP：如社交 feed，宁可读到旧数据也要可用
        return {"consistent": False, "available": True}
    raise ValueError("prefer 必须是 'C' 或 'A'")


def run():
    assert decide(False, "C") == {"consistent": True, "available": True}
    assert decide(True, "C") == {"consistent": True, "available": False}   # 保一致 -> 牺牲可用
    assert decide(True, "A") == {"consistent": False, "available": True}   # 保可用 -> 牺牲一致
    try:
        decide(True, "X")
        assert False
    except ValueError:
        pass
    print("✅ 全部通过: CAP 在分区下的 CP/AP 取舍")


if __name__ == "__main__":
    run()
