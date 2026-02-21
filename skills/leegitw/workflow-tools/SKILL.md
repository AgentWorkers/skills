---
name: workflow-tools
version: 1.4.0
description: 通过循环检测、并行处理以及文件大小分析功能，更高效地提升工作效率。
author: Live Neon <contact@liveneon.dev>
homepage: https://github.com/live-neon/skills/tree/main/agentic/workflow-tools
repository: leegitw/workflow-tools
license: MIT
tags: [agentic, workflow, tools, parallel, mce, loops]
layer: extensions
status: active
alias: wt
disable-model-invocation: true
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

这是一套统一的工作流辅助工具集合，包括开环检测、并行/串行决策框架、MCE文件分析以及子工作流的生成等功能，整合了原有的四项独立技能。

**触发方式**：需要通过明确的命令来调用这些工具。

**基础技能**：`loop-closer`、`parallel-decision`、`MCE`（最小上下文工程，Minimal Context Engineering）、`subworkflow-spawner`。

**已移除的技能**：`pbd-strength-classifier`（因与`/fm classify`功能重复而不再使用）。

## 安装

```bash
openclaw install leegitw/workflow-tools
```

**依赖项**：
- `leegitw/failure-memory`（用于处理循环相关的数据）
- `leegitw/constraint-engine`（用于执行相关的约束检查）

```bash
# Install with dependencies
openclaw install leegitw/context-verifier
openclaw install leegitw/failure-memory
openclaw install leegitw/constraint-engine
openclaw install leegitw/workflow-tools
```

**独立使用方式**：
- `loop-closer`用于检测循环；`parallel-decision`用于判断任务应采用并行还是串行执行；`MCE`用于分析文件大小。
- 当这些工具被集成使用时，它们会提供基于约束条件的工作流建议。

**数据处理**：该工具仅用于执行指令（配置选项`disable-model-invocation: true`），它提供工作流辅助功能和分析框架，但本身不调用任何人工智能模型。不会使用外部API或第三方服务。分析结果会被保存在工作区的`output/`子目录中。

**⚠️ 文件访问**：
- `wt loops`命令会读取用户指定的目录和文件进行分析：
  - `/wt loops [path]`：扫描指定的目录（默认为当前工作目录）
  - `/wt mce <file>`：读取指定的文件以进行大小分析
- 元数据中仅包含配置路径和输出路径的声明。详细信息请参阅“安全注意事项”部分。

## 解决的问题**

工作流中常常存在一些常见问题，例如：
- 未完成的循环、关于任务应采用并行还是串行执行的决策、文件体积过大等。这套工具提供了针对这些问题的辅助功能：
  - **循环检测**：在标记任务完成之前，识别出“DEFERRED”（延迟处理）、“PLACEHOLDER”（占位符）和“TODO”（待办事项）等标记。
  - **并行决策**：提供一个五因素框架，用于判断何时适合采用并行处理。
  - **MCE分析**：识别出文件大小超过预设阈值的文件，并提出拆分建议。

**设计理念**：这些工具专注于单一功能，避免过度复杂化工作流的处理流程——只需完成检测、决策、分析，然后继续执行下一步操作。

## 使用方法

```
/wt <sub-command> [arguments]
```

## 子命令

| 命令            | 中文            | 逻辑              | 触发条件          |
|-----------------|-----------------|-----------------|----------------|
| `/wt loops`        | 循环检测          | 扫描文件，识别循环标记       | 明确的命令            |
| `/wt parallel`      | 并行处理          | 根据五因素框架判断并行或串行    | 明确的命令            |
| `/wt mce`        | 文件大小分析        | 分析文件大小并给出拆分建议   | 明确的命令            |
| `/wt subworkflow`     | 生成子工作流        | 调用指定的ClawHub技能     | 明确的命令            |

## 参数

### `/wt loops`

| 参数            | 是否必填 | 说明                |
|-----------------|-----------------|-------------------|
| path            | 否             | 要扫描的目录（默认为当前工作目录）    |
| --pattern        | 否             | 用于检测的自定义模式（逗号分隔）     |
| --exclude        | 否             | 要排除的路径（逗号分隔）       |

### `/wt parallel`

| 参数            | 是否必填 | 说明                |
|-----------------|-----------------|-------------------|
| task            | 是             | 需要分析的任务描述         |
| --factors       | 否             | 需要评估的具体因素（默认为全部5个）     |

### `/wt mce`

| 参数            | 是否必填 | 说明                |
|-----------------|-----------------|-------------------|
| file            | 是             | 需要分析的文件           |
| --threshold       | 否             | 文件行数阈值（默认为200）       |
| --suggest        | 否             | 是否生成拆分建议         |

