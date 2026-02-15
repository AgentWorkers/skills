---
name: claw-me-maybe
version: 1.2.0
description: **Clawdbot的Beeper集成功能**  
通过Beeper Desktop API，您可以发送消息并搜索WhatsApp、Telegram、Signal、Discord、Slack、Instagram、iMessage、LinkedIn和Facebook Messenger等平台上的聊天记录。该功能还支持发送反应（如点赞、评论等）、设置提醒、添加附件以及标记消息为已读。实现跨平台统一的消息自动化处理——只需简单请求即可。
author: nickhamze
keywords: Beeper, messaging, WhatsApp, Telegram, Signal, Discord, Slack, Instagram, iMessage, LinkedIn, Facebook Messenger, Google Messages, Google Chat, chat automation, unified messaging, Desktop API, send messages, search messages, reactions, reminders, multi-platform, cross-platform messaging, chat search, message history, unread messages
metadata: {"clawdbot":{"emoji":"📟","skillKey":"claw-me-maybe","requires":{"bins":["curl"]},"homepage":"https://www.beeper.com","defaultEnv":{"BEEPER_API_URL":"http://localhost:23373"}}}
user-invocable: true
---

# Claw Me Maybe - Beeper桌面API与多平台消息传递功能 📟

**你的“小龙虾”（Clawdbot）终于可以联系到你（以及其他人）了！**  
现在，你的Clawdbot可以通过*所有*聊天平台与你进行交流。WhatsApp？Telegram？Signal？Discord？Slack？Instagram私信？LinkedIn？iMessage？**全部都可以！**只需一个技能，一个工具即可实现。

