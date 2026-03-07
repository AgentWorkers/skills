---
name: team-builder
description: >
  在 OpenClaw 上部署一个多代理的 SaaS 成长团队，该团队具备共享工作空间、异步收件箱通信、定时任务执行（通过 cron 脚本调度）以及深度项目代码扫描（Deep Dive）功能，并支持可选的 Telegram 集成。此方案适用于用户需要创建 AI 代理团队、构建多代理系统、组建增长/营销/产品团队，或为 SaaS 产品矩阵部署代理的情况。系统支持自定义团队名称、代理角色、代码扫描模型以及时区设置，同时支持 Telegram 机器人功能。
  **主要特点：**
  - **多代理架构**：支持多个代理协同工作。
  - **共享工作空间**：团队成员可以实时共享项目信息和资源。
  - **异步通信**：确保团队成员之间的沟通高效且不阻塞其他操作。
  - **定时任务**：通过 cron 脚本自动执行重复性或定时性任务。
  - **深度代码扫描（Deep Dive）**：全栈开发人员会对代码库进行全面扫描，生成包含产品详细信息的文档（如数据库架构、路由规则、模型、服务接口、认证机制、集成情况等）。
  - **Telegram 集成**：支持通过 Telegram 与团队成员进行实时沟通和协作。
  - **可定制性**：允许用户根据需求自定义团队名称、代理角色和代码扫描模型。
  - **全面的产品信息**：生成的文档为所有代理提供决策所需的所有关键信息。
  **应用场景：**
  - **AI 代理团队**：用于开发智能自动化流程。
  - **多代理系统**：构建复杂的多代理系统。
  - **增长/营销/产品团队**：协助提升产品性能和用户满意度。
  - **SaaS 产品矩阵**：为多个 SaaS 产品统一管理代理和任务。
  **适用场景示例：**
  - **企业内部协作**：促进团队成员之间的高效沟通和协作。
  - **产品开发**：帮助开发人员更快地理解产品结构和功能。
  - **项目管理**：确保所有团队成员对项目有统一的认识和理解。
  - **自动化流程**：自动化重复性或定时性任务，提高工作效率。
  通过使用 OpenClaw 和上述功能，用户可以轻松构建和维护一个高效、灵活的多代理 SaaS 团队，从而提升产品开发和运营效率。
---
# 团队构建器

一次性在 OpenClaw 上部署一个包含 7 个代理的 SaaS 成长团队。

## 系统影响与先决条件

> **运行前请阅读。** 此功能会创建文件并修改系统配置。

### 创建的内容
- 一个新的工作区目录，包含约 40 个文件（代理配置、共享知识、收件箱、看板）
- `apply-config.js` – 一个脚本，用于修改 `~/.openclaw/openclaw.json`（添加代理、绑定关系以及代理间的通信配置）。在写入之前会自动备份。
- `create-crons.ps1` / `create-crons.sh` – 两个脚本，用于通过 `openclaw cron add` 命令创建定时任务。
- 运行这些脚本后，必须**重启网关**（`openclaw gateway restart`）。

### 功能不会自动执行的操作
- 不会直接修改 `openclaw.json` – 需要手动运行 `apply-config.js`。
- 不会自动创建定时任务 – 需要手动运行定时任务脚本。
- 不会自动重启网关 – 需要手动执行重启操作。

### 可选功能：Telegram
- 如果在设置过程中提供了 Telegram 机器人令牌，`apply-config.js` 也会添加 Telegram 账户配置和绑定关系。
- 需要：来自 @BotFather 的 Telegram 机器人令牌，以及您的 Telegram 用户 ID。
- 需要：能够访问 Telegram API（代理可通过代理设置代理来配置代理的访问权限）。

### 可选功能：ACP / Claude Code
- 全栈开发代理被配置为通过 ACP 调用 Claude Code 来执行复杂的编码任务。
- 需要：在 OpenClaw 环境中配置了兼容 ACP 的编码代理。
- 如果不使用此功能，则无需额外设置。

