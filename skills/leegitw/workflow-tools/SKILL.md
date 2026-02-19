---
name: workflow-tools
version: 1.1.0
description: 通过循环检测、并行决策以及文件大小分析功能，更高效地提升工作效率。
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

这是一套统一的工作流辅助工具，涵盖了开环检测、并行/串行决策框架、MCE文件分析以及子工作流的生成等功能，整合了原有的四项独立技能。

**触发方式**：需要显式调用这些工具。

**源技能**：`loop-closer`、`parallel-decision`、`MCE`（最小上下文工程，Minimal Context Engineering）、`subworkflow-spawner`。

**已移除的技能**：`pbd-strength-classifier`（其功能已被`/fm classify`替代，因此不再需要）。

## 安装

```bash
openclaw install leegitw/workflow-tools
```

**依赖项**：
- `leegitw/failure-memory`（用于处理循环上下文）
- `leegitw/constraint-engine`（用于执行约束检查）

```bash
# Install with dependencies
openclaw install leegitw/context-verifier
openclaw install leegitw/failure-memory
openclaw install leegitw/constraint-engine
openclaw install leegitw/workflow-tools
```

**独立使用**：
- 开环检测、并行决策和MCE分析可以独立运行；
- 完整集成后，这些工具能够提供基于约束条件的工作流建议。

**数据处理**：
- 所有工作流分析都在代理的权限范围内进行，不依赖外部API或第三方服务；
- 如果代理使用了云托管的LLM（如Claude、GPT等），数据会作为代理正常操作的一部分进行处理；
- 分析结果会被保存在工作区的`output/`子目录中。

## 解决的问题**

工作流中常常会出现各种问题：循环无法结束、关于并行或串行执行的决策困难、文件体积过大等问题。这套工具提供了针对这些常见问题的解决方案：
1. **开环检测**：在标记任务完成之前，识别出`DEFERRED`（推迟处理）、`PLACEHOLDER`（占位符）和`TODO`（待办事项）标记。
2. **并行决策**：提供一个五因素框架，用于判断何时适合采用并行或串行方式。
3. **MCE分析**：识别文件大小超过预设阈值的文件，并提出拆分建议。

**设计理念**：
- 这些工具专注于单一功能，避免过度复杂化；它们负责检测问题、做出决策、进行分析，然后让用户继续处理后续工作。

## 使用方法

```
/wt <sub-command> [arguments]
```

## 子命令

| 命令          | 中文            | 逻辑                | 触发条件            |
|----------------|------------------|------------------|------------------|
| `/wt loops`       | 循环检测          | 扫描文件中是否存在未完成的标记    | 显式调用            |
| `/wt parallel`     | 并行处理          | 根据五因素框架判断并行或串行    | 显式调用            |
| `/wt mce`       | 文件大小分析        | 检查文件行数是否超过阈值    | 显式调用            |
| `/wt subworkflow`    | 生成子工作流        | 调用指定的ClawHub技能      | 显式调用            |

## 参数说明

### `/wt loops`

| 参数            | 是否必填          | 说明                |
|----------------|------------------|----------------------|
| path            | 否               | 要扫描的目录（默认为当前目录）        |
| --pattern        | 否               | 用于检测的自定义模式（逗号分隔）       |
| --exclude        | 否               | 需要排除的路径（逗号分隔）        |

### `/wt parallel`

| 参数            | 是否必填          | 说明                |
|----------------|------------------|----------------------|
| task            | 是               | 需要评估的任务描述          |
| --factors       | 否               | 需要评估的具体因素（默认为全部5个）     |

### `/wt mce`

| 参数            | 是否必填          | 说明                |
|----------------|------------------|----------------------|
| file            | 是               | 需要分析的文件            |
| --threshold       | 否               | 文件行数阈值（默认为200）         |
| --suggest        | 否               | 是否生成拆分建议           |

### `/wt subworkflow`

| 参数            | 是否必填          | 说明                |
|----------------|------------------|----------------------|
| task            | 是               | 任务描述              |
| --skill          | 是否指定使用的ClawHub技能       |                   |
| --background       | 否               | 是否在后台运行            |

