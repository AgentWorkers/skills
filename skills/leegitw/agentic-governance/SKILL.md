---
name: agentic-governance
version: 1.2.0
description: 保持约束条件的有效性——通过自动检测数据过时性来实现生命周期管理
author: Live Neon <contact@liveneon.dev>
homepage: https://github.com/live-neon/skills/tree/main/agentic/governance
repository: leegitw/agentic-governance
license: MIT
tags: [agentic, governance, state, lifecycle, review]
layer: governance
status: active
alias: gov
disable-model-invocation: true
metadata:
  openclaw:
    requires:
      config:
        - .openclaw/governance.yaml
        - .claude/governance.yaml
      workspace:
        - output/governance/
        - output/constraints/
        - agentic/INDEX.md
---
# 治理（Governance）

该技能负责约束管理的状态监控、定期审查、索引生成、双向验证以及模式迁移等功能，整合了原本分散的6项子技能。

**触发条件**：定期维护（periodic maintenance）或HEARTBEAT事件。

**依赖的子技能**：constraint-reviewer（约束审查工具）、index-generator（索引生成工具）、round-trip-tester（双向验证工具）、governance-state（状态管理工具）、slug-taxonomy（路径命名规则工具）、adoption-monitor（合规性监控工具，来自safety模块）。

## 安装

```bash
openclaw install leegitw/governance
```

**依赖库**：
- `leegitw/constraint-engine`（用于存储约束数据）
- `leegitw/failure-memory`（用于存储观察数据）

**独立使用说明**：
- 索引生成和双向验证功能可以独立运行；但完整的治理功能需要`constraint-engine`和`failure-memory`的集成。

**数据管理说明**：
- 该技能仅用于提供治理相关的模板和审查流程，**不直接调用任何AI模型**。所有结果都会写入工作区的`output/governance/`目录中。该技能仅访问其元数据中指定的路径。

## 功能说明

长期未被审查的约束会变得过时，未被质疑的规则可能成为固定不变的“教条”。该技能管理约束的整个生命周期，包括：
1. **状态跟踪**：记录约束的当前状态（激活、暂停或已退役）。
2. **定期审查**：每90天对约束进行重新评估。
3. **索引生成**：生成可视化仪表板，以便快速查看约束的运行状况。

**核心理念**：良好的治理是主动的——约束不仅需要创建，还需要持续维护。

## 使用方法

```
/gov <sub-command> [arguments]
```

## 子命令

| 命令 | 中文 | 逻辑 | 触发条件 |
|---------|-------|-------|---------|
| `/gov state` | 状态查询 | 查询系统中的约束状态 | HEARTBEAT事件 |
| `/gov review` | 审查请求 | 将待审查的约束添加到审查队列 | HEARTBEAT事件 |
| `/gov index` | 生成索引 | 从技能配置文件生成索引文件 | 显式触发 |
| `/gov verify` | 验证一致性 | 检查源文件与编译后的文件是否一致 | 显式触发 |
| `/gov migrate` | 迁移约束模式 | 将约束模式从版本v(n)升级到v(n+1) | 显式触发 |

## 参数说明

### `/gov state` 命令

| 参数 | 是否必填 | 说明 |
|--------|--------|---------|
| --summary | 否 | 仅显示摘要（默认显示全部状态） |
| --alerts | 否 | 仅显示待处理的警报 |

### `/gov review` 命令

| 参数 | 是否必填 | 说明 |
|--------|--------|---------|
| --due | 否 | 仅显示即将到期的审查任务（默认） |
| --all | 否 | 显示所有需要审查的约束 |
| --complete | 否 | 标记审查任务为已完成 |

### `/gov index` 命令

| 参数 | 是否必填 | 说明 |
|--------|--------|---------|
| --path | 否 | 输出路径（默认为`agentic/INDEX.md`） |
| --format | 否 | 格式：`markdown`或`json`（默认） |

### `/gov verify` 命令

| 参数 | 是否必填 | 说明 |
| source | 是 | 源文件或目录 |
| compiled | 是 | 编译后的文件或目录 |
| --strict | 否 | 发现任何差异即视为验证失败 |

### `/gov migrate` 命令

