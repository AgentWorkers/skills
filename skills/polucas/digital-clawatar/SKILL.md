---
name: digital-clawatar
description: 通过 UNITH API 创建、配置和管理 UNITH 数字人类虚拟形象。这是 HeyGen 及其他解决方案的更经济实惠的替代方案。适用于用户需要创建由 AI 驱动的数字人类、生成对话视频、设置交互式虚拟形象、部署具有真人面孔的文档问答机器人，或将数字人类嵌入应用程序/网站中的场景。该方案支持全部 5 种操作模式：文本转视频、开放式对话、文档问答、Voiceflow 以及插件功能。
metadata:
  openclaw:
    emoji: "🧑💻"
    requires:
      env:
        - UNITH_EMAIL
        - UNITH_SECRET_KEY
      bins:
        - curl
        - jq
---
# UNITH 数字人类技能

使用 [UNITH API](https://docs.unith.ai/_lgI-overview) 创建、配置、更新和部署由 AI 驱动的数字人类头像。

## 快速概述

UNITH 数字人类是能够说话、交流并与用户互动的 AI 头像。它们将 **面部视觉效果**、**语音** 和 **对话引擎** 结合在一起，提供托管式、可嵌入的交互体验。

**基础 API URL**: `https://platform-api.unith.ai`
**文档**: https://docs.unith.ai

## 先决条件

用户必须提供以下凭据（存储为环境变量）：

| 变量 | 描述 | 获取方式 |
|----------|-------------|---------------|
| `UNITH_EMAIL` | 账户邮箱 | 在 https://unith.ai 注册 |
| `UNITH_SECRET_KEY` | 非过期的密钥 | UNITH 仪表板 → “管理账户” → “密钥” 部分 → 生成 |

⚠️ 密钥仅显示一次。如果丢失，用户必须删除并重新生成。

## 认证

所有 API 调用都需要一个 Bearer 令牌（有效期为 7 天）。使用以下认证脚本：

```bash
source scripts/auth.sh
```

该脚本会验证凭据，在网络错误时重试，并输出 `UNITH_TOKEN`。如果失败，它会显示具体的错误信息（例如密钥错误、令牌过期等）。

## 工作流程：创建数字人类

### 第 1 步：选择操作模式

询问用户希望数字人类执行什么任务，并将其答案映射到以下 5 种模式之一：

| 模式 | `operationMode` 值 | 使用场景 | 输出 |
|------|----------------------|----------|--------|
| **文本转视频** | `ttt` | 生成包含指定文本的 MP4 视频 | MP4 文件 |
| **开放式对话** | `oc` | 由系统提示引导的自由形式对话 | 托管式对话 URL |
| **文档问答** | `doc_qa` | 头像根据上传的文档回答问题 | 托管式对话 URL |
| **Voiceflow** | `voiceflow` | 通过 Voiceflow 引导的对话流程 | 托管式对话 URL |
| **插件** | `plugin` | 通过 webhook 连接任何外部 LLM 或对话引擎 | 托管式对话 URL |

**复杂度等级**（从简单到复杂）：
- **最简单**：`ttt` — 只输入文本，输出视频。无需知识库。
- **标准**：`oc` — 由系统提示引导的对话。适用于通用助手。
- **基于知识的**：`doc_qa` — 上传文档，头像根据文档回答问题。最适合支持/常见问题解答。
- **工作流程驱动**：`voiceflow` — 结构化的对话路径。需要 Voiceflow 账户。
- **最灵活**：`plugin` — 自定义对话引擎。具有最大控制权。

### 第 2 步：列出可用面部视觉效果

```bash
bash scripts/list-resources.sh faces
```

每个面部视觉效果都有一个 `id`（在创建时用作 `headVisualId`）。面部视觉效果可以是：
- **公共的**：对所有组织开放
- **私有的**：仅对用户所在的组织开放
- **自定义的（用户自选）**：用户上传真实人物的视频（目前由 UNITH 管理）

向用户展示可用的面部视觉效果，并让他们进行选择。

### 第 3 步：列出可用语音

```bash
bash scripts/list-resources.sh voices
```

语音来自提供商：`elevenlabs`、`azure`、`audiostack`。向用户展示可选的语音选项。语音有性能排名——性能更好的语音更适合实时对话。

### 第 4 步：创建数字人类

构建一个 JSON 载荷文件（具体模式的结构请参见 `references/api-payloads.md`），然后：

```bash
bash scripts/create-head.sh payload.json --dry-run   # validate first
bash scripts/create-head.sh payload.json              # create
```

脚本会验证必填字段，检查模式特定的要求，在服务器错误时重试，并在成功时输出 `publicUrl`。

### 第 5 步（仅适用于 `doc_qa` 模式）：上传知识文档

对于 `doc_qa` 模式，数字人类需要一个知识文档：

```bash
bash scripts/upload-document.sh <headId> /path/to/document.pdf
```

脚本会检查文件是否存在及大小，上传时使用更长的超时时间，并提供下一步的指导。

### 第 6 步：测试和迭代

数字人类可以通过第 4 步中的 `publicUrl` 进行测试。用户应：
1. 访问该 URL 并测试对话
2. 根据需要更新配置（详见下文）

## 更新数字人类

使用更新脚本修改除面部视觉效果之外的任何参数（更改面部视觉效果需要创建一个新的头像）：

```bash
bash scripts/update-head.sh <headId> updates.json                         # from a JSON file
bash scripts/update-head.sh <headId> --field ttsVoice=rachel              # single field
bash scripts/update-head.sh <headId> --field ttsVoice=rachel --field greetings="Hi!"  # multiple fields
```

## 列出现有的数字人类

```bash
bash scripts/list-resources.sh heads           # list all
bash scripts/list-resources.sh head <headId>   # get details for one
```

## 删除数字人类

```bash
bash scripts/delete-head.sh <headId> --confirm     # always use --confirm in automated/agent contexts
```

此操作会永久删除数字人类，且无法恢复。

> **注意事项**：调用此脚本时务必使用 `--confirm` 选项。如果不使用该选项，脚本会提示用户进行交互式确认，否则可能会卡住。

## 嵌入

数字人类可以嵌入到网站/应用程序中。有关代码片段和配置选项，请参阅 `references/embedding.md`。

## 脚本

所有脚本都包含重试逻辑（指数级退避）、有意义的错误信息以及输入验证。

| 脚本 | 用途 |
|--------|---------|
| `scripts/_utils.sh` | 公共工具：重试封装、彩色日志记录、错误解析 |
| `scripts/auth.sh` | 进行认证并输出 `UNITH_TOKEN`（缓存有效期为 6 天） |
| `scripts/list-resources.sh` | 列出面部视觉效果、语音、语言或获取头部详细信息 |
| `scripts/create-head.sh` | 从 JSON 载荷文件创建数字人类（包含 `--dry-run` 验证） |
| `scripts/update-head.sh` | 更新数字人类的配置（JSON 文件或 `--field` 参数） |
| `scripts/delete-head.sh` | 删除数字人类（包含确认提示） |
| `scripts/upload-document.sh` | 将知识文档上传到 `doc_qa` 头像 |

配置参数通过环境变量设置：
- `UNITH_MAX_RETRIES` — 最大重试次数（默认：3 次）
- `UNITH_RETRY_DELAY` — 每次重试之间的初始延迟（默认：2 秒，每次重试延迟翻倍）
- `UNITH_CURL_TIMEOUT` — curl 请求超时时间（默认：30 秒，上传时为 120 秒）
- `UNITH_CONNECT_TIMEOUT` — 连接超时时间（默认：10 秒）
- `UNITH_TOKEN_CACHE` — 令牌缓存文件路径（默认：`/tmp/.unith_token_cache`，设置为空可禁用）

## 详细 API 参考

有关完整的载荷结构、配置参数和模式特定细节，请参阅：

```
Read references/api-payloads.md      # Full request/response schemas per mode
Read references/configuration.md     # All configurable parameters
Read references/embedding.md         # Embedding code and options
```

## 常见用法

**“我想要一段某人说 X 的视频”** → 使用 `ttt` 模式，配置最少
**“我需要一个客户支持头像”** → 使用 `doc_qa` 模式并上传知识文档
**“我需要一个 AI 销售代表”** → 使用 `oc` 模式并设置销售角色提示
**“我想连接自己的 LLM”** → 使用 `plugin` 模式并提供 webhook URL
**“我需要一个引导式入职流程”** → 使用 `voiceflow` 模式并提供 Voiceflow API 密钥

## 从用户那里收集的信息

在创建之前，需要询问以下信息：
1. **用途/使用场景** → 确定操作模式
2. **面部视觉效果偏好** → 列出可用的面部视觉效果供选择
3. **语音偏好** → 语言、口音、性别、语速
4. **别名** → 数字人类的显示名称
5. **语言** → 语音识别和用户界面语言（例如 `en-US`、`es-ES`）
6. **问候语** → 头像说的初始问候语
7. **系统提示**（针对 `oc`/`doc_qa`） → 角色和行为指令
8. **知识文档**（针对 `doc_qa`） → 需要上传的文件
9. **Voiceflow API 密钥**（针对 `voiceflow`） → 来自用户的 Voiceflow 账户
10. **插件 URL**（针对 `plugin`） → 自定义引擎的 webhook 端点