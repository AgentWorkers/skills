---
name: memory-setup
description: 配置并验证 OpenClaw 的内存检索功能，以确保数据的持久性。此功能适用于启用 `memory_search`/`memory_get` 操作、解决内存检索问题，或在 OpenClaw 工作区中设置 `MEMORY.md` 及相关配置文件（如 `memory/*.md`）时使用。
---
# 内存设置（OpenClaw）

为 OpenClaw 配置持久化的内存，以便代理能够检索之前的决策、偏好设置和待办事项。

## 1) 准备工作区文件

在工作区的根目录下，应保留以下文件：

- `MEMORY.md`（长期存储的摘要信息）
- `memory/YYYY-MM-DD.md`（每日笔记）

可选的文件结构包括：

- `memory/projects/`
- `memory/system/`
- `memory/groups/`

## 2) 在 OpenClaw 配置中启用内存搜索功能

在 **`agentsdefaults.memorySearch`** 配置项中进行设置（而非顶级的 `memorySearch` 配置项）。

示例：

```json
{
  "agents": {
    "defaults": {
      "memorySearch": {
        "enabled": true,
        "provider": "local",
        "includeDefaultMemory": true,
        "maxResults": 20,
        "minScore": 0.3
      }
    }
  }
}
```

**注意事项：**
- `includeDefaultMemory: true` 会索引 `MEMORY.md` 以及所有以 `.md` 结尾的文件。
- 可用的数据提供者包括：`local`、`openai`、`gemini`、`voyage`、`mistral`。
- 如果使用远程提供者，请设置相应的 API 密钥（通过环境变量或 `memorySearch.remote.apiKey`）。

## 3) 重启并验证设置

- 修改配置后，重启 OpenClaw 代理。
- 通过以下命令进行验证：
  - `openclaw status`
  - `openclaw memory status`（如果您的 CLI 版本支持该命令）

## 4) 测试检索功能

询问与过去相关的问题，然后验证代理的响应行为：
1. 调用 `memory_search` 函数进行搜索。
2. 在需要时使用 `memory_get` 函数获取具体的内容。
3. 在适当的情况下，提供内容的来源路径和具体行号。

## 5) 故障排除

### `memory_search` 功能不可用
- 确保 `agentsdefaults.memorySearch.enabled = true`。
- 确保系统策略允许使用内存检索功能。
- 重启 OpenClaw 代理。

### 检索结果质量较低
- 降低 `minScore` 值（例如设置为 `0.2`）以扩大搜索范围。
- 增加 `maxResults` 值（例如设置为 `30`）以获取更多结果。
- 在 `MEMORY.md` 和每日日志中记录更详细的信息。

### 使用本地提供者时出现问题
- 确认本地模型的路径和配置是否正确。
- 如有必要，可以将提供者切换为远程服务，并设置 API 密钥。

## 6) 推荐的操作流程

在回答关于过去的工作内容、决策、日期、人员、偏好设置或待办事项的问题时，请按照以下步骤操作：
1. 首先使用 `memory_search` 进行搜索。
2. 如需要获取具体信息，再使用 `memory_get` 函数。
3. 如果搜索结果的可信度较低，应说明已检查了内存数据。

这样能够确保回答的准确性和可追溯性。