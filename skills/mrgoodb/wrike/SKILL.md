---
name: wrike
description: 通过 Wrike API 管理项目、任务和工作流程。创建任务、更新任务状态并跟踪工作进度。
metadata: {"clawdbot":{"emoji":"📊","requires":{"env":["WRIKE_ACCESS_TOKEN"]}}}
---
# Wrike  
项目管理平台。  

## 环境  
```bash
export WRIKE_ACCESS_TOKEN="xxxxxxxxxx"
```  

## 文件夹列表  
```bash
curl "https://www.wrike.com/api/v4/folders" -H "Authorization: Bearer $WRIKE_ACCESS_TOKEN"
```  

## 创建任务  
```bash
curl -X POST "https://www.wrike.com/api/v4/folders/{folderId}/tasks" \
  -H "Authorization: Bearer $WRIKE_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "New Task", "status": "Active"}'
```  

## 任务列表  
```bash
curl "https://www.wrike.com/api/v4/tasks" -H "Authorization: Bearer $WRIKE_ACCESS_TOKEN"
```  

## 链接  
- 文档：https://developers.wrike.com