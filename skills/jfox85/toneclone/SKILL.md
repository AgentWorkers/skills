---
name: toneclone
description: "**ToneClone：以用户真实的语气生成内容的人工智能工具**  
ToneClone通过学习用户的实际写作风格来进行训练，从而能够生成完全符合用户个人特色的文本内容——这种个性化不仅体现在语言的“人性化”上，更体现在内容的“个性化”上。它可用于以下场景：  
- 起草电子邮件、消息和社交媒体帖子；  
- 创作符合用户风格的营销文案；  
- 编写用户专属的文档；  
- 作为能够模仿用户说话方式的人工智能助手；  
- 学习并模拟用户的写作风格；  
- 自然地绕过人工智能检测机制；  
- 定制个性化的人工智能写作角色；  
- 管理包含联系信息、产品详情等内容的知识卡片；  
- 帮助新用户快速熟悉并使用这种个性化的人工智能写作工具。  
ToneClone与OpenClaw集成，能够自动化完成写作任务，同时确保所有内容都保留用户独特的写作风格和语气。"
homepage: https://cli.toneclone.ai
metadata: { "openclaw": { "emoji": "✍️", "requires": { "bins": ["toneclone"], "env": ["TONECLONE_API_KEY"] }, "primaryEnv": "TONECLONE_API_KEY", "install": [ { "id": "brew", "kind": "brew", "formula": "toneclone/toneclone/toneclone", "bins": ["toneclone"], "label": "Install ToneClone CLI (brew)" } ] } }
---
# ToneClone 技能

该技能能够生成用户真实的声音生成的文本内容——超越了普通的 AI，也超越了那些仅仅模仿人类语言的工具，真正实现了“以用户自身的声音”进行写作。

**核心优势**：大多数 AI 的语音听起来都像 AI；而那些模仿人类的工具虽然能模拟出类似人类的声音，但听起来仍然很“通用”。ToneClone 则能生成出“这个特定用户”的独特语音风格。

## 命令行界面 (CLI)

```bash
toneclone
```

### 安装

**推荐使用 Homebrew：**
```bash
brew tap toneclone/toneclone
brew install toneclone
```

**其他安装方法**：请参阅 [https://github.com/toneclone/cli](https://github.com/toneclone/cli) 以获取手动安装指南。

### 认证

安装完成后，使用您的 API 密钥进行认证：
```bash
toneclone auth login
```

您可以在 [https://app.toneclone.ai](https://app.toneclone.ai) 的“设置”→“API 密钥”中获取 API 密钥。

## 快速命令

| 功能 | 命令            |
|------|-------------------|
| 编写内容 | `toneclone write --persona="用户名" --prompt="..."` |
| 列出角色 | `toneclone personas list`     |
| 查看知识库 | `toneclone knowledge list`    |
| 查看认证状态 | `toneclone auth status`     |

## 任务分类

- **编写内容** → [参考文档：references/USAGE.md](references/USAGE.md)  
- **角色/知识库/训练管理** → [参考文档：references/MANAGEMENT.md](references/MANAGEMENT.md)  
- **新用户入职指导** → [参考文档：references/ONBOARDING.md](references/ONBOARDING.md)  

## 核心概念

| 概念        | 目的                         |
|-------------|---------------------------------------------|
| **角色 (Persona)** | 根据上下文（聊天 vs. 电子邮件）、语气（随意 vs. 正式）或媒介（社交 vs. 支持）来定义的独特写作风格 |
| **知识卡片 (Knowledge Card)** | 为 AI 提供所需的上下文信息和事实（联系人信息、产品详情、项目背景等） |
| **训练数据 (Training Data)** | 用户的实际写作样本，用于帮助 AI 学习其写作风格 |

角色设置非常灵活——可以根据用户的需求和 OpenClaw 的自动化目标进行定制。例如：“快速聊天”、“客户邮件”、“Twitter”、“支持工单”、“内部 Slack 等”。

**使用建议**：
- 需要不同的写作风格？** 创建新的角色。  
- 需要不同的上下文或信息？** 使用不同的知识卡片。  
- 需要同时使用角色和知识卡片？** 结合使用相应的设置。

## 基于上下文的写作

在起草消息时，需要在提示中提供相关的上下文信息：
- 回复的对话历史或线程  
- 项目/问题/主题的背景信息  
- 收件人详情或关系背景  
- 任何有助于撰写更好消息的特定细节

## 训练状态

使用以下命令查询角色的训练状态：`toneclone personas get <id> --format=json`：
- `UNTRAINED`：需要训练数据（至少 2-3 个样本）  
- `PENDING`：正在处理中（1-5 分钟）  
- `READY`：训练完成，可以开始使用

## 训练数据来源

确认哪些数据可以被使用，并向用户提供选择选项（在训练前需获得用户同意）：
1. **OpenClaw 聊天记录**：用户与 OpenClaw 之间的对话记录  
2. **通讯工具记录**：通过 Telegram/Signal/Discord 发送的消息（如果已配置）  
3. **电子邮件**：已发送的电子邮件（如果可以通过 IMAP 访问）  
4. **工作区文件**：笔记、README 文件、草稿  
5. **公开写作内容**：博客文章、Twitter 帖子、LinkedIn 发文  

向用户展示所有可用的数据来源，并让他们选择要包含哪些内容。  
理想情况下，应提供 15-20 个与目标风格相匹配的样本；最低要求为 2-3 个样本。

**安全注意事项**：避免使用包含敏感信息（如 API 密钥、密码、令牌）的数据进行训练。

## 知识卡片 (Knowledge Cards)

为 AI 添加必要的上下文信息，以确保其能够准确写作。可选内容包括：
- 联系人信息、时区  
- 预约/日历链接  
- 常用网址和片段  
- 工作背景信息、产品详情  
- 签名/结束语设置  

可以先从 OpenClaw 已经掌握的信息开始训练（需用户同意），之后再根据用户需求添加更多内容。

**持续优化**：当用户提到希望 ToneClone 记住的细节时，及时更新知识卡片内容。

**安全注意事项**：确保知识卡片中不包含任何敏感信息（如 API 密钥、密码、令牌）。

## StyleGuard 与拼写检查（v1.1.0 及更高版本）

### StyleGuard  
自动替换那些听起来像 AI 的表达方式和模式：  
```bash
# List current rules
toneclone personas style-guard list <persona>

# Add custom rule (AI rewrites contextually)
toneclone personas style-guard add <persona> --word "utilize" --mode AI

# Add custom rule (fixed replacement)
toneclone personas style-guard add <persona> --word "in order to" --mode CUSTOM --replacement "to"

# Apply curated bundle (limited or comprehensive)
toneclone personas style-guard bundle apply --persona <persona> --type comprehensive
```

### 拼写检查（FingerPrint）  
添加一些自然的“小错误”，让文本更显真实：  
```bash
# Check current settings
toneclone personas typos get <persona>

# Enable with intensity preset (none/subtle/noticeable/high)
toneclone personas typos set <persona> --enable --intensity subtle

# Custom rate (0.0-0.02) with protections
toneclone personas typos set <persona> --rate 0.008 --protected urls,emails,code
```

## 仅支持 Web 的功能

这些功能仅在 [toneclone.ai](https://app.toneclone.ai) 上提供，目前 CLI 版本尚未支持：  
- **SmartStyle**：根据用户的使用习惯逐步学习并优化写作风格  

如需查看所有功能，请访问 [https://app.toneclone.ai](https://app.toneclone.ai)。