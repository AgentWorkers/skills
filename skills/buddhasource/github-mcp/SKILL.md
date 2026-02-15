---
name: github-mcp
description: GitHub MCP服务器用于仓库管理、文件操作、PR/问题跟踪、分支管理以及与GitHub API的集成。它支持AI代理克隆仓库、阅读代码、创建/更新文件、管理问题及拉取请求、搜索代码，并能与GitHub平台进行交互。该工具对于开发工作流程、代码审查自动化、持续集成/持续部署（CI/CD）管理以及仓库操作至关重要。当代理需要处理Git仓库、管理开发流程、自动化GitHub任务或与源代码交互时，GitHub MCP服务器是不可或缺的工具。
---

# GitHub MCP 服务器

> **为 AI 代理提供完整的 GitHub 集成**

将 AI 代理连接到 GitHub，以实现仓库管理、代码操作、问题跟踪、拉取请求以及完整的 GitHub API 功能。

## 为什么选择 GitHub MCP？

### 🤖 代理原生的 GitHub 工作流
使代理能够执行之前需要手动 API 集成的复杂 GitHub 操作：
- 克隆和导航仓库
- 读取和修改文件
- 创建问题和建议
- 审查代码和讨论
- 管理分支和发布

### 🔐 安全认证
基于 OAuth 的认证机制，具有细粒度的权限控制。代理仅能访问您授权的内容。

### 📦 常见操作的零配置
预配置了最常见的 GitHub 工作流工具，无需手动调用 API。

## 安装

### 选项 1：官方 MCP 服务器（已归档 - 由社区维护）

```bash
# Community-maintained GitHub MCP server
npm install -g @modelcontextprotocol/server-github

# Or build from source
git clone https://github.com/modelcontextprotocol/servers-archived
cd servers-archived/src/github
npm install
npm run build
```

### 选项 2：第三方实现
有多个社区实现的版本。请查看 [MCP 注册表](https://registry.modelcontextprotocol.io/) 以获取最新选项。

## 配置

将以下配置添加到您的 MCP 客户端配置中：

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_your_token_here"
      }
    }
  }
}
```

### 获取 GitHub 令牌

1. 访问 https://github.com/settings/tokens
2. 生成新的令牌（经典类型）或细粒度令牌
3. 选择权限范围：
   - `repo` - 完整的仓库访问权限
   - `read:user` - 读取用户信息
   - `read:org` - 读取组织数据（如需要）

**建议使用细粒度令牌**：
- 仓库权限：内容（读/写）、问题（读/写）、拉取请求（读/写）
- 组织权限：成员信息（如果需要访问组织仓库）

## 可用工具

### 仓库操作

#### 1. **创建仓库**
```
Agent: "Create a new repository called 'my-project'"
```

#### 2. **克隆仓库**
```
Agent: "Clone the OpenAI GPT-4 repository"
```

#### 3. **列出仓库文件**
```
Agent: "What files are in the src/ directory?"
```

### 文件操作

#### 4. **读取文件**
```
Agent: "Show me the README.md file"
Agent: "Read the contents of src/index.ts"
```

#### 5. **创建/更新文件**
```
Agent: "Create a new file docs/API.md with API documentation"
Agent: "Update the version in package.json to 2.0.0"
```

#### 6. **搜索代码**
```
Agent: "Search for files containing 'authentication logic'"
Agent: "Find where the DatabaseConnection class is defined"
```

### 问题与拉取请求管理

#### 7. **创建问题**
```
Agent: "Create an issue: 'Add dark mode support'"
```

#### 8. **列出问题**
```
Agent: "Show me all open bugs"
Agent: "What issues are assigned to me?"
```

#### 9. **创建拉取请求**
```
Agent: "Create a PR to merge feature/login into main"
```

#### 10. **审阅拉取请求**
```
Agent: "Review PR #42 and check for security issues"
```

### 分支操作

#### 11. **创建分支**
```
Agent: "Create a new branch called 'feature/user-auth'"
```

#### 12. **列出分支**
```
Agent: "Show all branches in this repo"
```

#### 13. **合并分支**
```
Agent: "Merge 'develop' into 'main'"
```

### 高级操作

#### 14. **创建发布**
```
Agent: "Create a release v2.0.0 with the latest changes"
```

#### 15. **搜索仓库**
```
Agent: "Find popular React component libraries"
```

#### 16. **分支克隆**
```
Agent: "Fork the Vue.js repository to my account"
```

## 代理工作流示例

### 代码审阅自动化
```
Human: "Review all PRs and flag security issues"

