# Month4 L10：停车场 LLD  （对应 docs/04-design-patterns-lld/parking-lot-lld.mdx）
# 目标：需求落成内聚的类 + 在会变处（计费）用策略
# 用法：python labs/month04/m4l10_parking/test_parking.py


class ParkingLot:
    def __init__(self, capacity, fee_strategy):
        self.capacity = capacity
        self.occupied = 0
        self.fee = fee_strategy       # 计费策略可插拔

    def park(self):
        if self.occupied >= self.capacity:
            return None               # 满
        self.occupied += 1
        return self.occupied          # ticket id

    def leave(self, hours):
        if self.occupied > 0:
            self.occupied -= 1
        return self.fee(hours)


def flat(hours):
    return 10


def hourly(hours):
    return 3 * hours


def run():
    lot = ParkingLot(capacity=2, fee_strategy=hourly)
    assert lot.park() == 1 and lot.park() == 2
    assert lot.park() is None         # 满
    assert lot.leave(4) == 12         # 按时计费
    lot2 = ParkingLot(2, flat)        # 换计费策略，ParkingLot 不改
    lot2.park()
    assert lot2.leave(4) == 10
    print("✅ 全部通过: 停车场 LLD（内聚类 + 计费策略可换）")


if __name__ == "__main__":
    run()
