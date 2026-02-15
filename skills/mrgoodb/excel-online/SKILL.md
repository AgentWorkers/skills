---
name: excel-online
description: 通过 Microsoft Graph API 读写 Excel 文件。在 OneDrive/SharePoint 中管理工作簿、工作表和单元格。
metadata: {"clawdbot":{"emoji":"📗","requires":{"env":["MICROSOFT_ACCESS_TOKEN"]}}}
---

# Excel Online（Microsoft Graph）

通过 Microsoft 365 实现 Excel 自动化。

## 环境配置

```bash
export MICROSOFT_ACCESS_TOKEN="xxxxxxxxxx"
```

## 列出 OneDrive 中的工作簿

```bash
curl "https://graph.microsoft.com/v1.0/me/drive/root/search(q='.xlsx')" \
  -H "Authorization: Bearer $MICROSOFT_ACCESS_TOKEN"
```

## 获取工作表

```bash
curl "https://graph.microsoft.com/v1.0/me/drive/items/{item-id}/workbook/worksheets" \
  -H "Authorization: Bearer $MICROSOFT_ACCESS_TOKEN"
```

## 读取数据范围

```bash
curl "https://graph.microsoft.com/v1.0/me/drive/items/{item-id}/workbook/worksheets/{sheet-name}/range(address='A1:D10')" \
  -H "Authorization: Bearer $MICROSOFT_ACCESS_TOKEN"
```

## 向数据范围写入内容

```bash
curl -X PATCH "https://graph.microsoft.com/v1.0/me/drive/items/{item-id}/workbook/worksheets/{sheet-name}/range(address='A1:B2')" \
  -H "Authorization: Bearer $MICROSOFT_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"values": [["Name", "Value"], ["Test", 123]]}'
```

## 添加工作表

```bash
curl -X POST "https://graph.microsoft.com/v1.0/me/drive/items/{item-id}/workbook/worksheets" \
  -H "Authorization: Bearer $MICROSOFT_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "NewSheet"}'
```

## 创建表格

```bash
curl -X POST "https://graph.microsoft.com/v1.0/me/drive/items/{item-id}/workbook/worksheets/{sheet-name}/tables/add" \
  -H "Authorization: Bearer $MICROSOFT_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"address": "A1:C5", "hasHeaders": true}'
```

## 运行公式

```bash
curl -X POST "https://graph.microsoft.com/v1.0/me/drive/items/{item-id}/workbook/functions/sum" \
  -H "Authorization: Bearer $MICROSOFT_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"values": [[1, 2, 3, 4, 5]]}'
```

## 链接：
- OneDrive: https://onedrive.live.com
- 文档：https://docs.microsoft.com/en-us/graph/api/resources/excel