### 涉及的凭证
- **Telegram 机器人令牌**（可选） – 存储在 `openclaw.json` 中，用于代理与 Telegram 之间的通信绑定。
- **模型 API 密钥** – 必须已在 OpenClaw 的模型提供者中配置（此功能不负责配置）。

### 建议操作
- 运行前请查看生成的 `apply-config.js` 文件。
- 运行后请检查 `openclaw.json` 的备份情况。
- 在启用所有定时任务之前，先用 2-3 个代理进行测试。

## 团队架构

默认的 7 代理 SaaS 成长团队（可定制为 2-10 个代理）：

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

为避免冲突，每个团队使用带有前缀的代理 ID（例如 `alpha-chief-of-staff`、`beta-growth-lead`）。每个团队都有自己的工作区子目录。

### 灵活的团队规模

向导允许您从可用的角色中选择 2-10 个代理。可以跳过不需要的角色。默认的 7 代理配置适用于大多数 SaaS 场景，但您也可以根据需要减少代理数量（3-4 个代理）或通过自定义角色进行扩展。

### 模型自动检测

向导会扫描您的 `openclaw.json` 中注册的模型提供者，并根据角色类型自动推荐合适的模型：

| 角色类型 | 适用场景 | 自动检测模式 |
|-----------|----------|-------------------|
| 思维型 | 战略性角色（如首席、增长团队、内容团队、产品团队） | `/glm-5\|opus\|o1\|deepthink/i` |
| 执行型 | 运营角色（如数据分析师、情报分析师、全栈开发） | `/glm-4\|sonnet\|gpt-4/i` |
| 快速型 | 轻量级任务 | `/flash\|haiku\|mini/i` |

您也可以手动指定模型 ID。

## 部署流程

### 第一步：收集配置信息

向用户请求以下信息（如果没有提供，则使用默认值）：

| 参数 | 默认值 | 说明 |
|-----------|---------|-------------|
| 团队名称 | Alpha Team | 用于所有文档和配置文件中 |
| 工作区目录 | `~/.openclaw/workspace-team` | 共享工作区的根目录 |
| 时区 | Asia/Shanghai | 用于定时任务的安排 |
| 早晨简报时间 | 8 | 首席的早晨汇报时间 |
| 傍晚简报时间 | 18 | 首席的傍晚汇报时间 |
| 思维模型 | zai/glm-5 | 适用于战略角色 |
| 执行模型 | zai/glm-4.7 | 适用于执行角色 |
| CEO 称谓 | Boss | 代理在通信中如何称呼 CEO |

可选：Telegram 用户 ID、代理设置代理的代理令牌、代理使用的代理。

### 第二步：运行部署脚本

```bash
node <skill-dir>/scripts/deploy.js
```

此步骤为交互式操作，会询问第一步中的所有问题，并生成完整的工作区配置。

### 第三步：应用配置

```bash
node <workspace-dir>/apply-config.js
```

将代理信息添加到 `openclaw.json` 中，同时保留现有的配置。

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
- `shared/decisions/active.md` – 战略计划、优先事项
- `shared/products/_index.md` – 产品信息、关键词、竞争对手信息（包括代码目录路径！）
- `shared/knowledge/competitor-map.md` – 竞争对手分析
- `shared/knowledge/tech-standards.md` – 编码标准

### 第七步：触发深度分析

在填写完产品信息及代码目录后，通知产品负责人触发深度分析：
1. 产品负责人通过收件箱向全栈开发团队发送扫描请求。
2. 全栈开发团队进入每个项目目录并生成知识文件。
3. 产品负责人审核生成的文件是否完整。
4. 所有代理都能获得对项目的深入理解，从而做出更明智的决策。

## 定时任务安排

| 时间 | 代理 | 任务 | 执行频率 |
|--------|-------|------|-----------|
| H-1 | 数据分析师 | 数据分析 + 用户反馈 | 每日 |
| H-1 | 情报分析师 | 竞争对手分析 | 每周一/周三/周五 |
| H | 首席 | 早晨简报 | 每日 |
| H+1 | 成长团队负责人 | 地理位置分析 + SEO + 社区动态 | 每日 |
| H+1 | 内容负责人 | 每周内容计划 | 每周一 |
| H+10 | 首席 | 傍晚简报 | 每日 |

