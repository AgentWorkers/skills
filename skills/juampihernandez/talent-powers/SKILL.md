---
name: talent-powers
description: 通过 Talent Protocol API 查询构建器的信誉数据：获取构建器的排名、验证用户身份（Twitter/Farcaster/GitHub/钱包信息）、按地理位置或国家进行搜索、获取用户的凭证信息，并结合 GitHub 数据来完善构建器的信息。
---

# 人才能力（Talent Powers）

从 [Talent Protocol](https://talent.app) 查询专业数据——这是一个用于追踪区块链开发者的平台。

**使用此功能可：**
- 按地理位置、技能或身份（Twitter/GitHub/Farcaster/钱包）查找经过验证的开发者；
- 查看开发者的声誉分数和排名；
- 将 Twitter 账户与钱包关联起来；
- 验证用户的真实身份；
- 查找开发者的资质信息（收入、贡献、参与过的黑客马拉松、签订的合同等）；
- 了解开发者正在参与或开发的项目。

**API 密钥：** https://talent.app/~/settings/api  
**基础 URL：** `https://api.talentprotocol.com`

```bash
curl -H "X-API-KEY: $TALENT_API_KEY" "https://api.talentprotocol.com/..."
```

## 端点（Endpoints）

| 端点（Endpoint） | 功能（Function） |
|------------|-------------------|
| `/search/advanced/profiles` | 按身份、标签、排名或验证状态搜索开发者资料 |
| `/profile` | 通过 ID 获取开发者资料 |
| `/accounts` | 获取开发者关联的钱包、GitHub 账户及社交媒体信息 |
| `/socials` | 获取开发者的社交媒体资料和简介 |
| `/credentials` | 获取开发者的数据信息（收入、关注者数量、参与过的黑客马拉松等） |
| `/human_checkmark` | 验证用户身份是否经过人工审核 |
| `/farcaster/scores` | 批量查询 Farcaster 用户的信息 |

## 关键参数（Key Parameters）

**身份验证：**
```
query[identity]={handle}&query[identity_type]={twitter|github|farcaster|ens|wallet}
```

**筛选条件（Filters）：**
```
query[human_checkmark]=true
query[verified_nationality]=true
query[tags][]=developer
```

**排序方式（Sorting）：**
```
sort[score][order]=desc&sort[score][scorer]=Builder%20Score
```

**分页（Pagination）：`page=1&per_page=250`（每页最多显示 250 条记录）

## URL 编码（URL Encoding）

`[` = `%5B`, `]` = `%5D`, 空格 = `%20`

## 响应字段（Response Fields）

- `builder_score.rank_position`：主要指标
- `location`：用户输入的地理位置（会在响应中返回）
- `scores[]`：使用 `builder_score_2025` 获取最新的排名信息

## 地理位置筛选（Location Filter）

**请勿使用** `query[standardized_location]=Country` —— 该方式无效。

**建议使用 `customQuery` 并结合正则表达式进行筛选：**

```bash
curl -X POST -H "X-API-KEY: $TALENT_API_KEY" -H "Content-Type: application/json" \
  "https://api.talentprotocol.com/search/advanced/profiles" \
  -d '{
    "customQuery": {
      "regexp": {
        "standardized_location": {
          "value": ".*argentina.*",
          "case_insensitive": true
        }
      }
    },
    "humanCheckmark": true,
    "sort": { "score": { "order": "desc", "scorer": "Builder Score" } },
    "perPage": 50
  }'
```

更多使用示例请参阅 [use-cases.md](references/use-cases.md#by-location-country)。

## 限制条件（Limitations）

- 每页最多显示 250 条记录
- 大多数端点仅支持 GET 请求（`customQuery` 需使用 POST 请求）
- 简单的 `query[standardized_location]` 参数可能无法正常工作，请使用 `customQuery` 和正则表达式进行筛选

## GitHub 数据扩展（GitHub Enrichment）

通过 `/accounts` 获取用户的 GitHub 账户后，可进一步获取其相关项目信息：

```bash
# 1. Get GitHub username
/accounts?id={profile_id} → { "source": "github", "username": "..." }

# 2. Query GitHub
GET https://api.github.com/users/{username}                           # Profile
GET https://api.github.com/users/{username}/repos?sort=stars&per_page=5   # Top repos
GET https://api.github.com/users/{username}/repos?sort=pushed&per_page=5  # Recent
GET https://api.github.com/users/{username}/events/public             # Commits
GET https://api.github.com/search/issues?q=author:{username}+type:pr+state:open  # Open PRs
```

GitHub 令牌：https://github.com/settings/tokens（未使用令牌时每小时请求 60 次，使用令牌时每小时请求 5000 次）

## 参考资料（References）

- [endpoints.md](references/endpoints.md) —— 完整的端点文档
- [use-cases.md](references/use-cases.md) —— 常见使用场景
- [github-enrichment.md](references/github-enrichment.md) —— GitHub 数据相关说明