---
name: happenstance
description: 使用 **Happenstance API** 在你的专业人脉网络中搜索并研究相关人员。
metadata:
  openclaw:
    requires:
      env:
        - HAPPENSTANCE_API_KEY
      bins:
        - curl
    primaryEnv: HAPPENSTANCE_API_KEY
---
# Happenstance

使用Happenstance API可以搜索您的网络，并获取人员的详细研究资料。

文档链接：https://developer.happenstance.ai

## 认证

所有请求都需要`HAPPENSTANCE_API_KEY`环境变量。请将其作为Bearer令牌传递：

```
Authorization: Bearer $HAPPENSTANCE_API_KEY
```

基础URL：`https://api.happenstance.ai`

## 计费

- **搜索**：每次搜索消耗2个信用点（包括“查找更多”功能）。
- **研究**：每完成一项研究消耗1个信用点。
- 通过`GET /v1/usage`查询剩余信用点。
- 可在https://happenstance.ai/settings/api购买信用点。

## 可用操作

### 1. 搜索您的网络

在各个群组和联系人中搜索人员。搜索操作是异步进行的。

**开始搜索：**

```bash
curl -s -X POST https://api.happenstance.ai/v1/search \
  -H "Authorization: Bearer $HAPPENSTANCE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "engineers who have worked on AI infrastructure",
    "include_my_connections": true,
    "include_friends_connections": true
  }'
```

您也可以通过添加`"group_ids": ["uuid1", "uuid2"]`来在特定群组内进行搜索。群组ID可通过`GET /v1/groups`获取。

至少需要提供一个搜索条件：`group_ids`、`include_my_connections: true`或`include_friends_connections: true`。

**响应：**

```json
{"id": "search-uuid", "url": "https://happenstance.ai/search/search-uuid"}
```

**轮询结果**（每5-10秒一次，直到状态变为`COMPLETED`或`FAILED`）：

```bash
curl -s https://api.happenstance.ai/v1/search/SEARCH_ID \
  -H "Authorization: Bearer $HAPPENSTANCE_API_KEY"
```

**完成后的响应包含：**

- `status`：`RUNNING`、`COMPLETED`或`FAILED`
- `results`：人员信息数组，每个条目包含`id`、`name`、`current_title`、`current_company`、`summary`、`weighted_traits_score`、`socials`（包含`happenstance_url`、`linkedin_url`、`twitter_url`）、`mutuals`和`traits`
- `has_more`：布尔值，表示是否还有更多结果可用
- `mutuals`：互连人员的顶层数组（结果通过索引引用）
- `traits`：特征定义的顶层数组（结果通过索引引用）

### 2. 查找更多结果

当搜索结果中的`has_more`为`true`时，可以获取额外的结果（排除之前已返回的人员）。此操作消耗2个信用点。

```bash
curl -s -X POST https://api.happenstance.ai/v1/search/SEARCH_ID/find-more \
  -H "Authorization: Bearer $HAPPENSTANCE_API_KEY"
```

**响应：**

```json
{"page_id": "page-uuid", "parent_search_id": "search-uuid"}
```

然后使用`page_id`继续轮询结果：

```bash
curl -s "https://api.happenstance.ai/v1/search/SEARCH_ID?page_id=PAGE_ID" \
  -H "Authorization: Bearer $HAPPENSTANCE_API_KEY"
```

### 3. 研究一个人

获取特定人员的详细职业资料。操作是异步进行的。

**开始研究：**

```bash
curl -s -X POST https://api.happenstance.ai/v1/research \
  -H "Authorization: Bearer $HAPPENSTANCE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"description": "Garry Tan, CEO of Y Combinator, @garrytan on Twitter"}'
```

请尽可能包含更多详细信息（全名、公司、职位、位置、社交账号），以获得最佳搜索结果。

**响应：**

```json
{"id": "research-uuid"}
```

**轮询结果**（每5-10秒一次，直到状态变为`COMPLETED`、`FAILED`或`FAILED_AMBIGUOUS`）：

```bash
curl -s https://api.happenstance.ai/v1/research/RESEARCH_ID \
  -H "Authorization: Bearer $HAPPENSTANCE_API_KEY"
```

**完成后的响应包含一个`profile`对象，其中包含：**

- `person_metadata`：`full_name`、`alternate_names`、`profile_urls`、`current_locations`、`tagline`
- `employment`：工作记录数组，包含`company_name`、`job_title`、`start_date`、`end_date`、`description`
- `education`：教育背景数组，包含`university_name`、`degree`、`start_date`、`end_date`
- `projects`：项目记录数组，包含`title`、`description`、`urls`
- `writings`：出版物记录数组，包含`title`、`description`、`date`、`urls`
- `hobbies`：兴趣爱好数组
- `summary`：包含相关链接的总体文本摘要

### 4. 列出群组

获取可搜索的群组列表：

```bash
curl -s https://api.happenstance.ai/v1/groups \
  -H "Authorization: Bearer $HAPPENSTANCE_API_KEY"
```

返回格式：`{"groups": [{"id": "uuid", "name": "Group Name"}, ...]`。

### 5. 查询信用点和使用情况

```bash
curl -s https://api.happenstance.ai/v1/usage \
  -H "Authorization: Bearer $HAPPENSTANCE_API_KEY"
```

返回剩余信用点数（`balance_credits`）、是否拥有信用点（`has_credits`）、购买记录（`purchases`）、使用历史以及自动刷新设置。

## 错误处理

错误信息遵循RFC 7807格式：

```json
{"type": "about:blank", "title": "Bad Request", "status": 400, "detail": "Description must not be empty", "instance": "/v1/research"}
```

主要状态码：
- `401`：API密钥无效或缺失
- `402`：信用点不足
- `429`：并发请求过多（最多同时进行10个搜索或研究请求）
- `500`/`503`：服务器错误，请稍后重试。

## 提示

- 在开始多次搜索或研究请求之前，请务必检查剩余信用点。
- 搜索通常在30-60秒内完成；研究可能需要1-3分钟。
- 每次搜索最多返回30个结果。可使用“查找更多”功能获取更多页面。
- 在展示搜索结果时，请包含人员的姓名、职位、公司名称、摘要以及Happenstance个人资料链接。
- 用户连接的资料来源越多，搜索结果越准确。