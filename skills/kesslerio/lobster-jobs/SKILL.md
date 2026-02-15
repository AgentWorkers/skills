---
name: lobster-jobs
description: 将 OpenClaw 的 cron 作业转换为 Lobster 工作流。分析、检查并验证作业迁移过程。在将自动化流程转换为具有恢复功能的、需要审批的工作流时使用此方法。
metadata:
  openclaw:
    emoji: 🦞
    requires:
      bins: ["openclaw", "python3"]
---

# lobster-jobs

将 OpenClaw 的 cron 作业转换为带有审批机制和可恢复执行功能的 Lobster 工作流。

## 目的

OpenClaw 的 cron 作业分为以下两类：
- **systemEvent**：简单的 shell 命令（完全确定性的）
- **agentTurn**：用于生成 AI 代理的自然语言指令（灵活性较高，但依赖大量文本数据）

Lobster 工作流具有以下特点：
- **确定性执行**：每个步骤都不会由大型语言模型（LLM）重新规划
- **审批机制**：需要用户明确批准的强制停止操作
- **状态管理**：能够记住执行进度和检查点
- **可恢复执行**：可以精确地从暂停的位置继续执行

此功能用于分析现有的 cron 作业，并将其转换为 Lobster 工作流。

## 命令

### 第一层（现已可用）

#### `lobster-jobs list`
列出所有 cron 作业及其对应的 Lobster 迁移完成度评分。

输出类别：
- ✅ **完全可迁移**：简单的 shell 命令（systemEvent）
- 🟡 **部分可迁移**：包含确定性和 LLM 步骤的混合作业（agentTurn）
- ❌ **不可迁移**：需要大量 LLM 推理的作业

#### `lobster-jobs inspect <job-id>`
详细检查指定的 cron 作业的迁移情况。

显示内容：
- 作业元数据（调度信息、目标、数据负载类型）
- Lobster 迁移状态及原因
- 数据负载预览
- 迁移建议

#### `lobster-jobs validate <workflow-file>`
验证 Lobster 工作流的 YAML 文件是否符合规范。

检查内容：
- 必需字段（名称、步骤）
- 步骤结构（ID、命令）
- 审批机制的语法
- 条件语句的语法

### 第二层（现已可用）

#### `lobster-jobs convert <job-id>`
将一个 cron 作业转换为 Lobster 工作流。

```bash
lobster-jobs convert 17fe68ca
lobster-jobs convert 17fe68ca --output-dir ~/workflows
lobster-jobs convert 17fe68ca --force  # Overwrite existing
```

生成结果：
- 在 `~/.lobster/workflows/` 目录下生成 `.lobster` 格式的工作流文件
- 从 systemEvent 或 agentTurn 数据负载中提取命令
- 自动验证生成的工作流

选项：
- `--output-dir, -o`：自定义输出目录
- `--force, -f`：覆盖现有工作流
- `--keep-on-error`：即使验证失败也保留文件

#### `lobster-jobs new <name>`
使用模板从头开始创建一个新的 Lobster 工作流。

```bash
lobster-jobs new my-workflow
lobster-jobs new my-workflow --template with-approval
lobster-jobs new my-workflow --template stateful
```

可用模板：
- `simple-shell`：基本命令执行工作流
- `with-approval`：带有审批机制的工作流
- `stateful`：具有状态跟踪功能的工作流

## 安装

```bash
# Add to PATH
export PATH="$PATH:/home/art/niemand/skills/lobster-jobs/bin"

# Or create symlink
ln -s /home/art/niemand/skills/lobster-jobs/bin/lobster-jobs ~/.local/bin/
```

## 快速入门

```bash
# See all your cron jobs and their migration status
lobster-jobs list

# Inspect a specific job
lobster-jobs inspect 17fe68ca

# Convert a job to Lobster workflow
lobster-jobs convert 17fe68ca

# Create a new workflow from template
lobster-jobs new my-workflow --template with-approval

# Validate a workflow file
lobster-jobs validate ~/.lobster/workflows/my-workflow.lobster
```

## 工作流文件格式

```yaml
name: my-workflow
description: Optional description

steps:
  - id: fetch_data
    command: some-cli fetch --json
    
  - id: process
    command: some-cli process
    stdin: $fetch_data.stdout
    
  - id: approve_send
    command: approve --prompt "Send notification?"
    approval: required
    
  - id: send
    command: message.send --channel telegram --text "Done!"
    condition: $approve_send.approved
```

## 迁移策略

### 推荐的封装方式
保留 cron 作为调度工具，将数据负载修改为调用 Lobster 的接口：

```json
{
  "payload": {
    "kind": "systemEvent",
    "text": "lobster run ~/.lobster/workflows/my-workflow.lobster"
  }
}
```

优点：
- 可轻松回滚（只需恢复数据负载）
- 支持增量迁移
- 现有的 cron 调度机制依然可用

## 处理大型语言模型的判断结果

对于同时需要确定性和 LLM 推理的作业：

```yaml
steps:
  - id: gather
    command: gh issue list --json title,body
    
  - id: triage
    command: clawd.invoke
    prompt: "Classify these issues by urgency"
    
  - id: notify
    command: telegram-send
```

工作流本身是确定性的；大型语言模型（LLM）的执行过程被视为一个“黑盒”步骤。

## 特殊情况

| 问题 | 处理方法 |
|-------|----------|
| **幂等性** | 工作流会记录步骤完成情况，因此重启是安全的 |
| **审批超时** | 可配置超时时间并设置默认处理方式 |
| **敏感信息的处理** | 使用环境变量或 1Password 作为安全机制 |
| **部分失败** | 在写入数据之前先进行验证 |

## 参考资料

- Lobster：https://github.com/openclaw/lobster
- Lobster 的愿景（Vision）：https://github.com/openclaw/lobster/blob/main/VISION.md