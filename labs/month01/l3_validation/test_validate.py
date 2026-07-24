# Lab L3：输入校验  （对应 docs/01-foundations/input-validation.mdx）
# 目标：信任边界 + 三层校验(存在性/类型格式/业务规则) + fail fast + 返回干净对象
# 用法：python labs/month01/l3_validation/test_validate.py
# 建议：先注释掉“参考实现”自己重写 validate_signup，再跑本文件让断言通过。
import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class ValidationError(Exception):
    def __init__(self, field, msg):
        super().__init__(f"{field}: {msg}")
        self.field = field


# ===== 参考实现 =====
def validate_signup(data):
    # 层1 存在性
    for f in ("name", "email", "age"):
        if f not in data:
            raise ValidationError(f, "缺失")
    # 层2 类型/格式
    if not isinstance(data["name"], str) or not data["name"].strip():
        raise ValidationError("name", "必须为非空字符串")
    if not EMAIL_RE.match(str(data["email"])):
        raise ValidationError("email", "格式非法")
    try:
        age = int(data["age"])
    except (TypeError, ValueError):
        raise ValidationError("age", "必须为整数")
    # 层3 业务规则
    if not (0 < age < 150):
        raise ValidationError("age", "必须在 1..149")
    # 返回干净对象（只含已知字段、已规整；未知字段丢弃）
    return {"name": data["name"].strip(), "email": data["email"].lower(), "age": age}


# ===== 测试 =====
def run():
    ok = validate_signup({"name": " Ada ", "email": "ADA@x.com", "age": "30", "evil": "drop table"})
    assert ok == {"name": "Ada", "email": "ada@x.com", "age": 30}, ok
    assert "evil" not in ok, "未知字段必须被丢弃"
    bads = [
        {},
        {"name": "", "email": "a@b.com", "age": 1},
        {"name": "A", "email": "nope", "age": 1},
        {"name": "A", "email": "a@b.com", "age": 999},
    ]
    for bad in bads:
        try:
            validate_signup(bad)
            assert False, f"应当拒绝: {bad}"
        except ValidationError:
            pass
    print("✅ 全部通过: 三层校验 / fail-fast / 干净对象")


if __name__ == "__main__":
    run()