### `/wt subworkflow`

| 参数            | 是否必填 | 说明                |
|-----------------|-----------------|-------------------|
| task            | 是             | 需要执行的任务描述         |
| --skill         | 否             | 要使用的ClawHub技能         |
| --background       | 否             | 是否在后台执行           |

## 配置

配置文件的加载顺序（优先级依次为）：
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

### 开环检测

该工具用于检测未完成的任务：
- 常见标记包括：`DEFERRED`（延迟处理）、`PLACEHOLDER`（临时代码）、`TODO`（待办事项）等。

### 并行/串行决策框架

通过五个因素来判断任务是否适合并行处理：
- **团队协作**：不同人员能否独立完成任务？
- **任务耦合度**：任务之间的依赖关系如何？
- **接口清晰度**：任务之间的边界是否明确？
- **处理方式**：处理方式是否一致？
- **集成难度**：任务合并的复杂性如何？

根据这些因素，工具会给出是否适合并行的建议：

| 因素            | 判断标准            | 是否适合并行          |
|-----------------|-----------------|-------------------|
| 5/5            | 非常适合并行          |
| 4/5            | 需要配合协调机制的并行处理 |
| 3/5            | 可以根据具体情况判断       |
| 2/5            | 适合串行处理，但可包含并行子任务 |
| 0-1/5            | 完全适合串行处理         |

### MCE（最小上下文工程）

根据文件大小来评估代码的效率：
- 如果文件行数不超过200行，则符合MCE标准，无需特殊处理。
- 如果文件行数超过200行，则建议进行重构。

拆分建议的依据包括：
- 函数/方法的逻辑结构
- 文件的逻辑分组
- 代码的导入依赖关系
- 测试覆盖范围

### 子工作流生成

该工具可以将任务委托给ClawHub中的其他技能来执行：

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

## 集成方式

- **依赖关系**：
  - 该工具依赖于`failure-memory`（用于处理循环相关的数据）和`constraint-engine`（用于执行约束检查）。
  - 被其他工具（如`governance`用于循环检测、`review-orchestrator`用于并行决策）所使用。

## 错误处理

| 错误条件 | 处理方式                |
|-----------|-------------------------|
| 子命令无效       | 显示可用的子命令列表             |
| 文件未找到       | 显示错误信息：“文件未找到：{path}”       |
| 未检测到循环标记     | 显示信息：“未检测到循环标记”         |
| 所需技能未安装     | 显示错误信息：“所需技能未找到：{skill}”     |

## 使用后的后续步骤

调用该工具后：
- 如果检测到未完成的循环，需要优先处理高优先级的循环。
- 如果建议采用并行处理，需要创建相应的并行任务流。
- 如果文件大小超过阈值，需要根据分析结果进行拆分。
- 如果子工作流已完成，需要审核并整合其输出结果。

## 工作区文件

该工具会读取和写入以下文件：
- 配置文件（`.openclaw/workflow-tools.yaml`和`.claude/workflow-tools.yaml`）
- 用户指定的目录（通过`/wt loops`命令访问）
- 分析结果（保存在`output/`子目录中）

**安全注意事项**：
- 该工具会访问配置文件以及用户指定的目录和文件。
- 但它仅读取文件内容，不会修改源文件或系统环境变量。
- `wt loops`和`wt mce`命令会读取用户指定的任意路径（超出配置范围的路径）。
- 该工具不调用AI模型，也不发送数据到外部服务，不会执行任意代码。

**路径扫描注意事项**：
- `wt loops`命令会递归扫描指定目录，可能会读取敏感内容，请谨慎使用`--exclude`参数来避免扫描敏感路径。
- `wt subworkflow`命令会调用系统中安装的ClawHub技能，这些技能的执行权限取决于它们自身的配置。

**关于权限**：
- 使用`wt subworkflow`命令时，请注意生成的子任务的权限设置。
- 安装的技能权限取决于该工具本身及其调用的其他技能。

**来源说明**：
该工具由Live Neon（https://github.com/live-neon/skills）开发，并通过`leegitw`账户发布在ClawHub平台上。

**验收标准**：
- `/wt loops`能识别所有标准的循环标记。
- 能根据优先级对循环进行分类。
- `/wt parallel`能综合考虑五个判断因素。
- `/wt mce`能准确识别超出阈值的文件并给出拆分建议。
- `/wt mce --suggest`能生成可行的拆分方案。
- `/wt subworkflow`能正确调用ClawHub技能。
- 支持在后台执行子工作流。
- 所有分析结果都会保存在工作区文件中。

---

*该工具整合了原有的四项独立技能，发布日期为2026年2月15日。*