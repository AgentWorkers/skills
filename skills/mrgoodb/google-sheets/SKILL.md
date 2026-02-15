---
name: google-sheets
description: 读写 Google Sheets 的数据。通过 Sheets API 创建电子表格、更新单元格以及管理工作表。
metadata: {"clawdbot":{"emoji":"📊","requires":{"env":["GOOGLE_ACCESS_TOKEN"]}}}
---

# Google Sheets

电子表格自动化

## 环境配置

```bash
export GOOGLE_ACCESS_TOKEN="ya29.xxxxxxxxxx"
```

## 读取电子表格数据

```bash
curl "https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}/values/Sheet1!A1:D10" \
  -H "Authorization: Bearer $GOOGLE_ACCESS_TOKEN"
```

## 向单元格写入数据

```bash
curl -X PUT "https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}/values/Sheet1!A1:B2?valueInputOption=USER_ENTERED" \
  -H "Authorization: Bearer $GOOGLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"values": [["Name", "Score"], ["Alice", 95]]}'
```

## 添加新行

```bash
curl -X POST "https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}/values/Sheet1!A:D:append?valueInputOption=USER_ENTERED" \
  -H "Authorization: Bearer $GOOGLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"values": [["New", "Row", "Data", "Here"]]}'
```

## 创建电子表格

```bash
curl -X POST "https://sheets.googleapis.com/v4/spreadsheets" \
  -H "Authorization: Bearer $GOOGLE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"properties": {"title": "My New Sheet"}}'
```

## 获取电子表格元数据

```bash
curl "https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}" \
  -H "Authorization: Bearer $GOOGLE_ACCESS_TOKEN"
```

## 清除指定范围的数据

```bash
curl -X POST "https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}/values/Sheet1!A1:Z100:clear" \
  -H "Authorization: Bearer $GOOGLE_ACCESS_TOKEN"
```

## 链接：
- 控制台：https://console.cloud.google.com/apis/library/sheets.googleapis.com
- 文档：https://developers.google.com/sheets/api/reference/rest