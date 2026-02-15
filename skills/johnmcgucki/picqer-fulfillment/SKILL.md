# FutureFulfillment Picqer 仪表盘 v2

这是一个仅提供 JSON 格式数据的 API，用于获取仪表盘信息。不返回 Markdown 格式的响应。

## 命令

所有命令的返回值均为 JSON 格式，不提供任何文字说明。

### `dashboard.fetch`
返回包含关键绩效指标（KPIs）、选项列表（picklists）、库存信息以及收入数据的完整仪表盘数据对象。

**输入格式：**
```json
{
  "command": "dashboard.fetch",
  "filters": {
    "dateFrom": "2024-01-01",
    "dateTo": "2024-01-31",
    "picker": "",
    "client": ""
  }
}
```

### `picklists.fetch`
仅返回选项列表的数据（包括选项的状态、选择情况以及相关统计数据）。

**输入格式：**
```json
{
  "command": "picklists.fetch",
  "filters": {}
}
```

### `stock.fetch`
返回库存变动情况，并对库存商品进行分类（分为“慢动商品”和“快动商品”）。

**输入格式：**
```json
{
  "command": "stock.fetch",
  "filters": {}
}
```

### `revenue.fetch`
返回销售库存商品的客户的收入数据。

**输入格式：**
```json
{
  "command": "revenue.fetch",
  "filters": {}
}
```

## 响应格式

所有响应均以 JSON 格式返回。成功响应的示例：
```json
{
  "kpis": { "openPicklists": 42, "closedPicklists": 128, ... },
  "picklists": { "open": [...], "closed": [...], "pickerStats": [...] },
  "stock": { "rows": [...] },
  "revenue": { "perClient": [...] },
  "filtersUsed": { ... }
}
```

错误响应的示例：
```json
{ "error": "Picqer API not configured" }
```

## 安全性

- API 密钥仅存储在本地 `.env` 文件中；
- OpenClaw 配置文件中不包含任何认证信息；
- 仅通过 Tailscale 进行访问。