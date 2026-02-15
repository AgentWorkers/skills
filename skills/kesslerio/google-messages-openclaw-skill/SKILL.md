---
name: google-messages
description: 通过 Google Messages 的网页界面（messages.google.com）发送和接收短信/RCS 消息。当需要执行以下操作时，请使用该功能：发送文本消息、查看短信、通过 Google Messages 发送消息，或将收到的短信转发到其他渠道。
metadata: {"openclaw": {"emoji": "💬", "requires": {"tools": ["browser"], "bins": ["node"], "env": ["SMS_NOTIFICATION_TARGET", "SMS_NOTIFICATION_CHANNEL"]}}}
---

# Google Messages 浏览器技能

使用 `browser` 工具通过 `messages.google.com` 自动发送和接收 SMS/RCS 消息。

## 概述

Google Messages for Web 允许您通过浏览器发送和接收来自 Android 手机的短信。此技能实现了这一功能。

**要求：**
- 安装了 Google Messages 应用的 Android 手机
- 手机和计算机处于同一网络中（用于初始的 QR 配对）
- 浏览器配置有持久会话（使用 `openclaw` 或您喜欢的浏览器配置文件）

**注意：** 如果使用其他浏览器配置文件，请将示例中的 `profile=openclaw` 替换为您的配置文件名。

---

## 快速参考

| 动作 | 命令 |
|--------|---------|
| 打开配对页面 | `browser action=open profile=openclaw targetUrl="https://messages.google.com/web/authentication"` |
| 检查会话状态 | `browser action=snapshot profile=openclaw` — 查看对话列表或 QR 码 |
| 截取屏幕截图 | `browser action=screenshot profile=openclaw` |

---

## 初始设置（QR 配对）

首次设置需要扫描 QR 码：

1. **打开 Google Messages Web**  
   ```
   browser action=open profile=openclaw targetUrl="https://messages.google.com/web/authentication"
   ```

2. **截取 QR 码** 并分享给用户  
   ```
   browser action=screenshot profile=openclaw
   ```

3. **用户使用手机扫描 QR 码：**
   - 打开 Android 上的 Google Messages 应用
   - 点击 ⋮ 菜单 → “设备配对” → “QR 码扫描器”
   - 扫描 QR 码

4. **验证连接** — 屏幕截图应显示对话列表，而不是 QR 码

**重要提示：** 启用 “记住这台电脑” 以保持会话状态。

---

## 发送消息

1. **导航到对话页面**  
   ```
   browser action=navigate profile=openclaw targetUrl="https://messages.google.com/web/conversations"
   ```

2. **截取屏幕截图并找到目标对话**  
   ```
   browser action=snapshot profile=openclaw
   ```  
   在对话列表中找到对应的联系人，并记下其引用（`ref`）。

3. **点击对话**  
   ```
   browser action=act profile=openclaw request={"kind": "click", "ref": "<ref>"}
   ```

4. **输入消息**（从截图中找到相应的文本框引用）  
   ```
   browser action=act profile=openclaw request={"kind": "type", "ref": "<input_ref>", "text": "Your message"}
   ```

5. **点击发送**（找到发送按钮的引用）  
   ```
   browser action=act profile=openclaw request={"kind": "click", "ref": "<send_ref>"}
   ```

---

## 接收消息（实时通知）

此技能包含一个用于接收实时 SMS 通知的 Webhook 系统。

### 组件

1. **sms-webhook-server.js** — 接收通知并转发到 OpenClaw 通道
2. **sms-observer.js** — 浏览器脚本，用于监控新消息

### 设置

1. **设置环境变量：**  
   ```bash
   export SMS_NOTIFICATION_TARGET="telegram:YOUR_CHAT_ID"
   export SMS_NOTIFICATION_CHANNEL="telegram"
   ```

2. **启动 Webhook 服务器：**  
   ```bash
   node <skill>/sms-webhook-server.js
   ```

3. **将观察器注入浏览器**（详见 `references/observer-injection.md`）

### systemd 服务（持久化会话）

```bash
cp <skill>/systemd/google-messages-webhook.service ~/.config/systemd/user/
# Edit service file: set SMS_NOTIFICATION_TARGET in Environment=
systemctl --user daemon-reload
systemctl --user enable --now google-messages-webhook
```

---

## 阅读消息

请参阅 `references/snippets.md` 以获取以下 JavaScript 代码片段：
- 获取最近的对话记录
- 获取当前对话中的消息
- 检查会话状态

---

## 故障排除

| 问题 | 解决方案 |
|---------|----------|
| QR 码无法显示 | 会话已过期，请重新配对 |
| 元素无法找到 | Google 更新了用户界面，请检查屏幕截图中的新选择器 |
| 发送按钮不可用 | 消息输入框为空或手机断开连接 |
| 观察器未检测到新消息 | 查看浏览器控制台中的 `[SMS Observer]` 日志 |
| Webhook 未收到通知 | 确认 Webhook 服务器正在运行：`curl http://127.0.0.1:19888/health` |

---

## 选择器参考

Google Messages 使用 Angular 组件。这些组件可能会随更新而变化。

| 元素 | 选择器 |
|---------|----------|
| 对话列表 | `mws-conversations-list` |
| 对话项 | `mws-conversation-list-item` |
| 消息输入框 | `textarea[aria-label*="message"]` |
| 发送按钮 | `button[aria-label*="Send"]` |
| QR 码 | `mw-qr-code` |

---

## 限制

- 手机必须处于在线状态（消息通过手机同步）
- 浏览器标签页必须保持打开状态以接收通知
- 会话在大约 14 天无操作后过期
- 页面重新加载时观察器可能会丢失（需要重新注入）

---

## 安全性

- Webhook 仅监听本地地址（127.0.0.1）
- 不存储任何凭据（会话信息保存在浏览器 cookie 中）
- 配对链接涉及用户的手机信息，请妥善处理

## 许可证

Apache-2.0