## 配置

配置文件按优先级顺序加载：
1. `.openclaw/workflow-tools.yaml`（OpenClaw标准配置）
2. `.claude/workflow-tools.yaml`（Claude代码兼容性配置）
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

系统会扫描文件中未完成的任务，并识别以下标记：
- `DEFERRED:`：表示任务被推迟处理
- `PLACEHOLDER:`：表示代码为临时占位符
- `TODO:`：表示任务待处理
- `FIXME:`：表示存在错误或需要修复的问题
- `HACK:`：表示技术上的临时解决方案
- `XXX:`：表示需要进一步审查的代码

### 并行与串行决策框架

通过五个因素来判断是否适合采用并行处理：
- **团队协作**：不同人员能否独立处理任务的不同部分？
- **任务耦合度**：任务之间的依赖关系如何？
- **接口清晰度**：任务之间的边界是否明确？
- **处理方式**：处理方式是否一致？
- **集成难度**：任务合并的复杂性如何？

根据这些因素，系统会给出是否采用并行的建议：

| 因素            | 判断结果            | 是否适合并行处理         |
|-------------------|------------------|----------------------|
| 5/5            | 非常适合并行处理        |
| 4/5            | 需要设置并行执行检查点        |
| 3/5            | 根据具体情况判断         |
| 2/5            | 建议优先采用串行处理       |
| 0-1/5            | 建议优先采用串行处理       |

### MCE（最小上下文工程）

根据文件行数来评估文件是否适合并行处理：
- 行数 ≤ 200：符合MCE标准，无需特殊处理
- 201-300：接近阈值，建议考虑重构
- > 300：超出MCE标准，建议拆分文件

拆分建议的依据包括：
- 函数/方法的逻辑结构
- 文件的逻辑分组
- 文件的导入依赖关系
- 测试覆盖范围

### 生成子工作流

系统会将任务分配给相应的ClawHub技能进行处理：

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

### 示例：基础设施中的开环检测

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
  - 该工具依赖于`leegitw/failure-memory`（处理循环上下文）和`leegitw/constraint-engine`（执行约束检查）；
  - 被`governance`（工作流管理工具）和`review-orchestrator`（并行决策工具）所使用。

## 错误处理情况

| 错误条件            | 处理方式                |
|------------------|----------------------|
| 子命令无效          | 显示可用的子命令列表            |
| 文件未找到          | 显示错误信息：“文件未找到：{path}”       |
| 未检测到匹配模式        | 显示提示信息：“未检测到开环标记”       |
| 所需技能不可用        | 显示错误信息：“所需技能未找到：{skill}”     |

## 后续操作

调用该工具后：
- 如果检测到未完成的循环，需要优先处理高优先级的循环；
- 如果建议采用并行处理，需要创建相应的并行任务流；
- 如果文件大小超出MCE阈值，需要执行拆分建议；
- 如果子工作流已完成，需要审查并整合分析结果。

## 工作区文件

该工具会读写以下文件：

```
output/
├── loops/
│   └── scan-YYYY-MM-DD.md    # Loop scan results
├── parallel-decisions/
│   └── task-YYYY-MM-DD.md    # Decision records
├── mce-analysis/
│   └── file-YYYY-MM-DD.md    # MCE analysis results
└── subworkflows/
    └── SW-YYYYMMDD-XXX/      # Subworkflow outputs
        ├── status.json
        └── results.md
```

## 验收标准：
- `/wt loops`能够识别所有标准类型的未完成任务；
- `/wt loops`能够按优先级（高/中/低）对任务进行分类；
- `/wt parallel`能够综合考虑所有五个因素并给出明确建议；
- `/wt mce`能够识别超出大小阈值的文件；
- `/wt mce --suggest`能够生成可执行的拆分建议；
- `/wt subworkflow`能够正确调用相应的ClawHub技能；
- `/wt subworkflow`支持在后台运行；
- 分析结果会被保存在工作区文件中。

---

*这些工具整合自原有的四项独立技能，完成于2026年2月15日。*