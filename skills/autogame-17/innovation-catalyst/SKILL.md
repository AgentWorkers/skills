# 创新催化剂

该工具分析系统状态（内存、工具、事件），并生成战略性的创新提案，以打破进化过程中的停滞局面。

## 主要功能

- **差距分析：**识别技能领域中的不足之处。
- **停滞检测：**发现被阻塞的任务或反复出现的故障。
- **战略提案：**提出可操作的改进建议（如学习新技能、优化流程或进行结构调整）。
- **与 Feishu 系统集成：**生成详细的 Feishu 报告。

## 使用方法

```bash
# Run manually
node skills/innovation-catalyst/index.js

# Target a specific user/group
node skills/innovation-catalyst/index.js --target "ou_xxx"
```

## 协议集成

当系统检测到“稳定成功阶段”（`stable_success_plateau`）时，该技能会由 `gene_gep_innovate_from_opportunity` 基因触发，为后续的进化周期提供必要的“启动点”。

## 所需依赖模块

- `skills/feishu-evolver-wrapper/feishu-helper.js`（用于发送 Feishu 报告）
- 系统内存文件（`MEMORY.md`、`TOOLS.md`、`RECENT_EVENTS.md`）