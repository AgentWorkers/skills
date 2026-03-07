---
name: manus
version: "1.1.0"
description: 通过Manus API创建和管理AI代理任务。Manus 1.5能够自主浏览网页、使用各种工具，并完成整个工作流程。同时，还提供了成本更为低廉的Manus-1.5-Lite版本可供选择。
author: mvanhorn
license: MIT
repository: https://github.com/mvanhorn/clawdbot-skill-manus
homepage: https://manus.im
metadata:
  openclaw:
    emoji: "🤖"
    requires:
      env:
        - MANUS_API_KEY
    primaryEnv: MANUS_API_KEY
    tags:
      - agent
      - automation
      - manus
      - web-browsing
---
# Manus AI Agent

使用Manus API来创建自主运行的AI任务。Manus可以浏览网页、使用各种工具，并生成完整的结果（如报告、代码、演示文稿等）。

## API基础

`https://api.manus.ai/v1`

## 认证

请求头：`API_KEY: <your-key>`

认证方式：
- 通过环境变量 `MANUS_API_KEY` 设置
- 或者在openclaw配置文件中设置 `skills.manus.apiKey`

## 推荐的工作流程

当使用Manus执行需要生成文件（如幻灯片、报告等）的任务时，请按照以下步骤操作：

1. 使用 `createShareableLink: true` 创建任务。
2. 通过任务ID（`task_id`）查询任务完成情况。
3. 从响应中提取输出文件并下载到本地。
4. 通过直接文件附件的方式将文件发送给用户（不要依赖manus.im提供的共享链接）。

## 创建任务

```bash
curl -X POST "https://api.manus.ai/v1/tasks" \
  -H "API_KEY: $MANUS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Your task description here",
    "agentProfile": "manus-1.6",
    "taskMode": "agent",
    "createShareableLink": true
  }'
```

响应内容：
```json
{
  "task_id": "abc123",
  "task_title": "Task Title",
  "task_url": "https://manus.im/app/abc123"
}
```

## 代理配置文件

| 配置文件名 | 描述 | 适用场景 |
|---------|-------------|---------|
| `manus-1.6` | 标准配置（默认） | 适用于大多数任务 |
| `manus-1.6-lite` | 更快速、占用资源更少 | 适用于简单任务 |
| `manus-1.6-max` | 高性能配置 | 适用于复杂、耗时的任务 |

**提示：** 除非用户另有指定，否则始终使用 `manus-1.6` 配置。

## 任务模式

| 模式 | 描述 |
|------|-------------|
| `chat` | 对话模式 |
| `adaptive` | 自动选择最佳处理方式 |
| `agent` | 完全自主的代理模式（推荐用于生成文件） |

## 查询任务状态及输出结果

```bash
curl "https://api.manus.ai/v1/tasks/{task_id}" \
  -H "API_KEY: $MANUS_API_KEY"
```

状态值：`pending`（待处理）、`running`（运行中）、`completed`（已完成）、`failed`（失败）

**重要提示：** 当任务状态为 `completed` 时，请检查 `output` 数组中的文件信息：
- 寻找类型为 `output_file` 的条目。
- 直接从 `fileUrl` 下载文件。
- 将文件保存到本地后作为附件发送给用户。

## 提取输出文件

任务响应中包含以下类型的输出文件：
```json
{
  "output": [
    {
      "content": [
        {
          "type": "output_file",
          "fileUrl": "https://private-us-east-1.manuscdn.com/...",
          "fileName": "presentation.pdf"
        }
      ]
    }
  ]
}
```

请使用 `curl` 命令下载这些文件，并直接发送给用户，不要依赖共享链接。

## 列出所有任务

```bash
curl "https://api.manus.ai/v1/tasks" \
  -H "API_KEY: $MANUS_API_KEY"
```

## 最佳实践：

1. 在告知用户任务完成之前，务必先查询任务是否真的已完成。
2. 将输出文件下载到本地，而不是使用manus.im提供的链接（这些链接可能不可靠）。
3. 对于需要生成文件或文档的任务，使用 `agent` 模式。
4. 设定合理的预期时间——复杂任务可能需要2到10分钟或更长时间才能完成。

## 文档资源：

- API参考文档：https://open.manus.ai/docs
- 主要用户手册：https://manus.im/docs