# Labs · 动手实验

每个章节的"动手 Lab（必做）"对应本目录下的一个实验。教材里出现的
`python labs/monthXX/.../test_*.py` 命令，指向的就是这里的文件。

## 结构约定

```
labs/
├── run_all.py                 # 一键运行所有实验：python labs/run_all.py [monthXX]
├── month01/                   # 对应 Month 1（编程系统基石）
│   ├── signup.py              # 参考实现（可被 test 导入）
│   ├── test_signup.py         # 断言测试，直接 python 运行
│   ├── l3_validation/
│   │   └── test_validate.py   # 自包含：参考实现 + 断言，跑通打印 ✅
│   └── ...
└── monthXX/ ...
```

每个 `test_*.py`：

- **零依赖**：只用 Python 标准库，直接 `python3 labs/.../test_xxx.py` 即可运行，无需 pytest。
- **自验证**：内含断言，全部通过时打印 `✅ 全部通过: ...`。
- **含参考实现**：文件里带一份正确的参考实现。**建议先自己重写实现、再跑测试**，
  测试全绿即说明你的实现正确。

## 运行

```bash
python labs/run_all.py            # 跑全部
python labs/run_all.py month01    # 只跑 Month 1
python labs/month01/l6_idempotency/test_payment.py   # 跑单个
```

## 进度

| 月份 | 状态 |
|---|---|
| Month 01 编程系统基石 | ✅ 15/15 可运行并通过 |
| Month 02–12 | ⏳ 逐月补齐中 |
