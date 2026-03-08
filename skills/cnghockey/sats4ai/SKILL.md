---
name: sats4ai
description: 这是一个基于比特币技术的AI工具市场，通过MCP平台提供多种服务：生成图像（Flux、Seedream、Recraft）、文本（Kimi K2.5、DeepSeek、GPT-OSS）、视频（Kling V3）、音乐、语音、3D模型、视觉分析、文件转换以及短信等功能。所有服务均按使用次数计费，支持使用比特币Lightning进行微支付。无需API密钥或注册账号，也不需要信用卡。当你需要AI生成工具并且希望使用Lightning微支付时，就可以使用该平台。该平台兼容任何Lightning钱包。
homepage: https://sats4ai.com/openclaw
metadata:
  openclaw:
    emoji: "⚡"
    requires:
      bins: []
---
# Sats4AI — 由比特币驱动的AI工具

Sats4AI是一个MCP服务器，允许您使用比特币Lightning支付来使用10多种AI工具。无需API密钥或注册，仅通过Lightning支付进行身份验证。

## 设置

将Sats4AI MCP服务器添加到您的`openclaw.json`文件中：

```json
{
  "mcpServers": {
    "sats4ai": {
      "url": "https://sats4ai.com/api/mcp"
    }
  }
}
```

完成以上设置后，您就可以使用所有提供的工具了。

## 需要一个Lightning钱包

为了支付费用，请在Sats4AI之外再添加一个用于存储Lightning钱包的MCP服务器。以下是两种常见的设置方式：

**选项A：Lightning Wallet MCP**（推荐）  
```bash
npm install -g lightning-wallet-mcp
lw register --name "my-agent"   # 保存API密钥
lw deposit 10000                # 为钱包充值
```

**选项B：Alby MCP Server**  
```json
{
  "mcpServers": {
    "sats4ai": {
      "url": "https://sats4ai.com/api/mcp"
    },
    "wallet": {
      "command": "npx",
      "args": ["-y", "@getalby/mcp"],
      "env": {
        "NWC_CONNECTION_STRING": "nostr+walletconnect://YOUR_CONNECTION_STRING"
      }
    }
  }
}
```

请从[Alby Hub](https://getalby.com/ai)获取您的NWC连接字符串。

## 可用工具

连接成功后，您可以调用以下工具：

### 支付流程  
1. **create_payment**：为任何服务生成Lightning发票，指定所需的工具和模型。  
2. **Pay the invoice**：使用您的Lightning钱包（Lightning Wallet MCP、Alby或其他Lightning钱包）支付发票。  
3. **Call the tool**：传递`paymentId`以执行相应的服务。

### AI工具  

| 工具 | 功能 | 费用（Sats） |
|------|-------------|-------------|
| **generate_image** | 将文本转换为图像（Flux、Seedream、Recraft） | 100-200 |
| **generate_text** | 与Kimi K2.5、DeepSeek、GPT-OSS进行文本交流 | 5-15+ |
| **generate_video** | 将文本/图像转换为视频（Kling V3） | 2,500 |
| **generate_music** | 使用AI创作带人声的歌曲（MiniMax） | 200 |
| **generate_speech** | 将文本转换为语音（MiniMax语音） | 300 |
| **transcribe_speech** | 将音频转换为文本（Whisper） | 10 |
| **generate_3d_model** | 将图像转换为3D模型（Hunyuan 3D） | 350 |
| **analyze_image** | 图像分析（Qwen-VL） | 21 |
| **convert_file** | 在200多种文件格式之间进行转换 | 50 |
| **send_sms** | 向任何国家发送短信 | 根据费用而定 |

### 示例：生成图像  
1. 调用`create_payment`，选择工具“image”，模型“Best”。  
2. 使用生成的Lightning发票进行支付。  
3. 调用`generate_image`，传入`paymentId`和提示内容“a sunset over mountains”，模型“Best”。  
4. 接收Base64格式的图像数据。

### 示例：使用Kimi K2.5生成文本  
1. 调用`create_payment`，选择工具“text-generation”，模型“Best”。  
2. 支付至少15个Sats的费用。  
3. 调用`generate_text`，传入支付ID和您的文本内容。  
4. 接收生成的文本结果。

Kimi K2.5在编程、数学和推理能力方面可与Claude 4.6和GPT-5.2相媲美，每次请求的费用约为0.006美元。

## 通过L402接口使用Sats4AI  

您也可以通过L402接口使用Sats4AI：  
```bash
lnget --max-cost 500 POST https://sats4ai.com/api/l402/image \
  -d '{"input":{"prompt":"a sunset over mountains"},"model":"Best"}'
```

无需额外的MCP服务器设置，`lnget`会自动在收到402个响应后支付相应的Lightning费用。

## 隐私政策  
- 无需注册、无需账户、无需电子邮件地址。  
- 无需API密钥，支付即作为身份验证方式。  
- 不需要进行KYC（了解客户）或身份验证。  
- 服务过程中的提示内容和输出结果不会被记录。

## 链接  
- 官网：https://sats4ai.com  
- OpenClaw使用指南：https://sats4ai.com/openclaw  
- MCP文档：https://sats4ai.com/mcp  
- L402文档：https://sats4ai.com/l402  
- 服务发现：https://sats4ai.com/.well-known/l402-services