---
name: webflow-seo-geo
description: End-to-end workflow for SEO/GEO content updates in Webflow: prioritize via GSC, draft/refresh content, create patch JSONs, update Webflow CMS via API, set images/alt/SEO, publish, and handle technical SEO fixes (canonical domain, redirects). Use for blog/service SEO refreshes and GEO/location page optimization.
---

# Webflow SEO/GEO

## 快速入门（默认工作流程）
1) **优先级确定**：参考 Google Search Console (GSC) 的数据以及站点规划文档。
2) **内容起草**：撰写或更新文案（使用自然的语言风格，明确表达意图，并设置强烈的呼叫行动（CTA）。
3) **JSON 数据更新**：将 Webflow 中的元素数据写入本地的 `/out/` 文件夹。
4) **通过 API 发布**：使用 POST 请求创建新元素或更新现有元素，然后进行发布。
5) **图片处理**：设置 `image-de-couverture`、`image---alt-text` 以及元描述和标题。
6) **技术检查**：确保网站使用正确的规范域名、处理重定向请求，并检查站点地图的状态以及 GSC 的相关设置。

## 首先查看的资料
- **SEO 计划文档**：你的 SEO 计划文档。
- **每日日志**：你的每日 SEO 日志。
- **现有元素**：从 Webflow 中导出的数据（位于 `/webflow_items/` 目录下）。
- **更新后的数据**：本地的 `/out/` 文件夹。

## Webflow API（v2）——使用方法
请使用环境变量 `WEBFLOW_API_TOKEN`。
- **创建元素**：`POST /v2/collections/{collection_id}/items`
- **更新元素**：`PATCH /v2/collections/{collection_id}/items/{item_id}`
- **发布元素**：`POST /v2/collections/{collection_id}/items/publish`（需要提供 `itemIds`）
- **列出元素**：`GET /v2/collections/{collection_id}/items`（支持分页查询）

**集合 ID**
- 请替换为你的实际集合 ID（从 Webflow API 获取）。

**重要字段**
- `name`、`slug`、`contenu-de-l-article`、`seo---meta-description`
- `image-de-couverture`（格式：{fileId}/{url}/{alt}
- `image---alt-text`
- `date-de-redaction`、`categorie`

## 内容编写指南
- **表达直接、具体且具有可操作性**。
- **每个部分只包含一条信息**。
- **使用内部链接指向相关服务和博客文章**。
- **在页面顶部或接近结尾处设置呼叫行动（CTA）**。
- **提供 3–5 个简短的问答（FAQ），以提高点击率（CTR）。

## 地理相关内容/本地页面
- 在标题和元描述中明确指出页面的地理位置（城市名称）。
- 添加 2–3 个与地点相关的信息（如地址、城市名称）以及相关证明。
- 提供指向相关服务页面的链接。

## 技术性 SEO 的快速优化技巧
### 规范域名（www 与非 www）
- 请在 Webflow 的用户界面中设置主域名（而非通过 API）。
- 确保非 www 域名为默认域名，这样 Webflow 会自动处理 301 重定向和规范设置。

### 站点地图（Sitemap）
- 确保站点地图指向规范域名：`https://yourdomain.tld/sitemap.xml`。
- 检查 `robots.txt` 文件中是否包含了站点地图的 URL。

## 需要查阅的参考资料
- **Webflow API 详细信息**：`references/webflow_api.md`
- **内容复制/SEO 编写指南**：`references/seo_copy_patterns.md`
- **数据更新模板**：`references/patch_templates.md`