## 生成的文件结构

```
<workspace>/
├── AGENTS.md, SOUL.md, USER.md  (auto-injected)
├── apply-config.js, create-crons.ps1/.sh, README.md
├── agents/<7 agent dirs>/       (SOUL.md + MEMORY.md + memory/)
└── shared/
    ├── briefings/, decisions/, inbox/ (v2: with status tracking)
    ├── status/team-dashboard.md     (chief-of-staff maintains, all agents read first)
    ├── data/                        (public data pool, data-analyst writes, all read)
    ├── kanban/, knowledge/
    └── products/
        ├── _index.md                (product matrix overview)
        ├── _template/               (knowledge directory template)
        └── {product}/               (per-product knowledge, up to 20 files)
            ├── overview.md, architecture.md, database.md, api.md, routes.md
            ├── models.md, services.md, frontend.md, auth.md, integrations.md
            ├── jobs-events.md, config-env.md, dependencies.md, devops.md
            ├── test-coverage.md, tech-debt.md, domain-flows.md, data-flow.md
            ├── i18n.md, changelog.md, notes.md
```

## 知识管理

每个共享知识文件都有指定的所有者。只有所有者代理才能更新文件；其他代理只能阅读文件。

| 文件 | 所有者 | 更新触发条件 |
|------|-------|---------------|
| geo-playbook.md | growth-lead | 在地理位置分析实验或发现新信息后 |
| seo-playbook.md | growth-lead | 在 SEO 实验完成后 |
| competitor-map.md | intel-analyst | 在每次竞争对手分析完成后 |
| content-guidelines.md | content-chief | 在确定写作模式后 |
| user-personas.md | data-analyst | 在获得新的用户洞察后 |
| tech-standards.md | product-lead | 在确定技术架构后 |

### 更新规则
更新知识文件时，所有者必须：
1. 在文件顶部添加日期戳：`## [YYYY-MM-DD] <更新内容>`
2. 说明更新原因并提供数据依据。
3. 未经 CEO 批准，不得删除现有内容（只能追加新内容，不得替换原有内容）。

### 首席的职责
首席在每周的审查中监控知识文件的状态：
- 文件是否定期更新？
- 文件之间是否存在冲突？
- 是否有需要归档的过时内容？

### 自我进化机制

代理通过反馈循环逐步改进自己的策略：

```
1. Execute task (cron or inbox triggered)
2. Collect results (data, metrics, outcomes)
3. Analyze: what worked vs what didn't
4. Update knowledge files with proven strategies (with evidence)
5. Next execution reads updated knowledge → better performance
```

这里的“自我进化”指的是代理根据实际情况动态调整策略，而不是随机更改规则。更新内容必须：
- **基于数据**：有具体的数据支持或实际结果作为依据。
- **逐步进行**：只添加新的发现，不要全部重写。
- **可追溯**：带有日期戳和证据，以便其他人可以验证。

### 代理可以自行更新的文件
- 他们自己的知识文件（根据上述的所有者列表）。
- 他们自己的 `MEMORY.md` 文件（记录学习内容和决策）。
- `shared/data/` 目录中的输出文件（仅限数据分析师更新）。

### 需要 CEO 批准的操作
- `shared/decisions/active.md`（战略计划的更改）。
- 添加/删除代理或调整团队架构。
- 外部发布或支出相关的决策。

## 公共数据层

`shared/data/` 目录作为所有代理的只读数据源：
- **数据分析师**：写入每日指标、用户反馈摘要、异常警报。
- **所有代理**：阅读这些数据以辅助决策。
- 格式：结构化的 Markdown 或 JSON 格式，文件名包含日期（例如 `metrics-2026-03-01.md`）。
- 保留期限：保留 30 天，旧文件会被归档。

## 项目深度分析——代码扫描

代理可以通过自动化代码扫描深入了解每个 SaaS 产品。这一点非常重要——没有深入的项目理解，团队的决策将仅停留在表面。

