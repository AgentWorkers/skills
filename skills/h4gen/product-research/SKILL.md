---
name: product-spy
description: **元技能：通过关联社交热点信号与市场竞争数据来寻找电商热门产品，并生成可用于店铺发布的商品信息。**  
适用于用户需要寻找适合代发货或白标销售的畅销产品时，该技能可提供明确的数据支持及执行指导。
homepage: https://clawhub.ai
user-invocable: true
disable-model-invocation: false
metadata: {"openclaw":{"emoji":"🕵️","requires":{"bins":["node","npx","goplaces"],"env":["TAVILY_API_KEY","GOOGLE_PLACES_API_KEY","MATON_API_KEY"],"config":[]},"note":"Requires local installation of tavily-search, goplaces, api-gateway, and at least one deployment path (woocommerce or shopify)."}}
---

## 目的  
通过结合以下因素来识别产品机会：  
1. 社交媒体上的热度；  
2. 地区需求分析；  
3. 市场竞争情况/销售数据；  
4. 店铺的部署准备情况。  

这是一种协调性工具，但不能保证一定能带来盈利。  

## 必需安装的技能  
- `tavily-search`（最新版本：`1.0.0`）  
- `goplaces`（最新版本：`1.0.0`）  
- `api-gateway`（最新版本：`1.0.29`）  
- 部署目标：  
  - 通过 `api-gateway` 部署到 `woocommerce`；  
  - 或者部署到 `shopify`（最新版本：`1.0.1`，目前处于维护状态）。  

## 安装/更新步骤：  
```bash
npx -y clawhub@latest install tavily-search
npx -y clawhub@latest install goplaces
npx -y clawhub@latest install api-gateway
npx -y clawhub@latest install shopify
npx -y clawhub@latest update --all
```  

## 验证步骤：  
```bash
npx -y clawhub@latest list
```  

## 必需的凭证  
- `TAVILY_API_KEY`（用于趋势分析和数据收集）  
- `GOOGLE_PLACES_API_KEY`（通过 `goplaces` 获取地区需求数据）  
- `MATON_API_KEY`（用于访问市场/部署相关的 API）  

## 预检步骤：  
```bash
echo "$TAVILY_API_KEY" | wc -c
echo "$GOOGLE_PLACES_API_KEY" | wc -c
echo "$MATON_API_KEY" | wc -c
```  

## 强制性要求：  
- 如果缺少任何凭证，切勿默默失败；  
- 必须返回错误信息（`MissingAPIKeys`），并指出缺失的凭证及受影响的步骤；  
- 对于未受影响的步骤，继续执行，并在需要时将输出标记为“部分完成”（`Partial`）。  

## 需要用户首先提供的输入信息：  
- `product_niche`（例如：`pets`）  
- `target_region`（国家/城市范围）  
- `target_store`（`woocommerce` 或 `shopify`）  
- `risk_tolerance`（风险容忍度：`low`、`medium`、`high`）  
- `max_cogs`（最大成本）  
- `min_margin_target`（最低利润率）  
- `shipping_time_limit_days`（运输时间限制）  
- `ad_angle`（广告宣传策略，例如：问题解决方案、用户生成内容演示、前后对比等）  

**注意：** 在明确所有约束条件之前，切勿提议进行产品部署。  

## 工具功能说明：  
### `tavily-search`  
用于趋势分析和供应商信息收集：  
- 查找产品相关的热门话题和趋势列表；  
- 收集社交媒体上的证据；  
- 定位供应商信息（如 AliExpress、Alibaba 或网站目录）；  
- 提取竞争对手的店铺信息/产品页面数据。  

### `goplaces`  
用于地区需求分析：  
- 查询目标地区的本地商家信息；  
- 比较不同城市/地区的需求数据；  
- 为产品发布或测试提供地理优先级建议。  
**重要限制：**  
- `goplaces` 是一个地理位置数据接口，而非直接的社会趋势监测工具；  
- 应将其视为地区需求的参考依据，而非独立的趋势预测工具。  

