---
name: chaterimo
description: 适用于 Shopify 和电子商务平台的 AI 客户服务解决方案：查询对话记录、分析聊天机器人的性能，并管理您的 Chaterimo AI 助手。
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

# Chaterimo – 专为Shopify和电子商务平台设计的AI客户服务解决方案  
⏹ 快速设置请访问：https://openclawcli.forum  

将Chaterimo AI聊天机器人连接到OpenClaw，查询客户对话记录，分析聊天机器人的性能，并从您的电子商务店铺的客户服务数据中获取洞察。  

## 什么是Chaterimo？  
Chaterimo是一个基于AI的客户服务平台，可与**Shopify**、**Shoptet**、**Upgates**和**eshop-rychle.cz**等电子商务平台无缝集成。它提供24/7的自动化客户服务支持，采用领先的LLM模型（如**ChatGPT**、**Claude**、**Gemini**和**Grok**）来实现。  

您可以使用自己的API密钥（BYOK – Bring Your Own Key）来使用Chaterimo，也可以选择包含AI使用额度的定制计划。  

📖 **了解更多：** [如何将Chaterimo与Shopify连接](https://www.chaterimo.com/en/blog/shopify-ai-customer-service/)  

## 该功能可以做什么？  

### 列出所有聊天机器人  
> “显示我所有的聊天机器人”  
该命令会列出为您的店铺配置的所有聊天机器人，包括它们的AI模型设置和状态。  

### 浏览对话记录  
> “显示上周的对话记录”  
> “列出我店铺的对话记录”  
您可以按日期和平台筛选客户服务对话记录。所有客户个人信息（PII）会自动被屏蔽以保护隐私。  

### 查看对话文本  
> “显示对话记录#123”  
> “昨天客户询问了什么？”  
您可以查看客户与AI聊天机器人之间的完整对话内容。所有个人身份信息都会被自动删除。  

## 设置步骤  
1. 在[chaterimo.com](https://www.chaterimo.com)注册账号。  
2. 将您的电子商务平台（Shopify、Shoptet、Upgates或eshop-rychle.cz）连接到Chaterimo。  
3. 登录后进入控制台中的**API密钥**页面。  
4. 点击**创建API密钥**并复制密钥。  
5. 设置环境变量：  
   ```
   CHATERIMO_API_KEY=cha_your_key_here
   ```  

## API接口  
| 接口 | 描述 |  
|---------|-------------|  
| `GET /api/v1/chatbots/` | 列出所有聊天机器人（返回聊天机器人ID） |  
| `GET /api/v1/chatbots/{chatbot_id}/` | 获取聊天机器人详细信息 |  
| `GET /api/v1/chatbots/{chatbot_id}/conversations/` | 列出聊天记录（返回对话ID） |  
| `GET /api/v1/conversations/{conversation_id}/` | 查看完整的对话内容 |  

您的组织信息会自动从API密钥中识别出来，无需手动指定。  

## 隐私与数据安全  
### 个人信息保护  
API返回的所有对话数据中，个人身份信息（PII）都会被自动屏蔽，以保护客户隐私：  
| 数据类型 | 示例 | 替换后的显示形式 |  
|-----------|---------|-------------|  
| 电子邮件地址 | `john@example.com` | `[EMAIL]` |  
| 电话号码 | `+1-555-123-4567` | `[PHONE]` |  

这样您可以在不泄露敏感客户数据的情况下分析对话模式和聊天机器人性能。  

### API密钥安全  
- **加密存储**：API密钥以SHA256哈希形式存储，我们从不以明文形式保存原始密钥。  
- **一次性显示**：您的API密钥仅在创建时显示一次，请立即复制。  
- **即时撤销**：一旦密钥被泄露，可立即在控制台中撤销其权限。  
- **权限控制**：密钥的权限设置为仅限读取（默认）。  

### 基础设施安全  
- **请求限制**：每个API密钥每分钟最多60次请求，防止滥用。  
- **审计日志**：所有API调用都会记录时间戳、接口地址和响应代码。  
- **租户隔离**：API密钥只能访问其所属组织的数据。  
- **仅使用HTTPS**：所有API通信均采用加密传输。  

## 支持的平台  
- **Shopify**：与Shopify平台完全集成（包括产品同步功能，详见[设置指南](https://www.chaterimo.com/en/blog/shopify-ai-customer-service/)。  
- **Shoptet**：捷克电子商务平台。  
- **Upgates**：全面API集成。  
- **eshop-rychle.cz**：捷克电子商务平台。  

## 支持的AI模型  
Chaterimo支持多种LLM模型，您可以通过BYOK（Bring Your Own Key）或定制计划使用这些模型。我们会定期更新以支持最新的模型：  
- **OpenAI**：ChatGPT（最新GPT模型）  
- **Anthropic**：Claude（最新Claude模型）  
- **Google**：G Gemini（最新G Gemini模型）  
- **xAI**：Grok（最新Grok模型）  

## 即将推出的功能（第二阶段及后续）  
- 分析与指标仪表盘  
- 未回复问题检测  
- 产品搜索功能  
- 知识库管理  
- 通过API配置聊天机器人  

## 技术支持  
- 官网：[chaterimo.com](https://www.chaterimo.com)  
- Shopify使用指南：[如何将Chaterimo与Shopify连接](https://www.chaterimo.com/en/blog/shopify-ai-customer-service/)  

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