---
name: skill-cortex
description: Skill Cortex 是系统的能力核心（即系统执行特定任务的能力基础）。当系统缺乏某种能力时，它会自动从 ClawHub 或 GitHub 上获取相应的技能（即实现该能力的代码或资源），并在使用后将其释放。每次技能的使用都会被 Skill Cortex 学习并巩固；未来遇到相同任务时，系统能够直接执行这些技能，而无需再进行搜索。Skill Cortex 仅管理系统的短期能力记忆，从不干扰系统的长期技能（即长期存储的技能数据）。通过不断的强化与遗忘机制，Skill Cortex 不断重构自身的能力架构，从而实现持续进化。
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - clawhub
---
# Skill Cortex

当已安装的技能无法完成当前任务时，此机制会被触发。如果您能够自行完成任务，请直接执行，无需触发此流程。

Cortex 数据文件：`~/.openclaw/skill-cortex/cortex.json`（数据结构详见 `docs/DESIGN.md`）。

---

## 第一阶段：感知

1. 读取 `cortex.json` 文件（如果文件缺失或损坏，请跳至第 3 步）。
2. 将用户的任务描述与 `sensory.patterns` 中的信号进行语义匹配（无需完全匹配，根据您的判断来评估意图是否一致）。匹配成功后，查找对应的技能区域，根据 `effective_weight`（`effective_weight = weight * max(0.3, 1 - days_since_last_used / 180)` 对候选技能进行排序，过滤掉被禁用的技能以及 `effective_weight` 小于 0.3 的技能，然后进入第二阶段。
3. 如果匹配失败，使用 ClawHub 进行搜索：`clawhub search "<3-5 个英文关键词>"`。仅查看搜索结果摘要，选择最多 **3** 个候选技能。如果相关结果少于 2 个，可补充在 GitHub 上进行搜索（并将该来源标记为“未审核”）。

---

## 第二阶段：验证与授权

### 反射模式（快速路径）

当满足以下所有条件时，可以选择最合适的技能进入反射模式：
- `reflex: true` 且 `effective_weight` ≥ 0.90 且连续成功次数 ≥ 5 次
- **无写入副作用**（`side_effects` 中不包含 `write:`、`delete:`、`shell:` 前缀）
- **版本与存储记录一致**（技能的 slug 和版本号匹配）

在反射模式下，**会跳过执行计划的确认**。但安装技能仍需用户确认：

```
⚡ Skill Cortex reflex: todoist-cli v1.2.0 (96% success rate)
   Task: query today's todos (read-only) | Will install and execute. Say cancel to abort.
```

如果版本发生变化，系统会自动降级为标准模式。

### 标准模式

向用户展示候选技能的信息（名称、描述、评分、下载量、来源、安全扫描状态、使用历史）。**在安装前需获得用户的明确批准**。

如果用户的 `prefrontal.lessons` 中包含与当前任务相关的学习记录，这些记录将保留下来，用于第三阶段。

---

## 第三阶段：执行

### 3.1 安装技能

```bash
clawhub install <slug>
```

如果安装失败，系统会自动切换到下一个候选技能。最多切换 **2** 次，之后停止并报告失败原因。

### 3.2 执行计划

读取已安装技能的 SKILL.md 文件，并向用户展示以下信息：
- 任务步骤概要
- 副作用的严重程度：🟢 仅读 🟡 写入 🔴 破坏性操作 🔑 敏感信息 ⚙️ shell 命令
- 相关的学习记录（如果有）——例如，主动检查是否存在常见的依赖项缺失

在反射模式下，此步骤会被跳过。在标准模式下，系统会等待用户的确认。

### 3.3 执行任务

按照技能的指示完成任务。

### 3.4 失败处理

| 失败类型 | 处理方式 |
|---|---|
| `dependency_missing` | 向用户显示需要安装的依赖项，确认后再继续执行 |
| `api_error` | 等待 3 秒后重试一次 |
| `auth_error` | 提示用户检查凭据，不自动重试 |
| `task_mismatch` | 卸载当前技能，建议切换到下一个候选技能 |
| `runtime_error` | 卸载当前技能，建议切换到下一个候选技能 |

