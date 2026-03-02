---
name: team-builder
description: 在 OpenClaw 上部署一个多代理的 SaaS 成长团队，该团队具备共享工作空间、异步收件箱通信功能、定时任务处理能力，并支持可选的 Telegram 集成。适用于用户需要创建 AI 代理团队、构建多代理系统、设置增长/营销/产品团队，或为 SaaS 产品矩阵部署代理的场景。支持自定义团队名称、代理角色、模型、时区以及 Telegram 机器人。
---
# 团队构建器

能够一次性在 OpenClaw 上部署一个包含 7 个代理的 SaaS 成长团队。

## 系统影响与先决条件

> **运行前请阅读。** 该功能会创建文件并修改系统配置。

### 创建的内容
- 一个新的工作区目录，其中包含约 40 个文件（代理配置、共享知识、收件箱、看板）
- `apply-config.js` – 一个脚本，用于修改 `~/.openclaw/openclaw.json`（添加代理、绑定关系以及代理间的通信配置）。在写入之前会自动备份。
- `create-crons.ps1` / `create-crons.sh` – 两个脚本，用于通过 `openclaw cron add` 命令创建定时任务。
- 运行这些脚本后，必须**重启网关**（使用 `openclaw gateway restart` 命令）。

### 该功能不会自动执行的内容
- 不会直接修改 `openclaw.json` 文件 – 需要手动运行 `apply-config.js`。
- 不会自动创建定时任务 – 需要手动运行定时任务脚本。
- 不会自动重启网关 – 需要手动执行重启操作。

### 可选功能：Telegram
- 如果在设置过程中提供了 Telegram 机器人令牌，`apply-config.js` 也会添加 Telegram 账户的配置和绑定关系。
- 需要：来自 @BotFather 的 Telegram 机器人令牌，以及您的 Telegram 用户 ID。
- 需要：能够访问 Telegram API（代理可以通过代理配置进行代理设置）。

### 可选功能：ACP / Claude Code
- 全栈开发代理被配置为通过 ACP 生成 Claude Code 以执行复杂的编码任务。
- 需要：在 OpenClaw 环境中配置了兼容 ACP 的编码代理。
- 如果不使用此功能，则无需额外设置。

### 所涉及的凭证
- **Telegram 机器人令牌**（可选） – 存储在 `openclaw.json` 中，用于代理与 Telegram 之间的通信。
- **模型 API 密钥** – 必须已在 OpenClaw 的模型提供者中配置（此功能不负责处理这些密钥）。

### 建议操作
- 运行前请查看生成的 `apply-config.js` 文件。
- 运行后请检查 `openclaw.json` 的备份情况。
- 在启用所有定时任务之前，先用 2-3 个代理进行测试。

## 团队架构

默认的 7 代理 SaaS 成长团队（可扩展至 2-10 个代理）：

```
CEO
 |-- Chief of Staff (dispatch + strategy + efficiency)
 |-- Data Analyst (data + user research)
 |-- Growth Lead (GEO + SEO + community + social media)
 |-- Content Chief (strategy + writing + copywriting + i18n)
 |-- Intel Analyst (competitor monitoring + market trends)
 |-- Product Lead (product management + tech architecture)
 |-- Fullstack Dev (full-stack dev + ops, spawns Claude Code with role-based prompts)
```

### 多团队支持

一个 OpenClaw 实例可以运行多个团队：

```bash
node <skill-dir>/scripts/deploy.js                  # default team
node <skill-dir>/scripts/deploy.js --team alpha      # named team "alpha"
node <skill-dir>/scripts/deploy.js --team beta       # named team "beta"
```

每个团队使用带有前缀的代理 ID（例如 `alpha-chief-of-staff`、`beta-growth-lead`）以避免冲突。每个团队都有自己的工作区子目录。

### 灵活的团队规模

向导允许您从可用的角色中选择 2-10 个代理。可以选择不需要的角色。默认的 7 代理配置适用于大多数 SaaS 场景，但您也可以根据需要减少代理数量（例如 3-4 个代理），或通过自定义角色进行扩展。

### 模型自动检测

向导会扫描您的 `openclaw.json` 文件中的已注册模型提供者，并根据角色类型自动推荐合适的模型：

| 角色类型 | 适用场景 | 自动检测模式 |
|-----------|----------|-------------------|
| 思维型 | 战略角色（如首席、增长团队、内容团队、产品团队） | `/glm-5\|opus\|o1\|deepthink/i` |
| 执行型 | 运营角色（如数据分析师、情报分析师、全栈开发人员） | `/glm-4\|sonnet\|gpt-4/i` |
| 快速型 | 需要快速处理的任务 | `/flash\|haiku\|mini/i` |

您也可以手动指定模型 ID。

## 部署流程

### 第一步：收集配置信息

向用户请求以下配置信息（如果未提供则使用默认值）：

| 参数 | 默认值 | 说明 |
|-----------|---------|-------------|
| 团队名称 | Alpha Team | 用于所有文档和配置文件中 |
| 工作区目录 | `~/.openclaw/workspace-team` | 共享工作区的根目录 |
| 时区 | Asia/Shanghai | 用于定时任务的调度 |
| 早晨简报时间 | 8 | 首席的早晨汇报时间 |
| 傍晚简报时间 | 18 | 首席的傍晚汇报时间 |
| 思维型模型 | zai/glm-5 | 适用于战略角色 |
| 执行型模型 | zai/glm-4.7 | 适用于执行角色 |
| CEO 称谓 | Boss | 代理在报告中使用的称呼 |

