---
name: agentic-governance
version: 1.3.0
description: 保持约束条件的有效性——通过自动检测数据过时性来实现生命周期管理
author: Live Neon <contact@liveneon.dev>
homepage: https://github.com/live-neon/skills/tree/main/agentic/governance
repository: leegitw/agentic-governance
license: MIT
tags: [agentic, governance, lifecycle, maintenance, health-checks, observability, compliance, staleness]
layer: governance
status: active
alias: gov
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

该技能集涵盖了约束管理的状态监控、定期审查、索引生成、双向验证以及架构迁移等功能，整合了原有的6个独立技能。

**触发条件**：定期维护（periodic maintenance）或HEARTBEAT事件。

**依赖组件**：
- `leegitw/constraint-engine`（用于存储约束数据）
- `leegitw/failure-memory`（用于存储观察数据）

**独立使用说明**：
- 索引生成和双向验证功能可独立运行；但完整的治理功能需要`constraint-engine`和`failure-memory`的集成。

**数据处理说明**：
该技能在代理的权限范围内执行操作。触发后，它会使用代理配置的模型进行治理分析和审查，不会调用任何外部API或第三方服务。所有结果会被保存在工作区的`output/governance/`目录下。

## 功能说明

长期未被审查的约束会变得过时，未被质疑的规则可能沦为固执的教条。该技能负责管理约束的生命周期，包括：
1. **状态跟踪**：记录约束当前是处于活动状态、暂停状态还是已退役状态。
2. **定期审查**：每90天对约束进行重新评估，以确保其仍然符合当前的需求。
3. **索引生成**：生成可视化界面，以便快速查看约束的运行状况。

**核心理念**：
良好的治理是主动的——约束不仅需要创建，还需要持续的维护。

## 使用方法

（具体使用方法请参见相应的子命令部分。）

## 子命令

| 命令            | 中文            | 逻辑                | 触发条件            |
|------------------|------------------|------------------|------------------|
| `/gov state`       | 状态查询           | 获取当前治理状态           | HEARTBEAT            |
| `/gov review`       | 审查             | 将待审查的约束加入审查队列       | HEARTBEAT            |
| `/gov index`       | 生成索引           | 从技能文件生成索引文件       | 显式调用             |
| `/gov verify`       | 验证             | 检查源文件与编译后的文件是否一致 | 显式调用             |
| `/gov migrate`       | 迁移架构版本         | 将架构版本从v(n)升级到v(n+1)    | 显式调用             |

## 参数说明

### `/gov state` 命令

| 参数            | 是否必填            | 说明                |
|------------------|------------------|------------------|
| --summary       | 否               | 仅显示摘要（默认显示全部状态）     |
| --alerts        | 否               | 仅显示待处理的警报         |

### `/gov review` 命令

| 参数            | 是否必填            | 说明                |
|------------------|------------------|------------------|
| --due           | 否               | 仅显示即将到期的审查任务       |
| --all           | 否               | 显示所有需要审查的约束         |
| --complete       | 否               | 将审查标记为已完成         |

### `/gov index` 命令

| 参数            | 是否必填            | 说明                |
|------------------|------------------|------------------|
| --path          | 否               | 输出路径（默认：`agentic/INDEX.md`）     |
| --format        | 否               | 格式：`markdown`（默认）或`json`     |

### `/gov verify` 命令

| 参数            | 是否必填            | 说明                |
|------------------|------------------|------------------|
| source           | 是               | 源文件或目录           |
| compiled        | 是               | 编译后的文件或目录         |
| --strict         | 否               | 发现任何差异即视为验证失败       |

### `/gov migrate` 命令

| 参数            | 是否必填            | 说明                |
|------------------|------------------|------------------|
| --to            | 目标架构版本         | 目标架构版本           |
| --dry-run        | 否               | 显示迁移方案但不执行实际迁移       |

## 配置说明

配置信息按优先级顺序从以下文件加载：
1. `.openclaw/governance.yaml`（OpenClaw标准配置）
2. `.claude/governance.yaml`（Claude代码兼容性配置）
3. 系统默认配置

### 治理状态模型（Core Governance Model）

### 审查周期

约束需要定期进行审查。审查的频率可以自定义（默认为每90天一次）：

