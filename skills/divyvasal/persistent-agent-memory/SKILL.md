---
name: persistent-agent-memory
description: "为任何代理（agent）添加持久性内存（persistent memory），以便其能够记住之前的工作内容、在会话之间保持上下文信息，并继续执行长时间运行的工作流程。适用场景包括：  
(1) 以后需要使用某些事实或偏好设置；  
(2) 按主题或意图检索存储的记忆内容；  
(3) 删除与特定查询匹配的记忆记录。  
**不适用于以下场景**：  
- 网页搜索；  
- 文件系统搜索；  
- 代码搜索——这些场景应使用其他工具来完成。"
metadata:
  {
    "openclaw":
      {
        "requires": { "env": ["CORAL_API_KEY"], "bins": ["curl", "python3"] },
        "primaryEnv": "CORAL_API_KEY",
        "homepage": "https://coralbricks.ai",
        "privacyPolicy": "https://www.coralbricks.ai/privacy",
        "emoji": "🧠",
      },
  }
---
# 持久化代理内存（Persistent Agent Memory）

内存存储和检索功能由 Coral Bricks 提供支持。该系统用于存储事实信息、用户偏好及上下文数据，并可根据语义内容进行后续检索。所有存储的数据都保存在默认的集合中。

## 设置（Setup）

请设置您的 API 密钥（可在 [https://coralbricks.ai](https://coralbricks.ai) 获取）：

```bash
export CORAL_API_KEY="ak_..."
```

（可选）您可以自定义 API 的 URL（默认值为 `https://search-api.coralbricks.ai`）：

```bash
export CORAL_API_URL="https://search-api.coralbricks.ai"
```

## 工具（Tools）

### `coral_store` — 存储数据

用于存储文本及可选的元数据，以便后续根据语义内容进行检索。

```bash
scripts/coral_store "text to store" [metadata_json]
```

- `text`（必填）：需要存储的内容
- `metadata_json`（可选）：元数据的 JSON 字符串，例如 `{"source":"chat","topic":"fitness"}`

返回值：包含 `status` 字段的 JSON 对象（例如 `{"status": "success"}`）。

示例：

```bash
scripts/coral_store "User prefers over-ear headphones with noise cancellation"
scripts/coral_store "Q3 revenue was $2.1M" '{"source":"report"}'
```

### `coral_retrieve` — 根据语义内容检索数据

根据文本的语义相似度检索已存储的数据，并按相关性对结果进行排序。

```bash
scripts/coral_retrieve "query" [k]
```

- `query`（必填）：用于描述需要检索内容的自然语言查询
- `k`（可选，默认值为 10）：返回的结果数量

返回值：一个包含 `results` 数组的 JSON 对象，每个元素包含 `text` 和 `score`。

示例：

```bash
scripts/coral_retrieve "wireless headphones preference" 5
scripts/coral_retrieve "quarterly revenue" 10
```

### `coral_delete_matching` — 根据查询删除数据

删除与指定查询匹配的数据。请明确指定需要删除的内容。

```bash
scripts/coral_delete_matching "query"
```

- `query`（必填）：用于描述需要删除的数据的自然语言查询

返回值：一个确认操作完成的 JSON 对象。

示例：

```bash
scripts/coral_delete_matching "dark mode preference"
scripts/coral_delete_matching "forget my workout notes"
```

## 隐私政策（Privacy）

[隐私政策](https://www.coralbricks.ai/privacy)

## 注意事项（Notes）

- 所有数据都保存在默认的集合中；这些集合对代理程序是不可见的。
- 所有文本都会被转换为 768 维的向量以支持语义匹配。
- 结果会按照余弦相似度进行排序（分数越高，相关性越强）。
- 存储的数据会在会话之间持续保留。
- `metadata` 字段支持自由格式的 JSON 数据；您可以使用它来为数据添加标签以便于筛选。
- 有关更多详细信息和示例，请参阅 [AI 代理的持久化内存功能](https://www.coralbricks.ai/blog/persistent-memory-openclaw)。

## 索引延迟（存储后需要一段时间才能检索）

在极少数情况下，数据可能在存储后需要 1 秒左右的时间才能被成功检索到。