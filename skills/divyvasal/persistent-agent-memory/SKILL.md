---
name: persistent-agent-memory
description: "为任何代理添加持久性内存（persistent memory），使其能够记住之前的工作内容、在会话之间保持上下文信息，并继续执行长时间运行的工作流程。"
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

该功能由 Coral Bricks 提供，用于存储和检索内存数据。它可以存储事实、偏好设置以及相关上下文信息，并允许用户根据特定主题或意图来检索这些数据。所有存储的内存信息都保存在默认的集合中。

**适用场景：**  
- 需要记住某些事实或偏好设置以供后续使用；  
- 根据主题或意图检索已存储的信息；  
- 删除与特定查询匹配的内存记录。

**不适用场景：**  
- 网页搜索、文件系统搜索或代码搜索——请使用其他相应的工具。

## 设置  

请设置您的 API 密钥（可在 [https://coralbricks.ai](https://coralbricks.ai) 获取）：  
```bash
export CORAL_API_KEY="ak_..."
```

（可选）您可以自定义 API 的 URL（默认值为 `https://search-api.coralbricks.ai`）：  
```bash
export CORAL_API_URL="https://search-api.coralbricks.ai"
```

## 工具  

### `coral_store` — 存储内存数据  

用于存储文本及其元数据（可选），以便后续根据语义进行检索。  
**参数说明：**  
- `text`（必填）：需要存储的内容  
- `metadata_json`（可选）：元数据的 JSON 字符串，例如 `{"source":"chat","topic":"fitness"}`  

**返回值：**  
包含 `status` 字段的 JSON 对象（例如 `{"status": "success"}`）。  

**示例：**  
```bash
scripts/coral_store "User prefers over-ear headphones with noise cancellation"
scripts/coral_store "Q3 revenue was $2.1M" '{"source":"report"}'
```

### `coral_retrieve` — 根据语义检索内存数据  

根据内容的语义相似性来检索已存储的信息，并按相关性对结果进行排序。  
**参数说明：**  
- `query`（必填）：用于描述要检索内容的自然语言查询  
- `k`（可选，默认值为 10）：返回的结果数量  

**返回值：**  
包含 `results` 数组的 JSON 对象，每个元素包含 `text` 和 `score`。  

**示例：**  
```bash
scripts/coral_retrieve "query" [k]
```

### `coral_delete_matching` — 根据查询删除内存数据  

删除与指定查询匹配的内存记录。  
**参数说明：**  
- `query`（必填）：用于指定要删除的内存记录的相关查询  

**返回值：**  
确认操作完成的 JSON 对象。  

**示例：**  
```bash
scripts/coral_delete_matching "query"
```

## 隐私政策  

[隐私政策](https://www.coralbricks.ai/privacy)  

## 其他说明：**  
- 所有内存数据都保存在默认的集合中，且这些集合对代理程序是不可见的；  
- 所有文本数据都会被转换为 768 维的向量以支持语义匹配；  
- 检索结果会按照余弦相似度进行排序（分数越高，相关性越高）；  
- 存储的内存数据会在会话之间保持持久性；  
- `metadata` 字段支持自定义格式的 JSON 数据，可用于对内存记录进行分类和过滤；  
- 详情和更多示例请参阅 [AI 代理的持久化内存功能](https://www.coralbricks.ai/blog/persistent-memory-openclaw)。  

## 索引延迟  

在极少数情况下，存储后的数据可能需要最多 1 秒才能立即被检索到。