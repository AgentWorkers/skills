# Router NIMIMORE

这是一个专为 OpenClaw 设计的智能模型路由器。它能够根据查询的特点自动选择最合适的 AI 模型，从而在成本和性能之间实现平衡。

## 描述

Router NIMIMORE 会分析您的查询内容，并将其自动路由到最合适的 AI 模型：

- **简单查询** → 经济型模型（节省 85% 的成本）
- **代码相关任务** → 标准型模型（节省 47% 的成本）
- **复杂推理任务** → 高端模型（提供最佳的质量）

## 工具

- `router.select` - 为查询选择最优模型
- `router.analyze` - 分析查询特征
- `router.demo` - 运行路由演示

## 使用方法

```bash
# Route a query
python scripts/router.py --query "帮我写个Python函数"

# Run demo
python scripts/router.py --demo

# With context length
python scripts/router.py --query "总结文档" --context-length 5000
```

## 配置

无需配置，即可直接使用。

## 支持的模型

| 模型 | 等级 | 单次使用成本（美元） | 适用场景 |
|-------|------|-----------------|-------------------|
| moonshot/kimi-k2.5 | 高端 | 0.015 | 复杂推理任务 |
| bailian/qwen-max | 标准型 | 0.008 | 代码处理及中文处理 |
| bailian/qwen-plus | 标准型 | 0.004 | 一般任务 |
| bailian/qwen-turbo | 经济型 | 0.002 | 简单查询 |

## 特点

- ✅ 自动模型选择
- ✅ 查询特征分析
- ✅ 成本优化
- ✅ 支持多个服务提供商
- ✅ 具有上下文感知的路由功能

## 开发者

Franco

## 许可证

MIT-0