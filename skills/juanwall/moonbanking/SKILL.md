---
name: moonbanking
description: **完整访问 Moon Banking API 端点**  
该接口可获取地球上所有银行的相关数据，包括银行信息、投票记录、评分、搜索结果、国家概况、全球银行分布情况以及银行的加密货币支持情况等。使用环境变量 `MOON BANKING_API_KEY` 进行身份验证。
homepage: https://docs.moonbanking.com/openclaw-skill
requires:
  env: ["MOON_BANKING_API_KEY"]
metadata:
  openclaw:
    emoji: "💰"
    requires:
      env: ["MOON_BANKING_API_KEY"]
      bins: ["curl", "jq"]
    os: ["linux", "darwin", "win32"]
    credentials:
      primary:
        key: MOON_BANKING_API_KEY
        description: API key for authenticating requests to https://api.moonbanking.com/v1 (Moon Banking Pro plan required)
        type: api_key
        required: true
        sensitive: true
---

# Moon Banking API

您可以通过访问 https://api.moonbanking.com/v1 来查询 Moon Banking API，获取关于地球上所有银行的数据，以及全球和各国层面的银行汇总信息。该 API 提供了关于银行、国家、相关故事、投票记录、全球概览等丰富的信息。

## 设置与身份验证

- 设置环境变量：  
  `MOON BANKING_API_KEY=您的 API 密钥`  
  （您需要购买 [Moon Banking Pro 计划](https://moonbanking.com/pro) 才能获取 API 密钥。购买计划后，您可以在 [Moon Banking 仪表板](https://moonbanking.com/settings/api/manage-api-keys) 中创建 API 密钥。）

- 每个请求都必须包含以下头部信息：  
  `Authorization: Bearer $MOON BANKING_API_KEY`

- 使用 `exec` 命令结合 `curl -s`（静默模式）并将输出结果传递给 `jq`，以获得格式清晰、易于阅读的 JSON 数据。

- 如果未安装 `jq`，可以忽略 `| jq .` 部分——代理程序仍然可以解析原始 JSON 数据。

### 标准的 `curl` 请求格式

```bash
curl -s -H "Authorization: Bearer $MOON_BANKING_API_KEY" \
     "https://api.moonbanking.com/v1/ENDPOINT?param=value&another=val" | jq .
```

## 所有 API 端点

### 1. /banks  
该端点允许您获取分页显示的所有银行列表。默认情况下，每页最多显示十家银行。您可以根据银行名称进行搜索，按国家进行筛选，并按多种字段对银行进行排序；同时还可以查看相关数据（如评分、国家信息等）。  
**常用参数**  
- `limit`（可选） - （1–100，默认值为 10）  
- `starting_after`（可选）  
- `ending_before`（可选）  
- `sortBy`（可选） - （名称、排名、countryRank、storiesCount、countryId、overall_score、overall_total、overall_up、overall_down、cryptoFriendly_score、cryptoFriendly_total、cryptoFriendly_up、cryptoFriendly_down、customerService_score、customerService_total、customerService_up、customerService_down、feesPricing_score、feesPricing_total、feesPricing_up、feesPricing_down、digitalExperience_score、digitalExperience_total、digitalExperience_up、digitalExperience_down、securityTrust_score、securityTrust_total、securityTrust_up、securityTrust_down、accountFeatures_score、accountFeatures_total、accountFeatures_up、accountFeatures_down、branchAtmAccess_score、branchAtmAccess_total、branchAtmAccess_up、branchAtmAccess_down、internationalBanking_score、internationalBanking_total、internationalBanking_up、internationalBanking_down、businessBanking_score、businessBanking_total、businessBanking_up、businessBanking_down、processingSpeed_score、processingSpeed_total、processingSpeed_up、processingSpeed_down、transparency_score、transparency_total、transparency_up、transparency_down、innovation_score、innovation_total、innovation_up、innovation_down、investmentServices_score、investmentServices_total、investmentServices_up、investmentServices_down、lending_score、lending_total、lending_up、lending_down）  
- `sortOrder`（可选） - （升序/降序）  
**查询参数**  
- `search`（可选）  
- `include`（可选） - （scores、country、meta）  
- `countryId`（可选）  
- `countryCode`（可选）  
**示例**  
```bash  
curl -s -H "Authorization: Bearer $MOON BANKING_API_KEY" \
     "https://api.moonbanking.com/v1/banks?limit=10&search=ethical&sortBy=overall_score&sortOrder=desc&include=scores,country&countryCode=US" | jq .  
```

### /banks/by-hostname  
This endpoint allows you to retrieve banks by hostname. It will return up to one bank per country that matches the provided hostname. The hostname is normalized (www. prefix removed if present) and matched against both the primary hostname and alternative hostnames.  
**Query params**  
- `hostname` (required)
- `include` (optional) - (scores, country)
- `pageTitle` (optional)  
**Example**  
```  
curl -s -H "Authorization: Bearer $MOON BANKING_API_KEY" \
     "https://api.moonbanking.com/v1/banks/by-hostname?hostname=fidelity.com&include=scores,country" | jq .  
```

### /banks/{id}  
This endpoint allows you to retrieve a specific bank by providing the bank ID. You can include related data like scores and country information in the response.  
**Query params**  
- `include` (optional) - (scores, country)  
**Path params**  
- `id` (required)  
**Example**  
```  
curl -s -H "Authorization: Bearer $MOON BANKING_API_KEY" \
     "https://api.moonbanking.com/v1/banks/6jkxE4N8gHXgDPK?include=scores,country" | jq .  
```

### 2. /bank-votes  
This endpoint allows you to retrieve a paginated list of bank votes. You can filter by bank ID, category, country, vote type (upvote or downvote), and other parameters.  
**Common params**  
- `limit` (optional) - (1–100, default 10)
- `starting_after` (optional)
- `ending_before` (optional)
- `sortBy` (optional) - (createdAt)
- `sortOrder` (optional) - (asc, desc)  
**Query params**  
- `bankId` (optional)
- `categories` (optional)
- `isUp` (optional)
- `countryCode` (optional)
- `include` (optional) - (bank, country)  
**Example**  
```  
curl -s -H "Authorization: Bearer $MOON BANKING_API_KEY" \
     "https://api.moonbanking.com/v1/bank-votes?limit=10&bankId=bank_abc&isUp=true&countryCode=US&sortBy=createdAt&sortOrder=desc&include=scores,country" | jq .  
```

### 3. /countries  
This endpoint allows you to retrieve a paginated list of all countries. By default, a maximum of ten countries are shown per page. You can search countries by name or 2-letter code, sort them by various fields, and include related data like scores.  
**Common params**  
- `limit` (optional) - (1–100, default 10)
- `starting_after` (optional)
- `ending_before` (optional)
- `sortBy` (optional) - (name, code, rank, banksCount, storiesCount, overall_score, overall_total, overall_up, overall_down, cryptoFriendly_score, cryptoFriendly_total, cryptoFriendly_up, cryptoFriendly_down, customerService_score, customerService_total, customerService_up, customerService_down, feesPricing_score, feesPricing_total, feesPricing_up, feesPricing_down, digitalExperience_score, digitalExperience_total, digitalExperience_up, digitalExperience_down, securityTrust_score, securityTrust_total, securityTrust_up, securityTrust_down, accountFeatures_score, accountFeatures_total, accountFeatures_up, accountFeatures_down, branchAtmAccess_score, branchAtmAccess_total, branchAtmAccess_up, branchAtmAccess_down, internationalBanking_score, internationalBanking_total, internationalBanking_up, internationalBanking_down, businessBanking_score, businessBanking_total, businessBanking_up, businessBanking_down, processingSpeed_score, processingSpeed_total, processingSpeed_up, processingSpeed_down, transparency_score, transparency_total, transparency_up, transparency_down, innovation_score, innovation_total, innovation_up, innovation_down, investmentServices_score, investmentServices_total, investmentServices_up, investmentServices_down, lending_score, lending_total, lending_up, lending_down)
- `sortOrder` (optional) - (asc, desc)  
**Query params**  
- `search` (optional)
- `include` (optional) - (scores)  
**Example**  
```  
curl -s -H "Authorization: Bearer $MOON BANKING_API_KEY" \
     "https://api.moonbanking.com/v1/countries?limit=10&search=swiss&sortBy=overall_score&sortOrder=desc&include=scores" | jq .  
```

### /countries/{code}  
This endpoint allows you to retrieve a specific country by providing the 2-letter ISO country code. You can include related data like scores in the response.  
**Query params**  
- `include` (optional) - (scores)  
**Path params**  
- `code` (required)  
**Example**  
```  
curl -s -H "Authorization: Bearer $MOON BANKING_API_KEY" \
     "https://api.moonbanking.com/v1/countries/US?include=scores" | jq .  
```

### 4. /stories  
This endpoint allows you to retrieve a paginated list of all stories. By default, a maximum of ten stories are shown per page. You can search stories by text content, filter by bank ID, sort them by various fields, and include related data like bank and country information.  
**Common params**  
- `limit` (optional) - (1–100, default 10)
- `starting_after` (optional)
- `ending_before` (optional)
- `sortBy` (optional) - (createdAt, thumbsUpCount)
- `sortOrder` (optional) - (asc, desc)  
**Query params**  
- `search` (optional)
- `include` (optional) - (bank, country)
- `countryCode` (optional)
- `bankId` (optional)
- `tags` (optional)  
**Example**  
```  
curl -s -H "Authorization: Bearer $MOON BANKING_API_KEY" \
     "https://api.moonbanking.com/v1/stories?limit=10&search=swiss&sortBy=createdAt&sortOrder=desc&include=bank,country&countryCode=US&bankId=bank_abc" | jq .  
```

### /stories/{id}  
This endpoint allows you to retrieve a specific story by providing the story ID. You can include related data like bank and country information in the response.  
**Query params**  
- `include` (optional) - (bank, country)  
**Path params**  
- `id` (required)  
**Example**  
```  
curl -s -H "Authorization: Bearer $MOON BANKING_API_KEY" \
     "https://api.moonbanking.com/v1/stories/8HsY5nBc7jAqM4u?include=bank,country" | jq .  
```

### 5. /world  
This endpoint allows you to retrieve global overview data that aggregates banks votes, stories and other data across all banks in all countries. You can include related data like scores in the response.  
**Query params**  
- `include` (optional) - (scores)  
**Example**  
```  
curl -s -H "Authorization: Bearer $MOON BANKING_API_KEY" \
     "https://api.moonbanking.com/v1/world?include=scores" | jq .  
```

### 6. /search  
Search across banks, countries, and stories. You can specify which entities to search using the include parameter. If no include value is provided, all entities will be searched.  
**Common params**  
- `limit` (optional) - (1–50, default 10)  
**Query params**  
- `q` (required)
- `include` (optional) - (banks, countries, stories)  
**Example**  
```  
curl -s -H "Authorization: Bearer $MOON BANKING_API_KEY" \
     "https://api.moonbanking.com/v1/search?q=crypto+friendly+banks&include=banks,countries,stories&limit=15" | jq .  
```

## Best Practices & Tips

- Use `jq` filters to extract useful fields, e.g.:  
  ```  
  | jq '.data[] | {name, overall_score, rank, country?.name}'  
```  

- 错误处理：  
  - 401/403 → 请检查或设置 `MOON BANKING_API_KEY`  
  - 404 → ID 或代码无效  
  - 429 → 请求次数达到限制（请稍后重试）  

- 分页处理：使用之前响应中的 `starting_after` 和 `ending_before` 参数进行分页。  

- 请始终以易于理解的方式展示结果（例如：排名最高的银行、各国银行排名、热门故事等），而不仅仅是原始 JSON 数据。  

- 对于复杂的查询，可以多次调用 `exec` 命令来组合多个请求。  

每当需要查询或讨论与银行相关的信息时（包括但不限于排名、评价、国家对比、客户体验或全球银行业务洞察等），都可以使用此 API。