切换候选技能需要用户的同意。如果所有候选技能都失败，系统会提供详细的失败原因及相应的解决方法。

---

## 第四阶段：学习与清理

无论任务是否成功，系统都会执行以下操作：

### 4.1 更新技能权重

- 成功时：`new_weight = old + (1 - old) * 0.15 * (1 / (1 + successes_in_last_7d))`
- 失败时：`new_weight = old * decay`（不同失败类型的权重系数不同：task_mismatch: 0.4 / runtime: 0.6 / auth: 0.8 / dependency: 0.85 / api: 0.9）
新技能的初始权重为 0.5。记录技能文件的字符数（`skill_md_chars`）和版本号（`version`）。
如果该技能对应的区域不存在，系统会创建该区域。同时更新 `last_used`（最后一次使用时间）。

### 4.2 更新感知数据

- 如果任务是通过搜索完成的（即感知匹配失败），从任务描述中提取 2–4 个关键词，并将其添加到对应的技能模式中。注意不要创建重复的模式。
- **实体过滤（强制要求）**：在添加关键词之前，去除所有具体的实体信息（如人名、公司名称、地名、日期、数值、文件名、URL、电子邮件等），仅保留动词和抽象名词。
  **示例**：用户输入“查找 Alice 的 Q3 销售报告”，则应提取的关键词为 `["query", "sales", "report"]`，而不是 `["Alice", "Q3"]`。

### 4.3 更新学习记录

只有在满足特定条件时，才会将学习记录添加到用户的 `prefrontal` 数据中（格式必须规范）：

```jsonc
// Type 1: Same failure type occurs 2+ times → dependency pre-check
{ "type": "dependency_warning", "region": "...", "key": "imagemagick", "action": "check_bin_before_install", "confidence": 0.6 }
// Type 2: Skill description does not match actual capability
{ "type": "skill_quality_warning", "slug": "xxx", "detail": "does not support batch ops", "confidence": 0.6 }
// Type 3: User environment is typically ready
{ "type": "env_ready", "region": "...", "key": "TODOIST_API_KEY", "confidence": 0.6 }
```

每次验证成功后，学习记录的信心值增加 0.1（最大值为 1.0）。在信心值低于 0.3 时，这些记录会被删除。

### 4.4 启用反射模式

当满足以下所有条件时，启用反射模式：成功次数 ≥ 5 次、`effective_weight` ≥ 0.90 且无写入副作用。
在任何失败或版本更新的情况下，系统会立即将 `reflex` 设置为 `false`。

### 4.5 清理操作

- **默认操作**：卸载该技能。使用 `clawhub uninstall <slug>` 命令卸载技能。
- **建议保留技能**：当满足以下条件时：成功次数 ≥ 3 次、`effective_weight` ≥ 0.8 且技能文件的字符数（`skill_md_chars`）小于 8000 个。如果用户同意保留，技能将保持安装状态，并从 `motor` 数据中删除相关记录（由 OpenClaw 的原生管理系统管理）；如果用户拒绝保留，则正常卸载技能。

### 4.6 数据优化

- **技能库优化**：
  - `motor` 每个区域最多保留 5 个候选技能；总共最多保留 80 个区域。
  - 如果某个区域的技能被删除，该区域的模式也会被删除。
  - 每个模式最多保留 10 个关键词。
  - `prefrontal` 数据中最多保留 30 条学习记录；如果相关区域的技能被删除，这些记录也会被删除。

---

## 系统规则

1. 严禁干扰长期使用的技能。
2. 安装任何技能都需要用户的确认（包括在反射模式下）。
3. 安装依赖项需要单独的用户确认。
4. 写入操作永远不会进入反射模式；版本更新会自动降级系统到标准模式。
5. 最多允许切换 2 个候选技能。
6. 如果 Cortex 文件损坏，系统会直接使用 ClawHub 进行搜索，并在任务完成后重新构建 Cortex 数据。
7. 在执行任何操作前，必须读取最新的 Cortex 文件；合并更改内容，切勿覆盖原有数据。
8. 本系统为单会话设计；在多个会话期间，Cortex 数据可能会不一致。