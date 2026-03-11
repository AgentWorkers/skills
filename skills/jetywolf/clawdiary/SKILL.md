---
slug: clawdiary-guardian
name: ClawDiary Guardian
version: 1.1.9
tags: [security, audit, guard, mcp]
license: MIT-0
metadata:
  openclaw:
    requires:
      env: [CLAWDIARY_API_KEY]
    redaction_regex_and_truncation: true
    approved_by_human: true
---

# ClawDiary Guardian

这是一个用于与ClawDiary集成的OpenClaw技能。ClawDiary是一个基于云的审计日志系统，同时也是AI代理执行高风险操作时的拦截网关。

## 如何获取API密钥（注册）

要使用此技能，您需要一个ClawDiary API密钥。

1. **访问ClawDiary官网：** 访问[clawdiary.org](https://clawdiary.org)。
2. **注册并订阅：** 选择一个套餐并按照注册流程操作。
3. **获取API密钥：** 注册完成后，您将获得唯一的`CLAWDIARY_API_KEY`。

如果您希望自行托管实例，请参考[ClawDiary设置文档](https://github.com/jetywolf/claw-diary)。

## 在OpenClaw中的配置

使用上述步骤获取的`CLAWDIARY_API_KEY`来配置您的代理。请注意，所有以`/v1/`开头的API端点都需要通过`Authorization: Bearer <API_KEY>`头部进行身份验证。

## 功能与使用方法

### 1. **主动监控（审批机制）**
**端点：** `POST https://api.clawdiary.org/v1/guard`
**使用场景：** 在执行任何高风险、具有破坏性或出站操作（如运行bash命令、删除文件、发送邮件）之前。
**操作方式：**
调用此端点并等待响应。如果响应显示“red-light”，操作将被阻止，直到人类用户通过Telegram进行批准。只有当响应返回`approved: true`时，操作才能继续执行。

示例请求：
```json
{
  "agent_id": "openclaw",
  "action_type": "execute_bash",
  "command": "rm -rf /tmp/data",
  "params": { "cwd": "/home/user" },
  "thought": "Cleaning up temporary files"
}
```

### 2. **被动审计（日志记录）**
**端点：** `POST https://api.clawdiary.org/v1/audit`
**使用场景：** 操作完成后。
**操作方式：**
报告操作内容、成本及相关数据。这有助于人类操作员异步审查代理的使用情况。

示例请求：
```json
{
  "agent_id": "openclaw",
  "session_id": "sess-001",
  "action_type": "tool_call",
  "cost": 0.003,
  "payload": { "tool": "search_web", "query": "weather in London" }
}
```

### 3. **共享日志记录**
**端点：** `POST https://api.clawdiary.org/v1/diary`（写入），`GET https://api.clawdiary.org/v1/diary?owner_id=...`（查询）
**使用场景：** 为同一所有者跨多个设备（代理）共享日志记录。这允许代理同步状态更新和上下文信息。

示例写入请求：
```json
{
  "owner_id": "alice",
  "lobster_id": "office-mac",
  "content": "Finished API integration today. All good."
}
```

## MCP支持
ClawDiary提供了一个MCP描述文件，位于`GET https://api.clawdiary.org/mcp.json`。将此文件导入MCP客户端后，系统会自动注册`request_human_approval`工具以处理主动监控功能。