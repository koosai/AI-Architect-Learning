#!/usr/bin/env python3
"""一键运行 labs 下所有 test_*.py，逐个报告通过/失败。

用法：
    python labs/run_all.py            # 跑全部
    python labs/run_all.py month01    # 只跑某个月
"""
import os
import sys
import subprocess

LABS_ROOT = os.path.dirname(os.path.abspath(__file__))


def find_tests(scope):
    root = os.path.join(LABS_ROOT, scope) if scope else LABS_ROOT
    out = []
    for dirpath, _dirs, files in os.walk(root):
        for f in sorted(files):
            if f.startswith("test_") and f.endswith(".py"):
                out.append(os.path.join(dirpath, f))
    return sorted(out)


def main():
    scope = sys.argv[1] if len(sys.argv) > 1 else ""
    tests = find_tests(scope)
    if not tests:
        print(f"未找到测试（scope={scope!r}）")
        return 1
    passed, failed = 0, 0
    for t in tests:
        rel = os.path.relpath(t, os.path.dirname(LABS_ROOT))
        r = subprocess.run([sys.executable, t], capture_output=True, text=True)
        if r.returncode == 0:
            passed += 1
            print(f"  ✅ {rel}")
        else:
            failed += 1
            print(f"  ❌ {rel}\n{(r.stdout + r.stderr).strip()}")
    print(f"\n汇总: {passed} 通过 / {failed} 失败 / 共 {len(tests)}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
