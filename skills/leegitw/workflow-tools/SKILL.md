---
name: workflow-tools
version: 1.4.0
description: 通过循环检测、并行决策以及文件大小分析，更高效地开展工作。
author: Live Neon <contact@liveneon.dev>
homepage: https://github.com/live-neon/skills/tree/main/agentic/workflow-tools
repository: leegitw/workflow-tools
license: MIT
tags: [agentic, workflow, automation, orchestration, parallel, decision-making, loops, task-management]
layer: extensions
status: active
alias: wt
metadata:
  openclaw:
    requires:
      config:
        - .openclaw/workflow-tools.yaml
        - .claude/workflow-tools.yaml
      workspace:
        - output/loops/
        - output/parallel-decisions/
        - output/mce-analysis/
        - output/subworkflows/
---
# 工作流工具（Workflow Tools）

这是一套统一的工作流辅助工具集合，包括开环检测、并行/串行决策框架、MCE文件分析以及子工作流的生成等功能。这些工具整合了原有的四项独立技能。

**触发方式**：需要通过明确的命令进行调用。

**基础技能**：`loop-closer`、`parallel-decision`、`MCE`（最小上下文工程，Minimal Context Engineering）、`subworkflow-spawner`。

**已移除的技能**：`pbd-strength-classifier`（因与`/fm classify`功能重复而被移除）。

## 安装

```bash
openclaw install leegitw/workflow-tools
```

**依赖项**：
- `leegitw/failure-memory`（用于处理循环相关的数据）
- `leegitw/constraint-engine`（用于实施相关规则）

```bash
# Install with dependencies
openclaw install leegitw/context-verifier
openclaw install leegitw/failure-memory
openclaw install leegitw/constraint-engine
openclaw install leegitw/workflow-tools
```

**独立使用方式**：
- `loop-closer`用于检测循环；`parallel-decision`用于决策判断；`MCE`用于文件大小分析。这些工具可独立使用。
- 当它们被集成后，可以提供基于约束条件的工作流建议。

**数据处理**：
该工具在代理的权限范围内运行。触发后，它会使用代理配置的模型来进行工作流分析和决策支持，不会调用任何外部API或第三方服务。分析结果会被保存在工作区的`output/`子目录中。

**⚠️ 文件访问**：
- `wt loops`命令会读取用户指定的目录和文件进行分析：
  - `/wt loops [path]`：扫描指定的目录（默认为当前工作目录）
  - `/wt mce <file>`：读取指定的文件以进行大小分析
  元数据中仅包含配置路径和输出路径的声明。详情请参见“安全注意事项”。

## 解决的问题**

工作流中常常会出现一些问题，比如循环无法结束、需要决定是并行执行还是串行执行、文件体积过大等。这套工具提供了针对这些常见问题的解决方案：
1. **循环检测**：在标记任务完成之前，会识别出`DEFERRED`（延迟）、`PLACEHOLDER`（占位符）和`TODO`（待办）等标记。
2. **并行决策**：提供一个五因素框架，用于判断何时适合采用并行或串行方式。
3. **MCE分析**：识别出文件大小超过阈值的文件，并提出分割建议。

**设计理念**：
这些工具专注于单一功能，避免过度复杂化工作流的处理流程——只需完成检测、决策、分析，然后继续执行下一步操作。

## 使用方法

```
/wt <sub-command> [arguments]
```

## 子命令

| 命令            | 中文            | 逻辑                | 触发条件            |
|-----------------|------------------|------------------|-------------------|
| `/wt loops`        | 循环检测          | 扫描文件中的延迟/占位符/待办标记→返回开环列表 | 明确调用            |
| `/wt parallel`       | 并行决策          | 根据五因素框架判断并行或串行方式 | 明确调用            |
| `/wt mce`        | 文件大小分析        | 文件行数超过200行→返回分割建议   | 明确调用            |
| `/wt subworkflow`      | 生成子工作流        | 将任务分配给指定的ClawHub技能   | 明确调用            |

## 参数

### `/wt loops`

| 参数            | 是否必填            | 说明                |
|-----------------|------------------|----------------------|
| path            | 否                | 要扫描的目录（默认为当前工作目录）     |
| --pattern        | 否                | 用于检测的自定义模式（逗号分隔）     |
| --exclude        | 否                | 要排除的目录路径（逗号分隔）     |

### `/wt parallel`

| 参数            | 是否必填            | 说明                |
|-----------------|------------------|----------------------|
| task            | 是                | 需要分析的任务描述         |
| --factors        | 否                | 需要评估的具体因素（默认为全部5个）     |

### `/wt mce`

| 参数            | 是否必填            | 说明                |
|-----------------|------------------|----------------------|
| file            | 是                | 需要分析的文件           |
| --threshold       | 否                | 文件行数阈值（默认为200行）       |
| --suggest        | 否                | 是否生成分割建议           |

### `/wt subworkflow`

| 参数            | 是否必填            | 说明                |
|-----------------|------------------|----------------------|
| task            | 是                | 需要执行的任务描述         |
| --skill          | 否                | 要使用的ClawHub技能         |
| --background       | 否                | 是否在后台执行           |

