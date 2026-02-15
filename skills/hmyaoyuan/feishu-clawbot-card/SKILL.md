# Feishu ClawBot Card (FCC)

**Feishu 上的 AI 代理的通用名片协议。**

此技能允许 OpenClaw 机器人创建、交换和存储标准化的身份卡片（“ClawCards”）。它就像一个名片册，帮助您的 AI 记住每个用户的身份。

## 📦 安装

```bash
openclaw install HMyaoyuan/feishu-clawbot-card
```

## 🚀 使用指南

### 1. 🆔 创建您的名片（定义身份）
首先，定义您的身份。运行此命令一次，以便在本地注册表中注册您的信息。

```bash
node skills/feishu-clawbot-card/index.js mint '{
  "display_name": "MyBotName",
  "feishu_id": "cli_a...", 
  "avatar": { "url": "https://..." },
  "bio": {
    "species": "Robot",
    "mbti": "INTJ",
    "desc": "I am a helpful coding assistant."
  },
  "capabilities": ["coding", "search"]
}'
```
*注意：`feishu_id` 应为您的应用程序 ID（`cli_...`）或用户 Open ID（`ou_...`）。*

### 2. 📤 共享您的名片（导出）
生成一个可共享的 JSON 代码块，以便发送给其他机器人或人类。

```bash
# Get the JSON for a specific bot (by name or ID)
node skills/feishu-clawbot-card/index.js export "MyBotName"
```
**输出：** 一个 JSON 代码块。复制该代码并通过聊天发送给他人！

### 3. 📥 保存朋友的名片（导入）
当有人根据 FCC v1 协议向您发送他们的名片 JSON 时，将其保存到您的注册表中。

```bash
# Paste the received JSON string
node skills/feishu-clawbot-card/index.js import '{"protocol":"fcc-v1", ...}'
```

### 4. 📇 查看注册表（列表）
查看您认识的所有机器人。

```bash
node skills/feishu-clawbot-card/index.js list
```

### 5. 🎨 显示名片（渲染）
生成一个精美的 Feishu 富文本（Post）JSON，以便在聊天中显示名片。

```bash
node skills/feishu-clawbot-card/index.js render "MyBotName"
```

## 📜 协议规范（FCC v1）

有效的名片必须遵循以下 JSON 结构：

```json
{
  "protocol": "fcc-v1",
  "id": "uuid...",
  "display_name": "Name",
  "feishu_id": "cli_... or ou_...",
  "avatar": { "url": "https://..." },
  "bio": {
    "species": "...",
    "mbti": "...",
    "desc": "..."
  },
  "capabilities": ["tag1", "tag2"]
}
```