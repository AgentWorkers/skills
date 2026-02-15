# MCP 前置条件设置

这是一项用于验证和配置 Product Guide Writer 工作流程所需 MCP（Model Context Protocol）服务器的技能。

## 概述

Product Guide Writer 需要依赖多个 MCP 服务器来提供外部集成功能。该技能可帮助验证所需的 MCP 是否已正确配置，并在需要时指导用户完成设置。

## 使用场景

在以下情况下使用该技能：
- 首次启动 Product Guide Writer 时
- 在文档编写过程中遇到与 MCP 相关的错误时
- 设置新的开发环境时
- 解决 Confluence/GitHub 集成问题时

---

## 所需的 MCP 服务器

| MCP 服务器 | 功能 | 是否必需 | 使用的功能 |
|------------|---------|----------|---------------|
| **user-atlassian** | Confluence 搜索/发布、Jira 集成 | 是 | searchConfluenceUsingCql、createConfluencePage、getConfluenceSpaces |
| **user-github** | 仓库搜索、代码浏览 | 是 | search_repositories、search_code、get_file_contents |
| **user-Figma** | 设计原型检索 | 可选 | get_file、get_images |
| **user-elasticsearch-mcp** | 用于请求流程验证的日志分析 | 可选 | search、get |

---

## 第一步：验证 MCP 状态

### 1.1：检查已启用的 MCP 服务器

代理应通过检查 MCP 配置文件夹来验证 MCP 的可用性：

```
/Users/{username}/.cursor/projects/{workspace}/mcps/
```

查找以下目录：
- `user-atlassian/` - Atlassian MCP（必需）
- `user-github/` - GitHub MCP（必需）
- `user-Figma/` - Figma MCP（可选）
- `user-elasticsearch-mcp/` - Elasticsearch MCP（可选）

### 1.2：测试 Atlassian MCP 连接

使用 `getAccessibleAtlassianResources` 工具来验证 Atlassian 的身份验证：

```
Tool: CallMcpTool
Server: user-atlassian
ToolName: getAccessibleAtlassianResources
Arguments: {}
```

**预期响应：** 包含 Trading212 在内的可用 Atlassian Cloud 实例列表。

**如果出现错误：** 指导用户完成身份验证（参见第二步）。

### 1.3：验证对 GT 空间的访问权限

确认是否可以访问产品文档空间：

```
Tool: CallMcpTool
Server: user-atlassian
ToolName: getConfluenceSpaces
Arguments:
  cloudId: "trading212.atlassian.net"
  keys: ["GT"]
```

**预期响应：** GT（产品文档空间）的详细信息。

**如果出现错误：** 用户可能需要额外的 Confluence 权限。

---

## 第二步：MCP 配置指南

如果缺少或配置错误的 MCP，请指导用户进行相应的操作：

### 2.1：Atlassian MCP 的配置

**如果 `user-atlassian` 未配置：**

1. **打开设置：**
   - 按 `Cmd/Ctrl + ,` 打开设置
   - 导航到 “MCP 服务器” 或 “扩展程序”

2. **添加 Atlassian MCP：**
   - 在 MCP 市场中搜索 “Atlassian”
   - 安装官方的 Atlassian MCP 服务器
   - 或者手动将其添加到 `mcp.json` 文件中（官方的 Atlassian 远程 MCP）：
   ```json
   {
     "atlassian-mcp": {
       "url": "https://mcp.atlassian.com/v1/mcp"
     }
   }
   ```

3. **身份验证：**
   - 根据提示授权访问您的 Atlassian 账户
   - 授予访问 Trading212 工作区的权限
   - 确保您有权访问 GT Confluence 空间

4. **验证安装：**
   - 重启 Cursor
   - 重新运行步骤 1.2 中的验证检查

### 2.2：GitHub MCP 的配置

**如果 `user-github` 未配置：**

