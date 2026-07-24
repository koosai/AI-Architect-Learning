# Month2 L3：容量估算  （对应 docs/02-system-design-bridge/capacity-estimation.mdx）
# 目标：把“数量级心算”变成可复用函数（QPS / 峰值 / 存储）
# 用法：python labs/month02/m2l3_capacity/test_estimate.py


def daily_to_qps(daily_requests):
    return daily_requests / 86400


def peak_qps(avg_qps, peak_factor=3):
    return avg_qps * peak_factor


def storage_bytes(rows, bytes_per_row, replication=3):
    return rows * bytes_per_row * replication


def run():
    assert abs(daily_to_qps(86_400_000) - 1000) < 1e-6      # 8640 万/天 ≈ 1000 QPS
    assert peak_qps(1000) == 3000                            # 峰值按 3x 估
    assert storage_bytes(1_000_000, 1000, 3) == 3_000_000_000  # 1M 行 * 1KB * 3 副本 = 3GB
    print("✅ 全部通过: QPS / 峰值 / 存储 容量估算")


if __name__ == "__main__":
    run()
