---
name: Gemini Browser
description: 通过 OpenClaw 的 Browser Relay 功能，使用浏览器自动化来查询 Google Gemini。当您需要向 Gemini 提问并获取 AI 回答时，可以使用此方法。前提是您已经安装了 OpenClaw 并配置了 Browser Relay Chrome 扩展程序。
  Query Google Gemini via browser automation using OpenClaw's Browser Relay.
  Use when you need to ask Gemini questions and get AI responses.
  Requires OpenClaw with Browser Relay Chrome extension configured.
---
# Gemini浏览器技能

通过OpenClaw浏览器中继查询Google Gemini（`gemini.google.com`）并提取响应。

> **⚠️ 安全提示**：此技能会在您的**真实Chrome浏览器**中运行，并使用您的Google登录会话（通过CDP，即Chrome开发者工具协议）。代理将能够访问所关联标签页中的所有内容。请仅关联您明确允许代理控制的标签页。请参阅[安全注意事项](#security-considerations)。

## 先决条件

- **已安装并运行OpenClaw**（此技能使用OpenClaw的`browser`命令）
- **已安装并配置OpenClaw浏览器中继Chrome扩展程序**：
  - 该扩展程序默认绑定到本地回环地址`127.0.0.1:18792`
  - 必须在扩展程序选项中配置网关认证令牌
- 在Chrome中登录Google账户（Gemini需要身份验证）
- 使用`profile=chrome`通过您的现有Chrome会话进行中继（而非隔离的`profile=openclaw-managed`会话）

## 快速入门

```bash
# 1. Open Gemini in Chrome
open -a "Google Chrome" "https://gemini.google.com"

# 2. Manually click the Browser Relay extension icon on the Gemini tab to attach
#    (the badge will show "ON" when attached)

# 3. Verify relay is connected
browser action=status profile=chrome
# Should show cdpReady: true

# 4. List tabs
browser action=tabs profile=chrome
# Note the targetId for the Gemini tab
```

## 输入方法

Gemini使用**Quill富文本编辑器**（`contenteditable`元素），而不是标准的`<textarea>`。您需要通过JavaScript插入文本：

```
browser action=act profile=chrome targetId=<id> request={
  "kind": "evaluate",
  "fn": "(() => { const editor = document.querySelector('div.ql-editor[contenteditable=\"true\"]'); if (!editor) return 'editor not found'; editor.focus(); editor.innerHTML = '<p>YOUR_QUERY_HERE</p>'; editor.dispatchEvent(new Event('input', { bubbles: true })); return 'ok'; })()"
}
```

然后提交：

```
browser action=act profile=chrome targetId=<id> request={"kind":"press","key":"Enter"}
```

## 完整工作流程

### 1. 准备

在Chrome中打开Gemini，并**手动**将Browser Relay扩展程序添加到相关标签页。

```bash
open -a "Google Chrome" "https://gemini.google.com"
# Then click the Browser Relay extension icon on the Gemini tab
```

### 2. 获取标签页ID

```
browser action=tabs profile=chrome
```

找到Gemini标签页条目并记下其`targetId`。

### 3. 输入查询内容

```
browser action=act profile=chrome targetId=<id> request={
  "kind": "evaluate",
  "fn": "(() => { const editor = document.querySelector('div.ql-editor[contenteditable=\"true\"]'); if (!editor) return 'editor not found'; editor.focus(); editor.innerHTML = '<p>What is quantum computing?</p>'; editor.dispatchEvent(new Event('input', { bubbles: true })); return 'ok'; })()"
}
```

### 4. 提交请求

```
browser action=act profile=chrome targetId=<id> request={"kind":"press","key":"Enter"}
```

### 5. 等待响应

Gemini可能需要10到60秒才能完成响应。您可以通过检查“停止”按钮是否消失来判断查询是否完成：

```
browser action=act profile=chrome targetId=<id> request={
  "kind": "evaluate",
  "fn": "(() => { const stop = document.querySelector('button[aria-label*=\"Stop\"]'); return stop ? 'generating' : 'done'; })()"
}
```

### 6. 提取响应

**选项A — 复制到剪贴板（推荐，可保留Markdown格式）：**

```
# Take a snapshot and find the Copy button
browser action=snapshot profile=chrome targetId=<id>

# Click the Copy button by its ref from the snapshot
browser action=act profile=chrome targetId=<id> request={"kind":"click","ref":"<copy_button_ref>"}

# Read from clipboard
pbpaste
```

**选项B — 通过DOM提取（备用方案）：**

```
browser action=act profile=chrome targetId=<id> request={
  "kind": "evaluate",
  "fn": "(() => { const msgs = document.querySelectorAll('.model-response-text'); if (msgs.length === 0) return 'no response found'; return msgs[msgs.length - 1].innerText; })()"
}
```

## 新聊天会话

对于无关的查询，请启动一个新的聊天会话以避免数据混淆：

```
browser action=navigate profile=chrome targetId=<id> targetUrl="https://gemini.google.com"
```

## 响应完成信号

当以下条件满足时，表示响应已完成：
- “停止”按钮消失
- 响应下方出现“复制”按钮
- 显示建议的后续操作选项

## 安全注意事项

> **⚠️ 重要提示**：使用此技能前请了解以下风险：
1. **会话访问**：`profile=chrome`会使用您的真实Chrome会话及其所有登录信息。代理可以查看并操作该标签页中的所有内容，包括您的Google账户信息。
2. **JavaScript执行**：`evaluate`操作会在页面上下文中执行任意JavaScript代码。虽然此技能仅限于对输入字段进行DOM操作，但该机制本身具有较高的灵活性。
3. **需要手动操作**：必须**手动点击**Browser Relay扩展程序才能将其添加到标签页；代理无法自动添加标签页。请仅关联特定的Gemini标签页。
4. **仅限本地访问**：中继连接使用本地地址`127.0.0.1`，并需要认证令牌，从而防止远程访问。
5. **建议**：使用专门用于AI自动化的独立Chrome会话，并使用非主Google账户登录，以降低风险。

## 故障排除

| 问题 | 解决方案 |
|---------|----------|
| `cdpReady: false` | 点击Gemini标签页上的Browser Relay扩展程序图标以重新连接 |
| 未找到标签页 | 运行`browser action=tabs profile=chrome`以刷新标签页列表 |
| 未找到编辑器 | 页面可能尚未完全加载；请稍后重试。Gemini可能已修改DOM结构——请检查`div.ql-editor`元素 |
| 未找到复制按钮 | 响应可能仍在生成中；请先检查“停止”按钮的状态 |
| 登录失败 | 确保已在Chrome中登录Google账户 |
| 数据泄露风险 | 为避免数据混淆，请切换到`gemini.google.com`开始新的聊天会话 |