| 自上次审查以来的天数 | 状态                | 应采取的行动          |
|------------------|------------------|----------------------|
| 0-75            | 当前状态             | 无需特殊操作           |
| 76-90            | 即将到期             | 发出警告             |
| 91+            | 过期                 | 提升警报             |

> **注意**：此审查周期不会被程序强制执行，合规性依赖于HEARTBEAT P3检查及人工审核。
> 自动化审查功能（`/gov review --automated`）计划在未来的版本中实现。
> 详细审查计划请参考HEARTBEAT.md文件。

### 约束采用情况监控

监控不同会话中约束的采用情况：

| 指标                | 计算方法            | 目标值                |
|------------------|------------------|----------------------|
| 采用率            | 使用约束的会话数 / 总会话数     | >80%                 |
| 违规率            | 违规次数 / 总检查次数     | <5%                 |
| 覆盖率            | 被覆盖的约束数 / 违规次数     | <20%                 |

### 前缀规范

用于标识不同类型数据的标准化前缀：

| 前缀            | 所属领域            | 示例                  |
|------------------|------------------|----------------------|
| `git-*`           | 版本控制            | git-commit-message, git-branch-naming   |
| `test-*`           | 测试                | test-before-commit, test-coverage     |
| `workflow-*`           | 工作流程            | workflow-pr-review, workflow-deploy     |
| `security-*`           | 安全                | security-no-secrets, security-auth     |
| `docs-*`           | 文档                | docs-update-readme, docs-api       |
| `quality-*`           | 代码质量            | quality-lint, quality-format       |

## 输出结果

- `/gov state` 命令的输出结果
- `/gov review` 命令的输出结果
- `/gov index` 命令的输出结果
- `/gov verify` 命令的输出结果
- `/gov migrate` 命令的输出结果

### 示例用法

- **合规性审查示例**
- **安全审计准备示例**

## 集成关系

- **所属层级**：治理层（Governance Layer）
- **依赖组件**：`constraint-engine`（用于存储约束数据）、`failure-memory`（用于存储观察数据）
- **使用场景**：作为顶层治理工具（Used by: Top-level governance）

## 错误处理机制

- 如果输入无效的子命令，系统会列出可用的子命令选项。
- 如果系统中未找到约束，系统会显示提示信息：“系统中没有约束数据”。
- 如果状态文件损坏，系统会从约束数据文件重新生成索引。
- 在迁移过程中如果发现冲突，系统会显示冲突内容并需要手动解决。

## 后续操作

- 当有待处理的审查任务时，系统会自动处理这些任务并更新约束的生命周期信息。
- 如果有未处理的警报，系统会通知用户并跟踪处理进度。
- 如果索引文件过时，系统会重新生成索引文件。
- 如果检测到数据不一致（即“数据漂移”），系统会进行调查并协调解决。

## 工作区文件

该技能会读取和写入以下文件：
- `.openclaw/governance.yaml` 和 `.claude/governance.yaml` 中的配置文件
- `output/constraints/` 目录中的约束数据（通过`constraint-engine`获取）
- `.learnings/` 目录中的观察数据（通过`failure-memory`获取）
- 自定义的输出目录 `output/governance/`

**安全注意事项**：
- 该技能会访问以下文件：
  - `.openclaw/governance.yaml` 和 `.claude/governance.yaml` 中的配置文件
  - `output/constraints/` 目录中的约束数据
  - `output/governance/` 目录中的输出文件
- 但是不会访问工作区之外的文件、系统环境变量或外部API。

**其他限制**：
- 该技能不会向外部服务发送数据，也不会执行任意代码，也不会修改工作区之外的文件。

**依赖说明**：
- 该技能需要`constraint-engine`和`failure-memory`组件的支持才能正常运行。请确保这两个组件已安装。

**验收标准**：
- `/gov state` 能够显示完整的治理状态信息。
- `/gov review` 能够列出即将到期的审查任务。
- `/gov review` 能够提供明确的更新或退役选项。
- `/gov index` 能够从技能配置文件生成索引文件。
- `/gov verify` 能够检测源文件与编译后的文件之间的差异。
- `/gov migrate` 能够处理架构版本的迁移。
- 系统能够跟踪并报告约束的采用情况。
- 所有工作区文件都遵循规定的结构。

*该技能集整合自原有的6个独立技能，完成时间：2026年2月15日。*