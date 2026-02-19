---
name: agent-audit
description: >
  审核您的人工智能代理设置，以评估其性能、成本和投资回报率（ROI）。该工具会扫描 OpenClaw 的配置文件、定时任务（cron jobs）、会话历史记录以及模型使用情况，找出潜在的浪费并提出优化建议。适用于任何模型提供商（如 Anthropic、OpenAI、Google、xAI 等）。
  使用场景：
  1. 当用户请求“审核我的代理设置”或“优化我的成本”时；
  2. 当用户想知道哪些定时任务的运行成本较高或较低时；
  3. 当用户希望获得模型与任务匹配度的建议时；
  4. 当用户希望对其代理设置进行投资回报率分析时；
  5. 当用户想知道自己在哪些方面浪费了资源（例如 AI 许可证或计算资源）时。
  该工具的功能包括：
  - 检查 OpenClaw 的配置文件，确保所有设置都符合最佳实践；
  - 分析定时任务的执行频率和成本；
  - 评估模型使用情况，识别资源消耗较高的部分；
  - 提供优化建议，以降低运行成本并提高代理性能。
  请注意：该工具仅适用于基于 OpenClaw 构建的人工智能代理系统。
---
# 代理审计

扫描您的整个 OpenClaw 环境，并提供可操作的成本/性能优化建议。

## 该功能的用途

1. **扫描配置** — 读取 OpenClaw 的配置文件，将模型与代理/任务关联起来。
2. **分析 cron 日志** — 检查每个 cron 任务的模型使用情况、运行时间以及成功率。
3. **对任务进行分类** — 确定每个任务的复杂度等级。
4. **计算成本** — 根据提供商的定价标准，计算每个代理、每个 cron 任务以及每种任务类型的成本。
5. **提供改进建议** — 包含建议的置信度等级和风险提示。
6. **生成报告** — 生成包含具体节省金额估算的 markdown 报告。

## 运行审计

```bash
python3 {baseDir}/scripts/audit.py
```

**可选选项：**
```bash
python3 {baseDir}/scripts/audit.py --format markdown    # Full report (default)
python3 {baseDir}/scripts/audit.py --format summary     # Quick summary only
python3 {baseDir}/scripts/audit.py --dry-run             # Show what would be analyzed
python3 {baseDir}/scripts/audit.py --output /path/to/report.md  # Save to file
```

## 工作原理

### 第一阶段：发现
- 读取 OpenClaw 的配置文件（通常位于 `~/.openclaw/openclaw.json`）。
- 列出所有 cron 任务及其配置信息。
- 列出所有代理及其默认使用的模型。
- 从模型名称中识别出所使用的提供商（Anthropic、OpenAI、Google、xAI）。

### 第二阶段：历史数据分析
- 获取过去 7 天内的 cron 任务运行记录。
- 计算每个任务的平均 token 使用量、平均运行时间以及成功率。
- （如可用）获取任务会话历史记录。
- 按模型类型统计总 token 消耗量。

### 第三阶段：任务分类
将每个任务分为不同的复杂度等级：

| 复杂度等级 | 任务示例 | 推荐使用的模型 |
|---------|---------|-------------------|
| **简单** | 健康检查、状态报告、提醒、通知 | 最便宜的模型（如 Haiku、GPT-4o-mini、Flash、Grok-mini） |
| **中等** | 内容草稿、研究、总结、数据分析 | 中等复杂度的模型（如 Sonnet、GPT-4o、Pro、Grok） |
| **复杂** | 编码、架构设计、安全审查、需要细致思考的写作任务 | 最高级别的模型（如 Opus、GPT-4.5、Ultra、Grok-2） |

**分类依据：**
- **简单**：输出较短（<500 个 token），无需大量思考，具有重复性。
- **中等**：需要一定程度的推理能力，内容有一定模板化，属于研究性质的任务。
- **复杂**：输出较长，需要多步骤推理，涉及代码生成或安全关键任务，这些任务在较低级别的模型上可能无法完成。

### 第四阶段：提供改进建议
对于那些模型等级与实际任务复杂度不匹配的任务，系统会给出相应的改进建议：

```
⚠️ RECOMMENDATION: Downgrade "Knox Bot Health Check" from opus to haiku
   Current: anthropic/claude-opus-4 ($15/M input, $75/M output)
   Suggested: anthropic/claude-haiku ($0.25/M input, $1.25/M output)
   Reason: Simple status check averaging 300 output tokens
   Estimated savings: $X.XX/month
   Risk: LOW — task is simple pattern matching
   Confidence: HIGH
```

### 安全规则：**严禁** 下调模型等级：
- 编码/开发任务。
- 安全审查或审计任务。
- 之前在较低级别模型上失败过的任务。
- 用户明确选择了更高级别模型的任务。
- 需要复杂多步骤推理的任务。
- 用户标记为关键性的任务。

### 第五阶段：生成报告
生成一份清晰的 markdown 报告，内容包括：
1. **总体情况**：代理数量、cron 任务数量以及每月的预计成本。
2. **按代理划分的详细信息**：使用的模型、使用频率以及成本。
3. **按 cron 任务划分的详细信息**：使用的模型、执行频率、平均 token 使用量以及成本。
4. **改进建议**：根据节省潜力进行排序。
5. **潜在的总节省金额**：每月的预估节省额。
6. **配置修改建议**：需要更换的具体模型名称。

## 模型定价参考
有关所有提供商的当前定价信息，请参阅 [references/model-pricing.md](references/model-pricing.md)。
请在价格发生变化时更新该文件。

## 任务分类详细信息
有关任务如何被分类为不同复杂度等级的详细规则，请参阅 [references/task-classification.md](references/task-classification.md)。

## 重要说明：
- 该功能仅具有 **读取权限**，不会自动修改您的配置。
- 所有建议都会附带风险等级和置信度评分。
- 如果对任务的复杂度不确定，系统会默认保持当前使用的模型设置。
- 随着使用模式的变化，应定期（每月）重新运行审计。
- Token 计数是基于 cron 日志的估算值，实际成本取决于您的提供商的计费方式。