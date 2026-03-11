---
name: imessage
description: 使用 AppleScript 通过 macOS 的“Messages”应用程序发送 iMessage。适用于用户需要向电话号码发送文本消息或短信的情况。支持中文和英文消息；美国地区的电话号码需要以 “+1” 作为前缀。
---
# iMessage 技能

通过 AppleScript 使用 macOS 的 Messages 应用程序发送 iMessage 消息。

## 使用方法

当用户请求向某个电话号码发送消息时：

1. 从用户的请求中提取电话号码和消息内容。
2. 为美国地区的电话号码添加 “+1” 前缀（例如：8888888888 -> +18888888888）。
3. 使用 AppleScript 发送消息。

## AppleScript 命令

```bash
osascript << 'EOF'
tell application "Messages"
    activate
    send "MESSAGE_TEXT" to buddy "+1PHONE_NUMBER"
end tell
EOF
```

## 示例

**发送英文消息：**
- 用户：`发送消息到 8888888888，说“hello”`
- 命令：`send "hello" to buddy "+18888888888"`

**发送中文消息：**
- 用户：`发送到 8888888888 你好`
- 命令：`send "你好" to buddy "+18888888888"`

## 注意事项：

- Messages 应用程序必须已登录 iMessage/FaceTime 账户。
- 如果 AppleScript 失败，可能需要通过系统设置 > 隐私与安全 > 辅助功能来启用相关权限。
- 该功能支持任何文本内容（英文、中文、表情符号等）。