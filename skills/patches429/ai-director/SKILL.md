---
name: ai-director
description: AI短剧生成工具——包括账户管理、剧本编写和视频制作功能。支持X2C（Customer-to-Customer）计费模式，适用于商业部署。
metadata:
  {
    "openclaw":
      {
        "emoji": "🎬",
        "requires": { "bins": ["node"], "env": ["X2C_API_KEY"] },
        "primaryEnv": "X2C_API_KEY",
      },
  }
---
# AI Director - 人工智能短剧生成工具

这是一个完整的AI短剧生成解决方案，从概念到成品电影，集成了X2C平台的账户管理和计费功能。

## 多用户支持

每位用户都有独立的X2C账户凭证，存储在`credentials/{USER_ID}.json`文件中。

在调用脚本时，请设置`USER_ID`或`TELEGRAM_USER_ID`环境变量：

```bash
USER_ID=12345 node {baseDir}/scripts/ad-account-manager.js check-binding
```

OpenClaw会自动从聊天上下文中获取用户ID。

## 模块

### 1. 广告账户管理

负责绑定和验证X2C平台的账户。

```bash
# Send verification code
node {baseDir}/scripts/ad-account-manager.js send-code user@example.com

# Verify and get API Key
node {baseDir}/scripts/ad-account-manager.js verify user@example.com 123456

# Check binding status
node {baseDir}/scripts/ad-account-manager.js check-binding

# View config options
node {baseDir}/scripts/ad-account-manager.js config

# Unbind account
node {baseDir}/scripts/ad-account-manager.js unbind

# Direct bind with existing key
node {baseDir}/scripts/ad-account-manager.js bind --key "x2c_sk_xxx"
```

### 2. 广告角色管理

用于管理视频制作中的自定义角色。每位用户最多可以创建5个角色。

```bash
node {baseDir}/scripts/ad-character-manager.js list
node {baseDir}/scripts/ad-character-manager.js create <name> <gender> <image_url>
node {baseDir}/scripts/ad-character-manager.js delete <character_id>
```

| 参数          | 是否必填 | 选项                |
| -------------- | -------- | ------------------ |
| name         | 是       | 显示名称             |
| gender        | 是       | 男、女、其他             |
| image_url     | 是       | 公开URL（最大10MB）         |

### 3. 广告编剧（提示工程）

脚本编写工具会读取`references/AD-WRITER-GUIDE.md`文件，并根据用户的创意概念生成完整的剧本。输出内容包括：标题、剧情概要、角色简介、剧集大纲以及完整的剧本内容。

### 4. 广告制片（视频制作）

```bash
# View pricing and config
node {baseDir}/scripts/ad-producer.js config

# Generate script
node {baseDir}/scripts/ad-producer.js generate-script "your concept" --wait

# Check script status
node {baseDir}/scripts/ad-producer.js script-status <project_id>

# Produce video
node {baseDir}/scripts/ad-producer.js produce-video <project_id> 1 --wait

# Check video progress
node {baseDir}/scripts/ad-producer.js video-status <project_id> 1

# Full workflow (recommended)
node {baseDir}/scripts/ad-producer.js full-workflow "your concept" --duration 120
```

### 生成选项

| 参数                | 描述                          | 默认值                |
| ------------------ | -------------------------------- | ------------------- |
| --mode           | short_video / short_drama          | short_video           |
| --duration       | 60秒 / 120秒 / 180秒 / 300秒         | 120秒               |
| --ratio          | 9:16 / 16:9                        | 9:16                |
| --style           | 视频风格名称                    | -                    |
| --episodes        | short_video: 1集 / short_drama: 10集       | -                    |
| --language        | 中文 / 英文                        | 中文                 |
| --character-ids     | 角色UUID（用逗号分隔）                | -                    |
| --wait           | 是否等待生成完成                    | false                |

### 成本

| 项目                | 所需信用点数 | 价格（美元）            |
| ------------------ | ---------------------- | --------------------- |
| 脚本（短视频）         | 6                | 0.06美元             |
| 脚本（短剧）         | 60                | 0.60美元             |
| 60秒视频           | 299                | 2.99美元             |
| 120秒视频           | 599                | 5.99美元             |
| 180秒视频           | 799                | 7.99美元             |
| 300秒视频           | 999                | 9.99美元             |

## 质量评估

使用Gemini工具根据预设标准对视频质量进行评分。

```bash
node {baseDir}/scripts/quality-evaluator.js <video_url> --prompt "original prompt"
node {baseDir}/scripts/quality-evaluator.js <video_url> --json
```

需要设置`GEMINI_API_KEY`环境变量，或在配置文件中指定`geminiApiKey`。

## 自动迭代

系统会自动评估、优化脚本并重新生成，直到达到质量要求。

```bash
node {baseDir}/scripts/auto-iterate.js "your concept" \
  --duration 60 --style "style" --threshold 80 --max-iterations 5
```

## 重要规则

- 在生成视频前必须与用户确认所有参数。
- 仅使用配置文件中的预设值（如视频风格、类别等），禁止使用自定义值。
- 每个剧集的集数是固定的：短视频1集，短剧10集。
- 失败的生成尝试不会自动重试（否则会消耗信用点数）。
- 使用异步任务处理机制，避免因等待生成而阻塞程序。
- 输出的视频URL应完整无删减。
- 从视频URL中删除`&response-content-disposition=attachment`字段，以便在浏览器中正常播放。

## API参考

请参阅`references/X2C-OPEN-API.md`以获取完整的API文档。

## 账户凭证

用户凭证存储在`credentials/{USER_ID}.json`文件中：

```json
{
  "x2cApiKey": "x2c_sk_xxx",
  "x2cEmail": "your@email.com",
  "x2cUserId": "user-uuid"
}
```

或者，您也可以通过设置`X2C_API_KEY`环境变量，或在`~/.openclaw/openclaw.json`文件中的`skills."ai-director".env.X2C_API_KEY`进行配置。