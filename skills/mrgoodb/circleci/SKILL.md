---
name: circleci
description: 通过 API 管理 CircleCI 的管道（pipelines）、作业（jobs）和工作流程（workflows）。触发并监控构建过程（builds）。
metadata: {"clawdbot":{"emoji":"⭕","requires":{"env":["CIRCLECI_TOKEN"]}}}
---
# CircleCI  
持续集成平台。  

## 环境设置  
```bash
export CIRCLECI_TOKEN="xxxxxxxxxx"
```  

## 管道列表  
```bash
curl "https://circleci.com/api/v2/project/gh/{org}/{repo}/pipeline" \
  -H "Circle-Token: $CIRCLECI_TOKEN"
```  

## 触发管道  
```bash
curl -X POST "https://circleci.com/api/v2/project/gh/{org}/{repo}/pipeline" \
  -H "Circle-Token: $CIRCLECI_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"branch": "main"}'
```  

## 工作流程  
```bash
curl "https://circleci.com/api/v2/workflow/{workflowId}" -H "Circle-Token: $CIRCLECI_TOKEN"
```  

## 链接  
- 文档：https://circleci.com/docs/api/v2/