## 配置

配置文件按优先级顺序加载：
1. `.openclaw/workflow-tools.yaml`（OpenClaw标准配置）
2. `.claude/workflow-tools.yaml`（Claude代码兼容配置）
3. 系统默认配置

```yaml
# .openclaw/workflow-tools.yaml
loops:
  patterns:                  # Patterns to detect as open loops
    - "TODO:"
    - "FIXME:"
    - "HACK:"
    - "XXX:"
    - "DEFERRED:"
    - "PLACEHOLDER:"
  exclude:                   # Paths to exclude from scanning
    - "vendor/"
    - "node_modules/"
mce:
  threshold: 200             # Line threshold for MCE compliance
  warning_threshold: 300     # Line threshold for warning
parallel:
  default_factors: 5         # Number of factors to evaluate
```

### 核心逻辑

#### 开环检测

检测未完成的任务：
- 根据以下模式识别未完成的任务：
  - `DEFERRED:`：延迟处理的任务
  - `PLACEHOLDER:`：临时代码
  - `TODO:`：待办任务
  - `FIXME:`：存在问题的代码
  - `HACK:`：技术上的临时解决方案
  - `XXX:`：需要关注的代码

#### 并行与串行决策框架

通过五个因素来判断是否适合并行执行：
- **团队**：不同人员能否独立处理任务？
- **耦合度**：任务之间的依赖关系如何？
- **接口**：任务之间的边界是否清晰？
- **模式**：处理方式是否一致？
- **集成难度**：合并任务的复杂性如何？

根据这些因素，给出是否适合并行的建议：

| 因素          | 判断标准            | 是否适合并行            |
|-----------------|------------------|-------------------|
| 5/5           | 非常适合并行          |
| 4/5           | 需要协调才能并行        |
| 3/5           | 可以根据情况决定是否并行      |
| 2/5           | 建议串行执行          |
| 0-1/5           | 强烈建议串行执行        |

#### MCE（最小上下文工程）

根据文件大小来评估文件是否适合处理：
- 文件行数超过200行时，建议进行重构或分割。

分割建议的依据包括：
- 函数/方法的边界
- 逻辑分组
- 依赖关系
- 测试覆盖范围

#### 生成子工作流

将任务分配给相应的ClawHub技能执行：

```
Task → Skill Selection → Spawn → Monitor → Collect Results
```

**可用的技能类别**：
- `research-*`：调查与分析
- `generate-*`：内容生成
- `validate-*`：验证与测试
- `transform-*`：数据转换

### 示例：工作流分析流程

```
/wt parallel "Deploy new payment service to production"
[PARALLEL VS SERIAL ANALYSIS]
Task: "Deploy new payment service to production"

Factor Analysis:
1. Team: ✗ Serial - Single SRE team handles deploys
2. Coupling: ✗ Serial - Payment depends on auth service
3. Interface: ✓ Parallel - Clear API contracts defined
4. Pattern: ✗ Serial - Requires sequential rollout (canary → staging → prod)
5. Integration: ✗ Serial - Payment gateway integration must be verified

Score: 1/5 factors favor parallel
Recommendation: SERIAL deployment
Rationale: High-risk service requiring careful sequential verification.
```

### 示例：基础设施中的循环检测

```
/wt loops infra/ --pattern "MANUAL:,HARDCODED:"
[OPEN LOOPS DETECTED]
Scanned: ./infra
Files checked: 23

Infrastructure Issues (5):
  infra/terraform/main.tf:45  HARDCODED: AWS region
  infra/k8s/deployment.yaml:78  MANUAL: replica count
  infra/docker/Dockerfile:12  TODO: multi-stage build
  infra/scripts/deploy.sh:34  FIXME: rollback not implemented
  infra/helm/values.yaml:56  PLACEHOLDER: production secrets

Summary: 2 high, 2 medium, 1 low priority
Action: Address HARDCODED and FIXME before next release.
```

## 输出结果

### `/wt loops` 的输出结果

```
[OPEN LOOPS DETECTED]
Scanned: ./src
Files checked: 47

Open loops found (12):

High Priority (FIXME, XXX):
  src/auth/handler.go:45  FIXME: race condition in token refresh
  src/api/client.go:123   XXX: review error handling

Medium Priority (TODO):
  src/handlers/user.go:78  TODO: add input validation
  src/db/queries.go:234    TODO: optimize query
  src/utils/hash.go:12     TODO: add caching

Low Priority (DEFERRED, PLACEHOLDER):
  src/config/loader.go:89  DEFERRED: support YAML config
  src/templates/email.go:34 PLACEHOLDER: email templates
  ...

Summary: 2 high, 5 medium, 5 low priority loops
Action: Address high priority loops before release.
```

### `/wt parallel` 的输出结果

