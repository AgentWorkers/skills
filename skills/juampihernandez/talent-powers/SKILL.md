---
name: builder-data
description: 通过 Talent Protocol API 查询构建器（Query Builder）的信誉数据。可以获取构建器的排名（Rank），验证用户的身份（是否为真人），解析用户的身份信息（来自 Twitter、Farcaster、GitHub 或钱包），按地理位置/国家进行搜索，获取用户的凭证信息，并结合 GitHub 数据对构建器的信息进行进一步补充。
---

# 人才能力

从 [Talent Protocol](https://talent.app) 查询专业数据——这是一个追踪开发者的平台

**使用此技能可以：**
- 按位置、技能或身份（Twitter/GitHub/Farcaster/钱包）查找经过验证的开发者
- 查看开发者的声誉（默认显示排名，仅在请求时提供分数）
- 将 Twitter 账户与钱包地址关联起来
- 验证用户的真实身份
- 搜索开发者的信息（收入、贡献、参加过的黑客马拉松、签订的合同等）
- 查看每位开发者正在开发的项目

## 所需凭证

| 变量 | 是否必需 | 说明 | 获取途径 |
|----------|----------|-------------|-----------|
| `TALENT_API_KEY` | 是 | Talent Protocol 的 API 密钥（用于读取个人资料/身份数据） | https://talent.app/~/settings/api |
| `GITHUB_TOKEN` | 否 | 个人访问令牌，可提高 GitHub 的请求速率限制（从每小时 60 次增加到 5,000 次） | https://github.com/settings/tokens |

**基础 URL：** `https://api.talentprotocol.com`

```bash
curl -H "X-API-KEY: $TALENT_API_KEY" "https://api.talentprotocol.com/..."
```

## 端点

| 端点 | 功能 |
|----------|---------|
| `/search/advanced/profiles` | 按身份、标签、排名或验证结果搜索个人资料 |
| `/profile` | 通过 ID 获取个人资料 |
| `/accounts` | 获取关联的钱包、GitHub 账户及社交媒体信息 |
| `/socials` | 获取社交媒体资料及个人简介 |
| `/credentials` | 获取开发者的数据（收入、关注者数量、参加过的黑客马拉松等） |
| `/human_checkmark` | 验证用户身份（可选，默认不使用） |
| `/scores` | 获取开发者的排名（默认）或分数（仅在请求时提供） |

## 关键参数

**身份验证：**
```
query[identity]={handle}&query[identity_type]={twitter|github|farcaster|ens|wallet}
```

**筛选条件（所有条件均为可选，仅在查询相关时使用）：**
```
query[tags][]=developer              # filter by tag (developer, designer, etc.)
query[verified_nationality]=true     # only verified nationality
query[human_checkmark]=true          # only human-verified (reduces results significantly)
```

**排序方式：**
```
sort[score][order]=desc&sort[score][scorer]=Builder%20Score
```

**分页：`page=1&per_page=250`（每页最多显示 250 条记录）**

## URL 编码

`[` = `%5B`, `]` = `%5D`, 空格 = `%20`

## 响应字段

**默认返回的字段（除非用户特别请求分数）：**
- `builder_score.rank_position` - 主要排名指标
- `scores[].rank_position`（当 `slug = "builder_score"` 时） - 最新排名

**仅在用户请求分数时返回：**
- `builder_score.points` - 分数值
- `scores[].points` - 单个项目的得分
- `location` - 用户输入的位置信息（会包含在响应中）

## 地理位置筛选

**请勿使用** `query[standardized_location]=Country`——该方法无效。

**建议使用 `customQuery` 和正则表达式进行筛选：**

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
    "sort": { "score": { "order": "desc", "scorer": "Builder Score" } },
    "perPage": 50
  }'
```

更多示例请参阅 [use-cases.md](references/use-cases.md#by-location-country)。

## 限制：

- 每页最多显示 250 条记录
- 大多数端点仅支持 GET 请求（`customQuery` 需要 POST 请求）
- 简单的 `query[standardized_location]` 参数可能无法正常工作，请使用 `customQuery` 和正则表达式进行筛选

## 通过 GitHub 丰富数据

从 `/accounts` 获取开发者关联的 GitHub 项目/仓库信息：

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

**建议使用 GitHub 令牌：** 未使用令牌时，GitHub 每小时仅允许 60 次请求；使用个人访问令牌后，每小时请求次数可增加到 5,000 次。
- 创建令牌的方法：https://github.com/settings/tokens → “生成新令牌（经典模式）”，公共数据无需指定权限范围
- 使用方法：`-H "Authorization: token $GITHUB_TOKEN"`）

## 参考资料：

- [endpoints.md](references/endpoints.md) - 完整的端点文档
- [use-cases.md](references/use-cases.md) - 常见使用场景
- [github-enrichment.md](references/github-enrichment.md) - 如何通过 GitHub 丰富数据