# Month12 L4：模型 Provider 层  （对应 docs/12-capstone/model-provider-layer.mdx）
# 目标：把模型调用藏在统一接口后，让 mock/本地/云可切换、上层不改、无 key 可跑
# 用法：python labs/month12/m12l4_provider/test_provider.py


class ModelProvider:
    def __init__(self, backend="mock", api_key=None):
        self.backend = backend
        self.api_key = api_key

    def complete(self, prompt):
        if self.backend == "mock":
            return f"[mock] {prompt[:20]}"            # 无 key 可跑
        if self.backend == "cloud":
            if not self.api_key:
                raise RuntimeError("missing api key")
            return f"[cloud] {prompt[:20]}"
        return f"[local] {prompt[:20]}"


def run():
    assert ModelProvider("mock").complete("hello world").startswith("[mock]")
    assert ModelProvider("local").complete("hi").startswith("[local]")
    try:
        ModelProvider("cloud").complete("x")          # 云缺 key
        assert False
    except RuntimeError:
        pass
    assert ModelProvider("cloud", api_key="k").complete("x").startswith("[cloud]")
    print("✅ 全部通过: Provider 层（统一接口，mock/local/cloud 可切，无 key 可跑）")


if __name__ == "__main__":
    run()
