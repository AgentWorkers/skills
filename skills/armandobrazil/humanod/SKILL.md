---
slug: humanod
display_name: Humanod
version: 1.0.0
tags: hiring, physical-tasks, api
description: 通过 Humanod API 雇佣人类来完成实际任务。
credentials:
  - HUMANOD_API_KEY
---
# Humanod

**Humanod API** 允许 AI 代理雇佣人类来完成体力劳动任务（如摄影、送货、检查等）。

## 配置

要使用此功能，您需要一个 **Humanod API 密钥**。  
获取方式：[https://www.humanod.app/developer/keys](https://www.humanod.app/developer/keys)

## 工具

### 创建任务  
向系统提交新任务：  
- **端点**：`POST /tasks`  
- **认证方式**：Bearer Token（令牌认证）

### 查看任务状态  
查看任务是否已完成：  
- **端点**：`GET /tasks/{id}`