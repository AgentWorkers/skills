---
name: linkdapi-openclaw
description: >
  **完整的 LinkdAPI 集成 OpenClaw 技能**  
  该技能涵盖了 LinkdAPI 的所有 50 多个接口（endpoint），以及 Python/Node.js/Go 语言的 SDK、认证机制、速率限制功能以及实际应用示例。无论用户需要查询 LinkedIn 用户资料、搜索 LinkedIn 用户或公司信息、丰富潜在客户信息、研究 LinkedIn 上的职位信息、抓取 LinkedIn 的帖子或文章、进行 B2B 业务开发、获取 LinkedIn 公司数据，还是调用任何 LinkedIn 数据 API，都可以使用此技能。  
  **使用说明：**  
  无论用户的需求是什么（例如“在 LinkedIn 上找到我”、“查询这家公司”或“在 LinkedIn 上搜索柏林的工程师”），都应优先使用此技能来完成与 LinkedIn 数据相关的任务。
version: 1.0.0
author: LinkdAPI Team
---
# LinkdAPI技能 — LinkedIn数据API

使用此技能通过LinkdAPI REST API访问**LinkedIn**的专业人士数据。

> 完整的端点参考（包含参数、枚举和响应格式）→ `references/api-ref.md`
> 结构化的端点清单（JSON格式）→ `references/skills.json`

---

## ⚠️ 认证 — 请先阅读

| 参数 | 值 |
|---|---|
| **认证头** | `X-linkdapi-apikey` |
| **基础URL** | `https://linkdapi.com` |
| **环境变量** | `LINKDAPI_KEY` |

```bash
curl -s -H "X-linkdapi-apikey: $LINKDAPI_KEY" \
  "https://linkdapi.com/api/v1/profile/overview?username=ryanroslansky" | jq .
```

⛔ **切勿使用`x-api-key`或`Authorization: Bearer`——这两种方式都会导致401错误。正确的认证头是`X-linkdapi-apikey`。**

---

## 核心概念

| 术语 | 含义 | 获取方式 |
|---|---|---|
| `username` | LinkedIn的个人标识符（例如：`linkedin.com/in/USERNAME`） | 从URL中获取 |
| `urn` | LinkedIn的内部ID（例如：`ACoAAAA...`） | 从`profile/overview`响应中获取 |
| `id`（公司） | LinkedIn公司的ID | 从`companies/company/info`或`companies/name-lookup`中获取 |
| `jobId` | LinkedIn职位的ID | 从职位搜索结果中获取 |
| `geoUrn` | 地理位置过滤器ID | 从`geos/name-lookup`中获取 |
| `cursor` | 分页令牌 | 从之前的响应中获取 |

**在使用需要`urn`的端点时，请务必先获取`urn`。**

---

## 端点快速参考

### 个人资料 — `/api/v1/profile/`
| 端点 | 参数 | 用途 |
|---|---|---|
| `overview` | `username` | 基本信息 + `urn` | 从这里开始查询 |
| `details` | `urn` | 职位、教育背景、语言信息 |
| `contact-info` | `username` | 电子邮件、电话、网站信息 |
| `about` | `urn` | 关于个人资料的简介 |
| `full` | `username` 或 `urn` | 一次性获取所有信息 |
| `full-experience` | `urn` | 完整的工作经历 |
| `certifications` | `urn` | 持有的证书 |
| `education` | `urn` | 教育背景 |
| `skills` | `urn` | 技能和推荐信息 |
| `social-matrix` | `username` | 关注者和联系人 |
| `recommendations` | `urn` | 推荐人和被推荐人 |
| `similar` | `urn` | 类似的个人资料 |
| `reactions` | `urn`, `cursor` | 个人资料的互动记录 |
| `interests` | `urn` | 兴趣爱好 |
| `services` | `urn` | 提供的服务 |
| `username-to-urn` | `username` | 通过用户名查询对应的`urn` |

### 公司 — `/api/v1/companies/`
| 端点 | 参数 | 用途 |
|---|---|---|
| `name-lookup` | `query` | 通过名称搜索公司 |
| `company/info` | `id` 或 `name` | 公司详细信息 |
| `company/info-v2` | `id` | 扩展信息 |
| `company/similar` | `id` | 类似的公司 |
| `company/employees-data` | `id` | 公司员工数量及分布 |
| `company/affiliated-pages` | `id` | 子公司信息 |
| `company/posts` | `id`, `start` | 公司发布的帖子 |
| `company/universal-name-to-id` | `universalName` | 通用名称对应的ID |
| `jobs` | `companyIDs`, `start` | 公司发布的职位信息 |

