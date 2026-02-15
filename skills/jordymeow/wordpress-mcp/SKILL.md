---
name: wordpress-mcp
description: 通过 AI 引擎使用 MCP（Model Context Protocol）来管理 WordPress 网站。该工具可用于创建/编辑文章、进行 SEO 分析、数据统计、媒体管理、分类系统操作、社交媒体调度、多语言内容处理（Polylang）以及执行任何与 WordPress 管理相关的任务。需要安装 AI Engine 插件（免费），并确保 MCP Server 已启用。在涉及 WordPress 网站管理、内容工作流程或 WP 相关任务时，也可使用该工具。
---

# WordPress MCP

通过 AI Engine 的 MCP 服务器来管理 WordPress 网站。AI Engine 是一个免费的 WordPress 插件，它提供了全面的 MCP 接口。

## 设置

用户需要：
1. 安装了 **AI Engine** 插件（免费：https://wordpress.org/plugins/ai-engine/）
2. 在 AI Engine 的 **设置 → MCP** 中启用 MCP 服务器
3. 在 MCP 设置中设置一个 **Bearer Token**

连接详细信息应存储在用户的 `TOOLS.md` 文件中：
```
## WordPress MCP
- **URL:** https://example.com/wp-json/mcp/v1/http
- **Bearer Token:** <token from AI Engine MCP settings>
```

## 如何调用 MCP 工具

所有调用都使用 JSON-RPC 2.0 协议，并通过 HTTP POST 方法进行：

```bash
curl -s -X POST <MCP_URL> \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"<tool_name>","arguments":{...}}}'
```

### 发现可用工具

列出可用的工具（具体工具取决于已启用的功能）：
```json
{"jsonrpc":"2.0","id":1,"method":"tools/list"}
```

始终使用 `tools/list` 来查看当前网站支持哪些功能。

### 连接性检查
```json
{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"mcp_ping","arguments":{}}}
```

## MCP 功能（模块化）

工具被分为不同的功能组，网站管理员可以在 AI Engine 的 **设置 → MCP 功能** 中进行启用或禁用。**默认情况下，仅启用 WordPress 核心功能。**始终使用 `tools/list` 来查看可用的所有工具。

| 功能 | 默认状态 | 描述 |
|---------|---------|-------------|
| **WordPress** | ✅ 启用 | 文章、页面、评论、用户、媒体、分类法、设置 |
| **插件** | 禁用 | 安装、激活、更新和修改插件 |
| **主题** | 禁用 | 安装、激活、切换和自定义主题 |
| **数据库** | 禁用 | 在 WordPress 数据库上执行 SQL 查询 |
| **Polylang** | 禁用 | 多语言内容（需要 Polylang 插件） |
| **WooCommerce** | 禁用 | 产品、订单、客户（需要 WooCommerce 插件） |
| **SEO Engine** | 禁用 | SEO 分析、统计（需要 SEO Engine 插件） |
| **Social Engine** | 禁用 | 社交媒体调度（需要 Social Engine 插件） |
| **Dynamic REST** | 禁用 | 直接访问 WordPress 的 REST API |

有关每个工具的详细信息，请参阅 `references/features.md`。

## 常见工作流程

### 内容审核（WordPress + SEO Engine）
1. `mwseo_get_seo_statistics` — 获取网站的整体 SEO 状态
2. `mwseo_get_posts_needing_seo` — 查找需要优化 SEO 的文章
3. 使用循环：`mwseo_do_seo_scan` 对每篇文章进行处理，然后使用 `mwseo_set_seo_title` 和 `mwseo_set_seo_excerpt` 进行优化

### 发布文章（WordPress 核心功能）
1. 使用 `wp_create_post` 方法创建文章，传入 `post_title`、`post_content` 和 `post_status: "draft"` 参数
2. 如果启用了 SEO Engine，可以设置 SEO 元数据
3. 当文章准备就绪后，使用 `wp_update_post` 方法并将 `post_status` 设置为 “publish”

### 翻译工作流程（Polylang）
1. `pll_translation_status` — 查看翻译的缺失部分
2. `pll_get_posts_missing_translation` — 获取需要翻译的文章及其目标语言
3. `pll_create_translation` — 创建与原文关联的翻译版本

### 多站点管理

将多个站点信息存储在 `TOOLS.md` 文件中，并通过站点名称进行选择：
```
### My Blog
- **URL:** https://blog.example.com/wp-json/mcp/v1/http
- **Token:** abc123

### My Shop
- **URL:** https://shop.example.com/wp-json/mcp/v1/http
- **Token:** xyz789
```

## 提示

- 使用 `wp_get_post_snapshot` 代替多次调用，一次请求即可获取文章内容、元数据和分类法信息
- 使用 `wp_alter_post` 进行搜索和替换操作，无需重新上传整个内容
- `wp_get_posts` 默认不返回完整文章内容，如需获取全文请使用 `wp_get_post`
- 分析数据的日期参数应使用 `start_date` 和 `end_date`（而非驼峰式命名法）
- 始终先运行 `tools/list`，因为可用的工具取决于管理员启用了哪些功能