| 参数 | 是否必填 | 说明 |
| --to | 是 | 目标模式版本 |
| --dry-run | 否 | 显示迁移前的变化（不实际应用更改） |

## 配置方式

配置信息按优先级顺序从以下文件加载：
1. `.openclaw/governance.yaml`（OpenClaw标准配置）
2. `.claude/governance.yaml`（Claude代码兼容性配置）
3. 系统默认配置

## 核心逻辑

### 约束状态管理模型

```
┌─────────────────────────────────────────┐
│           GOVERNANCE STATE               │
├─────────────────────────────────────────┤
│ Constraints:                             │
│   - Active: 5                           │
│   - Draft: 2                            │
│   - Retiring: 1                         │
│   - Retired: 12                         │
├─────────────────────────────────────────┤
│ Reviews:                                 │
│   - Due: 2 (approaching 90-day mark)    │
│   - Overdue: 0                          │
├─────────────────────────────────────────┤
│ Health:                                  │
│   - Circuit: CLOSED                     │
│   - Violations (30d): 3                 │
│   - Adoption rate: 85%                  │
├─────────────────────────────────────────┤
│ Alerts:                                  │
│   - [WARN] CON-001 due for review       │
│   - [INFO] 2 new observations eligible  │
└─────────────────────────────────────────┘
```

### 审查周期

约束需要定期进行审查。审查的频率可以自定义（默认为90天）：

```yaml
# .openclaw/governance.yaml
governance:
  review_cadence_days: 90    # Default
  warning_threshold: 15      # Days before due to warn
```

| 自上次审查以来的天数 | 状态 | 应采取的行动 |
|------------------------|--------|--------|
| 0-75 | 当前状态 | 无需行动 |
| 76-90 | 即将到期 | 发出警告 |
| 91+ | 过期 | 提升警报 |

> **注意**：此审查周期**不通过程序强制执行**，依赖HEARTBEAT P3检查及人工操作。未来计划实现自动化审查功能（`/gov review --automated`）。
> 详细审查计划请参考HEARTBEAT.md文件。

### 合规性监控

跟踪各会话中约束的采用情况：
- **采用率**：使用约束的会话数 / 总会话数 > 80%
- **违规率**：违规次数 / 总检查次数 < 5%
- **覆盖率**：被覆盖的约束数 / 违规次数 < 20%

### 路径命名规则

用于区分观察数据和约束数据的标准化前缀：
- `git-*`：版本控制相关（如`git-commit-message`, `git-branch-naming`）
- `test-*`：测试相关（如`test-before-commit`, `test-coverage`）
- `workflow-*`：工作流程相关（如`workflow-pr-review`, `workflow-deploy`）
- `security-*`：安全相关（如`security-no-secrets`, `security-auth`）
- `docs-*`：文档相关（如`docs-update-readme`, `docs-api`）
- `quality-*`：代码质量相关（如`quality-lint`, `quality-format`）

## 输出结果

### `/gov state` 命令的输出

```
[GOVERNANCE STATE]
Updated: 2026-02-15 10:30:00

=== Constraints ===
Active: 5 | Draft: 2 | Retiring: 1 | Retired: 12

=== Circuit Breaker ===
Status: CLOSED (healthy)
Violations (30d): 3

=== Reviews ===
Due: 2 constraints approaching 90-day mark
  - CON-20251120-001: "Always run tests" (day 87)
  - CON-20251125-003: "Lint before commit" (day 82)

=== Adoption ===
Rate: 85% (target: >80%)
Sessions tracked: 47

=== Alerts ===
[WARN] CON-20251120-001 due for review in 3 days
[INFO] 2 observations eligible for constraint generation
```

### `/gov review` 命令的输出

```
[CONSTRAINT REVIEW QUEUE]

Due for review (2):

1. CON-20251120-001: "Always run tests before commit"
   Age: 87 days | Status: active
   Violations (90d): 2 | Overrides: 0
   Adoption: 92%

   Options:
   a) Renew for 90 days: /ce lifecycle CON-20251120-001 active
   b) Begin retirement: /ce lifecycle CON-20251120-001 retiring
   c) Immediate retire: /ce lifecycle CON-20251120-001 retired

2. CON-20251125-003: "Always lint before commit"
   Age: 82 days | Status: active
   Violations (90d): 5 | Overrides: 1
   Adoption: 78%

   [WARN] Below adoption target (80%)
   Consider: Clarify constraint or improve tooling
```