```
[PARALLEL VS SERIAL ANALYSIS]
Task: "Implement authentication and authorization"

Factor Analysis:

1. Team (独立性):
   ✓ Parallel - Auth and authz can be assigned separately

2. Coupling (結合度):
   ✗ Serial - Authz depends on auth tokens

3. Interface (境界):
   ✓ Parallel - Clear token interface between them

4. Pattern (手法):
   ✓ Parallel - Both follow established patterns

5. Integration (統合):
   ✗ Serial - Token format must match exactly

Score: 3/5 factors favor parallel

Recommendation: SERIAL with parallel sub-tasks
Rationale: Core dependency between auth and authz, but sub-components
           within each can be developed in parallel.

Suggested approach:
1. Define token interface (serial, required first)
2. Implement auth + authz (parallel, once interface stable)
3. Integration testing (serial, final step)
```

### `/wt mce` 的输出结果

```
[MCE ANALYSIS]
File: src/handlers/user.go
Lines: 347

Status: ✗ EXCEEDS MCE THRESHOLD (200 lines)

Complexity Analysis:
  Functions: 12
  Avg function length: 29 lines
  Max function length: 67 lines (HandleUserUpdate)
  Import groups: 4

Split Suggestions:

1. Extract CRUD handlers (lines 45-180):
   → src/handlers/user_crud.go (~135 lines)
   - CreateUser, GetUser, UpdateUser, DeleteUser

2. Extract validation (lines 181-250):
   → src/handlers/user_validation.go (~70 lines)
   - ValidateUserInput, ValidateEmail, ValidatePassword

3. Keep orchestration (remaining):
   → src/handlers/user.go (~142 lines)
   - Handler setup, middleware, routing

After split: 3 files, all ≤200 lines ✓
```

### `/wt subworkflow` 的输出结果

```
[SUBWORKFLOW SPAWNED]
Task: "Research competitor authentication implementations"
Skill: research-web-analysis
Status: Running in background

Job ID: SW-20260215-001
Monitor: /wt subworkflow --status SW-20260215-001

Expected completion: ~5 minutes
Results will be written to: output/subworkflows/SW-20260215-001/
```

## 集成

- **依赖关系**：
  - 依赖于`failure-memory`（处理循环相关数据）和`constraint-engine`（实施规则）
  - 被`governance`（用于循环检测）和`review-orchestrator`（用于并行决策）等工具使用

## 可能出现的问题

| 错误情况           | 对应行为                         |
|-----------------|-----------------------------------------|
| 子命令无效         | 显示可用的子命令列表                   |
| 文件未找到         | 错误：“文件未找到：{path}”                     |
| 未找到匹配的模式       | 信息：“未检测到开环”                     |
| 所需技能不可用       | 错误：“所需技能未找到：{skill}”                   |

## 使用后的后续步骤

调用该工具后：
- 如果检测到循环，需优先处理高优先级的循环。
- 如果建议并行执行，创建相应的并行任务流。
- 如果文件大小超过MCE阈值，执行分割建议。
- 如果子工作流完成，需审核并整合结果。

## 工作区文件

该工具会读写以下文件：
- `.openclaw/workflow-tools.yaml`和`.claude/workflow-tools.yaml`中的配置文件
- 通过`/wt loops [path]`读取用户指定的目录（仅用于读取模式）
- 通过`/wt mce <file>`读取用户指定的文件（仅用于大小分析）
- 自定义的输出目录：
  - `output/loops/`：循环检测结果
  - `output/parallel-decisions/`：决策记录
  - `output/mce-analysis/`：文件分析结果
  - `output/subworkflows/`：子工作流输出结果

**⚠️ 重要提示**：
  元数据中仅包含配置路径和输出路径的声明，但`/wt loops`和`/wt mce`会读取用户指定的任意路径（包括超出配置范围的路径）。这是设计上的需求，因为分析需要访问目标文件。
- 该工具不会访问系统环境变量或外部API。
- 该工具不会发送数据到外部服务，也不会执行任意代码，仅进行读取操作。

**路径扫描注意事项**：
- `/wt loops`命令会递归扫描指定目录，包括敏感目录。请使用`--exclude`参数来避免扫描敏感路径。
- `/wt subworkflow`命令会调用系统中安装的ClawHub技能。这些技能会以它们自身的权限运行（不会提升系统权限）。
- 使用`/wt subworkflow`时，请注意权限问题，因为生成的子任务可能具有不同的权限设置。

**来源说明**：
该工具由Live Neon（https://github.com/live-neon/skills）开发，并通过`leegitw`账户发布在ClawHub平台上。维护者相同。

## 验收标准**：
- `/wt loops`能检测所有标准的循环模式。
- `/wt loops`能按优先级对循环进行分类。
- `/wt parallel`能根据五个因素进行判断。
- `/wt parallel`能给出明确的并行建议及理由。
- `/wt mce`能识别出超出大小的文件。
- `/wt mce --suggest`能生成可行的分割建议。
- `/wt subworkflow`能正确生成子工作流。
- `/wt subworkflow`支持在后台执行。
- 所有结果都会保存在工作区文件中。

---

*该工具整合自四个独立技能，发布日期为2026年2月15日。*