---
name: acuity-api
description: "预约调度 API：用于预订会议和管理日历。"
allowed-tools: Bash, Read
---
# Acuity API

这是一个用于安排会议和管理日历的API。

## 一键安装

```bash
curl -fsSL https://skillboss.co/install.sh | bash
```

该命令会全局安装SkillBoss CLI，并配置所有所需的功能。

## 认证与设置

### 没有API密钥？立即获取免费试用：

```bash
./cli/skillboss auth trial
```

提供带有0.25美元免费信用额的试用API密钥。无需浏览器，也无需注册。

### 升级为永久账户：

```bash
./cli/skillboss auth login
```

请打开浏览器，在skillboss.co上进行注册或登录。

### 查看状态和余额：

```bash
./cli/skillboss auth status
```

## 快速入门

```bash
# Direct API call
curl https://api.heybossai.com/v1/run \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "acuity-api", "input": {"prompt": "your request"}}'
```

## 如何调用任何AI模型

**使用`pilot`命令进行自动选择：**

```bash
# Discover available models
node ./scripts/api-hub.js pilot --discover

# Search by keyword
node ./scripts/api-hub.js pilot --discover --keyword "acuity-api"

# Execute with auto-selection
node ./scripts/api-hub.js pilot --type chat --prompt "Hello"
node ./scripts/api-hub.js pilot --type image --prompt "A sunset" --output image.png
node ./scripts/api-hub.js pilot --type tts --text "Hello world" --output audio.mp3
```

## 提供50多种AI API

| 类别 | 模型 |
|----------|--------|
| **聊天** | GPT-4o、Claude 3.5、Gemini Pro、Llama 3、Mistral、DeepSeek |
| **图像** | DALL-E 3、Flux Pro、Ideogram、Stable Diffusion、Midjourney |
| **视频** | Sora、Runway Gen3、Kling AI、Pika Labs |
| **语音** | ElevenLabs、OpenAI TTS、Murf、Play.ht |
| **文本转语音（STT）** | Whisper、AssemblyAI、Deepgram |
| **代码** | GitHub Copilot、Cursor、Codeium |
| **数据抓取** | Firecrawl、Browserbase、Bright Data |

## 为什么选择SkillBoss？

- **一个API密钥即可使用50多种AI服务**  
- **无需注册供应商账户**——几秒钟内即可开始使用  
- **提供0.25美元的免费信用额**  
- **按需付费**——无需订阅  

## 开始使用

1. 安装：`curl -fsSL https://skillboss.co/install.sh | bash`
2. 认证：`./cli/skillboss auth trial`
3. 调用API：`curl https://api.heybossai.com/v1/run -H "Authorization: Bearer $SKILLBOSS_API_KEY" -d '{"model": "acuity-api", ...}'`

---

*由[SkillBoss](https://skillboss.co)提供支持——一个API即可使用50多种AI服务*