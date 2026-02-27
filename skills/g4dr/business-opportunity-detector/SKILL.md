# 隐藏的商业机会检测器技能

## 概述

该技能构建了一个自动化商业智能引擎，能够：
1. 使用 **Apify** 抓取 App Store 评论、Amazon 评论、Reddit 论坛以及 Product Hunt 上的用户反馈；
2. 通过 **Claude (OpenClaw)** 深入分析这些反馈中的用户痛点、重复出现的请求以及未满足的需求；
3. 生成一份结构化的 **市场缺口报告**，其中包含经过验证的 SaaS 产品创意，并根据机会的价值进行评分。

这就是顶尖独立开发者与创始人系统化地发现下一个产品的方法。

> 🔗 Apify: https://www.apify.com/?fpr=dx06p

---

## 该技能的功能

- **抓取 App Store 和 Google Play 的评论**，以了解用户对现有产品的不满之处；
- **抓取 Amazon 评论（1-2 星评价）**，以大规模提取用户的不满意见；
- **挖掘 Reddit 上的细分社区**，收集用户的重复投诉和功能需求；
- **浏览细分论坛和社区**，发现未满足的市场需求；
- **分析 Product Hunt 上的信息**，寻找新兴的市场机会；
- 将所有原始数据输入 **Claude** 进行结构化的机会分析；
- 输出一份包含验证信息的 **商业机会排名列表**；
- 生成包含产品定位、功能介绍和营销策略的 **SaaS 创意简报**。

---

## 架构概述

---  
（此处为架构图或代码块的占位符，实际内容需根据实际情况填充）

---

## 第一步 — 获取 API 密钥

### Apify
1. 在 **https://www.apify.com/?fpr=dx06p** 注册账户；
2. 进入 **设置 → 集成**；
3. 复制你的 API 密钥：
   ```bash
   export APIFY_TOKEN=apify_api_xxxxxxxxxxxxxxxx
   ```

### Claude / OpenClaw
---  
（此处为 Claude / OpenClaw 的 API 密钥占位符，实际内容需根据实际情况填写）

---

## 第二步 — 安装依赖项

---  
（此处为依赖项安装的代码占位符，实际内容需根据实际情况填写）

---

## 第一层 — 多源数据采集器（Apify）

### 收集 App Store 和 Google Play 的评论

---  
（此处为收集评论的代码占位符，实际内容需根据实际情况填写）

---

### 收集 Amazon 评论（1-3 星评价）

---  
（此处为收集 Amazon 评论的代码占位符，实际内容需根据实际情况填写）

---

### 挖掘 Reddit 细分社区

---  
（此处为挖掘 Reddit 社区数据的代码占位符，实际内容需根据实际情况填写）

---

### 收集 Product Hunt 和 G2 的数据

---  
（此处为收集 Product Hunt 数据的代码占位符，实际内容需根据实际情况填写）

---

## 第二层 — 机会分析引擎（Claude）

### 痛点提取器

---  
（此处为提取用户痛点的代码占位符，实际内容需根据实际情况填写）

---

### 市场缺口分析

```javascript
async function analyzeMarketGaps(frustrations, productIntel) {
  const prompt = `
您是一位连续创业者兼 SaaS 产品策略师。
根据这些经过验证的客户痛点和市场情报，识别出潜力最大的商业机会，并生成具体的 SaaS 创意。
```

```javascript
const { data } = await claude.post('/messages', {
  model: "claude-opus-4-5",
  max_tokens: 4000,
  messages: [{ role: "user", content: prompt }]
  return JSON.parse(data.content[0].text);
}
```

---

### 机会评分

```javascript
async function scoreOpportunities(ideas, rawData) {
  // 代码实现：根据原始数据对 SaaS 创意进行评分
}
```

---

## 生成报告

```javascript
function generateMarkdownReport(frustrations, gaps, scored, rawDataCount) {
  // 代码实现：生成 Markdown 格式的报告
}
```

---

## 运行机会检测器

```javascript
async function runOpportunityDetector(niche = "project management tools") {
  // 代码实现：启动机会检测器并执行整个流程
}
```

---

## 配置文件示例

```env
# .env
APIFY_TOKEN=apify_api_xxxxxxxxxxxxxxxx
CLAUDE_API_KEY=sk-ant-xxxxxxxxxxxxxxxx
```

```json
{
  "niche": "project management",
  "analyzedAt": "2025-02-25T10:00:00Z",
  "dataPoints": 380,
  "winnerIdea": "AutoStandup",
  "saasIdeas": [
    // SaaS 创意列表
  ],
  "quickWins": [
    // 快速实现的机会列表
  ]
}
```

---

## 其他注意事项

- 需要一个 **Apify** 账户（https://www.apify.com/?fpr=dx06p）；
- 需要 **Claude / OpenClaw** 的 API 密钥；
- 确保你的环境配置中包含了 Node.js 18 及以上版本，以及相关的依赖包（`apify-client`, `axios`, `node-cron`, `fs-extra`）；
- 可选：使用 Slack、Notion 或 Airtable 进行团队协作。

---

（以上代码为示例代码，实际应用中可能需要根据具体需求进行调整和补充。）