---
name: doubao-image
description: 使用 Zhipu（智谱）的 Web 图像 API 来获取互联网上的图片。当用户请求网页图片、最新新闻或需要当前信息时，可以使用该 API。
allowed-tools: Bash(curl:*) Bash(jq:*)
env:
  - DOUBAO_API_KEY
---
# Zhipu Web Image

使用 Zhipu 的 Web 图像 API 从互联网中获取图片。

## ⚠️ 安全要求

**使用此功能之前，必须设置 `DOUBAO_API_KEY` 环境变量。**

### 安全最佳实践：

1. **切勿将 API 密钥存储在 ~/.bashrc 文件中**——密钥可能会被泄露。
2. **不要导入 shell 配置文件**——这样可以防止任意代码的执行。
3. **在运行脚本时直接设置环境变量**。
4. **请注意**：API 密钥会显示在进程列表（`ps aux`）中。

## 设置

```bash
# Set API key as environment variable
export DOUBAO_API_KEY="your_api_key"
```

**从以下链接获取您的 API 密钥：** https://www.bigmodel.cn/usercenter/proj-mgmt/apikeys

## 使用方法

### 快速获取图片

```bash
export DOUBAO_API_KEY="your_key"

curl -s -X POST "https://open.bigmodel.cn/api/paas/v4/chat/completions" \
  -H "Authorization: Bearer $DOUBAO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "glm-4-flash",
    "messages": [{"role": "user", "content": "搜索: YOUR_QUERY"}],
    "tools": [{"type": "web_image", "web_image": {"image_query": "YOUR_QUERY"}}]
  }' | jq -r '.choices[0].message.content'
```

### 使用脚本

```bash
export DOUBAO_API_KEY="your_key"
./image.sh "搜索内容"
```

## 安全分析

### ✅ 安全措施：
- **不导入 ~/.bashrc 或 shell 配置文件**。
- **使用 jq 进行 JSON 转义**（防止注入攻击）。
- **使用支持 TLS 1.2+ 的 HTTPS 协议**。
- **API 密钥通过环境变量传递（而非硬编码）**。
- **适当的错误处理**——敏感信息不会被泄露。
- **输入验证**（查询长度有限制）。
- **使用通用的错误信息**（不包含路径或文件信息）。

### ⚠️ 需要注意的事项：
- **进程列表可见性**：API 密钥会显示在 `ps aux` 中。
  - 仅应在受信任的环境中使用此功能。
  - 不建议在共享或多用户系统中使用。
- **API 端点**：`https://open.bigmodel.cn`（在生产环境中请进行验证）。
- **密钥权限**：使用具有最小权限的密钥。

## 安全特性

| 特性 | 实现方式 |
|---------|----------------|
| JSON 转义 | 使用 `jq --arg` 进行 JSON 转义，防止注入攻击。 |
| 输入验证 | 查询长度不超过 500 个字符。 |
| TLS 协议 | 强制使用 TLS 1.2+ 协议。 |
| 错误处理 | 使用通用的错误信息，避免敏感信息泄露。 |
| 超时设置 | 使用 30 秒的 curl 超时机制。 |

## 适用场景：

- 用户请求“获取图片”、“查找信息”或“了解相关内容”。
- 用户询问“最新的新闻是什么”。
- 用户需要从互联网获取当前信息。
- 用户希望了解最近发生的事件。

## API 端点

**官方端点：** `https://open.bigmodel.cn/api/paas/v4/chat/completions`

这是智谱（Zhipu）AI 的官方 API。