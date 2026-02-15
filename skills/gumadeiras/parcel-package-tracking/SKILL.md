---
slug: parcel
display_name: Parcel
description: 通过 Parcel API 追踪并添加配送记录。
---

# Parcel

通过 Parcel 应用程序的 API 来追踪包裹信息并添加新的配送记录。

## 配置

使用此功能需要 `PARCEL_API_KEY` 环境变量。您可以从 [web.parcelapp.net](https://web.parcelapp.net) 获取该密钥。

## 工具：`parcel`

用于控制 Parcel API 的命令行工具（CLI）。

### 参数

- `action`（必填）：`list`、`add` 或 `carriers` 中的一个。
- `mode`：对于 `list`，指定过滤模式（`active` 或 `recent`）。默认值为 `recent`。
- `tracking`：对于 `add`，输入包裹的追踪号码。
- `carrier`：对于 `add`，输入运输公司的代码（例如 `ups`、`usps`、`fedex`）。
- `description`：对于 `add`，输入包裹的描述。
- `notify`：对于 `add`，指定是否发送推送通知（布尔值）。
- `search`：对于 `carriers`，输入搜索字符串。

### 使用方法

**列出配送记录：**
```bash
# List recent deliveries
node ~/.clawdbot/skills/parcel/parcel-api.js list

# List active deliveries
node ~/.clawdbot/skills/parcel/parcel-api.js list --mode=active
```

**添加配送记录：**
```bash
node ~/.clawdbot/skills/parcel/parcel-api.js add \
  --tracking "1Z1234567890" \
  --carrier "ups" \
  --description "New Shoes" \
  --notify
```

**列出运输公司：**
```bash
node ~/.clawdbot/skills/parcel/parcel-api.js carriers "ups"
```