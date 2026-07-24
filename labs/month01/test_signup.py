# labs/month01/test_signup.py
# 用法：python labs/month01/test_signup.py
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from signup import signup, SignupError


def run():
    store, logs = {}, []
    r = signup("Ada", "ada@example.com", store=store, logs=logs)
    assert r["status"] == "ok", r
    # 重复报名 -> duplicate，不抛错、不重复写
    r2 = signup("Ada", "ada@example.com", store=store, logs=logs)
    assert r2["status"] == "duplicate", r2
    assert len(store) == 1, store
    # 非法输入 -> fail fast
    for bad in [("", "x@y.com"), ("Bob", "not-an-email")]:
        try:
            signup(*bad, store=store, logs=logs)
            assert False, "应当抛 SignupError"
        except SignupError:
            pass
    # 可观测：关键事件被记录
    kinds = [k for k, _ in logs]
    assert "signup_ok" in kinds and "signup_duplicate" in kinds, kinds
    print("✅ 全部通过: signup 的 边界/状态/失败/可观测 四概念协同正确")


if __name__ == "__main__":
    run()
