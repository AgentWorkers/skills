---
name: reporead
version: 1.1.0
description: 使用 RepoRead AI 分析 GitHub 仓库。当用户请求“分析仓库”、“生成文档”、“对仓库进行安全审计”或“创建 README 文件”时，可以使用该工具。该工具支持与 MCP 服务器的集成以及 REST API。
metadata:
  clawdis:
    primaryEnv: REPOREAD_API_KEY
    homepage: https://www.reporead.com
    requires:
      env:
        - REPOREAD_API_KEY
      anyBins:
        - curl
    config:
      requiredEnv:
        - REPOREAD_API_KEY
---
# RepoRead — 人工智能驱动的代码库分析平台

RepoRead 是一个基于人工智能的平台，能够分析 GitHub 代码库，并生成相应的文档、技术架构图、安全审计报告以及经过优化后的摘要内容。您可以通过 MCP 服务器（推荐方式）或 REST API 来分析任何公开的 GitHub 代码库。

## 快速入门

### 1. 获取 API 密钥

在 [reporead.com](https://www.reporead.com) 注册账号，并在 [reporead.com/settings](https://www.reporead.com/settings) 中创建一个 API 密钥。密钥前缀为 `rrk_`。

### 2. 设置环境变量

将以下代码添加到您的 shell 配置文件（`~/.zshrc` 或 `~/.bashrc`）中，以便在会话之间保持设置。

### 3. 验证连接

执行以下命令，以确认您的 API 密钥有效并查看当前的令牌余额。

### 4. 连接 MCP 服务器（推荐）

将以下代码添加到您的 MCP 配置文件中（例如 `claude_desktop_config.json` 或 `.mcp.json`）：

将 `rrk_your_api_key_here` 替换为您实际的 API 密钥。

## MCP 工具

当 MCP 服务器连接成功后，您可以使用以下工具：

| 工具 | 功能描述 |
|------|-------------|
| `import_repository(github_url)` | 通过 URL 导入 GitHub 代码库 |
| `list_repositories(page?, per_page?)` | 列出已导入的代码库 |
| `get_repository(repository_id)` | 根据 ID 获取代码库详情 |
| `start_analysis(repository_id, analysis_type, branch?)` | 提交分析任务 |
| `list_analyses(page?, per_page?, repository_id?, status?, analysis_type?)` | 带过滤器列出分析任务 |
| `get_analysis(analysis_id)` | 获取分析结果 |
| `get_analysis_status(analysis_id)` | 获取分析任务的简要状态 |
| `get_token_balance()` | 检查可用令牌数量 |

## REST API 替代方案

如果 MCP 服务器未配置，可以使用以下 REST API 脚本：

或者直接调用 REST API：

**基础 URL:** `https://api.reporead.com/public/v1`
**认证方式:** `Authorization: Bearer $REPOREAD_API_KEY`

| 端点 | 方法 | 功能描述 |
|----------|--------|-------------|
| `/repositories` | `POST` | 导入代码库（格式：`{"github_url": "..."}`） |
| `/repositories` | `GET` | 列出代码库（格式：`?page=1&per_page=20`） |
| `/repositories/{id}` | `GET` | 获取代码库详情 |
| `/analyses` | `POST` | 提交分析任务（格式：`{"repository_id": "...", "analysis_type": "..."}`） |
| `/analyses` | `GET` | 列出分析任务（格式：`?repository_id=...&status=...`） |
| `/analyses/{id}` | `GET` | 获取分析结果 |
| `/analyses/{id}/status` | 获取分析任务的简要状态 |
| `/tokens/balance` | `GET` | 检查令牌余额 |

---

## 选择分析类型

| 使用场景 | 分析类型 | 提供的内容 |
|---------|------|--------------|
| 新接触代码库，需要了解基本情况 | `technical` | 代码库架构、常用模式、关键组件 |
| 需要生成文档 | `readme` | 完整的 README 文档 |
| 部署前检查、代码审查或安全审计 | `security` | 漏洞分析、风险评估 |
| 需要可视化架构图 | `mermaid` | 代码库的工作流程和系统架构图 |
| 构建依赖代码库内容的 AI 工具 | `llmstxt` | 经过优化的摘要内容 |

**默认建议：** 如果不确定，选择 `technical` 类型。
**完整文档：** 结合使用 `readme` 和 `mermaid`。
**免费 tier：** 仅提供 `readme` 和 `llmstxt` 功能。高级 tier 可使用所有分析类型。

---

## 工作流程

1. **检查令牌余额**：使用 `get_token_balance()` 确保有足够的令牌。
2. **检查是否已导入**：使用 `list_repositories()` 避免重复导入相同的代码库。
3. **导入代码库**：使用 `import_repository(github_url)`，并保存返回的 `id`。
4. **开始分析**：使用 `start_analysis(repository_id, analysis_type)`，并保存返回的 `id`。
5. **等待分析完成**：每隔 10 秒调用 `get_analysis_status(analysis_id)`，直到状态变为 `completed` 或 `failed`。
6. **获取分析结果**：使用 `get_analysis(analysis_id)`，结果中包含完整的分析输出。
7. **使用分析结果**：根据需要将其用于后续工作。

## 常见操作模式

### 在开始工作前了解代码库

当用户要求“解释这个代码库”或在编码前需要背景信息时：

1. 导入代码库。
2. 运行 `start_analysis(repo_id, "technical")`。
3. 等待分析完成。
4. 使用分析结果中的架构图、常用模式和组件描述作为开发依据。

### 生成文档

当用户需要 README 文件、文档或可视化图表时：

1. 导入代码库。
2. 同时运行以下命令：
   - `start_analysis(repo_id, "readme")`
   - `start_analysis(repo_id, "mermaid")`
3. 等待分析完成。
4. 将 README 内容与可视化图表结合使用。

### 部署前的安全检查

在审查代码库的漏洞或进行代码审查时：

1. 导入代码库。
2. 运行 `start_analysis(repo_id, "security")`。
3. 等待分析完成。
4. 查看分析结果，并向用户指出关键问题。

## 令牌使用注意事项

- **始终** 在开始分析前调用 `get_token_balance()` 检查令牌数量。
- 如果可用令牌不足，请告知用户，他们可以在 [reporead.com/settings](https://www.reporead.com/settings) 购买更多令牌。
- 许可用量：
  - 免费 tier：100K 令牌
  - Starter tier：500K 令牌
  - Growth tier：100K 令牌
- 较大的代码库会消耗更多令牌。
- `reserved_tokens` 列示了正在进行的分析任务所占用的令牌数量。

## 使用技巧

- **使用 `get_analysis_status()` 而不是 `get_analysis()`，因为它的请求数据量更小**。
- **建议每隔 10 秒检查一次分析进度**。分析时间根据代码库大小不同，通常在 1-5 分钟内完成。
- **状态值说明**：
  - `queued` → 正在处理
  - `processing` → 正在分析
  - `completed` 或 `failed` → 分析完成或失败
- 如果分析失败，请向用户显示 `error` 字段，避免自动重试。
- 在调用 `import_repository` 之前先使用 `list_repositories` 避免重复导入代码库。
- `branch` 参数是可选的，默认使用代码库的默认分支。
- 每分钟请求次数限制为 60 次。
- `analysis_type` 必须为 `readme`、`technical`、`security`、`mermaid` 或 `llmstxt` 中的一种。