### 工作原理
1. CEO 在 `shared/products/_index.md` 中添加产品信息（名称、URL、代码目录、技术栈）。
2. 产品负责人通过收件箱向全栈开发团队发送扫描请求。
3. 全栈开发团队进入项目目录（仅限读取）并扫描代码库。
4. 生成的知识文件会被保存在 `shared/products/{product}/` 目录下。
5. 所有代理在做出与产品相关的决策前都会阅读这些文件。

### 产品知识目录

每个产品都有一个包含最多 20 个文件的知识目录：

```
shared/products/{product}/
├── overview.md          ← Product positioning (from _index.md)
├── architecture.md      ← System architecture, tech stack, design patterns, layering
├── database.md          ← Full table schema, relationships, indexes, migrations
├── api.md               ← API endpoints, params, auth, versioning
├── routes.md            ← Complete route table (Web + API + Console)
├── models.md            ← ORM relationships, scopes, accessors, observers
├── services.md          ← Business logic, state machines, workflows, validation
├── frontend.md          ← Component tree, page routing, state management
├── auth.md              ← Auth scheme, roles/permissions matrix, OAuth
├── integrations.md      ← Third-party: payment/email/SMS/storage/CDN/analytics
├── jobs-events.md       ← Queue jobs, event listeners, scheduled tasks, notifications
├── config-env.md        ← Environment variables, feature flags, cache strategy
├── dependencies.md      ← Key dependencies, custom packages, vulnerabilities
├── devops.md            ← Deployment, CI/CD, Docker, monitoring, logging
├── test-coverage.md     ← Test strategy, coverage, weak spots
├── tech-debt.md         ← TODO/FIXME/HACK inventory, dead code, complexity hotspots
├── domain-flows.md      ← Core user journeys, domain boundaries, module coupling
├── data-flow.md         ← Data lifecycle: external → import → process → store → output
├── i18n.md              ← Internationalization, language coverage
├── changelog.md         ← Scan diff log (what changed between scans)
└── notes.md             ← Agent discoveries, gotchas, implicit rules
```

### 扫描级别

| 扫描级别 | 扫描范围 | 扫描时机 | 扫描结果 |
|-------|-------|------|--------|
| L0 快照 | 基础信息：目录结构、包、环境配置 | 初始设置时 | 架构、依赖关系、环境配置 |
| L1 框架结构 | 数据库、路由、模型、组件 | 初始设置时 | 数据库、路由、API、模型、前端 |
| L2 深度分析 | 服务、认证机制、任务流程、集成 | 根据需要 | 服务、认证机制、任务流程、集成、数据流 |
| L3 健康检查 | 技术债务、测试、安全性 | 定期/发布前 | 技术债务、测试覆盖率、DevOps 状态 |
| L4 增量分析 | 代码变更后的差异更新 | 发生代码变更后 | 日志记录 + 目标文件更新 |

### 内容标准

知识文件不仅记录了现有内容，还解释了其背后的原因：
- **设计决策**：选择这种设计的原因。
- **隐含的业务规则**：代码中隐藏的逻辑（例如，“72 小时后自动取消订单”）。
- **潜在问题**：修改某个模块可能引发的错误。
- **模块间的耦合关系**：修改 A 模块可能对 B 模块产生的影响。
- **性能瓶颈**：常见的性能问题、缺失的索引、性能瓶颈。

### 角色职责

| 角色 | 负责任务 |
|------|---------------|
| 产品负责人 | **管理**：触发扫描、审核质量、确保内容更新及时 |
| 全栈开发团队 | **执行**：进入代码目录、执行扫描、生成/更新知识文件 |
| 所有代理 | **使用**：在做出任何与产品相关的决策前阅读知识文件 |

### 根据技术栈自动选择扫描策略

全栈开发团队会自动识别技术栈，并应用相应的扫描策略：
- **Laravel/PHP**：迁移脚本、路由配置、模型、服务、中间件、策略配置、任务调度、控制台/内核配置。
- **React/Vue**：组件、路由配置、存储库、API 客户端、国际化配置。
- **Python/Django/FastAPI**：模型文件、URL 配置、视图文件、中间件配置、Celery 配置。
- **通用**：项目结构、Git 日志、待办事项/问题记录、环境配置文件、Docker 配置、持续集成配置、测试配置。

