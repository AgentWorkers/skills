---
name: smartsheet
description: 通过 Smartsheet API 管理工作表、行和列。实现电子表格工作流程的自动化。
metadata: {"clawdbot":{"emoji":"📋","requires":{"env":["SMARTSHEET_ACCESS_TOKEN"]}}}
---
# Smartsheet  
工作管理与协作工具。  

## 环境  
```bash
export SMARTSHEET_ACCESS_TOKEN="xxxxxxxxxx"
```  

## 列表工作表  
```bash
curl "https://api.smartsheet.com/2.0/sheets" -H "Authorization: Bearer $SMARTSHEET_ACCESS_TOKEN"
```  

## 获取工作表  
```bash
curl "https://api.smartsheet.com/2.0/sheets/{sheetId}" -H "Authorization: Bearer $SMARTSHEET_ACCESS_TOKEN"
```  

## 添加行  
```bash
curl -X POST "https://api.smartsheet.com/2.0/sheets/{sheetId}/rows" \
  -H "Authorization: Bearer $SMARTSHEET_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"toBottom": true, "cells": [{"columnId": 123, "value": "New Row"}]}'
```  

## 链接  
- 文档：https://smartsheet.redoc.ly