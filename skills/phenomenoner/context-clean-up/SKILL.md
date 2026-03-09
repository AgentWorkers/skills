---
name: context-clean-up
slug: context-clean-up
version: 1.0.7
license: MIT
description: >
  **使用场景：** 当提示信息的数量过多（导致回复速度变慢、成本上升或转录结果质量下降）时，且您需要一份按问题严重程度排序的故障列表以及相应的可逆修复方案。  
  **不适用场景：** 当您希望系统自动删除某些数据或进行无人值守的配置修改时。  
  **输出内容：** 仅提供审计报告（包含问题最严重的部分、3-8个风险较低的修复方案以及回滚操作的相关说明）。系统不会自动执行任何修改。
disable-model-invocation: true
allowed-tools:
  - sessions_list
  - sessions_history
  - session_status
metadata: { "openclaw": { "emoji": "🧹", "requires": { "bins": ["python3"] } } }
---
# 上下文清理（仅限审计使用）

该工具用于识别导致提示内容冗余的元素，并将其转化为一个**安全、可逆的优化方案**。

## 合同条款

- **默认仅限审计使用。**
- 不会自动删除任何内容。
- 不会进行无人值守的配置编辑。
- 不会进行后台的定时任务或会话清理操作。
- 如果您请求进行修改，该工具应提供以下信息：
  1. 具体的修改内容
  2. 预期的影响
  3. 回滚方案
  4. 验证步骤

## 安全性要求

- 禁止使用 `exec` 工具。
- 禁止使用 `read` 工具。
- 如果您需要文件级别的分析，请手动运行附带的脚本，并将分析结果以 JSON 格式输出。

## 快速入门

- 使用命令 `/context-clean-up` 可执行审计并生成可操作的优化方案（无需进行任何修改）。

### 可选的手动报告生成：

```text
python3 scripts/context_cleanup_audit.py --out context-cleanup-audit.json
```

### Windows 版本：

```text
py -3 scripts/context_cleanup_audit.py --out context-cleanup-audit.json
```

## 需要监控的指标（基于客观数据，而非主观感受）

在可能的情况下，优先使用最新的会话数据（`/context json`），而非基于主观感受的描述（如“系统看起来更简洁了”）。

**关键监控指标：**
- `eligibleskills`（符合条件的技能）
- `skills.promptChars`（技能提示字符）
- `projectContextChars`（项目上下文字符）
- `systemPromptChars`（系统提示字符）
- `promptTokens`（提示令牌）

如果无法获取准确的监控数据，可以参考问题较为严重的部分以及修改的范围，但请降低评估的准确性。

## 常见问题来源

1. **工具输出冗余**
   - 过大的 `exec` 输出结果
   - 过长的 `read` 输出结果
   - 过长的 `web_fetch` 数据负载

2. **自动化脚本产生的冗余信息**
   - 每次运行都会输出“OK”信息的定时任务
   - 除了警报信息外还包含其他内容的 heartbeat 消息

3. **引导文件（bootstrap）的冗余**
   - 过大的 `AGENTS.md`、`MEMORY.md`、`SOUL.md`、`USER.md` 文件
   - 直接嵌入在 `SKILL.md` 中的冗长运行手册

4. **环境配置中的冗余**
   - 过多始终显示在提示界面中的专业技能，这些技能实际上应该按需调用（即作为工作代理或子代理）

5. **总结信息的重复**
   - 重复的总结内容，其中包含历史细节而非仅与重启相关的关键信息

## 推荐的优化步骤（从低风险开始）

### 第一阶段——减少不必要的自动化输出
- 确保无操作的自动化脚本在成功执行时不会产生任何输出（设置为 `NO_REPLY`）。

### 第二阶段——优化引导文件
- 保持那些始终被注入系统的文件的篇幅较短。
- 将冗长的指导信息移至 `references/`、`memory/` 或外部笔记中。

### 第三阶段——减少环境配置中的冗余
- 从始终显示在提示界面中的专业技能中移除使用频率较低的技能。
- 对于需要专业处理的操作，优先使用工作代理或子代理来执行。

### 第四阶段——进行更高风险的修改
- 对涉及工具界面或运行时配置的修改，需提供更完善的回滚方案，并经过明确批准后才能实施。

## 工作流程（审计 → 生成优化方案）

### 第一步——确定优化范围
您需要以下信息：
- 工作区目录
- 状态目录（`<OPENCLAW_STATE_DIR>`）

**常见默认路径：**
- macOS/Linux：`~/.openclaw`
- Windows：`%USERPROFILE%\.openclaw`

### 第二步——运行审计脚本

```text
python3 scripts/context_cleanup_audit.py --workspace . --state-dir <OPENCLAW_STATE_DIR> --out context-cleanup-audit.json
```

**解读指南：**
- 过大的工具输出结果通常表示自动化脚本产生的冗余
- 大量的定时任务或系统日志通常表示自动化脚本的冗余
- 过长的引导文件通常表示引导文件本身的冗余

### 第三步——生成优化方案
优化方案应包括：
- 主要问题来源
- 优先考虑低风险的优化措施
- 预期的影响
- 回滚方案
- 验证步骤

### 第四步——验证优化效果
修改完成后，请确认：
- 自动化脚本在成功执行时是否不再产生任何输出
- 检查提示内容的增长情况是否有所改善
- 如果可能的话，比较优化前后的最新会话数据（`/context json`）

## 重要提示

OpenClaw 的运行时环境会在每次会话中生成相应的技能和配置信息。
因此，对技能或配置的优化通常**不会完全适用于当前会话**。
请使用新的会话来进行权威性的验证。

## 参考资料
- `references/out-of-band-delivery.md`
- `references/cron-noise-checklist.md`