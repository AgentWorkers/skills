# Feishu 搜索功能

Feishu（Lark）资源的统一搜索接口。

## 先决条件

- 请先安装 `feishu-common`。
- 该功能依赖于 `../feishu-common/index.js` 来处理令牌（token）和 API 认证。

## 功能特点

- **搜索消息**：可以在私信和群聊中查找聊天记录。
- **搜索文档**：可以查找文档、表格（sheets）和数据表（bitables）。
- **搜索日历**：（计划中）可以查找日历事件。

## 使用方法

```bash
# Search messages
node skills/feishu-search/index.js search_messages --query "bug report" --limit 10

# Search docs
node skills/feishu-search/index.js search_docs --query "Q3 Roadmap"
```

## 配置要求

需要标准的 Feishu 环境变量（`FEISHU_APP_ID`、`FEISHU_APP_SECRET`）或有效的 `FEISHU_TOKEN`。
该功能使用 `../feishu-common/index.js` 中提供的共享认证机制。