可选参数：Telegram 用户 ID、代理设置代理（proxy）以及 7 个 Telegram 机器人令牌。

### 第二步：运行部署脚本

```bash
node <skill-dir>/scripts/deploy.js
```

该步骤为交互式操作，会询问第一步中的所有问题，并生成完整的工作区配置。

### 第三步：应用配置

```bash
node <workspace-dir>/apply-config.js
```

将代理信息添加到 `openclaw.json` 中，同时保留原有的配置。

### 第四步：创建定时任务

```bash
# Windows
powershell <workspace-dir>/create-crons.ps1

# Linux/Mac
bash <workspace-dir>/create-crons.sh
```

### 第五步：重启网关

```bash
openclaw gateway restart
```

### 第六步：填写业务信息

用户需要编辑以下文件：
- `shared/decisions/active.md` – 战略计划和优先事项
- `shared/products/_index.md` – 产品信息、关键词、竞争对手信息
- `shared/knowledge/competitor-map.md` – 竞争对手分析
- `shared/knowledge/tech-standards.md` – 编码标准

## 定时任务安排

| 时间 | 代理 | 任务 | 执行频率 |
|--------|-------|------|-----------|
| 上午 | 数据分析师 | 数据分析 + 用户反馈 | 每日 |
| 上午 | 情报分析师 | 竞争对手分析 | 每周一、周三、周五 |
| 上午 | 首席 | 早晨简报 | 每日 |
| 下午 | 成长团队负责人 | 地理位置分析 + SEO + 社区活动 | 每日 |
| 下午 | 内容负责人 | 每周内容计划 | 每周一 |
| 下午 | 首席 | 傍晚简报 | 每日 |

（H = 早晨简报时间）

## 生成的文件结构

```
<workspace>/
├── AGENTS.md, SOUL.md, USER.md  (auto-injected)
├── apply-config.js, create-crons.ps1/.sh, README.md
├── agents/<7 agent dirs>/       (SOUL.md + MEMORY.md + memory/)
└── shared/
    ├── briefings/, decisions/, inbox/
    ├── data/                        (public data pool, data-analyst writes, all read)
    ├── kanban/, knowledge/, products/
```

## 知识管理

每个共享知识文件都有指定的所有者。只有所有者代理才能更新文件，其他代理只能阅读文件内容。

| 文件 | 所有者 | 更新触发条件 |
|------|-------|---------------|
| geo-playbook.md | growth-lead | 在完成地理位置分析或发现新信息后 |
| seo-playbook.md | growth-lead | 在完成 SEO 分析后 |
| competitor-map.md | intel-analyst | 在每次完成竞争对手分析后 |
| content-guidelines.md | content-chief | 在确定新的写作模式后 |
| user-personas.md | data-analyst | 在获得新的用户反馈后 |
| tech-standards.md | product-lead | 在确定新的编码标准后 |

### 更新规则
更新知识文件时，所有者必须：
1. 在文件顶部添加日期戳：`## [YYYY-MM-DD] <更新内容>`
2. 说明更新原因并提供数据依据
3. 未经 CEO 批准，不得删除现有内容（只能添加新内容，不得替换原有内容）

### 首席的职责
首席在每周的审查中负责监督知识文件的更新情况：
- 文件是否定期更新？
- 文件之间是否存在冲突？
- 是否有需要归档的过时内容？

## 自我进化机制

代理会通过反馈循环逐渐改进自己的策略：

```
1. Execute task (cron or inbox triggered)
2. Collect results (data, metrics, outcomes)
3. Analyze: what worked vs what didn't
4. Update knowledge files with proven strategies (with evidence)
5. Next execution reads updated knowledge → better performance
```

这并不意味着代理会随意更改规则。更新内容必须满足以下要求：
- **基于数据**：有具体的数据支持或实际结果作为依据
- **逐步进行**：只添加新的发现，不要完全重写原有内容
- **可追溯**：记录更新时间和证据，以便其他人验证

### 代理可以自行更新的文件
- 他们自己的知识文件（根据上述的所有者列表）
- 他们自己的 `MEMORY.md` 文件（记录学习内容和决策）
- `shared/data/outputs` 文件（仅限数据分析师）

### 需要 CEO 批准的操作
- 修改 `shared/decisions/active.md` 文件中的战略内容
- 添加或删除代理，或调整团队架构
- 外部发布或支出相关的决策

## 公共数据层

`shared/data/` 目录作为所有代理的只读数据存储库：
- **数据分析师**：写入每日指标、用户反馈摘要、异常警报
- **所有代理**：用于参考自己的决策
- 文件格式：结构化的 Markdown 或 JSON 格式，文件名包含日期（例如 `metrics-2026-03-01.md`）
- 保留期限：保留 30 天，过期的文件将被归档

## 关键设计决策
- **共享工作区**：确保所有代理都能访问所有文件
- **异步收件箱**（使用 `shared/inbox/to-*.md` 而不是 `agentToAgent`，以节省代理令牌并便于审计）
- **首席作为 CEO 与团队之间的沟通枢纽**
- **地理位置分析（GEO）是首要任务**（利用 AI 进行搜索，以开拓新市场）
- **全栈开发人员可以通过 ACP 生成 Claude Code 来处理复杂任务**

## 自定义设置
- 可以通过编辑 `scripts/deploy.js` 文件中的 `ROLES` 数组来添加或删除代理。
- 可以编辑 `references/soul-templates.md` 文件来修改 SOUL.md 模板。
- 可以编辑 `references/shared-templates.md` 文件来修改共享文件的模板。