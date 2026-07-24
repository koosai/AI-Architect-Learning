# Month6 L8：Sidecar 数据面  （对应 docs/06-cloud-enterprise-industrial/service-mesh.mdx）
# 目标：横切能力下沉到 sidecar、业务无感——服务网格数据面的核心
# 用法：python labs/month06/m6l8_sidecar/test_sidecar.py


def business(req):
    return {"echo": req["body"]}          # 业务只关心 body，对横切无感


def sidecar(handler, req):
    req = dict(req)
    req["mtls"] = True                    # sidecar 注入 mTLS
    metrics = {"count": 1}                # sidecar 记录指标
    resp = handler(req)
    resp["_via_sidecar"] = True
    return resp, metrics


def run():
    resp, metrics = sidecar(business, {"body": "hi"})
    assert resp == {"echo": "hi", "_via_sidecar": True}, resp   # 业务逻辑不变
    assert metrics["count"] == 1
    print("✅ 全部通过: Sidecar（横切下沉，业务无感）")


if __name__ == "__main__":
    run()
