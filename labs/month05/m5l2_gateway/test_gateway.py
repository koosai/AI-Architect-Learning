# Month5 L2：API 网关中间件链  （对应 docs/05-core-components/api-gateway.mdx）
# 目标：把横切能力做成可组合的中间件链（责任链），后端只收干净请求
# 用法：python labs/month05/m5l2_gateway/test_gateway.py


def make_gateway(middlewares, handler):
    def app(request):
        ctx = dict(request)
        for mw in middlewares:
            ctx = mw(ctx)
            if ctx.get("_reject"):
                return {"status": ctx["_reject"]}   # 链条中途拦截
        return handler(ctx)
    return app


def auth(ctx):
    if not ctx.get("token"):
        ctx["_reject"] = 401
    else:
        ctx["user"] = "ada"
    return ctx


def strip(ctx):
    ctx.pop("token", None)   # 清洗掉敏感字段
    return ctx


def run():
    handler = lambda ctx: {"status": 200, "user": ctx.get("user"), "has_token": "token" in ctx}
    gw = make_gateway([auth, strip], handler)
    ok = gw({"token": "t"})
    assert ok == {"status": 200, "user": "ada", "has_token": False}, ok   # 后端收到干净请求
    bad = gw({})
    assert bad == {"status": 401}, bad   # 未认证被链条拦截
    print("✅ 全部通过: 网关中间件责任链（认证/清洗，后端只收干净请求）")


if __name__ == "__main__":
    run()
