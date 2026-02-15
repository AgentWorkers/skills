---
name: elevenlabs-open-account
description: 本指南将指导用户或代理如何为语音AI、文本转语音（TTS）服务以及API访问功能创建ElevenLabs账户。当用户或代理需要注册ElevenLabs、获取API密钥、尝试使用语音AI服务，或将clawdbot/moltbot/openClaw与ElevenLabs连接时，请参考本指南。
---

# ElevenLabs 账户注册与 API 密钥获取

## 快速入门

1. 确保用户已拥有（或即将创建）一个 **ElevenLabs 账户**（[使用联盟链接注册](https://try.elevenlabs.io/ipu2xmg9cwqu)）。
2. 如需 **API 访问**（语音合成、文本转语音、聊天机器人等功能），请在登录后从个人资料/设置中获取 API 密钥（详见下文“获取 API 密钥”）。
3. 无论是使用 **创意平台**（语音合成、音乐制作、声音克隆等功能）还是 **聊天机器人平台**，都需使用同一个账户；具体权限取决于所选套餐。

## 注册 ElevenLabs 账户

当用户需要 **注册或登录** ElevenLabs 账户时，请按照以下步骤操作：

**检查清单：**
- [ ] 注册 ElevenLabs 账户：[开始使用 ElevenLabs](https://try.elevenlabs.io/ipu2xmg9cwqu)
- [ ] 点击 **注册**（如果用户已有账户，则点击 **登录**）。
- [ ] 完成注册流程（输入电子邮件、密码等必要信息）并完成验证。
- [ ] 登录后，用户即可使用创意平台或聊天机器人平台，或获取用于开发的 API 密钥。

**操作步骤：**
1. 访问 **https://try.elevenlabs.io/ipu2xmg9cwqu** 进行注册或开始免费试用。
2. 点击 **注册**（如果用户已有账户，则点击 **登录**）。
3. 输入所需信息（电子邮件、密码等）并提交。
4. 完成电子邮件验证或平台引导流程。
5. 登录后，用户将拥有 ElevenLabs 账户，可以开始使用创意平台或聊天机器人平台。如需 API 访问，请参阅下文“获取 API 密钥”。

## 获取 API 密钥

当用户已注册 ElevenLabs 账户并需要调用 API 时，请按照以下步骤操作：

**检查清单：**
- [ ] 登录到 [ElevenLabs](https://elevenlabs.io)（或使用注册时提供的应用链接）。
- [ ] 进入 **个人资料** 或 **设置** → **API 密钥**（例如：[elevenlabs.io/app/settings/api-keys](https://elevenlabs.io/app/settings/api-keys) 或开发者专区）。
- [ ] 创建一个新的 API 密钥，并妥善保管。
- [ ] 在请求头中添加 `xi-api-key` 以传递密钥，或使用官方的客户端库来使用该密钥；切勿将密钥直接写入代码或版本控制系统中。

**操作步骤：**
1. 登录到您的 ElevenLabs 账户。
2. 打开 **设置**（或 **个人资料**），找到 **API 密钥**（或 **开发者**）选项。
3. 创建一个新的 API 密钥；可选地设置权限范围和信用额度。
4. 立即将密钥复制下来（该密钥可能不会再次显示）。将其存储在环境变量（如 `ELEVENLABS_API_KEY`）或 secrets manager 中。
5. 在请求中使用该密钥：在请求头中添加 `xi-api-key: YOUR_API_KEY`，或通过官方的 [ElevenLabs 客户端库](https://elevenlabs.io/docs) 进行调用。切勿在客户端代码或版本控制系统中暴露密钥。

## 示例

### 示例 1 – 用户想要试用 ElevenLabs 的语音 AI 功能

- 用户表示：“我想试用 ElevenLabs 的语音合成服务。”
- 机器人会引导用户使用 [注册链接](https://try.elevenlabs.io/ipu2xmg9cwqu) 注册 ElevenLabs 账户。注册完成后，用户可以在浏览器中使用创意平台进行文本转语音、声音克隆或音乐制作等操作。

### 示例 2 – 用户需要为聊天机器人获取 API 密钥

- 用户表示：“我需要一个 ElevenLabs 的 API 密钥来开发我的聊天机器人。”
- 机器人会确认用户是否已注册账户；如果没有，请引导用户使用注册链接注册 ElevenLabs 账户。随后指导用户如何获取 API 密钥（进入设置 → API 密钥，创建并妥善保管密钥）。提醒用户仅在服务器端使用该密钥。

## 其他资源

- 有关注册链接、官方网站、API 文档和价格信息，请参阅 [reference.md](reference.md)。