### 职位 — `/api/v1/jobs/`
| 端点 | 参数 | 用途 |
|---|---|---|
| `search` | `keyword`, `location`, `timePosted`, `workArrangement`, `geoId`, `companyIds`, `jobTypes`, `experience`, `salary`, `start` | V1版本的职位搜索 |
| `job/details` | `jobId` | 职位详细信息（仅限已发布的职位） |
| `job/details-v2` | `jobId` | 所有状态的职位信息 |
| `job/similar` | `jobId` | 类似的职位 |
| `job/people-also-viewed` | `jobId` | 相关职位 |
| `job/hiring-team` | `jobId`, `start` | 招聘团队信息 |
| `posted-by-profile` | `profileUrn`, `start`, `count` | 由特定个人发布的职位 |

### 搜索 — `/api/v1/search/`
| 端点 | 关键参数 | 用途 |
|---|---|---|
| `people` | `keyword`, `title`, `currentCompany`, `geoUrn`, `industry`, `firstName`, `lastName`, `start`, `count` | 搜索专业人士 |
| `companies` | `keyword`, `geoUrn`, `companySize`, `hasJobs`, `industry`, `start`, `count` | 搜索公司 |
| `posts` | `keyword`, `sortBy`, `datePosted`, `authorJobTitle`, `fromOrganization`, `contentType`, `start` | 搜索帖子 |
| `jobs` | `keyword`, `workplaceTypes`, `datePosted`, `easyApply`, `companies`, `locations`, `experience`, `salary`, `under10Applicants`, `start`, `count` | V2版本的职位搜索 |
| `services` | `keyword`, `geoUrn`, `serviceCategory`, `profileLanguage`, `start`, `count` | 搜索服务提供商 |
| `schools` | `keyword`, `start`, `count` | 搜索学校 |

### 帖子 — `/api/v1/posts/`
| 端点 | 参数 | 用途 |
|---|---|---|
| `featured` | `urn` | 推荐帖子 |
| `all` | `urn`, `cursor`, `start` | 分页显示所有帖子 |
| `info` | `urn` | 单个帖子的详细信息 |
| `comments` | `urn`, `start`, `count`, `cursor` | 评论信息 |
| `likes` | `urn`, `start` | 评论的点赞数 |

### 评论 — `/api/v1/comments/`
| 端点 | 参数 | 用途 |
|---|---|---|
| `all` | `urn`, `cursor` | 所有评论 |
| `likes` | `urn`, `start` | 评论的点赞数 |

### 文章 — `/api/v1/articles/`
| 端点 | 参数 | 用途 |
|---|---|---|
| `all` | `urn`, `start` | 所有文章 |
| `article/info` | `url` | 文章详细信息 |
| `article/reactions` | `urn`, `start` | 文章的互动记录 |

### 查询
| 路径 | 参数 | 用途 |
|---|---|---|
| `/api/v1/geos/name-lookup` | `query` | 根据地理位置查询`geoUrn` |
| `/api/v1/g/title-skills-lookup` | `query` | 根据技能名称查询ID |
| `/api/v1/g/services-lookup` | `query` | 根据服务类别查询ID |

### 服务 — `/api/v1/services/`
| 端点 | 参数 | 用途 |
|---|---|---|
| `service/details` | 服务页面 |
| `service/similar` | 类似的服务 |

### 系统状态 — `/api/v1/status/` | 系统健康检查（无需认证）

---

## 常见工作流程

### 客户信息丰富化（个人资料研究）

```bash
# Step 1: Get URN
PROFILE=$(curl -s -H "X-linkdapi-apikey: $LINKDAPI_KEY" \
  "https://linkdapi.com/api/v1/profile/overview?username=TARGET_USERNAME")
URN=$(echo $PROFILE | jq -r '.data.urn')
echo "$(echo $PROFILE | jq -r '.data.fullName') → $URN"

# Step 2: Enrich in parallel
curl -s -H "X-linkdapi-apikey: $LINKDAPI_KEY" \
  "https://linkdapi.com/api/v1/profile/full-experience?urn=$URN" | jq '.data.experience[0]' &
curl -s -H "X-linkdapi-apikey: $LINKDAPI_KEY" \
  "https://linkdapi.com/api/v1/profile/skills?urn=$URN" | jq '.data.skills[:5]' &
curl -s -H "X-linkdapi-apikey: $LINKDAPI_KEY" \
  "https://linkdapi.com/api/v1/profile/contact-info?username=TARGET_USERNAME" | jq '.data' &
wait

# Or use full endpoint (one request, more credits)
curl -s -H "X-linkdapi-apikey: $LINKDAPI_KEY" \
  "https://linkdapi.com/api/v1/profile/full?username=TARGET_USERNAME" | jq .data
```

