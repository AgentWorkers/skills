---
name: brandomica
description: 检查品牌名称在各个域名、社交媒体账号、商标、应用商店以及 SaaS 平台上的使用安全性。获取品牌名称的可用性评分、安全性评估结果以及是否适合进行商标注册的决策。
version: 1.0.5
homepage: https://www.brandomica.com/mcp-server
metadata:
  openclaw:
    requires:
      bins:
        - npx
    emoji: "🔍"
    homepage: https://www.brandomica.com
    install:
      - kind: node
        package: brandomica-mcp-server
---
# Brandomica Lab — 品牌名称验证

您可以访问 Brandomica MCP 服务器来进行品牌名称的安全性检查。使用这些工具来帮助用户在发布产品前验证品牌名称。

## 可用工具

- **brandomica_check_all** — 全面品牌名称检查（包括域名、社交媒体平台、商标、应用商店、SaaS 服务以及可用性评分和安全性评估）。使用 `mode: "quick"` 进行快速的本地检查，或使用 `mode: "full"` 获取详细结果。
- **brandomica_assess_safety** — 快速的安全风险评估（0-100 分的评分，风险等级，以及风险因素的详细分析）。适合快速判断是否适合使用该品牌名称。
- **brandomica_filing_readiness** — 品牌名称申请准备情况总结（包括评估结果、风险等级、主要冲突点及可信度）。在安全性评估显示中等或高风险时使用该工具。
- **brandomica_compare_brands** — 并排比较 2-5 个品牌名称候选方案，并提供使用建议。
- **brandomica_batch_check** — 一次检查 2-50 个品牌名称，并按评分排序。
- **brandomica_brand_report** — 生成带有时间戳的证据文档（格式为 JSON）。
- **brandomica_check_domains** — 检查 6 种顶级域名（TLD）的可用性及价格信息。
- **brandomica_check_social** — 检查品牌名称在社交媒体平台（GitHub、Twitter、TikTok、LinkedIn、Instagram）上的可用性。
- **brandomica_check_trademarks** — 在美国专利商标局（USPTO）和欧洲知识产权局（EUIPO）进行商标搜索。
- **brandomica_check_google** — 在 Google 上搜索该品牌名称，检测是否存在竞争对手。
- **brandomica_check_appstores** — 检查品牌名称在 iOS App Store 和 Google Play 上的可用性。
- **brandomica_check_saas** — 检查品牌名称在各种软件包注册平台（如 npm、PyPI、crates.io 等）以及 SaaS 服务中的使用情况。

## 推荐的工作流程

1. 首先使用 `brandomica_assess_safety` 进行快速的风险评估。
2. 如果风险等级为中等或较高，再使用 `brandomica_filing_readiness` 获取详细的申请准备信息。
3. 使用 `brandomica_check_all` 对所有渠道进行全面的安全性检查。
4. 使用 `brandomica_compare_brands` 对比多个品牌名称候选方案。

## 品牌名称格式要求

品牌名称必须由小写字母、数字和连字符组成。工具会拒绝包含无效字符的名称。

## 自动化建议

- **创意生成与验证循环**：先生成多个品牌名称创意，然后使用 `brandomica_batch_check` 对它们进行批量检查。
- **域名查询**：使用 `brandomica_check_domains` 查找可用的域名及其价格信息。
- **商标查询**：在提交商标申请前，使用 `brandomica_filing_readiness` 确认商标是否已被注册。
- **竞争对手分析**：使用 `brandomica_check_google` 查看是否有其他公司使用类似的品牌名称。