---
name: rising-transfers-dna-finder
description: 使用“Rising Transfers”矢量DNA搜索功能，寻找价格更低且风格相匹配的足球运动员替代人选。
version: "1.0.0"
homepage: https://github.com/LeoandLeon/rising-transfers-clawhub-skills
metadata:
  clawdbot:
    emoji: "🧬"
    requires:
      env: ["RT_API_KEY"]
    primaryEnv: "RT_API_KEY"
---
# RT DNA Finder — 足球运动员相似性搜索

该功能可帮助您找到在市场价值较低的足球运动员中，与目标运动员具有较高相似性的球员。该服务基于Rising Transfers Intelligence API实现，通过pgvector算法计算2000多名球员的DNA相似度。

---

## 外部接口

| 接口地址 | 方法 | 发送的数据 | 用途 |
|----------|--------|-----------|---------|
| `https://api.risingtransfers.com/api/v1/intelligence/dna-search` | POST | `{ "name": "<player_name>" }` | 执行DNA相似度搜索 |
| `https://api.risingtransfers.com/api/v1/intelligence/player` | POST | `{ "name": "<player_name>" }` | 查询球员资料（可选） |

所有数据仅发送到上述接口，不会被本地存储。

---

## 安全与隐私

- **您提供的信息**：仅包括您在查询中输入的球员名称。
- **不会被存储的信息**：对话记录、其他安装的技能信息、本地文件以及API密钥（API密钥以HTTP头部形式传输，不会出现在请求体或日志中）。
- **Rising Transfers的数据处理方式**：API调用会被记录用于限制请求频率和计费；球员名称查询数据会在24小时后被删除。详情请参阅[隐私政策](https://risingtransfers.com/privacy)。
- **身份验证**：您的`RT_API_KEY`会在每次访问`api.risingtransfers.com`的请求中以`X-RT-API-Key`头部字段的形式发送。

---

## 模型调用说明

当您请求查找相似球员、价格更低的替代球员或DNA匹配的球员时，OpenClaw可以自动调用此功能。您可以通过在OpenClaw配置中设置`skill.auto-discover`为`false`来禁用自动调用功能。每次API调用会消耗Rising Transfers账户的信用点数（每次DNA搜索消耗10个信用点数）。

---

## 信任声明

使用此功能时，您输入的球员名称会发送至Rising Transfers（`api.risingtransfers.com`）。仅当您信任Rising Transfers并同意其处理这些信息时，才应安装此功能。Rising Transfers是一个专注于足球数据分析的平台，不会处理任何财务、个人或敏感数据。

---

## 触发条件

当用户提出以下请求时，该功能会被触发：
- 查找与特定球员相似的球员
- 寻找价格更低的替代球员
- 查找DNA匹配或风格相似的球员

示例：
- “帮我找到与Bellingham相似但价格更低的球员”
- “Rodri的DNA匹配替代球员有哪些？”
- “请推荐一名价格在2000万欧元以下的、风格相似的球员”

---

## 使用说明

1. 从用户请求中提取目标球员的名称（如果提到了球队名称，请一并记录下来以避免混淆）。
2. 调用DNA搜索接口：
   ```
   POST https://api.risingtransfers.com/api/v1/intelligence/dna-search
   Headers:
     X-RT-API-Key: <RT_API_KEY>
     Content-Type: application/json
   Body:
     { "name": "<player_name>", "team": "<team_name_if_provided>" }
   ```

3. 如果响应中包含`error: "INSUFFICIENT_CREDITS"`，则告知用户信用点数已用尽，并引导他们前往`api.risingtransfers.com`进行充值。
4. 如果响应中包含`error: "PLAYER_NOT_FOUND"`，请用户确认球员名称或提供球员所在的俱乐部名称。
5. 解析响应中的`data.alternatives`数组，为每个替代球员展示以下信息：
   - 球员名称及当前所属俱乐部
   - DNA相似度百分比（例如：“91%相似”）
   - 市场价值及与目标球员的价差（例如：“便宜6500万欧元”）
   - 位置和主要比赛风格标签
6. 以排名表格的形式展示结果，相似度最高的球员排在最前面。示例格式如下：

   | 排名 | 球员 | 俱乐部 | 相似度 | 市场价值 | 相比目标节省的费用 |
   |------|--------|------|-----------|-------|-------------------|
   | 1 | 名称 | 俱乐部 | 91% | 1500万欧元 | 便宜6500万欧元 |
   
7. 在展示结果后，可询问用户是否需要进一步了解这些球员的详细信息。
8. 请确保提供的统计数据真实可靠；如果API未返回任何替代球员信息，应明确告知用户并建议他们尝试查询其他球员。

---

## 错误处理

| 错误代码 | 用户提示信息 |
|-------|-------------|
| 401 Unauthorized | “您的RT_API_KEY无效或已过期。请在api.risingtransfers.com获取新的API密钥。” |
| 403 Insufficient Credits | “您的DNA搜索信用点数已用完。请在api.risingtransfers.com进行充值。” |
| 404 Player Not Found | “未找到该球员。请提供完整的球员名称或俱乐部名称。” |
| 429 Rate Limited | “请求次数过多。请稍后再试。” |
| 5xx Server Error | “Rising Transfers API暂时无法使用。请稍后再试。” |

---

## 使用要求

- **RT_API_KEY**：有效的Rising Transfers API密钥。您可以在[api.risingtransfers.com](https://api.risingtransfers.com)免费注册。免费账户每天可使用2次DNA搜索服务。
- **OpenClaw**：版本需达到v0.8.0或更高。
- **网络连接**：必须能够访问`api.risingtransfers.com`。

---

## 信用点数消耗

| 功能 | 消耗的信用点数 |
|--------|-----------------|
| DNA相似度搜索 | 10个信用点数 |
| 球员资料查询（可选） | 1个信用点数 |

免费账户：每天2次DNA搜索（该功能每天共消耗20个信用点数）。
高级账户（每月29美元）：每天50次DNA搜索。

---

## 开发者信息

Rising Transfers — [api.risingtransfers.com](https://api.risingtransfers.com)