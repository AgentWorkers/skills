---
name: slack-controller
description: 通过浏览器自动化来控制 Slack，实现发送消息、管理群组会议、屏幕共享、设置用户状态等功能，并以登录用户的身份执行相应操作。
---
# Slack 控制器（浏览器版）

该技能通过专用的自动化配置文件，实现对 Slack Web 客户端（`app.slack.com`）或桌面应用程序（通过调试端口）的自动化操作。这使得代理能够以您的身份发送消息、启动群组会议、共享屏幕以及管理您的状态。

## 先决条件

1. 已安装 **Slack 桌面应用程序**（推荐）或 **Google Chrome** 浏览器。
2. 在 macOS 的系统设置中，终端/鼠标需要具有 **屏幕录制** 和 **辅助功能** 权限。
3. 如果系统提示，您需要在自动化窗口/配置文件中手动登录一次。

## 使用方法

### 通过 OpenClaw 聊天界面操作：
- “给 Adeel 发送消息，内容为‘hello’”
- “与 Adeel 启动群组会议并共享我的屏幕”
- “将我的状态设置为‘正在开会’，持续 1 小时”
- “搜索‘季度报告’”

### 通过 CLI（手动操作）：

**发送消息：**
```bash
node ~/.cursor/skills/slack-controller/dist/index.js --action=sendMessage --target="adeel" --message="Hello there"
```

**启动群组会议及共享屏幕：**
```bash
node ~/.cursor/skills/slack-controller/dist/index.js --action=startHuddleAndScreenShare --target="general"
```

**离开群组会议：**
```bash
node ~/.cursor/skills/slack-controller/dist/index.js --action=leaveHuddle --target="general"
```

**设置状态：**
```bash
node ~/.cursor/skills/slack-controller/dist/index.js --action=setStatus --statusEmoji=":coffee:" --statusText="Lunch"
```

**搜索：**
```bash
node ~/.cursor/skills/slack-controller/dist/index.js --action=search --target="project updates"
```

## 可用操作：

- `sendMessage`：向用户或频道发送文本消息。
- `openChat`：直接打开聊天窗口。
- `sendHuddleInvite`：切换群组会议状态（标准加入模式）。
- `startHuddleAndScreenShare`：加入群组会议，等待界面提示后点击“共享屏幕”→“共享整个屏幕”。
- `leaveHuddle`：离开当前的群组会议。
- `setStatus`：设置自定义的状态表情和文本。
- `setPresence`：切换为“在线”/“离开”状态。
- `pauseNotifications`：暂停通知。
- `uploadFile`：将本地文件上传到聊天中。
- `addReaction`：对聊天中的最新消息做出反应。
- `search`：执行全局搜索并显示结果。