---
name: baidu-baike-search
description: 百度百科组件是一种知识服务工具，旨在为用户查询各种名词的权威百科解释。其核心功能是：当用户提供一个特定的“名词”（如物体、人物、地点、概念、事件等）时，该工具会返回来自百度百科的标准化、详细的条目解释。
homepage: https://baike.baidu.com/
metadata: { "openclaw": { "emoji": "📖", "requires": { "bins": ["curl"] ,"env":["BAIDU_API_KEY"]},"primaryEnv":"BAIDU_API_KEY" } }
---

# 百度百科

此技能允许 OpenClaw 代理通过百度百科搜索详细的条目解释。

## 设置

1. **API 密钥：** 确保 `BAIDU_API_KEY` 环境变量已设置为有效的 API 密钥。
2. **运行时环境：** API 密钥必须在运行时环境中可用。
3. **BAIDU_API_KEY：** 如需获取 API 密钥，请访问百度云平台（https://login.bce.baidu.com）并注册账户；如果已有账户，可前往 [API 密钥获取页面](https://console.bce.baidu.com/qianfan/ais/console/apiKey) 获取 API 密钥。

## API 表格
|    名称          |               路径                |            描述                                      |
|------------|---------------------------------|---------------------------------------|
|  LemmaList   | /v2/baike/lemma/get_list_by_title   | 查询与指定术语相同的条目列表，返回结果中的 `is_default` 字段表示主题术语 |
| LemmaContent | /v2/baike/lemma/get_content    | 根据条目 ID 或条目名称查询条目的解释或详细内容，建议使用条目 ID 进行查询 |

## 工作流程

1. 该技能仅支持搜索客观存在的事物（如事物、人物、地名、概念、事件等）的详细知识解释。因此，请在调用相关 API 之前提取这些名词。
2. 脚本会向百度百科搜索 API 发送 GET 请求。
3. API 会返回结构化的搜索结果，包括 `lemma_id`、`desc`、`url`、`lemma_summary`、`videos` 和 `relations` 等信息；如果查询的“名词”是知名人物或事物，系统会返回与该名词相关的人或事物的信息。
4. 如果根据默认术语名称查询的内容不准确，可以先使用 `LemmaList` API 查询术语列表，然后从列表中选择符合条件的术语 ID，再使用 `LemmaContent` API 查询该术语的内容。
5. 搜索脚本位于 `scripts/baidu_baike.sh` 文件中。

## API

### LemmaList API

#### 参数

- `lemma_title`：搜索条目的名称
- `top_k`：返回的结果数量（默认值：5）

#### 使用示例
```bash
curl -XGET 'https://appbuilder.baidu.com/v2/baike/lemma/get_content?lemma_title=刘德华' \
-H 'Authorization: Bearer BAIDU_API_KEY'
```

### LemmaContent API

#### 参数

- `search_type`：搜索类型（可选值：`lemmaTitle`、`lemmaId`）
- `search_key`：搜索关键字，可以是条目名称或条目 ID

#### 使用示例
```bash
curl -XGET 'https://appbuilder.baidu.com/v2/baike/lemma/get_content?search_type=lemmaTitle&search_key=刘德华' \
-H 'Authorization: Bearer BAIDU_API_KEY'
```

## 执行脚本

**示例 1：用户仅提供术语名称时**
```bash
BAIDU_API_KEY=xxx sh scripts/baidu_baike.sh 'search' '$lemmaTitle'
```

**示例 2：用户仅提供术语 ID 时**
```bash
BAIDU_API_KEY=xxx sh scripts/baidu_baike.sh 'search_by_id' '$lemmaId'
```

**示例 3：用户提供术语名称但希望根据术语 ID 进行搜索时**
```bash
BAIDU_API_KEY=xxx sh scripts/baidu_baike.sh 'list_by_title' '$lemmaTitle'
```