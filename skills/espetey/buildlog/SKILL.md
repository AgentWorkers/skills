---
name: buildlog
description: 记录、导出并分享您的人工智能编程会话，将其转换为可回放的构建日志（buildlogs）。
version: 1.0.0
author: buildlog.ai
repository: https://github.com/buildlog/openclaw-skill
homepage: https://buildlog.ai
---

# Buildlog 技能

使用该技能可以记录您的 OpenClaw 编码会话，并将它们分享到 buildlog.ai 上。

## 概述

Buildlog 技能能够实时捕获您在 OpenClaw 中的 AI 辅助编码会话，生成可复制的录制文件，便于与他人分享。非常适合以下场景：

- **教程**：逐步展示您的开发过程
- **文档编写**：为复杂的实现创建动态文档
- **调试**：回顾会话以了解问题所在
- **学习**：研究他人解决问题的方法

## 命令

### 录制

- **"Start a buildlog [title]"** — 开始录制新的会话
- **"Stop the buildlog"** — 停止录制（可选择上传）
- **"Pause the buildlog"** — 暂时暂停录制
- **"Resume the buildlog"** — 继续暂停的录制

### 导出

- **"Export this session as a buildlog"** — 将当前会话导出为 buildlog 格式
- **"Export the last [N] messages"** — 导出会话中的部分内容

### 上传

- **"Upload the buildlog"** — 将录制文件上传到 buildlog.ai
- **"Share the buildlog"** — 上传并获取可共享的链接

### 注释

- **"Add a note: [text]"** — 为当前内容添加注释
- **"Mark this as important"** — 标记重要内容
- **"Add chapter: [title]"** — 创建章节标记

### 状态

- **"Buildlog status"** — 查看录制状态
- **"Show buildlog info"** — 显示当前录制详情

## 配置

请将以下配置添加到您的 OpenClaw 配置文件中：

```json
{
  "skills": {
    "buildlog": {
      "apiKey": "your-api-key",
      "autoUpload": false,
      "defaultPublic": true,
      "includeFileContents": true,
      "maxFileSizeKb": 100
    }
  }
}
```

### 选项

| 选项 | 类型 | 默认值 | 描述 |
|--------|------|---------|-------------|
| `apiKey` | 字符串 | — | 您的 buildlog.ai API 密钥（公开上传时可选） |
| `autoUpload` | 布尔值 | `false` | 录制停止时自动上传 |
| `defaultPublic` | 布尔值 | `true` | 默认情况下使 buildlog 公开 |
| `includeFileContents` | 布尔值 | `true` | 包含文件内容快照 |
| `maxFileSizeKb` | 数字 | `100` | 允许的最大文件大小（以 KB 为单位） |

## 事件

该技能会触发以下事件：

- `buildlog:started` — 录制开始
- `buildlog:stopped` — 录制结束
- `buildlog:paused` — 录制暂停
- `buildlog:resumed` — 录制继续
- `buildlog:uploaded` — 录制文件成功上传
- `buildlog:error` — 发生错误

## 示例

### 基本录制

```
You: Start a buildlog "Building a REST API"
Assistant: 🔴 Recording started: "Building a REST API"

You: Create an Express server with TypeScript
Assistant: [creates files...]

You: Stop the buildlog
Assistant: Recording stopped. 12 exchanges captured.
         Would you like to upload to buildlog.ai?
```

### 回溯性导出

```
You: Export this session as a buildlog
Assistant: Exported 24 exchanges as buildlog.
         Title: "Untitled Session"
         Ready to upload?
```

## 隐私设置

- Buildlog 可以设置为公开或私密
- API 密钥不会包含在导出的文件中
- 您可以控制哪些内容被共享
- 您可以在 buildlog.ai 上随时删除 buildlog 文件