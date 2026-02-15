---
name: chaterimo
description: **适用于 Shopify 和电子商务的 AI 客户服务工具**  
- 查询对话记录  
- 分析聊天机器人的性能  
- 管理您的 Chaterimo AI 助手  

**主要功能：**  
1. **查询对话记录**：您可以轻松查看与客户的全部交互记录，以便更好地了解客户的需求和反馈。  
2. **分析聊天机器人性能**：通过详细的统计数据，您可以评估聊天机器人的工作效率和用户体验。  
3. **管理 Chaterimo AI 助手**：您可以配置和优化您的 AI 助手，以提供更优质的服务。  

**优势：**  
- **高效便捷**：所有功能均通过直观的界面轻松访问和管理。  
- **实时监控**：实时跟踪聊天机器人的运行状态和客户反馈。  
- **数据驱动**：基于大量数据优化聊天机器人的性能。  

**适合人群：**  
- **电子商务商家**：希望提升客户服务质量的企业主。  
- **软件开发人员**：需要集成 AI 助手的开发者。  

**立即尝试！**  
了解更多关于 Chaterimo 的信息，并开始提升您的电子商务体验。
emoji: 🛒
homepage: https://www.chaterimo.com
tags:
  - shopify
  - ecommerce
  - customer-service
  - chatbot
  - ai-assistant
  - conversations
  - analytics
  - support
  - shoptet
  - upgates
metadata:
  clawdis:
    primaryEnv: CHATERIMO_API_KEY
    requires:
      env:
        - CHATERIMO_API_KEY
    config:
      requiredEnv:
        - name: CHATERIMO_API_KEY
          description: Your Chaterimo API key. Generate at https://www.chaterimo.com/account/api-keys/
---

# Chaterimo – 专为 Shopify 和电子商务平台设计的 AI 客户服务

将您的 Chaterimo AI 聊天机器人连接到 OpenClaw，查询客户对话记录，分析聊天机器人的性能，并从您的电子商务店铺的客户服务数据中获取洞察。

## 什么是 Chaterimo？

Chaterimo 是一个基于 AI 的客户服务平台，可与 **Shopify**、**Shoptet**、**Upgates** 和 **eshop-rychle.cz** 等电子商务平台集成。它提供 24/7 的自动化客户支持，支持以下领先的 LLM（大型语言模型）：**ChatGPT**、**Claude**、**Gemini** 和 **Grok**。

您可以使用自己的 API 密钥（BYOK – Bring Your Own Key）来使用 Chaterimo，或者选择包含 AI 信用额度的定制计划。

📖 **了解更多：** [如何将 Chaterimo 与 Shopify 集成](https://www.chaterimo.com/en/blog/shopify-ai-customer-service/)

## 该功能可以做什么？

### 列出您的聊天机器人
> “显示我所有的聊天机器人”

列出为您的店铺配置的所有聊天机器人及其 AI 模型设置和状态。

### 浏览对话记录
> “显示上周的对话记录”
> “列出我店铺的对话记录”

您可以按日期和平台筛选客户服务对话记录。所有客户的个人身份信息（PII）都会被自动删除以保护隐私。

### 阅读对话记录
> “显示第 123 号对话”
> “昨天客户问了什么？”

查看客户与您的 AI 聊天机器人之间的完整对话记录。所有个人身份信息都会被自动隐藏。

## 设置

1. 在 [chaterimo.com](https://www.chaterimo.com) 注册。
2. 将您的电子商务平台（Shopify、Shoptet、Upgates 或 eshop-rychle.cz）连接到 Chaterimo。
3. 进入您的仪表板中的 **API 密钥** 部分。
4. 点击 **创建 API 密钥** 并复制密钥。
5. 设置环境变量：
   ```
   CHATERIMO_API_KEY=cha_your_key_here
   ```

## API 端点

| 端点 | 描述 |
|----------|-------------|
| `GET /api/v1/chatbots/` | 列出所有聊天机器人（返回聊天机器人 ID） |
| `GET /api/v1/chatbots/{chatbot_id}/` | 获取聊天机器人详情 |
| `GET /api/v1/chatbots/{chatbot_id}/conversations/` | 列出对话记录（返回对话 ID） |
| `GET /api/v1/conversations/{conversation_id}/` | 获取完整的对话记录（包含消息） |

您的组织信息会自动从您的 API 密钥中确定，无需手动指定。

## 隐私与数据安全

### 个人身份信息保护

API 返回的所有对话数据中的个人身份信息（PII）都会被自动删除，以保护客户隐私：

| 数据类型 | 示例 | 替换后的显示方式 |
|-----------|---------|-------------|
| 电子邮件地址 | `john@example.com` | `[EMAIL]` |
| 电话号码 | `+1-555-123-4567` | `[PHONE]` |

这样您可以分析对话模式和聊天机器人的性能，而不会暴露敏感的客户数据。

### API 密钥安全

- **哈希存储**：API 密钥以 SHA256 哈希的形式存储——我们从不以明文形式存储原始密钥。
- **一次性显示**：您的完整 API 密钥仅在创建时显示一次——请立即复制。
- **即时撤销**：一旦密钥被泄露，可以立即从仪表板中撤销其权限。
- **权限控制**：密钥的权限是有限的（默认为只读）。

### 基础设施安全

- **请求限制**：每个 API 密钥每分钟仅允许 60 次请求，以防止滥用。
- **审计日志**：所有 API 调用都会记录时间戳、端点和响应代码。
- **租户隔离**：API 密钥只能访问其所属组织的数据。
- **仅使用 HTTPS**：所有 API 流量在传输过程中都会被加密。

## 支持的平台

- **Shopify**：与产品同步的完整集成（[设置指南](https://www.chaterimo.com/en/blog/shopify-ai-customer-service/) |
- **Shoptet**：捷克电子商务平台集成。
- **Upgates**：完整的 API 集成。
- **eshop-rychle.cz**：捷克电子商务平台。

## 支持的 AI 模型

Chaterimo 支持多种 LLM 提供商，您可以通过 BYOK（Bring Your Own Key）或定制计划来使用这些模型。我们会定期更新，以包含每个提供商的最新模型：

- **OpenAI**：ChatGPT（最新的 GPT 模型）
- **Anthropic**：Claude（最新的 Claude 模型）
- **Google**：Geminii（最新的 Gemini 模型）
- **xAI**：Grok（最新的 Grok 模型）

## 即将推出的功能（第二阶段及以后）

- 分析与指标仪表板
- 未回答问题的检测
- 产品搜索
- 知识库管理
- 通过 API 配置聊天机器人

## 支持方式

- 官网：[chaterimo.com](https://www.chaterimo.com)
- Shopify 使用指南：[如何将 Chaterimo 与 Shopify 集成](https://www.chaterimo.com/en/blog/shopify-ai-customer-service/)

## 使用示例

```
User: Show me my chatbots
Assistant: You have 2 chatbots configured:

1. **Main Store Support** (GPT-4)
   - Language: English
   - Status: Active

2. **Czech Support** (Claude)
   - Language: Czech
   - Status: Active

User: Show me recent conversations from Main Store Support
Assistant: Here are the last 5 conversations:

1. Session #abc123 - 12 messages - Feb 4, 2026
2. Session #def456 - 8 messages - Feb 4, 2026
3. Session #ghi789 - 3 messages - Feb 3, 2026
...
```