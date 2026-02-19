---
name: ahrefs
description: >
  完成Ahrefs API的集成，以支持SEO分析功能。该集成涵盖了以下模块：  
  - **Site Explorer**（网站浏览器）：可查看域名信息、反向链接以及网站的排名情况；  
  - **Keywords Explorer**（关键词浏览器）：提供关键词的搜索量、难度等级以及搜索引擎结果页（SERP）的分析数据；  
  - **Rank Tracker**（排名追踪器）：用于实时监控网站的排名变化；  
  - **Site Audit**（网站审计）：对网站的技术SEO状况进行评估；  
  - **SERP Overview**（SERP概览）：提供搜索引擎结果页的详细信息；  
  - **Batch Analysis**（批量分析）：支持对多个网站或关键词进行批量处理；  
  - **Brand Radar**（品牌雷达）：帮助用户监测品牌在搜索引擎中的表现。  
  该API可应用于各种SEO相关场景，包括关键词研究、反向链接分析、竞争对手分析、网站技术审计以及排名追踪等。
version: 1.2.0
---
# Ahrefs SEO 分析

使用 Ahrefs API 查询和分析 SEO 数据，包括反向链接、关键词、排名和竞争情报。

## 先决条件

### API 访问权限
您需要拥有 Ahrefs 的订阅账户并具备 API 访问权限：
- **Lite**：基本指标，有限的过滤功能
- **Standard**：更多的 API 端点，部分过滤功能
- **Advanced**：高级过滤功能，更多数据
- **Enterprise**：完整的 API 访问权限，高级过滤功能，更高的请求速率限制

### 设置

