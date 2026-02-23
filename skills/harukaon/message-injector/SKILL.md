---
name: message-injector
description: "OpenClaw插件：在每条用户消息到达代理服务器之前，会在消息开头添加自定义文本。该插件可用于：在回复前强制执行`memory_search`操作、插入系统级指令、以及在每次对话中添加持久性提醒。该插件可通过工作区扩展程序进行安装，适用于WebChat、Telegram、Slack等所有聊天平台。"
---
# Message Injector

这是一个轻量级的 OpenClaw 工作区扩展程序，它利用 `before_agent_start` 钩子，在每条用户消息中通过 `prependContext` 方法插入自定义文本。

## 安装

### 1. 创建扩展程序目录

```bash
mkdir -p ~/.openclaw/workspace/.openclaw/extensions/message-injector
```

### 2. 复制插件文件

将 `scripts/index.ts` 和 `scripts/openclaw.plugin.json` 文件复制到扩展程序目录中：

```bash
cp scripts/index.ts ~/.openclaw/workspace/.openclaw/extensions/message-injector/
cp scripts/openclaw.plugin.json ~/.openclaw/workspace/.openclaw/extensions/message-injector/
```

### 3. 添加配置

在 `~/.openclaw/openclaw.json` 文件的 `plugins.entries` 部分添加以下配置：

```json
"message-injector": {
  "enabled": true,
  "config": {
    "enabled": true,
    "prependText": "Your custom text here"
  }
}
```

### 4. 重启 Gateway

```bash
openclaw gateway restart
```

## 配置参数

| 参数 | 类型 | 默认值 | 说明 |
|-------|------|---------|-------------|
| `enabled` | boolean | `true` | 是否启用该插件 |
| `prependText` | string | `""` | 每条用户消息前要插入的文本 |

## 示例用法

**强制执行内存搜索：**
```json
"prependText": "[⚠️ 回答前必须先 memory_search 检索相关记忆，禁止凭印象回答]"
```

**添加持久化上下文信息：**
```json
"prependText": "[当前项目：my-app | 技术栈：React + Node.js | 部署环境：AWS]"
```

**插入安全规则：**
```json
"prependText": "[RULE: Always verify file paths before deletion. Never run rm -rf without confirmation.]"
```

## 工作原理

该插件注册了一个 `before_agent_start` 钩子。当该钩子被触发时，它会返回 `{prependContext: prependText }`，OpenClaw 会将该文本插入到用户消息中，然后再由代理（agent）处理该消息。这种插入操作是在 Gateway 级别进行的，因此代理无法跳过或忽略它。

## 源代码

GitHub: https://github.com/Harukaon/openclaw-message-injector