### `/gov index` 命令的输出

```
[INDEX GENERATED]
Path: agentic/INDEX.md
Skills: 7
Updated: 2026-02-15 10:30:00

Contents:
- failure-memory (fm) - Core
- constraint-engine (ce) - Core
- context-verifier (cv) - Foundation
- review-orchestrator (ro) - Review
- governance (gov) - Governance
- safety-checks (sc) - Safety
- workflow-tools (wt) - Extensions
```

### `/gov verify` 命令的输出

```
[ROUND-TRIP VERIFICATION]
Source: docs/constraints/
Compiled: output/constraints/

Status: ✓ IN SYNC

Files checked: 12
Matches: 12
Drifts: 0
```

### 示例：合规性审查流程

```
/gov review --all
[CONSTRAINT REVIEW QUEUE]

Compliance Status (SOC 2):

1. CON-20260101-001: "Always encrypt PII at rest"
   Age: 45 days | Status: active
   Compliance: SOC 2 CC6.1
   Violations (90d): 0 | Adoption: 100%
   ✓ Compliant

2. CON-20260115-002: "Always log authentication events"
   Age: 31 days | Status: active
   Compliance: SOC 2 CC6.2
   Violations (90d): 1 | Adoption: 98%
   ⚠ Review violation on 2026-02-01

Summary: 12 constraints | 11 compliant | 1 needs review
```

### 示例：安全审计准备流程

```
/gov state --summary
[GOVERNANCE STATE]
Updated: 2026-02-15 14:00:00

Audit Readiness:
  Security constraints: 8 active
  Last review: 2026-02-10
  Violations (90d): 2 (both resolved)
  Override rate: 5% (within policy)

Recommendation: Ready for external audit.
```

## 系统集成

- **所属层级**：治理层（Governance）
- **依赖组件**：`constraint-engine`（存储约束数据）、`failure-memory`（存储观察数据）
- **使用场景**：作为顶层治理工具，用于全局管理约束规则

## 可能出现的错误情况

- **无效的子命令**：列出可用的子命令列表。
- **未找到约束**：提示“系统中不存在约束数据”。
- **状态文件损坏**：从约束数据文件重新构建索引。
- **迁移冲突**：显示冲突情况，需手动解决。

## 后续操作建议

调用该技能后：
- 如果有待审查的约束，需逐一处理并更新其生命周期状态。
- 对于待处理的警报，需通知用户并跟踪处理进度。
- 如果索引文件过时，需重新生成`INDEX.md`文件。
- 如果检测到数据不一致（“漂移”现象），需调查并解决差异。

## 工作区文件

该技能会读取/写入以下文件：
- `.openclaw/governance.yaml`和`.claude/governance.yaml`中的配置文件
- `output/constraints/`中的约束数据（通过`constraint-engine`访问）
- `.learnings/`中的观察数据（通过`failure-memory`访问）
- 自定义的输出目录`output/governance/`

**安全注意事项**：
- 该技能仅访问指定工作区内的文件：
  - `.openclaw/governance.yaml`和`.claude/governance.yaml`中的配置文件
  - `output/constraints/`中的约束数据
  - `output/governance/`中的输出文件
- 该技能**不访问**工作区之外的文件、系统环境变量或外部API。
- 该技能**不执行任何代码**（仅提供指令），也不向外部服务发送数据或修改外部文件。

**依赖说明**：
- 该技能依赖`constraint-engine`和`failure-memory`来获取数据。需同时安装这两个组件才能实现完整功能。

## 验收标准：
- `/gov state`能显示完整的治理状态信息。
- `/gov review`能列出需定期审查的约束。
- `/gov review`能提供明确的续期或退役选项。
- `/gov index`能从SKILL.md文件生成索引。
- `/gov verify`能检测源文件与编译后的文件是否一致。
- `/gov migrate`能处理模式版本的迁移。
- 能跟踪并报告合规性指标。
- 工作区文件的结构需符合文档要求。

---

*该技能整合自2026年2月15日的6个子技能。*