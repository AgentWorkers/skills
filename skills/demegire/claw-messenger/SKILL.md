# Claw Messenger

> 专为AI代理设计的iMessage、RCS和SMS通信工具。无需使用手机或Mac Mini。

Claw Messenger允许OpenClaw代理通过共享的基础设施发送和接收iMessage、RCS和SMS消息。您只需通过WebSocket进行连接，无需在您的端配置任何公共URL或Webhook。

## 设置（适用于AI代理）

请按照以下步骤操作：

### 第1步：人类用户创建账户

人类用户需在https://clawmessenger.com注册并选择一个套餐（提供免费试用）。在控制面板中，他们将获得一个实时API密钥以及频道配置信息。同时，他们还会看到一个特殊提示，其中包含该API密钥。如果忘记保存API密钥，也可以重新生成。

### 第2步：安装插件

在终端中运行以下命令：

```
openclaw plugins install @emotion-machine/claw-messenger
```

### 第3步：将频道配置添加到`.openclaw.json`文件中

作为代理，您需要从控制面板中获取API密钥（密钥前缀为`cm_live_`），或者获取API密钥页面上显示的包含密钥的特殊提示。获取密钥后，编辑`.openclaw.json`文件，在`channels`部分添加`claw-messenger`频道：

```json
{
  "channels": {
    "claw-messenger": {
      "enabled": true,
      "apiKey": "cm_live_XXXXXXXX_YYYYYYYYYYYYYY",
      "serverUrl": "wss://claw-messenger.onrender.com",
      "preferredService": "iMessage",
      "dmPolicy": "pairing",
      "allowFrom": ["+15551234567"]
    }
  }
}
```

将`cm_live_XXXXXXXX_YYYYYYYYYYYYYY`替换为实际的API密钥。如果`.openclaw.json`中已配置其他频道，请将`claw-messenger`的配置信息合并到现有的`channels`对象中，不要覆盖其他频道的配置。

配置字段：
- `apiKey`（必填）：来自控制面板的实时API密钥，前缀为`cm_live_`。
- `serverUrl`（必填）：WebSocket服务器的URL，使用`wss://claw-messenger.onrender.com`。
- `preferredService`（可选）：`"iMessage"`、`"RCS"`或`"SMS"`。默认值为`"iMessage"`。
- `dmPolicy`（可选）：`"open"`、`"pairing"`或`"allowlist"`。用于控制谁能向您发送消息。默认值为`"pairing"`。
- `allowFrom`（可选）：E.164电话号码数组。仅在`dmPolicy`设置为`"allowlist"`时使用。

### 第4步：开始使用

配置完成后，即可使用该频道进行所有iMessage、RCS和SMS通信。该插件提供了以下功能：
- `claw_messenger_status`：查看连接状态和当前使用的服务。
- `claw_messenger_switch_service`：在运行时切换iMessage、RCS和SMS之间的通信方式。

您可以使用该插件发送文本消息和媒体文件（图片、视频、音频、文档），使用iMessage的回复功能（tapback），发送输入提示信息，并参与群聊。

### 第5步：验证功能是否正常

有两种测试方法：

**方法A — 代理发起测试**：向人类用户的手机发送测试消息，例如：“Hello, this is your agent testing the Claw Messenger connection.”（您好，这是您的代理在测试Claw Messenger的连接。）

**方法B — 人类用户发起测试**：人类用户在控制面板的“Routes”页面上添加自己的电话号码。注册成功后，他们可以发送短信到共享的号码，消息将发送给您。未注册的号码因安全原因无法发送消息给您。

如果收到回复或人类用户确认收到消息，则说明设置完成。

## 消息传递机制

**发送消息**：您发送消息 -> 插件通过WebSocket发送 -> Emotion Machine服务器转发 -> 以iMessage/RCS/SMS的形式送达接收方。

**接收消息**：有人向共享的号码发送短信 -> Emotion Machine服务器查找对应的电话号码 -> 将消息转发到您的WebSocket连接 -> 插件将消息传递给您。

只有通过控制面板注册或首次发送消息建立连接的电话号码才能接收您的消息。未注册的号码将被安全地忽略。

## 计费

套餐信息请访问https://clawmessenger.com/billing。计费基于每个日历月份内的发送和接收消息数量。如果超出套餐限制，系统将拒绝发送消息，直到下一个计费周期或您升级套餐。

## 链接

- 控制面板：https://clawmessenger.com/dashboard
- 插件：@emotion-machine/claw-messenger