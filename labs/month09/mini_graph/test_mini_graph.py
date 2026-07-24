# Atlas · LangGraph：图状态机  （对应 docs/atlas/langgraph.mdx）
# 目标：节点 + 条件边组成的图状态机，可循环、可条件跳转
# 用法：python labs/month09/mini_graph/test_mini_graph.py


class StateGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def add_node(self, name, fn):
        self.nodes[name] = fn

    def add_edge(self, frm, cond_fn):
        self.edges[frm] = cond_fn

    def run(self, start, state, max_steps=10):
        cur = start
        path = []
        for _ in range(max_steps):
            state = self.nodes[cur](state)
            path.append(cur)
            nxt = self.edges.get(cur, lambda s: None)(state)   # 条件边决定下一节点
            if nxt is None:
                break
            cur = nxt
        return state, path


def run():
    g = StateGraph()
    g.add_node("inc", lambda s: {**s, "n": s["n"] + 1})
    g.add_edge("inc", lambda s: "inc" if s["n"] < 3 else None)   # 循环到 n>=3 停
    state, path = g.run("inc", {"n": 0})
    assert state["n"] == 3 and path == ["inc", "inc", "inc"]
    print("✅ 全部通过: LangGraph 图状态机（节点+条件边）")


if __name__ == "__main__":
    run()