1. 从 [Ahrefs 账户设置](https://ahrefs.com/api) 获取您的 API 令牌。
2. 在 OpenClaw 中进行配置：
   将令牌添加到 `~/.openclaw/workspace/.env` 文件中：
   ```bash
   AHREFS_API_TOKEN=your_api_token_here
   AHREFS_API_PLAN=enterprise  # Options: lite, standard, advanced, enterprise
   ```

3. 验证设置是否正确：
   ```bash
   grep AHREFS ~/.openclaw/workspace/.env
   ```

## 各计划的具体功能

### 所有计划
- 域名评分与 Ahrefs 排名
- 基本反向链接统计（总数）
- 自然搜索关键词数量
- 自然搜索流量估算
- 流量最高的页面

### Standard 及更高等级的计划
- 带有排名信息的自然搜索关键词（所有排名位置）
- 排名在前 1-3 位的关键词（通过 `org_keywords_1_3` 指标）
- 引用域名列表（基本信息）

### Advanced 及 Enterprise 计划
- **高级过滤**：按排名位置过滤关键词（仅限首页）
- **地理过滤**：按国家/顶级域名（TLD）过滤反向链接（例如 `.au` 域名）
- **详细关键词数据**：可以获取 `best_position`、`sum_traffic`、`volume` 等信息
- **详细反向链接数据**：可过滤的完整反向链接列表
- **更高的请求速率限制**：可以获取更多数据（超过 5000 条记录）

## 核心功能

### 网站分析器（域名分析）
获取任何域名的全面 SEO 指标：
- 域名评分（Domain Rating, DR）与 URL 评分（URL Rating, UR）
- 自然搜索流量估算
- 引用域名与反向链接
- 自然搜索关键词与排名
- 流量最高的页面
- 历史数据与趋势
- **[Advanced/Enterprise]**：按国家/顶级域名过滤
- **[Advanced/Enterprise]**：基于排名的过滤（仅限首页）

### 关键词分析器（关键词研究）
发现并分析关键词：
- 搜索量（全球及特定国家）
- 关键词难度（KD）评分
- 点击成本（CPC）估算
- 搜索引擎结果页（SERP）分析
- 相关关键词与建议
- 关键词创意与建议
- 上级主题分析
- 流量潜力估算

### 排名跟踪器（排名监控）
跟踪关键词的排名变化：
- 排名与可见性
- 竞争对手排名对比
- 搜索引擎结果页特征分析
- 历史排名数据
- 声量占比指标
- **注意：** 需要在 Ahrefs 中预先配置项目

### 网站审计（技术 SEO）
识别技术 SEO 问题：
- 爬取数据与网站健康状况评分
- 按严重程度划分的页面问题
- 内部链接分析
- 页面性能指标
- 移动设备可用性问题
- **注意：** 需要在 Ahrefs 中预先配置项目

### 搜索引擎结果页概览（SERP）
分析搜索引擎结果：
- 任何关键词的前 100 个自然搜索结果
- 搜索引擎结果页的特征
- 排名页面的域名指标
- 关键词难度分解
- 点击率估算

### 批量分析（批量处理）
高效处理多个目标：
- 每次请求最多可分析 100 个域名/URL
- 批量关键词指标
- 批量反向链接数据
- 适用于大型数据集

### 品牌雷达（品牌监控）
跟踪品牌表现：
- 品牌提及次数
- 声量占比
- 竞争品牌对比
- 情感分析准备

### 竞争对手分析
比较域名并识别机会：
- 并排显示域名对比
- 内容差距分析
- 关键词重叠与差异
- 反向链接差距分析
- 流量对比
- **[Advanced/Enterprise]**：过滤后的对比（仅限首页关键词、本地反向链接）

## API 结构

Ahrefs API 的基础 URL 为：`https://api.ahrefs.com/v3/site-explorer/`

### 认证
所有请求都需要在请求头中包含 API 令牌：
```
Authorization: Bearer {AHREFS_API_TOKEN}
```

**重要提示：** 使用 `AHREFS_API_TOKEN`，而非 `AHREFS_MCP_TOKEN`。

### 必需参数
所有 API 调用都需要以下参数：
- `date`：当前日期（格式为 `YYYY-MM-DD`
- `target`：域名（例如 `example.com`）

### 常见 API 端点
有关详细端点文档和参数，请参阅 [references/api-endpoints.md](references/api-endpoints.md)。

## API 单位管理

### 理解 API 单位
- 每个 API 请求会消耗您每月的 API 单位
- 费用取决于返回的记录数（每次请求至少 50 个单位）
- Enterprise 计划包含 API 单位；可额外购买单位
- 可在 [https://app.ahrefs.com/account/limits-and-usage/web] 查看使用情况

### 成本优化建议
1. **限制返回的记录数**：使用 `limit` 参数来降低成本
2. **选择特定列**：使用 `select` 参数仅获取所需的字段
3. **批量请求**：一次请求处理多个目标（最多 100 个）
4. **缓存结果**：将频繁访问的数据存储在本地
5. **使用日期范围**：在不需要时限制历史数据

### 请求速率限制
- **每分钟 60 次请求**（默认值）
- 超过限制时返回 HTTP 429 错误
- 实现指数级重试机制

## 使用示例

### 网站分析器 - 获取反向链接与引用域名
```bash
DATE=$(date +%Y-%m-%d)
curl -X GET "https://api.ahrefs.com/v3/site-explorer/backlinks-stats?date=$DATE&target=example.com" \
  -H "Authorization: Bearer $AHREFS_API_TOKEN"
```

返回结果：
```json
{
  "metrics": {
    "live": 4545,
    "all_time": 25318,
    "live_refdomains": 718,
    "all_time_refdomains": 3272
  }
}
```

### 获取自然搜索关键词与流量
```bash
DATE=$(date +%Y-%m-%d)
curl -X GET "https://api.ahrefs.com/v3/site-explorer/metrics?date=$DATE&target=example.com" \
  -H "Authorization: Bearer $AHREFS_API_TOKEN"
```

返回结果：
```json
{
  "metrics": {
    "org_keywords": 6925,
    "org_traffic": 38702,
    "org_keywords_1_3": 1560,
    "org_cost": 2372016
  }
}
```

### 获取域名评分
```bash
DATE=$(date +%Y-%m-%d)
curl -X GET "https://api.ahrefs.com/v3/site-explorer/domain-rating?date=$DATE&target=example.com" \
  -H "Authorization: Bearer $AHREFS_API_TOKEN"
```

返回结果：
```json
{
  "domain_rating": {
    "domain_rating": 43.0,
    "ahrefs_rank": 1189155
  }
}
```

### 获取流量最高的页面
```bash
DATE=$(date +%Y-%m-%d)
curl -X GET "https://api.ahrefs.com/v3/site-explorer/top-pages?date=$DATE&target=example.com&limit=10&select=url,sum_traffic" \
  -H "Authorization: Bearer $AHREFS_API_TOKEN"
```

### 关键词分析器 - 关键词研究
```bash
curl -X GET "https://api.ahrefs.com/v3/keywords-explorer/overview?keyword=seo+tools&country=us" \
  -H "Authorization: Bearer $AHREFS_API_TOKEN"
```

返回结果：
```json
{
  "keyword": "seo tools",
  "volume": 14000,
  "keyword_difficulty": 75,
  "cpc": 25.50,
  "serp_features": ["featured_snippet", "people_also_ask"],
  "traffic_potential": 18500
}
```

### 关键词分析器 - 相关关键词
```bash
curl -X GET "https://api.ahrefs.com/v3/keywords-explorer/related-keywords?keyword=seo+tools&country=us&limit=50" \
  -H "Authorization: Bearer $AHREFS_API_TOKEN"
```

### 搜索引擎结果页概览 - 分析搜索结果
___CODEBLOCK_13___

返回前 100 个自然搜索结果及域名指标。

### 排名跟踪器 - 获取项目排名
**注意：** 需要在 Ahrefs 网页界面中预先配置项目。

```bash
curl -X GET "https://api.ahrefs.com/v3/rank-tracker/project?project_id=12345" \
  -H "Authorization: Bearer $AHREFS_API_TOKEN"
```

### 网站审计 - 获取项目问题
**注意：** 需要在 Ahrefs 网页界面中预先配置项目。

```bash
curl -X GET "https://api.ahrefs.com/v3/site-audit/project?project_id=12345" \
  -H "Authorization: Bearer $AHREFS_API_TOKEN"
```

### 批量分析 - 多个域名
```bash
curl -X POST "https://api.ahrefs.com/v3/site-explorer/batch/metrics" \
  -H "Authorization: Bearer $AHREFS_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "targets": ["example.com", "competitor1.com", "competitor2.com"],
    "date": "2026-02-18"
  }'
```

一次请求返回所有域名的指标。

## 常见工作流程

### 关键词研究工作流程
1. 获取关键词概览（搜索量、难度、点击成本）
2. 获取相关关键词与建议
3. 分析排名靠前的内容在搜索结果页的表现
4. 识别关键词的难度和流量潜力
5. 导出优先级关键词列表

### 竞争分析工作流程
1. 比较域名指标（域名评分、流量、关键词）
2. 分析竞争对手的反向链接情况
3. 识别内容差距
4. 找出竞争对手排名但您未排名的关键词
5. 发现反向链接机会

### 技术 SEO 审计工作流程
**需要预先配置网站审计项目**
1. 获取网站健康状况概览
2. 按严重程度识别关键问题
3. 分析内部链接结构
4. 查看页面性能指标
5. 生成优先级修复列表

### 内容策略工作流程
1. 研究目标关键词（关键词分析器）
2. 分析排名靠前的内容（搜索引擎结果页概览）
3. 识别与竞争对手的内容差距
4. 根据流量潜力规划内容
5. 随时间跟踪排名变化（排名跟踪器）

### 批量域名分析工作流程
1. 编制目标域名列表
2. 发送批量 API 请求（最多 100 个域名）
3. 比较所有域名的指标
4. 识别模式与机会
5. 导出对比分析结果

## 最佳实践
1. **遵守请求速率限制**：遵守 API 的速率限制（默认为每分钟 60 次请求）
2. **管理 API 单位**：监控使用情况并优化请求（限制返回的记录数、选择所需列）
3. **缓存数据**：缓存频繁访问的数据
4. **分页处理**：对于大型数据集，使用 `limit` 和 `offset` 参数
5. **批量请求**：在分析多个目标时使用批量 API 端点
6. **错误处理**：检查 401（认证错误）、429（请求速率限制错误）、404（未找到错误）
7. **项目要求**：排名跟踪器和网站审计需要预先配置项目

## 环境变量
从工作区的 `.env` 文件中加载 API 令牌：
```powershell
# PowerShell
$env:AHREFS_API_TOKEN = (Get-Content ~/.openclaw/workspace/.env -Raw | Select-String "AHREFS_API_TOKEN=([^\r\n]+)" | ForEach-Object { $_.Matches.Groups[1].Value })
```

```bash
# Bash
export AHREFS_API_TOKEN=$(grep AHREFS_API_TOKEN ~/.openclaw/workspace/.env | cut -d'=' -f2)
```

## 响应格式
API 响应因端点而异，但通常返回 JSON 格式：

**统计端点**（反向链接统计、指标、域名评分）：
```json
{
  "metrics": { /* metric fields */ },
  "domain_rating": { /* rating fields */ }
}
```

**列表端点**（流量最高的页面、反向链接等）：
```json
{
  "pages": [ /* array of results */ ],
  "backlinks": [ /* array of results */ ]
}
```

## 故障排除

### 认证错误
- 确保 `.env` 文件中的令牌设置正确
- 检查令牌是否未过期
- 确保请求头中的令牌格式正确

### 请求速率限制
- 实现指数级重试机制
- 在适当的情况下缓存响应
- 使用批量 API 端点

### 数据未找到
- 检查域名/URL 的格式
- 确认域名是否存在于 Ahrefs 的索引中
- 尝试使用不同的域名格式（包含/不包含 `www`）