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

**全部 12 个月 + Atlas 引用实验已补齐：`python labs/run_all.py` → 154 通过 / 0 失败。**
质量门禁 LAB-REF：298 条引用路径 0 悬空。

| 月份 | 状态 |
|---|---|
| Month 01 编程系统基石 | ✅ 15 |
| Month 02 系统设计之桥 | ✅ 8 |
| Month 03 数据缓存队列 | ✅ 13 |
| Month 04 设计模式与 LLD | ✅ 12 |
| Month 05 分布式核心组件 | ✅ 12 |
| Month 06 云原生与企业级 | ✅ 12 |
| Month 07 LLM 系统 | ✅ 12 |
| Month 08 RAG | ✅ 12 + 5 Atlas |
| Month 09 Agent 架构 | ✅ 12 + 1 Atlas |
| Month 10 多智能体协议 | ✅ 12 |
| Month 11 生产级 AI 平台 | ✅ 12 + 3 Atlas |
| Month 12 毕业设计 Capstone | ✅ 12 |
| Atlas 案例专属实验 | ✅ 10（Snowflake/PinSage/Ray 等） |
