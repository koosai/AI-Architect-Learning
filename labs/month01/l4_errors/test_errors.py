# Lab L4：错误处理  （对应 docs/01-foundations/error-handling.mdx）
# 目标：区分 客户端错误(4xx) vs 服务端错误(5xx)；结构化传达；不吞不泄露内部细节
# 用法：python labs/month01/l4_errors/test_errors.py


class AppError(Exception):
    status = 500
    code = "internal"

    def to_body(self):
        return {"error": self.code, "message": str(self)}


class BadRequest(AppError):
    status = 400
    code = "bad_request"


class NotFound(AppError):
    status = 404
    code = "not_found"


def handle(fn):
    # 把任意异常映射为 (status, body)；未知异常 -> 500 且不泄露堆栈
    try:
        return 200, fn()
    except AppError as e:
        return e.status, e.to_body()
    except Exception:
        return 500, {"error": "internal", "message": "internal error"}


def _raise(exc):
    raise exc


def run():
    assert handle(lambda: {"ok": 1}) == (200, {"ok": 1})
    s, b = handle(lambda: _raise(BadRequest("missing field")))
    assert s == 400 and b["error"] == "bad_request", (s, b)
    s, b = handle(lambda: _raise(NotFound("user 7")))
    assert s == 404, (s, b)
    s, b = handle(lambda: 1 / 0)  # 未预期错误
    assert s == 500 and b["message"] == "internal error", (s, b)  # 不泄露 ZeroDivisionError
    print("✅ 全部通过: 错误分类 / 结构化 / 不泄露内部")


if __name__ == "__main__":
    run()
