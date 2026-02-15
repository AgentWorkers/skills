---
name: ziptax-sales-tax
description: >
  Look up U.S. sales tax rates using the ZipTax API. Use when the user asks about sales tax rates,
  tax calculations for a U.S. address/ZIP code/coordinates, freight or service taxability,
  jurisdiction-level tax breakdowns, use tax vs sales tax, or needs to integrate sales tax
  data into an application. Also handles account usage metrics and product taxability codes (TIC).
  Supports address-level (door-level), lat/lng, and postal code lookups across 12,000+ jurisdictions.
---

# ZipTax 销售税查询

## 设置

请将 `ZIPTAX_API_KEY` 环境变量设置为从 https://platform.zip.tax (DEVELOP > API Keys) 获取的 API 密钥。免费 tier 每月允许 100 次调用。**切勿公开分享您的 API 密钥。**

## 快速入门

### 地址查询（最准确）
```bash
curl -s "https://api.zip-tax.com/request/v60?address=200+Spectrum+Center+Drive+Irvine+CA+92618" \
  -H "X-API-KEY: $ZIPTAX_API_KEY"
```

### 邮政编码查询
```bash
curl -s "https://api.zip-tax.com/request/v60?postalcode=92618" \
  -H "X-API-KEY: $ZIPTAX_API_KEY"
```

### 经纬度查询
```bash
curl -s "https://api.zip-tax.com/request/v60?lat=33.6525&lng=-117.7479" \
  -H "X-API-KEY: $ZIPTAX_API_KEY"
```

## 工作流程

1. 确定查询类型：地址、经纬度或邮政编码
2. 使用 **v60**（最新版本）以获取完整的税收分类信息；使用 v10 可获取简单的综合税率
3. 向 `https://api.zip-tax.com/request/v60` 发送带有身份验证头的 GET 请求
4. 检查 `metadata.response.code`——值为 100 表示请求成功
5. 读取 `taxSummaries[0].rate` 以获取总销售税率
6. 读取 `baseRates` 数组以获取州/县/市/区的税收分类信息
7. 检查 `service.taxable` 和 `shipping.taxable` 以确定服务/运费是否需要征税

## 关键要点

- **地址 > 邮政编码**：地址查询会返回一个确切的结果；邮政编码查询会返回该邮政编码区域内的所有税率
- **身份验证**：使用请求头 `X-API-KEY` 或查询参数 `key`
- **税率格式**：小数形式（例如，0.0775 表示 7.75%）
- **响应代码 100** 表示请求成功；请检查 `metadata.response.code`
- **指标端点**（`/account/metrics`）不计入使用量限制

## 集成资源

- **`scripts/lookup.sh`**：用于快速查询的命令行工具。可以通过 `--address`、`--lat`/`--lng`、`--postalcode` 或 `--metrics` 参数来运行该脚本
- **`references/api-reference.md`：包含所有 API 端点、响应格式、代码示例、响应代码和 SDK 链接的完整参考文档。在需要了解端点详情或响应字段定义时请查阅此文件。