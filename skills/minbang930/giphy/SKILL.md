---
name: giphy-gif
description: 在 Discord 中搜索并发送与上下文相关的 Giphy GIF 图片。当用户请求 GIF 图片，或者当需要一个简短的视觉反应（如庆祝、幽默或表达情感）来提升对话氛围时，可以使用此功能。
---

# Giphy GIF搜索

从Giphy上查找相关的GIF，并将其自然地发送到Discord中。

## 行为规则

- 仅在用户明确请求时发送GIF。
- 在适合发送GIF的情境下（如庆祝、分享幽默内容或表达强烈情绪时），也可以主动发送GIF（无需用户请求）。
- 主动发送GIF的频率要适中（每个情境最多发送一个GIF，避免连续发送多个GIF）。
- 在严肃或信息量较大的对话中，优先使用纯文本。
- 确保搜索结果适合工作场合使用（`rating=g`）。

## API密钥（设置简单）

该技能仅需要一个变量：`GIPHY_API_KEY`。

### 选项A：临时使用（当前shell会话）

```bash
export GIPHY_API_KEY="your-api-key"
```

### 选项B：为OpenClaw永久设置（推荐）

将API密钥添加到`~/.openclaw/.env`文件中：

```bash
GIPHY_API_KEY=your-api-key
```

然后重启OpenClaw，以便环境变量生效。

### 验证

- 如果`GIPHY_API_KEY`存在，该技能即可正常使用。
- 如果缺失，请让用户设置API密钥后再尝试。

## 工作流程

1. 根据用户的意图构建Giphy搜索API请求的URL。
2. 对查询文本进行URL编码。
3. 向Giphy发送请求以获取结果。
4. 从`data[0].url`中提取第一个GIF的URL。
5. 将该URL发送到Discord。

## API请求模板

使用以下请求格式：

`https://api.giphy.com/v1/gifs/search?api_key=<KEY>&q=<ENCODED_QUERY>&limit=1&rating=g&lang=en`

## 输出规则

- 如果找到GIF的URL：仅发送该URL（Discord会自动嵌入GIF）。
- 如果未找到结果：发送一条简短的提示信息，并请求用户提供更具体的关键词。

## 有效的查询示例

- `happy dance`（快乐舞蹈）
- `facepalm reaction`（无奈的表情）
- `mind blown`（震惊的表情）
- `awkward silence`（尴尬的沉默）

## 备用提示信息

“我找不到符合您需求的GIF。能否提供更具体的关键词呢？”