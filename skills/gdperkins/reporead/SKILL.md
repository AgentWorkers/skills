---
name: reporead
version: 1.0.0
description: 使用 RepoRead AI 分析 GitHub 仓库。当用户请求“分析仓库”、“生成文档”、“对仓库进行安全审计”或“创建 README 文件”时，可以使用该工具。该工具支持与 MCP 服务器的集成以及 REST API 的使用。
---
# RepoRead — 人工智能驱动的代码库分析平台

RepoRead 是一个基于人工智能的平台，能够分析 GitHub 代码库，并生成相关文档、技术架构概述、安全审计报告、可视化图表以及经过优化后的 LLM（大型语言模型）生成的摘要。您可以通过 MCP 服务器（推荐方式）或 REST API 来分析任何公开的 GitHub 代码库。

## 设置

### 1. 获取 API 密钥

在 [reporead.com](https://www.reporead.com) 注册账号，并在 [reporead.com/settings](https://www.reporead.com/settings) 中创建 API 密钥。密钥前缀为 `rrk_`。

### 2. 连接 MCP 服务器（推荐方式）

将以下配置添加到您的 MCP 配置文件中（例如 `claude_desktop_config.json` 或 `.mcp.json`）：

```json
{
  "mcpServers": {
    "reporead": {
      "type": "streamable-http",
      "url": "https://api.reporead.com/mcp",
      "headers": {
        "Authorization": "Bearer rrk_你的_api_key_here"
      }
    }
  }
}
```

### MCP 工具

| 工具 | 描述 |
|------|-------------|
| `import_repository(github_url)` | 通过 URL 导入 GitHub 代码库 |
| `list_repositories(page?, per_page?)` | 列出已导入的代码库 |
| `get_repository(repository_id)` | 根据 ID 获取代码库详情 |
| `start_analysis(repository_id, analysis_type, branch?)` | 提交分析任务 |
| `list_analyses(page?, per_page?, repository_id?, status?, analysis_type?)` | 根据条件列出分析任务 |
| `get_analysis(analysis_id)` | 获取分析结果 |
| `get_analysis_status(analysis_id)` | 获取分析任务的进度状态 |
| `get_token_balance()` | 查看可用令牌数量 |

### 3. REST API 替代方案

在没有 MCP 支持的环境中，可以直接使用 REST API。

**基础 URL:** `https://api.reporead.com/public/v1`
**认证方式:** `Authorization: Bearer rrk_你的_api_key_here`

| MCP 工具 | 对应的 REST API 方法 |
|----------|----------------|
| `import_repository` | `POST /repositories` `{"github_url": "..."}` |
| `list_repositories` | `GET /repositories?page=1&per_page=20` |
| `get_repository` | `GET /repositories/{id}` |
| `start_analysis` | `POST /analyses` `{"repository_id": "...", "analysis_type": "..."}` |
| `list_analyses` | `GET /analyses?repository_id=...&status=...` |
| `get_analysis` | `GET /analyses/{id}` |
| `get_analysis_status` | `GET /analyses/{id}/status` |
| `get_token_balance` | `GET /tokens/balance` |

---

## 选择分析类型

| 使用场景 | 分析类型 | 提供的内容 |
|---------|------|--------------|
| 刚接触代码库，需要了解基本情况 | `technical` | 代码库架构、常用模式、关键组件 |
| 需要生成文档 | `readme` | 完整的 README 文档 |
| 部署前检查、代码审查或安全审计 | `security` | 漏洞分析、风险评估 |
| 需要可视化架构图 | `mermaid` | 系统和工作流程图 |
| 构建依赖代码库内容的 AI 工具 | `llmstxt` | 经过优化的 LLM 摘要 |

**默认建议：** 如果不确定选择哪种类型，使用 `technical`。
**完整文档：** 结合使用 `readme` 和 `mermaid`。
**免费套餐：** 仅提供 `readme` 和 `llmstxt`；高级套餐可解锁所有分析类型。

## 工作流程

1. **检查令牌数量**：使用 `get_token_balance()` 确保有足够的令牌。
2. **确认代码库是否已导入**：使用 `list_repositories()` 避免重复导入。
3. **导入代码库**：使用 `import_repository(github_url)`，并保存返回的 `id`。
4. **开始分析**：使用 `start_analysis(repository_id, analysis_type)`，并保存返回的 `id`。
5. **查询分析进度**：每 10 秒查询一次 `get_analysis_status(analysis_id)`，直到状态变为 `completed` 或 `failed`。
6. **获取分析结果**：使用 `get_analysis(analysis_id)`，结果中包含完整的分析内容。
7. **使用分析结果**：根据需要将其用于后续工作。

## 常见操作模式

### 在开始工作前了解代码库

当用户请求“解释这个代码库”或您需要相关背景信息时：

1. 导入代码库。
2. 运行 `start_analysis(repo_id, "technical")`。
3. 等待分析完成。
4. 使用分析结果中的架构信息、模式和组件描述作为工作依据。

### 生成文档

当用户需要 README 文档、技术文档或可视化图表时：

1. 导入代码库。
2. 同时运行 `start_analysis(repo_id, "readme")` 和 `start_analysis(repo_id, "mermaid")`。
3. 等待分析完成。
4. 将 README 内容与可视化图表结合使用。

### 部署前的安全检查

在审查代码库的漏洞或进行代码审查时：

1. 导入代码库。
2. 运行 `start_analysis(repo_id, "security")`。
3. 等待分析完成。
4. 查看分析结果，并将关键问题告知用户。

## 令牌使用注意事项

- **务必** 在开始分析前调用 `get_token_balance()`。
- 如果可用令牌不足，请告知用户，他们可以在 [reporead.com/settings](https://www.reporead.com/settings) 购买更多令牌。
- 许可令牌数量如下：免费套餐 100K 个，入门套餐 500K 个，高级套餐 100 万个。
- 大型代码库会消耗更多令牌。
- `reserved_tokens` 列显示了正在进行的分析所占用的令牌数量。

## 使用技巧

- 使用 `get_analysis_status()` 而不是 `get_analysis()`，因为它的请求数据量更小。
- 每 10 秒查询一次分析进度。
- 分析时间取决于代码库的大小，通常需要 1–5 分钟。
- 分析状态分为：`queued` → `processing` → `completed` 或 `failed`。
- 如果分析失败，请显示 `error` 字段，并告知用户不要自动重试。
- 在导入代码库之前使用 `list_repositories` 以避免重复导入错误。
- `branch` 参数是可选的，默认使用代码库的默认分支。
- 每分钟请求次数限制为 60 次。
- `analysis_type` 必须为 `readme`、`technical`、`security`、`mermaid` 或 `llmstxt` 中的一种。