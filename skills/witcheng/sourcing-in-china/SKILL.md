---
name: sourcing-in-china
description: 通过 MCP 服务器，您可以从 Made-in-China.com 搜索产品、供应商，并获取详细的产品信息。该功能适用于从中国采购产品、寻找制造商、比较供应商、查看最小订购量（MOQ）和价格，或任何涉及中国供应商的全球采购任务。当输入诸如 “source”（采购来源）、”find supplier”（寻找供应商）、”manufacturer”（制造商）、”MOQ”（最小订购量）、”made in china”（中国制造）、”China sourcing”（中国采购）或 “procurement”（采购）等关键词时，该功能会自动触发。
---
# 从中国采购产品

您可以使用 `mcporter` 和 `made-in-china` MCP 服务器，在 Made-in-China.com 上搜索产品、查找供应商并获取产品详细信息。

## 先决条件

- 已安装 `mcporter` CLI（通过 `npm i -g mcporter` 安装）
- `mcporter` 的 `made-in-china` 服务器已在 `config/mcporter.json` 中配置，SSE 端点为：`https://mcp.chexb.com/sse`
- 有关配置详情，请参阅 [mcporter 文档](https://mcporter.dev)。

## 可用工具

| 工具 | 功能 | 关键参数 |
|------|---------|------------|
| `search_products` | 按关键词搜索产品 | `keyword`, `page`（每页显示 30 个结果）|
| `search_suppliers` | 搜索制造商/供应商 | `keyword`, `page`（每页显示 10 个结果）|
| `get_product_detail` | 获取产品详细信息 | `url`（产品 URL）|

## 快速命令

```bash
# Search products
mcporter call made-in-china.search_products keyword="LED light" page=1

# Search suppliers
mcporter call made-in-china.search_suppliers keyword="LED light"

# Get product detail (use URL from search results)
mcporter call made-in-china.get_product_detail url="https://..."
```

## 采购工作流程

### 1. 产品发现

首先使用 `search_products` 按要求搜索产品。每个搜索结果包含：
- 产品名称、价格、最小订购量（MOQ）
- 主要规格（属性）
- 供应商名称和链接
- 产品图片

通过多次搜索不同页面来获取更多结果。根据需要调整关键词以提高搜索精度（例如，从 “LED” 精确搜索到 “12V LED 灯带 防水”）。

### 2. 供应商评估

使用 `search_suppliers` 搜索制造商。搜索结果包括：
- 公司名称和业务类型（制造商 / 贸易公司）
- 主要产品和所在地
- 认证标志（ISO、审核等）

**建议优先选择制造商而非贸易公司**，因为制造商通常能提供更优惠的价格。通过认证标志来判断产品质量。

### 3. 产品深入了解

对感兴趣的产品使用 `get_product_detail` 获取详细信息。返回的内容包括：
- 完整的产品规格和描述
- 所有产品图片
- 样品价格（如有的话）
- 产品分类和视频链接
- 供应商/品牌信息

### 4. 比较与推荐

在比较不同选项时，按以下标准进行排序：
- **价格范围**（单价 + 最小订购量）
- **供应商信誉**（认证标志、业务类型）
- **规格匹配度**（是否符合买家需求）
- **样品可用性**（是否提供样品价格）

## 最佳实践

- 使用英文关键词在 Made-in-China.com 上进行搜索，以获得更准确的结果
- 对同一关键词同时搜索产品和供应商，以便从不同角度了解情况
- 始终核对最小订购量——不同供应商之间的价格差异可能很大
- “制造商” 类型的供应商通常提供更优惠的单价
- 对比供应商的认证标志：经过审核的供应商优于普通供应商
- 如需详细规格信息，请使用 `get_product_detail` 进一步查询

## 输出格式

以清晰、易于阅读的格式呈现结果：
- 使用表格对比产品和供应商信息
- 突出显示价格、最小订购量和主要规格
- 包含产品和供应商页面的直接链接
- 标记重要的认证标志或证书

有关采购策略的更多信息，请参阅 [references/sourcing-guide.md](references/sourcing-guide.md)。