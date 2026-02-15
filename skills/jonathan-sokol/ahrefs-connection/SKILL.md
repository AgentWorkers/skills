---
name: ahrefs-mcp
description: >
  Access Ahrefs SEO data via the Ahrefs API for comprehensive SEO analysis, keyword research, backlink analysis, site audits, and competitive intelligence. Use when users mention: (1) SEO-related queries about websites, domains, or URLs, (2) Keyword research, rankings, or search volume data, (3) Backlink analysis or link profiles, (4) Domain metrics (DR, UR, traffic), (5) Competitor analysis or site comparison, (6) Rank tracking or SERP analysis, (7) Content gap analysis, (8) Site Explorer data requests. When uncertain if a query is SEO-related, ask if Ahrefs should be used.
---

# Ahrefs API

您可以通过Ahrefs API直接获取实时的SEO数据，用于分析网站、研究关键词、跟踪排名，并基于数据做出SEO决策。

## 首次使用说明

如果您是第一次使用Ahrefs API，请阅读[references/setup.md](references/setup.md)以获取完整的设置指南。您需要：
- 一个Ahrefs账户（企业计划可享受完整的API访问权限，Lite+计划可进行有限的免费测试查询）
- 来自您Ahrefs工作区的API密钥

设置完成后，请返回此处查看使用指南。

## 核心功能

Ahrefs API提供了以下功能：
1. **网站分析工具**（Site Explorer）：域名指标、反向链接、自然流量、引用域名
2. **关键词分析工具**（Keywords Explorer）：搜索量、关键词难度、SERP分析、相关关键词
3. **排名跟踪工具**（Rank Tracker）：排名跟踪、可见性指标、竞争对手排名（需要预先配置项目）
4. **网站审计工具**（Site Audit）：技术SEO问题、爬取数据、网站健康状况（需要预先配置项目）
5. **SERP概览**（SERP Overview）：任意关键词的前100个SERP结果
6. **批量分析**：每次请求最多处理100个目标
7. **品牌监控工具**（Brand Radar）：品牌表现数据

有关详细功能信息，请参阅[references/capabilities.md](references/capabilities.md)。

## 认证

所有API请求都需要通过`Authorization`头部传递API密钥：
```bash
Authorization: Bearer YOUR_API_KEY
```

请妥善保管您的API密钥。建议使用环境变量来存储密钥：
```bash
export AHREFS_API_KEY="your-api-key-here"
```

## 使用流程

### 1. 明确需求

确定需要哪些SEO数据：
- **域名/URL分析** → 使用网站分析工具的API端点
- **关键词数据** → 使用关键词分析工具的API端点
- **排名跟踪** → 使用排名跟踪工具的API端点（需要项目配置）
- **技术SEO检查** → 使用网站审计工具的API端点（需要项目配置）
- **SERP数据** → 使用SERP概览的API端点

### 2. 发送API请求

使用`curl`或其他类似工具调用Ahrefs API。基础URL为：`https://api.ahrefs.com/v3`

**示例 - 获取域名概览：**
```bash
curl -X GET "https://api.ahrefs.com/v3/site-explorer/domain-overview?target=example.com" \
  -H "Authorization: Bearer $AHREFS_API_KEY"
```

**示例 - 关键词指标：**
```bash
curl -X GET "https://api.ahrefs.com/v3/keywords-explorer/overview?keyword=seo+tools&country=us" \
  -H "Authorization: Bearer $AHREFS_API_KEY"
```

### 3. 处理并展示结果

- 解析JSON响应
- 提取相关指标
- 以清晰、可操作的格式展示数据
- 突出关键洞察和机会
- 根据分析结果提出下一步建议

## 常见工作流程

### 关键词研究 + 交叉参考

1. 用户提供关键词列表
2. 向关键词分析工具发送批量API请求
3. 解析并整合各项指标（搜索量、难度、CPC）
4. 以优先级建议的形式展示分析结果

有关详细的工作流程模式及示例API调用，请参阅[references/workflows.md](references/workflows.md)。

### 竞争分析

1. 确定目标域名和竞争对手
2. 分别调用每个域名的网站分析工具
3. 比较各项指标（反向链接数量、自然流量、引用域名）
4. 分析热门的自然搜索关键词
5. 识别内容差距
6. 提出可操作的改进建议

### 网站审计

**注意：** 需要在Ahrefs网站界面中预先配置网站审计项目。

1. 调用网站审计工具的API以获取项目数据
2. 按严重程度识别关键问题
3. 根据影响程度确定修复优先级
4. 提出技术建议

## API限制与最佳实践

### 请求速率限制
- 默认每分钟60次请求
- 超过限制时，API会返回HTTP 429错误
- 请使用指数退避策略进行重试

### API资源消耗

- 每次请求会消耗您每月的API资源额度
- 费用取决于返回的数据行数（每次请求至少消耗50个资源单位）
- 可在**账户设置 → 限制与使用**中跟踪资源使用情况
- 企业计划包含额外的API资源单位；也可额外购买

### 优化建议
- 尽可能使用批量请求（每次最多100个目标）
- 使用`limit`参数限制返回的结果行数
- 使用`select`参数选择所需的列以降低成本
- 在适当的情况下缓存结果
- 使用日期范围来限制历史数据的查询

### 计划特定的访问权限

- **企业计划**：享有完整的API访问权限
- **Lite/Standard/Advanced计划**：提供有限的免费测试查询次数（具体请查看您的计划）

## 错误处理

常见的HTTP状态码：
- `200 OK` - 请求成功
- `400 Bad Request` - 参数无效
- `401 Unauthorized` - API密钥无效或缺失
- `403 Forbidden` - 权限不足或计划限制
- `429 Too Many Requests` - 超过请求速率限制
- `500 Internal Server Error` - Ahrefs服务器出现问题

请始终检查响应状态并妥善处理错误。

## API密钥丢失时的处理方法

如果API密钥未配置：
1. 提供[references/setup.md](references/setup.md)中的设置指南
2. 指导用户如何在Ahrefs账户设置中生成API密钥
3. 说明如何安全地存储密钥（建议使用环境变量）
4. 通过简单的API调用测试连接是否正常

## 资源链接

- **API文档**：https://docs.ahrefs.com/docs/api/reference/introduction
- **API密钥管理**：https://app.ahrefs.com/account/api-keys
- **定价与限制**：https://ahrefs.com/pricing
- **限制与使用情况跟踪**：https://app.ahrefs.com/account/limits-and-usage/web