## 团队协调机制（版本 2）

### 收件箱协议（版本 2）（状态跟踪）

现在每个收件箱消息都包含一个 `status` 字段：
- `pending` → `received` → `in-progress` → `done`（或 `blocked`）
- 首席会监控超时情况：超过 4 小时的未处理消息需要立即处理。
- 被阻塞超过 8 小时的消息会上报给 CEO。
- 收件人收到消息后必须立即更新状态。

### 团队仪表板（`shared/status/team-dashboard.md`）

首席维护一个实时更新的“进度表”：
- 🔴 紧急/被阻塞的任务
- 📊 每个代理的状态信息（最后的活动时间、当前任务、状态图标）
- 📬 未处理的收件箱信息汇总（所有收件箱中的待处理/被阻塞消息）
- 🔗 代理间的任务链跟踪（任务之间的依赖关系）
- 📅 今日/明天的重点任务

**所有代理在上班时首先会阅读此文件**，以便快速了解团队状况。

### 首席的角色升级

首席从“简报编写者”升级为“活跃的团队协调者”：
- **阻塞任务检测**：监控所有收件箱中超过时效的消息。
- **主动提醒**：向延迟处理的代理发送提醒信息。
- **任务链跟踪**：跟踪多代理之间的协作流程。
- **问题升级**：持续存在的阻塞问题会上报给 CEO。
- **每天执行 4 次检查**（早晨简报、中午检查、下午检查、傍晚简报）。

### 定时任务安排（从 7 个任务增加到 10 个任务）

| 时间 | 代理 | 任务 | 目的 |
|------|-------|------|---------|
| 07:00 | 数据分析师 | 每日 | 数据收集 + 用户反馈扫描 |
| 08:00 | 首席 | 早晨简报 + 状态更新 |
| 09:00 | 成长团队负责人 | 每日 | 地理位置分析/SEO/社区动态 |
| 09:00 | 内容负责人 | 每日 | 内容创作 + 协作 |
| 10:00 | 全栈开发团队 | 每日 | 收件箱信息 + 深度分析 + 开发任务 |
| 12:00 | 首席 | 检查 | 仅进行路由检查 |
| 15:00 | 首席 | 检查 | 仅进行路由检查 |
| 18:00 | 首席 | 晚间简报 | 检查 + 下一天计划 |
| 07:00/10:00/15:00（周一/周三/周五） | 情报分析师 | 每周三次 | 竞争对手分析 |

### 这些变更的重要性

| 变更前 | 变更后 | 影响 |
|--------|-------|--------|
| 收件箱信息混乱 | 收件箱具有状态跟踪功能 | 消息可被及时处理 |
| 首席每天处理两次简报 | 首席每天处理四次简报，及时发现并解决问题 |
| 内容负责人每周处理一次简报 | 每天处理内容相关任务 |
| 无团队仪表板 | 每次会议都有仪表板 | 所有代理都能了解全面情况 |
| 无超时机制 | 自动超时机制确保任务不会遗漏 |

## 关键设计决策
- **共享工作区**：确保所有代理都能访问所有信息。
- **收件箱协议（版本 2）**：带有状态跟踪和超时机制，保证异步通信的可靠性。
- **首席作为协调者**：不仅负责编写简报，还负责发现并解决阻碍团队进展的问题。
- **团队仪表板**：作为团队状态的单一信息来源，由首席每天更新。
- **地理位置分析（GEO）作为首要任务**：利用 AI 进行高效搜索。
- **全栈开发团队通过 ACP 调用 Claude Code**：处理复杂任务。
- **项目深度分析**：让所有代理都能深入了解代码库，而不仅仅是了解产品表面信息。

## 自定义设置
- 在 `scripts/deploy.js` 中修改 `ROLES` 数组以添加或删除代理。
- 修改 `references/soul-templates.md` 文件以调整 SOUL.md 模板。
- 修改 `references/shared-templates.md` 文件以调整共享文件的模板。