# labs/month01/signup.py  （对应 docs/01-foundations/programming-systems-primer.mdx）
# 参考实现：报名系统的最小内核，演示四个概念在一处协同：
#   Boundary(边界校验) / State(状态外移) / Failure Mode(失败处理) / Observability(可观测)
# 建议：先自己实现 signup()，再对照本参考实现。
import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class SignupError(Exception):
    """用户可修复的输入错误（对应 4xx）。"""


def _validate(name, email):
    # Boundary：在信任边界上做校验，fail fast
    if not name or not name.strip():
        raise SignupError("name 不能为空")
    if not EMAIL_RE.match(email or ""):
        raise SignupError("email 格式非法")


def signup(name, email, *, store, logs):
    # State：用户表通过 store 注入，不放模块全局 -> 可水平扩展
    # Observability：关键节点打点
    logs.append(("signup_attempt", email))
    _validate(name, email)
    if email in store:
        # Failure Mode：重复报名是可预期错误，返回明确结果而不是崩
        logs.append(("signup_duplicate", email))
        return {"status": "duplicate", "email": email}
    store[email] = {"name": name.strip()}
    logs.append(("signup_ok", email))
    return {"status": "ok", "email": email}
