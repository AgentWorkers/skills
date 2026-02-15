---
name: hardcover
description: 通过 GraphQL API 从 Hardcover.app 查询阅读列表和书籍数据。以下情况会触发该功能：  
- 用户提及 Hardcover 时；  
- 用户询问自己的阅读列表或图书馆信息时；  
- 用户想了解书籍的阅读进度时；  
- 用户搜索书籍、作者或系列时；  
- 用户查询“正在阅读的书籍”、“想阅读的书籍”或“已读过的书籍”时。  
此外，该功能还可用于将阅读数据同步到其他系统（如 Obsidian 等），或帮助用户跟踪阅读目标。
homepage: https://hardcover.app
metadata:
  {
    "openclaw":
      {
        "emoji": "📚",
        "requires": { "env": ["HARDCOVER_API_TOKEN"] },
      },
  }
---

# Hardcover GraphQL API

您可以查询自己的阅读库、书籍元数据，以及Hardcover的图书目录。

## 配置

- **环境变量：** `HARDCOVER_API_TOKEN`（从 https://hardcover.app/settings 获取）
- **端点：** `https://api.hardcover.app/v1graphql`
- **速率限制：** 每分钟60次请求，超时时间为30秒，查询深度最多为3层

## 认证

所有请求都需要包含 `Authorization: Bearer {token}` 头部（`token` 从设置中获取，需在请求前加上 `Bearer ` 前缀）：

```bash
curl -X POST https://api.hardcover.app/v1/graphql \
  -H "Authorization: Bearer $HARDCOVER_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "query { me { id username } }"}'
```

## 工作流程

1. **首先获取用户ID** — 大多数查询都需要用户ID：
   ```graphql
   query { me { id username } }
   ```

2. **按状态查询** — 使用 `status_id` 进行过滤：
   - `1` = 想阅读
   - `2` = 正在阅读
   - `3` = 已读
   - `4` = 暂停
   - `5` = 未读完

3. **分页显示大量结果** — 使用 `limit` 和 `offset` 参数，并添加 `distinct_on: book_id` 以确保结果唯一：

## 常用查询

### 显示当前正在阅读的书籍及其阅读进度

```graphql
query {
  me {
    user_books(where: { status_id: { _eq: 2 } }) {
      user_book_reads { progress_pages }
      book {
        title
        pages
        image { url }
        contributions { author { name } }
      }
    }
  }
}
```

### 按状态查询书籍

```graphql
query ($userId: Int!, $status: Int!) {
  user_books(
    where: { user_id: { _eq: $userId }, status_id: { _eq: $status } }
    limit: 25
    offset: 0
    distinct_on: book_id
  ) {
    book {
      id
      title
      pages
      image { url }
      contributions { author { name } }
    }
  }
}
```

### 搜索书籍/作者/系列

```graphql
query ($q: String!, $type: String!) {
  search(query: $q, query_type: $type, per_page: 10, page: 1) {
    results
  }
}
```

`query_type`：`Book`, `Author`, `Series`, `Character`, `List`, `Publisher`, `User`

### 按书名查询书籍详情

```graphql
query {
  editions(where: { title: { _eq: "Oathbringer" } }) {
    title
    pages
    isbn_13
    edition_format
    publisher { name }
    book {
      slug
      contributions { author { name } }
    }
  }
}
```

## 限制

- 仅支持读取操作（目前不支持数据修改）
- 不支持文本搜索操作（如 `_like`, `_ilike`, `_regex`）
- 访问权限仅限于：您的个人数据、公开数据以及您关注的用户的数据
- API令牌的有效期为1年

## 实体参考

有关书籍、版本、作者、系列、用户书籍、活动、列表、目标等实体的详细字段说明，请参阅 [references/entities.md](references/entities.md)。

## 响应代码

| 代码 | 含义 |
|------|---------|
| 200 | 请求成功 |
| 401 | 令牌无效或已过期 |
| 429 | 超过速率限制 |