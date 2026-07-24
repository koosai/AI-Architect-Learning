# Month5 L11：Raft 选举  （对应 docs/05-core-components/consensus-coordination.mdx）
# 目标：term + 多数派投票 + 每 term 一票，验证唯一 leader、杜绝脑裂
# 用法：python labs/month05/m5l11_raft_election/test_election.py
from collections import Counter


class RaftCluster:
    def __init__(self, num_nodes):
        self.n = num_nodes
        self.voted = {}    # (term, voter) -> candidate

    def request_votes(self, candidate, term, voters):
        votes = 0
        for v in voters:
            key = (term, v)
            if key not in self.voted:      # 每个 voter 每个 term 只投一票
                self.voted[key] = candidate
                votes += 1
        return votes > self.n // 2         # 需严格多数派

    def leader_of_term(self, term):
        c = Counter(cand for (t, _), cand in self.voted.items() if t == term)
        for cand, cnt in c.items():
            if cnt > self.n // 2:
                return cand
        return None


def run():
    rc = RaftCluster(num_nodes=5)          # 多数派 = 3
    assert rc.request_votes("A", term=1, voters=[0, 1, 2]) is True    # A 拿 3 票当选
    # B 同 term 想拉同一批票 -> 已投过，只能拿到 node3 一票 -> 不当选（无脑裂）
    assert rc.request_votes("B", term=1, voters=[0, 1, 2, 3]) is False
    assert rc.leader_of_term(1) == "A"
    print("✅ 全部通过: Raft 选举（term+多数派+一票制 -> 唯一 leader，无脑裂）")


if __name__ == "__main__":
    run()
