---
name: wechat-send
description: "**通过 AppleScript 和 JXA 控制 macOS WeChat 桌面应用的用户界面来自动发送文本消息**  
该功能并非用于 OpenClaw 的聊天通道，而是用于控制您 Mac 上的 WeChat 图形用户界面（GUI），以代表您发送消息。适用场景包括：  
1. 当用户需要向某人发送微信消息时；  
2. 通知微信联系人；  
3. 批量向多个联系人发送消息。  
**所需条件：**  
- 已安装并登录 WeChat for Mac，且 WeChat 窗口处于可见状态；  
- 为 Node.js 应用程序授予了 macOS 的“辅助功能”（Accessibility）权限。  
**不适用场景：**  
- 读取或接收微信消息；  
- 管理群聊；  
- 传输文件/图片；  
- 将 WeChat 作为与 OpenClaw 的通信渠道使用。"
metadata: {"openclaw": {"os": ["darwin"], "author": "ryan_dream", "email": "ryanyang5@gmail.com"}}
---
# 通过自动化操作在 macOS 上的 WeChat 桌面应用向联系人发送消息

## 先决条件

- 已安装并登录了 WeChat for Mac
- 在 macOS 的“系统设置”→“隐私与安全”→“辅助功能”中，已授予 `node` 应用程序“辅助功能”权限
- WeChat 窗口必须处于打开状态（未最小化到 Dock）

## 使用方法

运行以下脚本：

```bash
bash scripts/wechat_send.sh "<contact_name>" "<message>"
```

### 示例

```bash
# Send a simple message
bash scripts/wechat_send.sh "Ryan" "你好！"

# Send a longer message
bash scripts/wechat_send.sh "Ellison" "明天下午3点开会，别忘了带文件"
```

## 工作原理

1. 激活 WeChat 并打开搜索功能（按 Cmd+F）
2. 输入联系人的名称，选择第一个搜索结果（按 Enter），然后关闭搜索功能（按 Escape）
3. 使用 JXA CGEvent 模拟鼠标操作点击消息输入框
4. 从剪贴板中粘贴消息内容（按 Cmd+V），然后按 Enter 发送消息

## 限制

- 联系人名称必须与 WeChat 中的实际联系人完全匹配（系统会自动选择第一个搜索结果）
- 无法发送图片或文件（仅支持文本消息）
- 无法读取收到的消息
- WeChat 窗口的位置会影响点击坐标（坐标会根据窗口边界自动计算）
- 如果搜索结果不正确，消息可能会发送给错误的人——请使用具体的联系人名称
- 每次只能发送一条消息；如需发送给多个接收者，请多次运行该脚本

## 故障排除

- **消息未发送**：确保 WeChat 窗口处于可见状态（未最小化），并且找到了正确的联系人
- **辅助功能相关错误**：在“系统设置”→“辅助功能”中重新授予 `node` 应用程序权限，然后重启相关服务
- **发送错误联系人**：使用更具体的联系人名称以避免搜索结果模糊