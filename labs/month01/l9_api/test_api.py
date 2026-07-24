# Lab L9：API 与 HTTP  （对应 docs/01-foundations/api-and-http.mdx）
# 目标：正确的 HTTP 方法语义与状态码；资源建模（/users, /users/{id}）
# 用法：python labs/month01/l9_api/test_api.py


class UsersAPI:
    def __init__(self):
        self.db = {}
        self.seq = 0

    def handle(self, method, path, body=None):
        parts = [p for p in path.split("/") if p]
        if parts and parts[0] == "users":
            if len(parts) == 1:
                if method == "POST":
                    if not body or "name" not in body:
                        return 400, {"error": "name required"}     # 输入不合法 -> 400
                    self.seq += 1
                    self.db[self.seq] = {"id": self.seq, **body}
                    return 201, self.db[self.seq]                  # 创建成功 -> 201
                if method == "GET":
                    return 200, list(self.db.values())
            elif len(parts) == 2:
                uid = int(parts[1])
                if uid not in self.db:
                    return 404, {"error": "not found"}             # 资源不存在 -> 404
                if method == "GET":
                    return 200, self.db[uid]
                if method == "PUT":
                    self.db[uid] = {**self.db[uid], **(body or {})}
                    return 200, self.db[uid]
                if method == "DELETE":
                    del self.db[uid]
                    return 204, None                               # 删除成功 -> 204
        return 405, {"error": "method not allowed"}


def run():
    api = UsersAPI()
    assert api.handle("POST", "/users", {"name": "Ada"})[0] == 201
    assert api.handle("POST", "/users", {})[0] == 400
    assert api.handle("GET", "/users/1")[0] == 200
    assert api.handle("GET", "/users/99")[0] == 404
    assert api.handle("DELETE", "/users/1")[0] == 204
    assert api.handle("GET", "/users/1")[0] == 404  # 已删除
    print("✅ 全部通过: HTTP 方法语义与状态码正确(201/400/404/204)")


if __name__ == "__main__":
    run()
