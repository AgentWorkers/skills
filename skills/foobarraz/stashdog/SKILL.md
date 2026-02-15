---
name: stashdog
version: 1.0.0
description: 连接到Raz的StashDog库存MCP服务器（通过mcp-remote使用OAuth进行身份验证），并执行常见的库存操作：列出物品、搜索物品以及添加物品。
---
# StashDog MCP 技能

StashDog 是 Raz 的物品管理应用程序。本技能文档介绍了如何连接到 StashDog MCP 服务器，并提供了用于执行常见任务的辅助命令。

## MCP 连接

- **端点：** `https://gmchczeyburroiyzefie.supabase.co/functions/v1/mcp-server/mcp`
- **认证方式：** OAuth（通过 `mcp-remote` 代理）
- **可用工具：** `list_items`、`search_items`、`get_item`、`add_item`、`edit_item`、`delete_item`

### 推荐的 MCP 服务器配置

请在您的 MCP 客户端配置中使用以下服务器信息：

```json
{
  "mcpServers": {
    "stashdog": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://gmchczeyburroiyzefie.supabase.co/functions/v1/mcp-server/mcp"
      ]
    }
  }
}
```

首次尝试连接后，请完成 OAuth 浏览器流程。

## 辅助命令（mcporter）

您可以使用 `mcporter` 直接调用这些工具：

```bash
# 1) Trigger OAuth and connect
mcporter auth "https://gmchczeyburroiyzefie.supabase.co/functions/v1/mcp-server/mcp"

# 2) List items
mcporter call "https://gmchczeyburroiyzefie.supabase.co/functions/v1/mcp-server/mcp/list_items" limit=25 offset=0 include_archived=false include_deleted=false

# 3) Search items
mcporter call "https://gmchczeyburroiyzefie.supabase.co/functions/v1/mcp-server/mcp/search_items" query="wrench" limit=20

# 4) Add an item
mcporter call "https://gmchczeyburroiyzefie.supabase.co/functions/v1/mcp-server/mcp/add_item" name="Socket Set" description="Metric sockets" tags='["tools","garage"]'
```

## 工具参考

- `list_items(limit, offset, include_archived, include_deleted)`  
- `search_items(query, limit)`  
- `get_item(item_id)`  
- `add_item(name, description?, tags?, container_id?, is_storage?)`  
- `edit_item(item_id, name?, description?, tags?, is_archived?)`  
- `delete_item(item_id)`