# Lab L16：Month 1 综合  （对应 docs/01-foundations/month1-capstone.mdx）
# 目标：让多个关注点正确协同 —— 校验 + 幂等 + 状态外移 + 错误分类 + 可观测
# 用法：python labs/month01/l16_capstone/test_signup_service.py
import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class SignupError(Exception):
    pass


class SignupService:
    def __init__(self, users_store, idem_store, logs):
        # 状态全部外移/注入：用户表、幂等表、日志
        self.users = users_store
        self.idem = idem_store
        self.logs = logs

    def signup(self, request_id, name, email):
        self.logs.append(("attempt", email))
        if request_id in self.idem:                      # 幂等：重试返回同结果
            return self.idem[request_id]
        if not name or not name.strip():                 # 校验
            raise SignupError("name 不能为空")
        if not EMAIL_RE.match(email or ""):
            raise SignupError("email 格式非法")
        if email in self.users:
            res = {"status": "duplicate", "email": email}  # 业务重复（可预期，非异常）
        else:
            self.users[email] = {"name": name.strip()}
            res = {"status": "ok", "email": email}
        self.idem[request_id] = res
        self.logs.append((res["status"], email))         # 可观测
        return res


def run():
    users, idem, logs = {}, {}, []
    svc = SignupService(users, idem, logs)
    r1 = svc.signup("r1", "Ada", "ada@example.com")
    assert r1["status"] == "ok", r1
    r2 = svc.signup("r1", "Ada", "ada@example.com")     # 幂等重试
    assert r2 == r1 and len(users) == 1, (r2, users)
    r3 = svc.signup("r2", "Ada2", "ada@example.com")    # 业务重复
    assert r3["status"] == "duplicate", r3
    try:
        svc.signup("r3", "", "x@y.com")                 # 校验失败
        assert False, "应抛 SignupError"
    except SignupError:
        pass
    assert ("ok", "ada@example.com") in logs, logs      # 可观测
    print("✅ 全部通过: 校验/幂等/状态外移/错误/可观测 五概念协同")


if __name__ == "__main__":
    run()