### `api-gateway`  
在具备相应连接的情况下，用于执行市场分析和店铺操作：  
- 提供市场/分析数据接口（如果用户账户中已配置）；  
- 可用于创建 `woocommerce` 产品草稿；  
- 如连接成功，还可提供类似 Search Console 的数据增强功能。  

### 操作限制：  
- 需要 `MATON_API_KEY`；  
- 需要为每个应用程序启用 OAuth 连接（`ctrl.maton.ai`）；  
- 仅凭 API 密钥无法完成所有操作。  

### 工具支持的平台：  
- `woocommerce` 已在 `api-gateway` 的文档中明确列出；  
- `shopify` 相关功能目前处于维护状态，可能无法使用；  
- `helium 10` 和 `jungle scout` 未在文档中列为 `api-gateway` 的官方支持工具。  

## 标准的因果流程：  
1. **趋势扫描（tavily-search）**：  
  - 发现近期在社交媒体上热度较高的产品。  
  - 例如：`TikTok 上的热门推荐 + 产品特性 + 过去 7 天内的提及次数。  

2. **社交媒体证据评分**：  
  - 根据产品的最新热度、信息来源的多样性以及提及频率对候选产品进行评分；  
  - 筛选时至少需要来自两个独立来源的证据。  

3. **地区需求分析（goplaces）**：  
  - 检查目标地区的市场需求情况；  
  - 优先考虑在多个地区都有销售记录的产品。  

4. **市场数据验证（api-gateway）**：  
  - 通过连接的供应商获取销售/竞争数据；  
  - 如果 `Helium 10` 或 `Jungle Scout` 无法使用，会触发错误提示并切换到备用方案。  

### 输出内容：  
- `TrendCandidates`：  
  - 筛选出的产品列表；  
  - 产品的评分结果及信息来源。  

- `MarketCheck`：  
  - 竞争情况与销售数据分析；  
  - 数据验证的状态及使用的服务提供商信息。  

- `SourcingTable`：  
  - 可用的供应商信息；  
  - 产品的预计成本；  
  - 运输时间预估；  
  - 风险提示。  

- `StoreDraft`：  
  - 产品标题、描述、主要优势；  
  - 建议的价格；  
  - 适用于 `woocommerce` 或 `shopify` 的产品草稿文件。  

- `TikTokAdScript`：  
  - 适用于 TikTok 广告的脚本；  
  - 广告展示内容；  
  - 呼吁用户采取的行动（CTA）。  

- `NextActions`：  
  - 发布和测试产品的具体步骤。  

## 质量控制：  
在最终输出之前，需验证：  
- 数据来源的时效性和可靠性；  
- 产品的经济性是否符合用户要求；  
- 部署路径的可行性；  
- 不支持的集成工具需明确标注；  
- 缺失的凭证或连接问题需及时报告。  

**错误处理：**  
- 如果缺少 `TAVILY_API_KEY`，返回错误信息 `MissingAPIKeys`，跳过趋势分析和供应商信息收集步骤，并请求提供产品链接；  
- 如果缺少 `GOOGLE_PLACES_API_KEY`，返回错误信息 `MissingAPIKeys`，跳过地区需求分析步骤；  
- 如果缺少 `MATON_API_KEY`，返回错误信息 `MissingAPIKeys`，跳过市场数据验证步骤；  
- 如果 `api-gateway` 连接失败（HTTP 400 错误），保持流程处于分析状态，并提供连接设置指导；  
- 如果 `shopify` 处于维护状态，标记部署为“受阻”，并提供 `woocommerce` 手动导入的备用方案；  
- 如果 `Helium 10` 或 `Jungle Scout` 无法使用，说明无法使用这些工具，并继续使用其他替代方案进行分析。  

**注意事项：**  
- 从不保证某个产品一定会成功；  
- 不得伪造销售数据、利润率或用户评价；  
- 不得隐瞒任何受限的集成工具；  
- 所有的推荐结果都应基于实际观察到的数据和明确的假设。