---
name: attio
description: Attio CRM集成工具用于管理公司、人员、交易、笔记、任务以及自定义对象。适用于处理Attio CRM数据、搜索联系人、管理销售流程、为记录添加备注、创建任务或同步潜在客户信息等场景。
---

# Attio CRM

通过 REST API 管理 Attio CRM。支持公司、人员、交易、列表（工作流程）、笔记和任务的管理。

## 设置

在环境变量或 `~/.env` 文件中设置 `ATTIO_API_KEY`：
```bash
echo "ATTIO_API_KEY=your_api_key" >> ~/.env
```

获取您的 API 密钥：访问 Attio → 工作区设置 → 开发者 → 新访问令牌

## 快速参考

### 对象（记录）

```bash
# List/search records
attio objects list                     # List available objects
attio records list <object>            # List records (companies, people, deals, etc.)
attio records search <object> <query>  # Search by text
attio records get <object> <id>        # Get single record
attio records create <object> <json>   # Create record
attio records update <object> <id> <json>  # Update record
```

### 列表（工作流程）

```bash
attio lists list                       # Show all pipelines/lists
attio entries list <list_slug>         # List entries in a pipeline
attio entries add <list_slug> <object> <record_id>  # Add record to pipeline
```

### 笔记

```bash
attio notes list <object> <record_id>  # Notes on a record
attio notes create <object> <record_id> <title> <content>
```

### 任务

```bash
attio tasks list                       # All tasks
attio tasks create <content> [deadline]  # Create task (deadline: YYYY-MM-DD)
attio tasks complete <task_id>         # Mark complete
```

## 示例

### 查找一家公司并添加笔记
```bash
# Search for company
attio records search companies "Acme"

# Add note to the company (using record_id from search)
attio notes create companies abc123-uuid "Call Notes" "Discussed Q1 roadmap..."
```

### 操作工作流程
```bash
# List pipeline stages
attio entries list sales_pipeline

# Add a company to pipeline
attio entries add sales_pipeline companies abc123-uuid
```

### 创建跟进任务
```bash
attio tasks create "Follow up with John at Acme" "2024-02-15"
```

## API 限制

- 请求速率限制：约 100 次/分钟
- 分页：对于大量数据集，请使用 `limit` 和 `offset` 参数进行分页

## 完整的 API 文档

https://docs.attio.com/