---
name: baidu-baike
description: 百度百科组件是一种知识服务工具，旨在为用户查询各种名词的权威百科解释。其核心功能是：当用户提供一个特定的“名词”（如物体、人物、地点、概念、事件等）时，该工具会返回来自百度百科的标准化、详细的条目解释。
homepage: https://baike.baidu.com/
metadata: { "openclaw": { "emoji": "📖", "requires": { "bins": ["curl"] } } }
---

# 百度百科

该技能允许 OpenClaw 代理通过百度百科搜索详细的条目说明。

## 设置

1. **API 密钥：** 确保 `BAIDU_API_KEY` 环境变量已设置为您的有效 API 密钥。
2. **运行时环境：** API 密钥应在运行时环境中可用。

## API 表格
|    名称          |                路径                |            描述                                      |
|------------|---------------------------------|---------------------------------------|
| LemmaList   | /v2/baike/lemma/get_list_by_title   | 查询与指定术语相同的条目列表，返回结果中的 `is_default` 字段表示该术语的主体术语 |
| LemmaContent | /v2/baike/lemma/get_content     | 根据条目 ID 或条目名称查询条目的说明或详细内容，建议使用条目 ID 进行查询 |

## 工作流程

1. 该技能仅支持搜索客观存在的事物（如事物、人物、地名、概念、事件等）的详细知识说明。因此，请在调用相关接口之前提取这些名词。
2. 脚本会向百度百科搜索 API 发送 GET 请求。
3. 如果查询的名词是知名人物或事物，API 会返回与该名词相关联的信息（如视频、关系等）。
4. 如果根据默认术语名称查询的内容不准确，您可以先使用 `LemmaList` API 查询术语列表，然后从列表中选择符合条件的术语 ID，再使用 `LemmaContent` API 查询该术语的内容。

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

- `search_type`：搜索类型，可选值包括：“lemmaTitle”和“lemmaId”
- `search_key`：搜索关键词，可以是条目名称或条目 ID

#### 使用示例
```bash
curl -XGET 'https://appbuilder.baidu.com/v2/baike/lemma/get_content?search_type=lemmaTitle&search_key=刘德华' \
-H 'Authorization: Bearer BAIDU_API_KEY'
```