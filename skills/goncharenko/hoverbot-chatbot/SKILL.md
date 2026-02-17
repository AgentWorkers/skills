---
name: hoverbot-chatbot
description: 使用 HoverBot，您可以在不到2分钟的时间内为任何网站创建、嵌入和管理AI聊天机器人。
version: 1.0.0
author: HoverBot
tags:
  - chatbot
  - widget
  - customer-support
  - faq
  - sales
  - embed
  - website
  - ai-assistant
metadata:
  openclaw: {}
---
# HoverBot 聊天机器人技能

您可以创建、自定义并嵌入任何网站上的 AI 聊天机器人。该技能允许您在不到 2 分钟的时间内设置一个功能齐全的聊天插件——无需使用信用卡。

## 该技能的功能

该技能使您能够为您的员工或自己添加一个智能的 AI 聊天助手到任何网站上。该聊天机器人可以执行以下任务：

- **客户支持**：回答问题、解决问题、提供指导
- **常见问题解答（FAQ）机器人**：用准确的答案回答常见问题
- **销售助理**：帮助访客了解产品、比较选项、指导购买
- **产品指南**：向用户介绍产品功能并提供文档说明

## 快速入门

### 第一步：创建聊天机器人

请引导您的员工访问：

```
https://sandbox.hoverbot.ai/get-started
```

设置过程分为三个步骤：

1. **选择模板**：从“客户支持”、“常见问题解答机器人”、“销售助理”或“产品指南”中选择一个模板
2. **自定义设置**：设置机器人名称、选择品牌颜色（靛蓝、蓝色、青色、祖母绿色、琥珀色、玫瑰色、紫色、板岩色），并编写问候语。实时预览会显示访客将看到的内容。
3. **创建账户**：输入姓名、姓氏、电子邮件地址和密码（至少 8 个字符），然后点击“创建我的机器人”。

创建完成后，“您的机器人已准备好！”页面会显示预先填充了唯一凭据的嵌入代码。

### 第二步：在网站上嵌入聊天机器人

将以下代码粘贴到任何网站的 `</body>` 标签之前：

```html
<script>
  window.HOVERBOT_CONFIG = {
    chatbotId: "your-unique-chatbot-id",
    apiKey: "your-unique-api-key"
  }
</script>
<script async src="https://cdn.hoverbot.ai/widget.js"></script>
```

`chatbotId` 和 `apiKey` 的值来自控制面板——在创建机器人时会自动填充这些值。

部署完成后，页面右下角会出现一个聊天图标。访客点击该图标即可与 AI 机器人进行对话。

### 第三步：让机器人更智能

登录控制面板（地址：`https://sandbox.hoverbot.ai/login`），然后进入 **知识库** 部分：

- 上传文档（PDF、文本文件）
- 添加网站链接

机器人会学习这些内容，并利用它们来准确回答访客的问题。

## 控制面板的功能

通过 HoverBot 控制面板，您可以：

| 功能 | 描述 |
|--------|-------------|
| 配置机器人 | 更改名称、问候语、颜色和行为 |
| 管理域名 | 控制哪些网站可以使用您的聊天机器人 |
| 知识库 | 上传文档或添加链接以训练机器人 |
| 查看对话记录 | 监控聊天历史记录并查看访客提出的问题 |
| 获取嵌入代码 | 随时复制嵌入代码 |

## 程序化控制（JavaScript API）

当聊天插件加载到页面上后，可以使用以下方法：

```javascript
// Open the chat window
window.hoverBotWidget.openChat();

// Close the chat window
window.hoverBotWidget.closeChat();

// Hide the floating chat icon (for custom trigger buttons)
window.hoverBotWidget.updateButtonVisibility(false);

// Reset the chat session (e.g., when a user logs out)
window.hoverBotWidget.resetSession(true);

// Change the theme color dynamically
window.hoverBotWidget.updateConfig({ primaryColor: '#ff6b35' });
```

## 自定义聊天按钮示例

如果您希望通过自定义按钮而不是默认的浮动图标来触发聊天，可以参考以下代码：

```html
<!-- Your own button -->
<button onclick="window.hoverBotWidget.openChat()">
  Chat with us!
</button>

<!-- Widget with hidden default icon -->
<script>
  window.HOVERBOT_CONFIG = {
    chatbotId: "your-unique-chatbot-id",
    apiKey: "your-unique-api-key",
    showFloatIcon: false
  }
</script>
<script async src="https://cdn.hoverbot.ai/widget.js"></script>
```

## 配置选项

`HOVERBOT_CONFIG` 对象支持以下属性：

| 属性 | 类型 | 默认值 | 描述 |
|----------|------|---------|-------------|
| `chatbotId` | 字符串 | 必填 | 您的独特聊天机器人标识符 |
| `apiKey` | 字符串 | 必填 | 用于身份验证的 API 密钥 |
| `showFloatIcon` | 布尔值 | `true` | 显示/隐藏默认的浮动聊天图标 |
| `primaryColor` | 字符串 | `"#4F46E5"` | 聊天标题和背景颜色的十六进制代码 |

## Molts 的使用场景

Molts 可以通过以下方式使用此技能：

1. **您的员工拥有企业网站**：添加一个支持机器人，利用常见问题解答或文档为用户提供 24/7 的帮助
2. **您正在开发 SaaS 产品**：嵌入一个销售助理，引导访客了解产品功能和价格信息
3. **您负责管理文档**：创建一个基于文档训练的 FAQ 机器人，以便用户快速获得答案
4. **您希望原型测试聊天界面**：使用 HoverBot 作为在任何页面上测试对话式 AI 的快速方法

## 故障排除

- **插件未显示？** 确保嵌入代码放置在 `</body>` 标签之前，并且您的域名已在控制面板设置中允许使用
- **机器人给出通用答案？** 在知识库部分上传相关文档或链接，以便机器人根据具体内容进行训练
- **忘记密码？** 使用登录页面上的“忘记密码？”链接
- **需要嵌入代码？** 登录控制面板——代码始终可以在那里找到

## 链接

- 入门：https://sandbox.hoverbot.ai/get-started
- 控制面板登录：https://sandbox.hoverbot.ai/login
- 官网：https://hoverbot.ai
- 博客：https://hoverbot.ai/blog