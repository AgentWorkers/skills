---
name: api-connector
description: 连接 REST API，管理认证流程，并处理响应数据。适用于 API 集成相关任务。
allowed-tools:
  - Read
  - Glob
  - Grep
  - Task
  - WebFetch
  - WebSearch
  - TodoWrite
  - AskUserQuestion
  - SlashCommand
  - Skill
  - NotebookEdit
  - BashOutput
  - KillShell
---

# api-connector - Claude Code Skill

该技能用于连接 REST API、管理身份验证以及处理响应，适用于 API 集成任务。

## 配置

使用该技能需要以下环境变量：

- `API_BASE_URL`：API 请求的基地址（默认值：https://api.example.com）
- `API_KEY`：API 认证密钥（**必填**）
- `API_TIMEOUT`：请求超时时间（以毫秒为单位，默认值：30000）

请在您的环境变量或 Claude Code 配置中设置这些值。

## 功能

- 支持 GET、POST、PUT、DELETE 请求
- 自动处理认证请求头
- 解析 JSON 格式的响应数据
- 实现速率限制和重试机制
- 支持响应缓存

## 配置

**必填项：**
- `API_KEY`：您的 API 认证密钥

**可选项：**
- `API_BASE_URL`：API 的基地址（默认值：https://api.example.com）
- `API_TIMEOUT`：请求超时时间（以毫秒为单位，默认值：30000）

## 使用方法

```
"Get data from /users endpoint"
"POST this JSON to /api/create"
"Check the API status"
```

## 安全性

该扩展仅以只读模式运行：
- 无法执行 bash 命令
- 无法编辑本地文件
- 无法将文件写入磁盘
- 仅向配置好的 API 端点发送 HTTP 请求

---

*该技能是通过 [skill-porter](https://github.com/jduncan-rva/skill-porter) 工具从 Gemini CLI 扩展程序转换而来的。*