Agent:
1. list_pull_requests(state="open")
2. For each PR:
   - get_pull_request(pr_number)
   - read_changed_files()
   - analyze for security vulnerabilities
   - create_review_comment(security_findings)
```

### 问题分类
```
Human: "Label all new issues with 'needs-triage'"

Agent:
1. list_issues(state="open", labels=null)
2. For each unlabeled issue:
   - read_issue(issue_number)
   - add_label("needs-triage")
```

### 发布自动化
```
Human: "Prepare v2.0.0 release"

Agent:
1. create_branch("release/v2.0.0")
2. update_file("package.json", version="2.0.0")
3. update_file("CHANGELOG.md", new_release_notes)
4. create_pull_request("release/v2.0.0" -> "main")
5. create_release(tag="v2.0.0", notes=changelog)
```

### 文档同步
```
Human: "Update documentation from code comments"

Agent:
1. search_code(query="* @description")
2. extract_docstrings()
3. generate_markdown_docs()
4. update_file("docs/API.md", generated_docs)
5. create_pull_request("Update API documentation")
```

## 使用场景

### 🛠️ 开发辅助工具
帮助开发者完成重复性的 GitHub 任务：创建问题、管理标签、更新文档、代码审阅。

### 🤖 持续集成/持续部署自动化
构建代理来触发工作流、检查构建状态、创建发布、管理部署。

### 📊 仓库分析
分析代码质量、跟踪问题解决时间、监控拉取请求的进度、生成报告。

### 🔍 代码搜索与发现
查找代码模式、识别依赖关系、发现类似的实现方式、定位技术债务。

### 📝 文档自动化
将代码注释同步到文档中、生成 API 参考、更新变更日志、维护 README 文件。

## 安全最佳实践

### ✅ 使用细粒度令牌
优先使用细粒度令牌，而非传统的PAT（Personal Access Tokens）。将权限范围限制在特定的仓库和操作上。

### ✅ 尽可能使用只读权限
如果代理仅需要读取代码或问题信息，授予只读权限。

### ✅ 使用环境变量
切勿将令牌硬编码在代码中，始终使用环境变量。

### ✅ 定期轮换令牌
定期轮换令牌，并设置过期日期。

### ✅ 监控代理行为
监控代理的操作。GitHub 的活动日志会记录所有 API 请求。

## 速率限制

**已认证的请求：**
- 每小时 5,000 次请求（每个用户）
- 搜索 API：每分钟 30 次请求

**最佳实践：**
- 尽可能缓存仓库数据
- 在适用的情况下批量执行操作
- 使用条件请求（`If-None-Match` 请求头）

## 与手动 GitHub API 集成的对比

| 任务 | 手动 API | GitHub MCP |
|------|------------|-----------|
| **设置时间** | 几小时（包括认证、SDK 和错误处理） | 几分钟（仅配置文件） |
| **所需代码** | 是（HTTP 客户端、认证、解析） | 否（MCP 工具自动处理） |
| **代理集成** | 需要手动定义工具 | 通过 MCP 自动完成 |
| **认证管理** | 需要自定义实现 | 内置的 OAuth 流程 |
| **错误处理** | 需要自定义重试逻辑 | 由服务器处理 |

## 故障排除

### “无效凭据”错误
- 确认令牌未过期
- 确保令牌具有所需的权限范围（`repo`、`read:user`）
- 检查环境变量中是否正确设置了令牌

### “资源未找到”错误
- 确认仓库名称格式：`owner/repo`
- 检查代理是否具有访问私有仓库的权限（如适用）
- 确保分支/文件路径存在

### 速率限制错误
- 等待速率限制重置（查看 `X-RateLimit-Reset` 请求头）
- 减少请求频率
- 如需更高限制，可以考虑使用 GitHub 应用程序

## 资源

- **MCP 注册表**：https://registry.modelcontextprotocol.io/
- **GitHub API 文档**：https://docs.github.com/en/rest
- **创建令牌**：https://github.com/settings/tokens
- **速率限制**：https://docs.github.com/en/rest/overview/rate-limits-for-the-rest-api

## 高级配置

```json
{
  "mcpServers": {
    "github": {
      "command": "node",
      "args": ["/path/to/github-mcp/build/index.js"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxx",
        "GITHUB_API_URL": "https://api.github.com",
        "DEFAULT_BRANCH": "main",
        "AUTO_PAGINATION": "true"
      }
    }
  }
}
```

---

**每个编码代理都需要的 GitHub 集成**：从代码审阅到发布自动化，GitHub MCP 为 AI 代理提供了完整的 GitHub 功能支持。