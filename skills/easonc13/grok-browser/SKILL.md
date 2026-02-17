---
name: grok-browser
description: 通过浏览器自动化来查询Grok AI。当您需要向Grok提问、获取AI回复或使用Grok的DeepSearch/Think功能时，请使用此方法。该方法会复制回复文本，而不会使用截图。
---
# Grok浏览器操作技巧

通过Chrome浏览器自动化工具查询Grok（grok.com）并复制其返回的响应内容。

## 先决条件

- 安装了Chrome浏览器，并启用了Browser Relay扩展程序
- 使用`profile=chrome`（切勿使用`profile=clawd`）

## 快速入门

```bash
# 1. Open Chrome with Grok
open -a "Google Chrome" "https://grok.com"
sleep 3

# 2. Attach browser relay
/Users/eason/clawd/scripts/attach-browser-relay.sh

# 3. Check tabs
browser action=tabs profile=chrome
```

## 输入方法（非常重要！）

Grok使用的是`contenteditable`元素，而非普通的文本框。需要使用JavaScript来获取并处理输入内容：

```javascript
// Type query via evaluate
browser action=act profile=chrome targetId=<id> request={
  "kind": "evaluate",
  "fn": "(() => { const editor = document.querySelector('[contenteditable=\"true\"]'); if(editor) { editor.focus(); editor.innerText = 'YOUR_QUERY_HERE'; return 'typed'; } return 'not found'; })()"
}
```

完成后按Enter键提交请求：

```
browser action=act profile=chrome targetId=<id> request={"kind":"press","key":"Enter"}
```

## 完整的工作流程

### 1. 打开Grok网站并连接Browser Relay

```bash
open -a "Google Chrome" "https://grok.com"
sleep 3
/Users/eason/clawd/scripts/attach-browser-relay.sh
```

### 2. 获取标签页ID

```
browser action=tabs profile=chrome
```

找到Grok相关的标签页，记下其`targetId`值。

### 3. 输入查询内容

```
browser action=act profile=chrome targetId=<id> request={
  "kind": "evaluate",
  "fn": "(() => { const e = document.querySelector('[contenteditable=\"true\"]'); if(e) { e.focus(); e.innerText = 'What is quantum computing?'; return 'ok'; } return 'fail'; })()"
}
```

### 4. 提交请求

```
browser action=act profile=chrome targetId=<id> request={"kind":"press","key":"Enter"}
```

### 5. 等待响应

```bash
sleep 10-20  # Grok can take 10-30 seconds
```

### 6. 拍摄屏幕截图并找到“复制”按钮

```
browser action=snapshot profile=chrome targetId=<id>
```

在响应区域中查找标有“Copy”字样的按钮（通常位于最后一条消息附近）。

### 7. 点击“复制”按钮

```
browser action=act profile=chrome targetId=<id> request={"kind":"click","ref":"<copy_button_ref>"}
```

### 8. 读取剪贴板内容

```bash
pbpaste
```

## 响应状态判断

当出现以下情况时，表示请求已完成并已收到响应：
- 响应文本下方出现了“复制”按钮
- 显示了响应耗时（例如：“952ms”）
- 出现了后续操作的建议按钮

## 对于不同主题的聊天，请重新开始新的对话

为了避免上下文混乱，请对不相关的查询使用新的聊天窗口：

```
browser action=navigate profile=chrome targetId=<id> targetUrl="https://grok.com"
```

或者使用快捷键Cmd+J来打开新窗口：

```
browser action=act profile=chrome targetId=<id> request={"kind":"press","key":"Meta+j"}
```

## 启用深度搜索（DeepSearch）

在提交请求之前，请先点击相应的按钮：

```
# In snapshot, find DeepSearch button
browser action=act profile=chrome targetId=<id> request={"kind":"click","ref":"<deepsearch_ref>"}
# Then type and submit as normal
```

## 故障排除

### 标签页未找到
重新运行连接脚本：

```bash
/Users/eason/clawd/scripts/attach-browser-relay.sh
```

### Browser Relay无法正常工作
检查其状态：
```
browser action=status profile=chrome
```
应显示`cdpReady: true`。

### 上下文信息溢出
请返回grok.com网站，不要继续使用旧的聊天记录。

### 多个Chrome窗口
关闭多余的Chrome窗口，仅保留一个窗口以确保Browser Relay的稳定运行。

### “复制”按钮未找到
可能是因为响应数据仍在传输中，请稍等片刻后再尝试截图。

## 示例操作流程

```
# Open and attach
exec: open -a "Google Chrome" "https://grok.com"
exec: sleep 3
exec: /Users/eason/clawd/scripts/attach-browser-relay.sh

# Get tab
browser action=tabs profile=chrome
# Returns targetId: ABC123...

# Type query
browser action=act profile=chrome targetId=ABC123 request={
  "kind":"evaluate",
  "fn":"(() => { const e = document.querySelector('[contenteditable=\"true\"]'); e.focus(); e.innerText = 'Explain quantum entanglement briefly'; return 'ok'; })()"
}

# Submit
browser action=act profile=chrome targetId=ABC123 request={"kind":"press","key":"Enter"}

# Wait
exec: sleep 15

# Snapshot to find Copy button
browser action=snapshot profile=chrome targetId=ABC123
# Find Copy button ref, e.g., e326

# Copy
browser action=act profile=chrome targetId=ABC123 request={"kind":"click","ref":"e326"}

# Read result
exec: pbpaste
```