1. **安装 GitHub MCP：**
   - 通常已随 Cursor 预装
   - 如果未安装，请将其添加到 `mcp_servers.json` 文件中：
   ```json
   {
     "github": {
       "command": "npx",
       "args": ["-y", "@modelcontextprotocol/server-github"],
       "env": {
         "GITHUB_TOKEN": "${GITHUB_TOKEN}"
       }
     }
   }
   ```

2. **配置 GitHub Token：**
   - 在 github.com/settings/tokens 创建个人访问令牌
   - 授予 `repo` 和 `read:org` 权限
   - 将令牌设置为环境变量：`export GITHUB_TOKEN=your_token`

3. **验证访问权限：**
   - 通过简单的仓库搜索来测试访问权限
   - 确保可以访问 Trading212 组织

### 2.3：可选的 MCP

**Figma MCP（用于 UI 文档）：**
- 安装：`@anthropic/mcp-server-figma`
- 需要 Figma 访问令牌
- 适用于记录用户界面相关的功能

**Elasticsearch MCP（用于日志验证）：**
- 安装：`@anthropic/mcp-server-elasticsearch`
- 需要访问 Elasticsearch 集群
- 用于第四阶段的验证

---

## 第三步：配置验证

配置完成后，运行全面的验证：

### 3.1：验证检查列表

```markdown
## MCP Configuration Status

### Required MCPs
- [ ] user-atlassian: Connected to trading212.atlassian.net
- [ ] user-github: Connected to Trading212 organization

### Optional MCPs
- [ ] user-Figma: {Connected / Not configured}
- [ ] user-elasticsearch-mcp: {Connected / Not configured}

### Confluence Access
- [ ] GT Space accessible: trading212.atlassian.net/wiki/spaces/gt
- [ ] Can search pages: searchConfluenceUsingCql works
- [ ] Can create pages: createConfluencePage permission confirmed

### GitHub Access
- [ ] Can search repositories: search_repositories works
- [ ] Can search code: search_code works
- [ ] Trading212 org accessible
```

### 3.2：测试搜索功能

执行搜索测试以确认所有功能是否正常：

```
Tool: CallMcpTool
Server: user-atlassian
ToolName: searchConfluenceUsingCql
Arguments:
  cloudId: "trading212.atlassian.net"
  cql: "space = GT AND type = page"
  limit: 5
```

如果搜索返回结果，则表示 Atlassian MCP 已正确配置。

---

## 故障排除

| 问题 | 原因 | 解决方案 |
|-------|-------|----------|
| “找不到 MCP 服务器” | MCP 未安装 | 按照第二步的设置指南进行操作 |
| “身份验证失败” | 令牌过期/无效 | 在 Cursor 设置中重新进行身份验证 |
| “无法访问 GT 空间” | Confluence 权限问题 | 向 Confluence 管理员请求访问权限 |
| “API 调用次数过多导致限制” | 等待片刻后重试，或使用缓存 |
| “Cloud ID 未找到” | 使用错误的 Atlassian 实例 | 使用 `getAccessibleAtlassianResources` 查找正确的 ID |

---

## 快速参考

### Atlassian Cloud ID
```
trading212.atlassian.net
```

### GT 空间详细信息
```
Space Key: GT
Space Name: Product Documentation
URL: https://trading212.atlassian.net/wiki/spaces/gt
```

### 有用的 CQL 查询

**查找所有产品文档：**
```
space = GT AND type = page AND title ~ "Product Guide"
```

**查找特定 OTT 的文档：**
```
space = GT AND type = page AND text ~ "{ott-name}"
```

**查找最近更新的页面：**
```
space = GT AND type = page AND lastmodified >= now("-30d")
```

---

## 与 Product Guide Writer 的集成

配置完 MCP 后，Product Guide Writer 将执行以下操作：
1. **第一阶段：** 使用 Atlassian MCP 搜索现有文档
2. **第四阶段：** 使用 Atlassian MCP 添加相关页面并选择性地进行发布
3. **整个过程中：** 使用 GitHub MCP 进行仓库搜索和代码查找

有关完整的工作流程，请参阅 [product-guide-writer/SKILL.md](../product-guide-writer/SKILL.md)。