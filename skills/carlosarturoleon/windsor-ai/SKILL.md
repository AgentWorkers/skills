---
name: windsor-ai
description: 连接到Windsor.ai MCP，可以通过自然语言方式访问325多种数据源，包括Facebook Ads、GA4、HubSpot、Shopify等。
metadata: {"clawdbot":{"emoji":"📊","requires":{"bins":["mcporter","npx","node"],"env":["WINDSOR_API_KEY"]}},"openclaw":{"primaryEnv":"WINDSOR_API_KEY"}}
---
# Windsor.ai 分析工具

使用此工具，您可以通过自然语言查询、探索和分析您的 [Windsor.ai](https://windsor.ai) 中连接的各种业务数据。Windsor.ai 从 325 个以上平台（如 Facebook Ads、Google Analytics 4、HubSpot、Shopify、TikTok Ads、Salesforce 等）收集数据，并通过一个统一的 MCP 接口提供这些数据。

## 适用场景

当用户询问以下问题时，可自动调用此工具：
- 活动效果、投资回报率（ROAS）、每点击成本（CPM）、每次点击费用（CPC）、点击率（CTR）
- 各渠道的广告支出明细或预算分析
- 销售流程、客户关系管理（CRM）数据或客户获取指标
- 电子商务业绩（收入、转化率、平均订单价值（AOV）
- 跨渠道归因或多触点分析
- 特定日期范围内的趋势分析
- 来自任何连接的广告、分析或 CRM 平台的数据

用户也可以直接使用 `/windsor-ai` 命令来调用此工具。

## 设置

在查询数据之前，必须先配置 Windsor.ai 的 MCP 连接。请按照以下步骤操作：

### 第一步：获取 Windsor.ai API 密钥

1. 登录您的 Windsor.ai 账户（网址：https://windsor.ai）
2. 转到账户仪表板或设置页面
3. 找到 API 密钥部分并复制该密钥

### 第二步：存储 API 密钥

将 API 密钥添加到 `clawdbot` 环境文件中：

```bash
echo 'WINDSOR_API_KEY=your_api_key_here' >> ~/.clawdbot/.env
```

请将 `your_api_key_here` 替换为您复制的密钥。

然后导出该密钥，以便 `mcporter` 可以识别它：

```bash
export WINDSOR_API_KEY=your_api_key_here
```

> **注意：** `mcporter` 需要将 `WINDSOR_API_KEY` 作为 shell 环境变量导出。仅将其存储在 `~/.clawdbot/.env` 文件中是不够的——它必须能够在当前 shell 会话中访问。
>
> **安全提示：** 避免将密钥添加到 `~/.zshrc` 或其他 shell 配置文件中，因为这会将密钥以明文形式存储在每个 shell 会话中。建议使用系统密钥链、秘密管理工具或权限受限的 `.env` 文件（例如：`chmod 600 ~/.clawdbot/.env`）。如果确实需要将其添加到 shell 配置文件中，请在不再需要时将其删除。

### 第三步：配置 `mcporter`

在项目的 `config/mcporter.json` 文件中添加 Windsor.ai 的配置信息。在 `mcpServers` 对象内添加以下内容：

```json
{
  "mcpServers": {
    "windsor-ai": {
      "description": "Windsor.ai MCP — natural language access to 325+  data sources.",
      "baseUrl": "https://mcp.windsor.ai/sse",
      "headers": {
        "Authorization": "Bearer ${WINDSOR_API_KEY}"
      }
    }
  }
}
```

如果 `mcpServers` 中已经存在其他条目，请将 `windsor-ai` 条目添加到其中。

### 第四步：验证连接

```bash
npx mcporter list
```

您应该会看到 `windsor-ai` 及其可用的工具列表。如果出现认证错误，请确认 `WINDSOR_API_KEY` 是否已正确设置在 `~/.clawdbot/.env` 文件中。

## 数据源查询

在查询数据之前，您可以先了解您的 Windsor.ai 账户中有哪些活跃的数据源：
- **列出已连接的数据源**：“我在 Windsor.ai 中连接了哪些数据源？”
- **查看可用字段**：“Windsor 中的 Facebook Ads 数据有哪些字段和指标？”
- **检查数据覆盖范围**：“Google Analytics 4 中最早可用的数据日期是什么？”
- **查看账户结构**：“显示所有连接到 Windsor.ai 的广告账户及其 ID。”

Windsor MCP 会自动检测您账户中的活跃连接源，并仅返回可用的数据。只有您在 Windsor.ai 仪表板中连接的源才能被查询。

## 使用方法

使用简单的英语语句来查询数据。Windsor MCP 会将您的问题转换为针对连接数据源的结构化查询语句。

### 如何构建查询

为了获得最佳结果，请务必包含以下信息：
- **数据来源**——或者请求 Windsor 在所有连接的来源中查询
- **指标**——支出、ROAS、点击次数、转化次数、收入、CPC、CTR 等
- **时间范围**——“过去 7 天”、“上个月”、“2025 年第一季度”、“截至当前日期”
- **任何筛选条件**——按活动、渠道、国家、设备、广告组等分类

### 查询示例

**单一数据源，单一指标：**
“我上周在 Facebook Ads 上的总支出是多少？”

**跨渠道比较：**
“比较过去 30 天内 Facebook Ads、Google Ads 和 TikTok Ads 的支出和 ROAS。”

**细分数据：**
“按活动划分 2025 年 3 月的 Google Ads 表现，显示展示次数、点击次数、转化次数和每次转化的成本。”

**趋势分析：**
“显示过去 90 天内我的 Facebook Ads 活动的 CPC 和 CTR 趋势。”

**表现最佳/最差的活动：**
“上个月 ROAS 最高的前 5 个活动是什么？表现最差的 5 个活动是什么？”

**异常检测：**
“上周哪些活动的表现出现了异常波动？”

## 报告生成

Windsor MCP 提供基础数据，Claude 会将这些数据整理成结构化的报告。您可以使用以下模板：

### 周度绩效报告

请求：“生成 [日期范围] 内所有连接渠道的周度绩效报告。”

Claude 会生成如下格式的报告：
1. **执行摘要**——总支出、总转化次数、综合 ROAS、环比变化
2. **渠道明细**——每个广告平台的支出和关键指标
3. **表现最佳的活动**——按支出和 ROAS 排名的前 3 个活动
4. **异常与警报**——表现超出或低于平均水平 20% 的活动
5. **建议**——基于渠道 ROAS 的预算重新分配建议

### 月度绩效报告

请求：“生成 [月份/年份] 内所有连接来源的月度绩效报告。”

Claude 会生成如下格式的报告：
1. **月度对比**——与前一个月相比的关键 KPI 及变化百分比
2. **渠道绩效表**——每个渠道的展示次数、点击次数、支出、转化次数、每次转化成本（CPA）和 ROAS
3. **活动亮点**——按收入贡献排名的前 5 个活动
4. **受众与创意洞察**——表现最佳的受众或创意（如果连接了社交广告数据）
5. **预算安排**——实际支出与计划预算的对比
6. **30 天展望**——基于过去趋势预测的季度末支出

### 客户可用报告

请求：“为 [账户/品牌] 生成 [日期范围] 的客户可用绩效报告。包括执行摘要、渠道明细、表现最佳的活动和关键建议。报告格式需符合专业标准。”

## 示例查询

**活动绩效：**
- “上个月所有渠道中 ROAS 最高的活动有哪些？”
- “哪些广告活动的预算浪费严重，转化率低？”
- “我的黑色星期五活动与去年相比表现如何？”

**支出分析：**
- “提供过去 90 天内各渠道的总支出明细。”
- “今年迄今为止我在 Facebook Ads 和 Google Ads 上分别支出了多少？”
- “本月我在所有连接的广告平台上的平均每日支出是多少？”

**受众与创意：**
- “哪些受众群体在 Facebook Ads 上的转化效果最好？”
- “在 TikTok 上，哪种广告创意格式（图片 vs. 视频）的转化率更高？”

**电子商务（需要 Shopify 或类似连接工具）：**
- “本月我的付费流量和自然流量带来的收入分别是多少？”
- “哪些产品类别通过 Google Ads 的转化率最高？”
- “按流量来源划分我的客户获取成本。”

**CRM 和销售流程（需要 HubSpot、Salesforce 或类似工具）：**
- “上个季度我的活动产生了多少潜在客户？”
- “通过付费社交渠道获得的潜在客户的平均交易额是多少？”

**趋势与预测：**
- “显示过去 6 个月内我的综合 ROAS 趋势。”
- “根据当前的支出趋势，季度末我的月度广告支出预计是多少？”

**跨渠道归因：**
- “哪些渠道对首次触达转化的贡献最大？”
- “我的 Facebook Ads 收入与 GA4 认定的收入相比如何？”

## 故障排除

**认证失败 / 401 错误：**
- 确认 `WINDSOR_API_KEY` 是否已设置在 `~/.clawdbot/.env` 中
- 在更新环境文件后重启 `mcporter`

**无法解析 ‘Authorization’ 头部信息 / 必须设置 WINDSOR_API_KEY：**
- `mcporter` 需要将该变量导出到 shell 环境中，而不仅仅是存储在 `.env` 文件中
- 运行命令：`export WINDSOR_API_KEY=your_api_key_here && npx mcporter list`
- 从 `.env` 文件加载变量：`export $(grep -v '^#' ~/.clawdbot/.env | xargs) && npx mcporter list`

**未找到数据源：**
- 在查询之前，您必须在 Windsor.ai 仪表板中至少连接一个数据源
- 访问 https://windsor.ai 连接您的广告平台或分析工具

**数据未更新：**
- Windsor.ai 按计划同步数据；数据更新频率取决于您的计划和使用的连接工具
- 查看 Windsor.ai 仪表板中每个连接工具的最近同步时间

**使用 `npx mcporter list` 后工具列表为空：**
- 确保 `config/mcporter.json` 中包含如设置步骤 3 中所示的 `windsor-ai` 条目
- 确认 `WINDSOR_API_KEY` 在环境变量中不是空字符串