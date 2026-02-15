---
name: linkedin
description: 通过浏览器中继或cookies实现LinkedIn自动化操作，包括发送消息、查看个人资料以及执行网络相关动作。
homepage: https://linkedin.com
metadata: {"clawdbot":{"emoji":"💼"}}
---

# LinkedIn

使用浏览器自动化工具与 LinkedIn 进行交互：查看消息、浏览个人资料、搜索以及发送好友请求。

## 好友请求方法

### 方法 1：Chrome 扩展程序 Relay（推荐）
1. 在 Chrome 中打开 LinkedIn 并登录。
2. 点击 Clawdbot 浏览器 Relay 工具栏图标，将相关标签页添加到工具栏中。
3. 使用 `browser` 工具，并设置 `profile="chrome"`。

### 方法 2：隔离浏览器（Isolated Browser）
1. 使用 `browser` 工具，并设置 `profile="clawd"`。
2. 访问 linkedin.com。
3. 手动登录（只需设置一次）。
4. 会话信息会保留下来，以便后续使用。

## 常见操作

### 查看好友请求状态
```
browser action=snapshot profile=chrome targetUrl="https://www.linkedin.com/feed/"
```

### 查看通知/消息
```
browser action=navigate profile=chrome targetUrl="https://www.linkedin.com/messaging/"
browser action=snapshot profile=chrome
```

### 搜索用户
```
browser action=navigate profile=chrome targetUrl="https://www.linkedin.com/search/results/people/?keywords=QUERY"
browser action=snapshot profile=chrome
```

### 查看个人资料
```
browser action=navigate profile=chrome targetUrl="https://www.linkedin.com/in/USERNAME/"
browser action=snapshot profile=chrome
```

### 发送消息（请先获得用户确认！）
1. 进入消息页面或个人资料页面。
2. 使用 `browser action=act`，并配合点击或输入操作来发送消息。
3. 在发送消息前，请务必确认消息内容。

## 安全规则
- **未经用户明确同意，切勿发送任何消息**。
- **未经确认，切勿接受或发送好友请求**。
- **避免频繁的自动化操作**——LinkedIn 对自动化行为非常敏感。
- 推荐的每小时操作次数上限为约 30 次。

## 会话 Cookie 方法（高级）
如果浏览器 Relay 不可用，可以从浏览器中提取 `li_at` Cookie：
1. 在浏览器中打开 LinkedIn 并登录。
2. 打开开发者工具（DevTools）→ 应用程序（Application）→ Cookies → linkedin.com。
3. 复制 `li_at` 值。
4. 将该值安全存储起来，以用于后续的 API 请求。

## 故障排除
- 如果登录失败：在浏览器中重新登录。
- 如果遇到操作次数限制：等待 24 小时后再尝试。
- 如果出现验证码：请在浏览器中手动完成验证码验证，然后再继续操作。