---
name: codifica
description: 当工作在代理之间或在你与人类之间传递时，该系统能够保持上下文的连贯性。它使用 Codifica 协议为每个代理提供关于任务、决策和交接情况的共享、持久化的存储空间——这些信息以纯文本的形式存储在 Git 中。
version: 1.0.0
homepage: https://github.com/davidedicillo/codifica
metadata: {"openclaw":{"emoji":"📋","requires":{"anyBins":["git"]}}}
---
# Codifica 协议代理

您正在使用 **Codifica 协议（v0.2）** 的仓库中工作——这是一种基于文件的协议，用于协调人类与 AI 代理之间的协作。  
Codifica 使用与代码一起提交的纯文本文件进行任务管理，无需外部服务、API 或数据库；Git 本身就充当了审计日志的角色。

## 开始工作之前  

1. 阅读仓库根目录下的 `codifica.json` 文件。  
2. 阅读该文件中引用的规范文件（通常位于 `codifica-spec.md`）。  
3. 阅读所有与 `state` 字段匹配的状态文件（该字段可以是字符串、通配符或数组）。  

**请务必在开始工作前阅读规范文件。**  
如果仓库中不存在 `codifica.json`，则此协议不适用，您可以正常进行工作。  

## 理解 `codifica.json` 的内容  

**关键字段：**  
- `state`：状态文件的路径。可以是 `"work.md"`、`work/*.md"`，或者是一个数组（例如 `["work/active.md", "work/done.md"]`）。  
- `rules`：可以是一个字符串（如 `"strict"`），也可以是一个对象，其中包含 `allowedAgents`、`file_scope`、`max_concurrent_tasks_per_agent`、`stale_claim_hours` 和 `custom_types` 等字段。  

如果 `rules` 是一个对象，请检查以下内容：  
- `allowedAgents`：如果该字段非空且您的代理名称不在其中，请停止操作并咨询人类管理员。  
- `file_scope.include`/`file_scope.exclude`：请勿修改超出允许范围的文件。  
- `max_concurrent_tasks_per_agent`：请勿同时处理超过此限制的任务数量。  

## 查找任务  

扫描所有状态文件，寻找满足以下条件的任务：  
- `state` 为 `todo`。  
- `owner` 与您的代理名称匹配（格式为 `agent:<your-name>`）或任务处于 `unassigned` 状态。  
- 所有依赖任务（`depends_on`）的状态均为 `done`。  

任务优先级依次为：`critical` > `high` > `normal` > `low`。  
在优先级相同的情况下，优先选择没有依赖任务的独立任务（即“叶子任务”）。  

## 提交任务  

在开始工作之前，您必须通过一次原子性提交来声明对任务的占有权：  
1. 将 `state` 设置为 `in_progress`。  
2. 将 `owner` 设置为 `agent:<your-name>`。  
3. 设置 `claimed_at` 为当前的 ISO-8601 时间戳。  
4. 添加一条记录任务占有情况的 `state_transitions` 条目。  

将所有这些更改一起提交。如果是在远程仓库中工作，请立即推送；如果推送失败（其他代理先占用了任务），请不要开始工作，而是重新评估并选择其他任务。  
将 `in_progress` 状态的未分配任务视为违反协议的行为。  

## 开始工作前阅读任务背景信息  

在开始任务之前，请阅读其 `context` 字段：  
- `context.files`：阅读这些文件以获取任务背景信息。  
- `contextreferences`：读取相关任务的 `execution_notes`。  
- `contextconstraints`：查看超出任务接受标准的强制性规则。  
- `context.notes`：查看人类管理员提供的指导性说明。  

如果任务有依赖关系，请同时阅读依赖任务的 `execution_notes`（特别是 `summary` 部分）和 `artifacts`，以便了解任务的具体要求。  

## 完成任务  

按照任务的接受标准完成任务，并遵守 `codifica.json` 中定义的 `file_scope`。  

## 记录任务完成情况  

完成任务后，请更新状态文件：  
1. 添加一条 `execution_notes` 条目（具体内容见 **CODE_BLOCK_1___**）。  
2. 将您生成的文件添加到 `artifacts` 中（具体内容见 **CODE_BLOCK_2___**）。  
3. 将任务状态更新为适当的下一状态：  
  - 对于 `build` 类型的任务：从 `in_progress` 更改为 `to_be_tested`。  
  - 对于其他类型的任务（`test`、`investigate`、`followup`）：从 `in_progress` 更改为 `done`（可以跳过 `to_be_tested`）。  
  - 将 `completed_at` 设置为任务完成的 ISO-8601 时间戳。  
4. 添加一条 `state_transitions` 条目（具体内容见 **CODE_BLOCK_3___**）。  
5. 提交更改，并在提交信息中注明任务 ID（例如：`FEAT-101：实现了登录流程`）。  

## 必须遵守的规则：  

- 在读取状态文件之前，请先拉取最新代码。  
- 在开始工作之前，必须通过一次提交来声明对任务的占有权。  
- 如果提交失败，请不要继续工作，而是选择其他任务。  
- 严禁修改 `human_review` 部分的内容。  
- 严禁删除或修改 `assets/` 目录下的文件。  
- 只有任务所有者才能将任务从 `to_be_tested` 状态更改为 `done`。  
- 严禁将任务状态设置为 `blocked` 或 `rejected`——只能由人类管理员执行此操作。  
- 严禁从其他代理处重新获取已被占用的任务——只能由人类管理员处理。  
- 严禁开始那些依赖关系未满足的任务。  
- 在完成任务后的 `execution_notes` 中添加简短的总结（最多 120 个字符）。  
- 记录您完成任务时生成的文件。  
- 在将任务状态更改为 `done` 时，设置 `completed_at`。  

## 请求任务阻塞  

如果您发现阻碍任务进展的问题（如依赖关系缺失、测试失败或需求不明确），请在 `execution_notes` 中添加说明，并建议将任务标记为 `blocked`。  
**请勿自行将任务状态设置为 `blocked`——只能由人类管理员执行此操作**。  

## 回答关于任务的问题  

当被询问您或其他代理完成了哪些任务时：  
- 根据 `owner`、`state`、`labels` 或 `completed_at` 等条件扫描状态文件。  
- 首先查看任务完成时的 `execution_notes` 中的 `summary` 字段以获取快速答案；  
- 如需更多详细信息，可进一步查看 `note` 和 `artifacts`。  
- 可通过 `completed_at` 和 `labels` 来按时间和领域筛选任务。  

这种方式比直接阅读聊天记录更为高效和有条理。  

## 解决冲突  

如果您的提交因 Git 冲突而失败：  
1. 先拉取最新的代码。  
2. 重新评估您的更改是否仍然适用。  
3. 重试或等待人类管理员的解决。  
对于同一任务的冲突，应交由人类管理员处理。  

## 任务状态说明  

**只有人类管理员才能将任务状态设置为 `blocked` 或 `rejected`。**  
**只有人类管理员才能将已被拒绝的任务重新开启。**