### 公司信息研究

```bash
CO_ID=$(curl -s -H "X-linkdapi-apikey: $LINKDAPI_KEY" \
  "https://linkdapi.com/api/v1/companies/company/info?name=google" | jq -r '.data.id')

curl -s -H "X-linkdapi-apikey: $LINKDAPI_KEY" \
  "https://linkdapi.com/api/v1/companies/company/employees-data?id=$CO_ID" | jq .data &
curl -s -H "X-linkdapi-apikey: $LINKDAPI_KEY" \
  "https://linkdapi.com/api/v1/companies/company/similar?id=$CO_ID" | jq .data &
curl -s -H "X-linkdapi-apikey: $LINKDAPI_KEY" \
  "https://linkdapi.com/api/v1/companies/jobs?companyIDs=$CO_ID&start=0" | jq .data &
wait
```

### ICP人员搜索

```bash
GEO_URN=$(curl -s -H "X-linkdapi-apikey: $LINKDAPI_KEY" \
  "https://linkdapi.com/api/v1/geos/name-lookup?query=San+Francisco" | jq -r '.data[0].urn')

curl -s -H "X-linkdapi-apikey: $LINKDAPI_KEY" \
  "https://linkdapi.com/api/v1/search/people?keyword=VP+Sales&title=VP+Sales&geoUrn=$GEO_URN&start=0" \
  | jq '.data.items'
```

### 职场市场分析

```bash
# V2 (richest filters)
curl -s -H "X-linkdapi-apikey: $LINKDAPI_KEY" \
  "https://linkdapi.com/api/v1/search/jobs?keyword=Software+Engineer&workplaceTypes=remote&datePosted=1week&easyApply=true" \
  | jq .data

# V1 (classic, location string)
curl -s -H "X-linkdapi-apikey: $LINKDAPI_KEY" \
  "https://linkdapi.com/api/v1/jobs/search?keyword=Marketing+Manager&location=London&timePosted=1week&workArrangement=hybrid" \
  | jq .data
```

### 内容研究

```bash
# Posts by a profile
curl -s -H "X-linkdapi-apikey: $LINKDAPI_KEY" \
  "https://linkdapi.com/api/v1/posts/all?urn=$URN&start=0" | jq .data

# Search posts by keyword
curl -s -H "X-linkdapi-apikey: $LINKDAPI_KEY" \
  "https://linkdapi.com/api/v1/search/posts?keyword=AI+marketing&sortBy=date_posted&datePosted=past-week" \
  | jq .data

# Articles
curl -s -H "X-linkdapi-apikey: $LINKDAPI_KEY" \
  "https://linkdapi.com/api/v1/articles/all?urn=$URN&start=0" | jq .data
```

---

## 错误处理

所有响应格式如下：`{"success": bool, "statusCode": int, "message": string, "errors": null|string, "data": ... }`

```bash
RESULT=$(curl -s -H "X-linkdapi-apikey: $LINKDAPI_KEY" \
  "https://linkdapi.com/api/v1/profile/overview?username=someuser")

if echo $RESULT | jq -e '.success == true' > /dev/null 2>&1; then
  echo "OK: $(echo $RESULT | jq -r '.data.fullName')"
else
  CODE=$(echo $RESULT | jq -r '.statusCode')
  MSG=$(echo $RESULT | jq -r '.message')
  echo "Error $CODE: $MSG"
  # 401=invalid key | 404=not found | 429=rate limited (retry with backoff) | 500=server error
  [ "$CODE" = "429" ] && sleep 5 && echo "Retry after backoff"
fi
```

---

## B2B营销策略

| 目标 | 使用的端点 |
|---|---|
| 客户信息丰富化 | `profile/overview` → `profile/full-experience` + `profile/skills` + `profile/contact-info` |
| ICP目标定位 | `geos/name-lookup` → 结合`title`、`currentCompany`和`geoUrn`搜索人员 |
| 竞争对手分析 | `companies/company/posts` 或 `search/posts?fromOrganization=ID` |
| 招聘动态 | `companies/jobs?companyIDs=ID` 以获取招聘信息 |
| 内容灵感 | `posts/all` 了解热门内容及互动数据 |
| 温暖外联准备 | `profile/recommendations` + `posts/all` 为沟通做准备 |
| 职位触发事件 | `jobs/posted-by-profile` 了解哪些公司正在招聘 |

---

## 参考文件

- **`references/api-ref.md`** — 包含所有端点的参数格式、枚举和响应字段的详细说明。在需要具体参数名称或响应字段结构时，请查阅此文件。
- **`references/skills.json`** — 所有端点的结构化清单（适用于自动化工具或集成）。