该功能由[Beeper](https://www.beeper.com)提供支持——这款应用能够统一管理你所有的聊天记录。

## 你的“小龙虾”能做什么？

🔍 **搜索信息** - “Sarah上周对项目说了什么？”你的Clawdbot会立刻在所有Beeper聊天记录中查找相关信息。  
💬 **随时随地发送消息** - “告诉妈妈我会晚到” → 消息会自动发送到WhatsApp；“在Slack上通知团队” → 一切搞定，无需切换应用程序。  
📊 **查看收件箱摘要** - “我错过了什么？”快速获取你在所有Beeper平台上的未读消息汇总。  
🔔 **设置提醒** - “明天提醒我回复这条消息” → 你的Clawdbot会帮你记住，省去你的麻烦。  
📎 **下载附件** - 从任何Beeper聊天中下载文件、图片和媒体文件。  
😀 **对消息做出反应** - 为任何Beeper平台上的消息添加表情符号反应。  
✅ **标记为已读** - 保持收件箱整洁，轻松标记消息为已读状态。

## 支持的Beeper平台  

你的Clawdbot可以连接到**Beeper支持的任何平台**：  
| 平台 | 支持状态 |  
|----------|--------|  
| WhatsApp | ✅ 全面支持 |  
| Telegram | ✅ 全面支持 |  
| Signal | ✅ 全面支持 |  
| Discord | ✅ 全面支持 |  
| Slack | ✅ 全面支持 |  
| Instagram私信 | ✅ 全面支持 |  
| Facebook Messenger | ✅ 全面支持 |  
| LinkedIn消息 | ✅ 全面支持 |  
| X（Twitter）私信 | ✅ 全面支持 |  
| Google消息 | ✅ 全面支持 |  
| Google Chat | ✅ 全面支持 |  
| iMessage | ✅ 仅支持macOS系统 |

**一个技能，十二个平台，无限可能。**

## 快速入门  

### 1. 安装Beeper  

还没有安装Beeper吗？[免费下载](https://www.beeper.com/download)——这款应用能将你所有的聊天记录整合在一起。  

### 2. 启用Beeper桌面API  

打开Beeper桌面应用 → **设置** → **开发者** → 将“Beeper桌面API”设置为**开启**。  
就这样，你的Clawdbot就可以直接访问你所有的聊天记录了。  

### 3. （可选）添加Beeper访问令牌  

为了实现更流畅的自动化操作，请获取访问令牌：  
1. 进入Beeper桌面 → 设置 → 开发者  
2. 点击“创建访问令牌”  
3. 将令牌添加到`~/.clawdbot/clawdbot.json`文件中：  
**（此处应插入实际的令牌代码）**  

**注意：**`BEEPER_API_URL`的默认值为`http://localhost:23373`——除非你在其他端口上运行Beeper，否则无需更改。  

## 与你的“小龙虾”交流  

设置完成后，只需自然地发出指令：  
> “显示我在Beeper中的未读消息”  
> “在我的Beeper聊天记录中搜索关于晚餐计划的消息”  
> “给John发一条WhatsApp消息，告诉他我正在路上”  
> “查看#general频道的最新消息”  
> “查找Lisa上周发送的所有消息”  
> “对那条消息添加👍的表情符号反应”  
> “将我的Discord聊天记录标记为已读”  

其余操作均由Clawdbot通过Beeper完成。  

## 技术细节  

（适合喜欢深入了解的技术爱好者）  

### Beeper API基础  

基础URL：`http://localhost:23373`（Beeper桌面应用必须处于运行状态）  

### 账户  

#### 查看所有连接的Beeper账户  

查看你在Beeper中连接的所有平台：  
**（此处应插入查询账户的代码）**  

**示例响应：**  
**（此处应插入返回的账户列表）**  

### 聊天记录  

#### 列出所有Beeper聊天记录  

**示例响应：**  
**（此处应插入聊天记录的列表）**  

#### 在Beeper中搜索聊天记录  

**示例响应：**  
**（此处应插入搜索结果的代码）**  

#### 获取聊天详情  

**示例响应：**  
**（此处应插入聊天详情的代码）**  

#### 创建新的Beeper聊天记录  

**示例响应：**  
**（此处应插入创建聊天记录的代码）**  

#### 归档/解压聊天记录  

**示例响应：**  
**（此处应插入归档/解压聊天的代码）**  

### 消息  

#### 查看聊天记录中的所有消息  

**示例响应：**  
**（此处应插入查看消息的代码）**  

#### 在所有Beeper平台中搜索消息  

**示例响应：**  
**（此处应插入搜索消息的代码）**  

#### 通过Beeper发送消息  

**示例响应：**  
**（此处应插入发送消息的代码）**  

#### 回复消息  

**示例响应：**  
**（此处应插入回复消息的代码）**  

#### 将消息标记为已读  

**示例响应：**  
**（此处应插入标记消息为已读的代码）**  

### 表情符号反应  

#### 为消息添加表情符号反应  

**示例代码：**  
**（此处应插入添加表情符号的代码）**  

#### 删除表情符号反应  

**示例代码：**  
**（此处应插入删除表情符号的代码）**  

### 联系人  

#### 在账户中查找联系人  

**示例响应：**  
**（此处应插入查找联系人的代码）**  

### 提醒功能  

#### 为聊天设置提醒  

**示例代码：**  
**（此处应插入设置提醒的代码）**  

#### 删除聊天提醒  

**示例代码：**  
**（此处应插入删除提醒的代码）**  

### 文件下载  

#### 下载聊天中的附件  

**示例代码：**  
**（此处应插入下载附件的代码）**  

## 高级技巧 🦞  

### 获取未读消息摘要  

**示例代码：**  
**（此处应插入获取未读消息摘要的代码）**  

### 在Beeper中查找特定聊天记录  

**示例代码：**  
**（此处应插入查找聊天记录的代码）**  

### 将所有聊天记录标记为已读  

**示例代码：**  
**（此处应插入标记所有聊天记录为已读的代码）**  

### 快速回复最后一条消息  

**示例代码：**  
**（此处应插入快速回复最后一条消息的代码）**  

### 检查Beeper是否已准备好  

**示例代码：**  
**（此处应插入检查Beeper连接状态的代码）**  

### 获取过去24小时的消息  

**示例代码：**  
**（此处应插入获取过去24小时消息的代码）**  

### 按服务过滤聊天记录  

**示例代码：**  
**（此处应插入按服务过滤聊天记录的代码）**  

## 需知事项  

- **Beeper桌面应用必须处于运行状态**——API功能依赖于Beeper桌面应用。  
- **本地化且私密**——Beeper API完全在本地机器上运行，你的消息不会通过外部服务器传输。  
- **请尊重各平台的使用规定**——频繁发送消息可能会导致WhatsApp等平台触发速率限制。  
- **iMessage仅支持macOS系统**。  
- **不同平台的表情符号支持情况不同**——Beeper会自动处理表情符号的显示问题。  

## 故障排除  

### “无法连接到Beeper”  
1. 确保Beeper桌面应用正在运行（可以在菜单栏中查看）。  
2. API是否已启用？进入Beeper → 设置 → 开发者 → Beeper桌面API。  
3. 检查端口：`curl http://localhost:23373/health`  

### “认证失败”  
1. 在Beeper中生成新的访问令牌（进入设置 → 开发者）。  
2. 确保令牌信息正确无误（无多余空格）。  
3. 或者直接删除令牌，Beeper会重新请求OAuth认证。  

### “找不到聊天记录”  
1. 确认聊天记录存在于Beeper应用中。  
2. 尝试使用不同的搜索关键词。  
3. 检查相关账户（WhatsApp、Telegram等）是否已连接到Beeper。  

### “某些表情符号无法使用”  
某些平台对表情符号的支持有限，可以尝试使用更常见的表情符号（如👍 ❤️ 😂 😮 😢 😡）。  

## 链接  

- [下载Beeper](https://www.beeper.com/download)  
- [Beeper开发者文档](https://developers.beeper.com)  
- [Beeper MCP](https://www.beeper.com/mcp)（适用于Claude Desktop和Cursor用户）  
- [Beeper桌面API参考文档](https://developers.beeper.com/desktop-api-reference/)  

## 致谢  

由@nickhamze和Clawdbot社区共同开发。  
技术支持来自[Beeper](https://www.beeper.com)——一个统一管理你所有聊天记录的应用。  

*“Claw Me Maybe”——因为你的“小龙虾”应该能够随时随地联系到你。*