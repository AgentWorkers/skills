---
name: outlook-hack
version: 2.6.0
description: "你的代理程序整天都在读取Outlook中的邮件，并为你草拟回复内容，但却一个都不会发送出去。即使你礼貌地请求它发送，它也不会这么做。"
metadata:
  {
    "openclaw":
      {
        "emoji": "📧",
        "os": ["linux", "darwin"],
        "requires":
          {
            "capabilities": ["browser"],
          },
        "notes":
          {
            "security": "This skill captures Outlook Web session tokens via browser tab sharing to make direct REST calls to Microsoft's internal APIs. No API keys or admin approval needed. SENDING IS CODE-DISABLED: the skill physically cannot send, reply, or forward emails. It reads, searches, and creates drafts only. Drafts land in the user's Drafts folder for manual review and sending. No credentials are stored beyond the session token lifetime (8-24 hours).",
          },
      },
  }
---
# Outlook 小工具

**你的 AI 功能不会在凌晨 3 点给 CEO 发送邮件。**

这并不是因为有什么设置或政策限制，而是因为代码本身根本无法发送邮件。我们像从小孩手中拿走电锯一样彻底移除了这个功能——没有任何商量余地。

**它的功能：**  
- 阅读邮件、搜索邮件内容，并生成回复草稿；这些草稿会保存在你的“草稿”文件夹中。你需要自行审核并决定是否发送。AI 本身永远不会发送邮件。

**它不会做什么：**  
- 不会向 IT 部门请求 API 访问权限；  
- 不需要管理员来启用 IMAP 功能；  
- 不会像某些浏览器扩展程序那样在 20 分钟后自动关闭；  
- 绝不会代表你发送、转发或回复邮件；  
- 也不会让你向合规部门解释为什么你的收件箱里会有 AI 生成的邮件。

**工作原理：**  
只需打开一次 Outlook Web 页面，OpenClaw 会从你的浏览器会话中获取认证令牌。完成一次身份验证后，它就可以全天候自动读取邮件内容，无需任何额外的 IT 支持或额外的扩展程序（如 OAuth 与 Azure AD 的交互）。  
无论令牌何时更新、会话何时过期，或者微软在周二下午 2 点决定更换 Cookie，我们都能确保系统正常运行——因为我们非常注重系统的稳定性。

**最让人担心的事情：**  
你的安全团队最害怕的就是“如果它不小心发送了邮件怎么办？”但实际上这个功能根本无法发送邮件。它只会生成草稿，是否发送由你决定。

## 主要功能：  
- 📧 阅读并搜索所有文件夹中的邮件  
- 📅 查看日历事件  
- 👥 浏览联系人信息  
- ✏️ 创建邮件草稿（草稿会保存在“草稿”文件夹中，永远不会自动发送）

## 技术原理：  
1. 通过“浏览器中继”（Browser Relay）将 Outlook Web 页面的信息共享给 OpenClaw；  
2. OpenClaw 获取你的认证会话令牌；  
3. 之后它就可以直接调用微软内部的 Outlook API 进行操作；  
4. 该功能会自动运行，直到会话自然过期（通常为 8 至 24 小时）；  
5. 第二天只需再次共享 Outlook Web 页面即可重新开始使用。  

**注意：**  
这个工具并不会抓取页面内容，而是直接使用 Outlook 自带的内部 API 进行操作，并通过你的浏览器会话进行身份验证。

## 完整技术栈：  
该工具可与 [**whatsapp-ultimate**](https://clawhub.com/globalcaos/whatsapp-ultimate) 结合使用以实现消息传递功能，也可与 [**jarvis-voice**](https://clawhub.com/globalcaos/jarvis-voice) 结合使用以实现语音交互。这是整个认知系统（包含 13 个工具）的一部分。  

👉 **[克隆它、修改它、甚至根据你的需求进行定制吧！](https://github.com/globalcaos/clawdbot-moltbot-openclaw)**