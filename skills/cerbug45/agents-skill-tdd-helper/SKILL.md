---
name: tdd-helper
description: 这是一个轻量级的辅助工具，用于为非确定性代理（non-deterministic agents）强制实现基于测试驱动开发（Test-Driven Development, TDD）风格的循环逻辑。
metadata:
  {
    "openclaw": {
      "requires": { "bins": ["python3", "pytest"] },
      "category": "development"
    }
  }
---
# tdd-helper

这是一个轻量级的辅助工具，用于为非确定性代理（non-deterministic agents）强制执行 TDD（测试驱动开发）风格的循环（test-driven loops）。

## 主要功能
- `tdd.py` 会包裹一个任务（task）：如果缺少测试或测试失败，该任务将不会被执行；同时，该工具会拒绝在运行“生产环境”（prod）代码之前执行其他代码。
- 支持监控代码格式检查（lint）和警告（warnings）（可选）；当警告被视作错误（warnings-as-errors）时，会阻止任务的继续执行。
- 通过环境变量（env）或 JSON 文件进行简单的配置。

## 使用方法
```bash
# Define tests in tests/ or specify via --tests
python tdd.py --tests tests/ --run "python your_script.py"
```