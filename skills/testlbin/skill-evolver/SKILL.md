---
name: skill-evolver
description: >
  这是一个完整的技能生命周期管理器，用于发现、编排、融合以及优化各项技能。它能够帮助用户决定使用哪些技能，如何组合或融合这些技能，以及是否将某个成功的工作流程转化为一个新的、可重复使用的技能。
  触发条件：
  - 用户询问如何选择或组合技能；
  - 单个技能无法满足需求，需要通过技能间的协同来完成任务；
  - 已解决的工作流程可能需要被保存为一个新的技能；
  - 需要将多个技能融合为一个统一的技能。
  不触发条件：
  - 用户明确请求某个特定的技能；
  - 原生的Claude功能显然能够满足用户的需求。
---
# Skill Evolver

先解决问题，再实现具体方案。

## 工作流程

### 第0阶段：设置输出目录
为当前会话创建一个带有时间戳的输出目录：
```bash
# Format: output/MM-DD-<feature-slug>/
# Example: output/03-09-pdf-translate/
mkdir -p "output/$(date +%m-%d)-<feature-slug>"
```

> **提示**：使用与任务相关的简短名称作为目录名（例如：`pdf-translate`、`data-export`、`api-integration`）

将输出路径保存下来，以供后续阶段使用：
```
OUTPUT_DIR=output/<created-directory>
```

### 第1阶段：意图分析
分析用户任务，并生成 `${OUTPUT_DIR}/01-intent.md` 文件。
参考模板：[references/templates/01-intent.md](references/templates/01-intent.md)

### 第2阶段：技能搜索
按照完整的技能搜索流程进行操作：
→ [references/skill-search.md](references/skill-search.md)

该流程包括：
- 命令行界面（CLI）的必备条件及安装
- 本地搜索 + 注册表搜索（双轨并行）
- 技能选择
- 安装与验证
- 安全性审计

**输出文件：**
- `${OUTPUT_DIR}/02-candidates.md` - 合并后的搜索结果
- `${OUTPUT_DIR}/02-verify.md` - 安装验证结果（如果已安装）
- `${OUTPUT_DIR}/02-audit.md` - 安全性审计报告（如果已安装）

### 第3阶段：深入分析
对每个候选技能进行深入分析：
按照 [references/skill-inspector.md](references/skill-inspector.md) 中的流程进行操作。

**输出文件：** `${OUTPUT_DIR}/03-inspection.md`

### 检查点：确定使用方案
分析完成后，评估这些技能是否能够解决问题：

**大型语言模型（LLM）的评估内容：**
- 技能的功能是否符合任务需求？
- 是否需要对其进行修改？
- 组合这些技能是否有价值？

**LLM的建议：**
- **协同使用**（技能匹配度高，无需重大修改）
- **技能融合**（技能部分匹配，组合后能产生新的价值）
- **使用原生技能**（未找到合适的技能）

用户的选项：
- **A**：协同使用（LLM推荐）
- **B**：技能融合（进入编码模式）
- **C**：改用原生技能
- **D**：重新分析（返回第3阶段）

### 第3.5阶段：技能融合（条件性）
仅当选择“技能融合”时执行此阶段：
按照 [references/skill-fusion.md](references/skill-fusion.md) 中的流程进行操作。

该流程包括：
- 融合方案的设计
- 调用技能生成工具
- 对融合后的技能进行安全审计

**输出文件：**
- `${OUTPUT_DIR}/03-fusion-spec.md` - 融合方案
- `${OUTPUT_DIR}/03-fusion-audit.md` - 融合后的安全审计报告（如果进行了融合）

### 第4阶段：协同使用
设计执行计划，并生成 `${OUTPUT_DIR}/04-orchestration.md` 文件。
参考模板：[references/templates/04-orchestration.md](references/templates/04-orchestration.md)

### 检查点：确认计划
使用 `AskUserQuestion` 工具（或类似的人机交互工具）来确认计划：
- **A**：按照此计划执行
- **B**：修改计划
- **C**：提供其他方案
- **D**：提出额外要求（然后调整计划）

### 第5阶段：执行
执行计划。对于每个步骤：
- 如果使用原生技能，请根据实际情况进行操作；
- 如果使用其他技能，请提供相应的输入参数来调用这些技能。

### 检查点：是否需要实现具体方案
使用 `AskUserQuestion` 工具（或类似的人机交互工具）来询问用户是否需要将结果固化成新的技能：
- **A**：是的，创建一个新的技能（调用 `skill-creator` 工具）
- **B**：不需要，这只是一个一次性操作
- **C**：将结果保存为草稿以供后续审查
- **D**：提出额外要求（然后调整计划范围）

## 原则
```
Priority: native > orchestration > temporary > persistent

- Prefer native for simple tasks
- Prefer orchestration when existing skills can solve it
- Materialize only after validation + proven reuse value
- Always provide option [D] for additional input
- Re-optimize when user provides new information
```