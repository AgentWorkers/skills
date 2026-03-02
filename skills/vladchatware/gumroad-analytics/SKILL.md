---
name: gumroad-analytics
description: **安全地每日获取Gumroad产品/销售分析数据（默认情况下不会保存任何原始的个人信息）**
metadata:
  openclaw:
    homepage: https://clawhub.ai/vladchatware/gumroad-analytics
    requires:
      bins: ["curl", "python3", "date"]
      config: ["~/.config/gumroad/credentials.json"]
---
# Gumroad 分析

以尊重用户隐私的方式收集 Gumroad 的分析数据。

## 该功能的用途

- 从 Gumroad API 获取销售数据（sales）和产品信息（products）
- 生成每日汇总 JSON 文件（包含销售数量和总收入）
- 默认情况下，不会存储原始的 API 响应内容（raw API payloads）

## 认证信息

所需文件：`~/.config/gumroad/credentials.json`

示例：

```json
{
  "access_token": "YOUR_GUMROAD_ACCESS_TOKEN"
}
```

**增强权限设置：**

```bash
chmod 600 ~/.config/gumroad/credentials.json
```

## 运行方式

```bash
bash skills/gumroad-analytics/scripts/fetch_metrics.sh
```

**可选的原始数据存储功能（需用户明确同意）：**

```bash
bash skills/gumroad-analytics/scripts/fetch_metrics.sh --store-raw
```

## 输出结果

**汇总文件（默认输出）：**
- `memory/metrics/gumroad/YYYY-MM-DD-summary.json`

**原始数据文件（仅在使用 `--store-raw` 选项时生成）：**
- `memory/metrics/gumroad/YYYY-MM-DD-raw-sales-redacted.json`
- `memory/metrics/gumroad/YYYY-MM-DD-raw-products.json`

## 注意事项：

- 销售数据的原始信息在写入文件前会被处理掉（`email` 和买家姓名字段会被删除）。
- 如果您不需要原始数据，请勿使用 `--store-raw` 选项。