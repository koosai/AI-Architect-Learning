# Month4 L1：开闭原则  （对应 docs/04-design-patterns-lld/change-driven-design.mdx）
# 目标：封装变化 + 开闭原则——加新类型 = 新增注册，而不是改核心逻辑
# 用法：python labs/month04/m4l1_ocp/test_shapes.py

SHAPE_AREA = {}


def register(name):
    def deco(fn):
        SHAPE_AREA[name] = fn
        return fn
    return deco


@register("circle")
def _circle(s):
    return 3.14159 * s["r"] ** 2


@register("rect")
def _rect(s):
    return s["w"] * s["h"]


def area(shape):
    return SHAPE_AREA[shape["type"]](shape)   # 核心逻辑：查表委托，永不修改


def run():
    assert abs(area({"type": "circle", "r": 1}) - 3.14159) < 1e-6
    assert area({"type": "rect", "w": 2, "h": 3}) == 6

    @register("square")   # 加新类型 = 新增注册，area() 一行不改
    def _square(s):
        return s["side"] ** 2

    assert area({"type": "square", "side": 4}) == 16
    print("✅ 全部通过: 开闭原则（注册表扩展，核心不改）")


if __name__ == "__main__":
    run()
