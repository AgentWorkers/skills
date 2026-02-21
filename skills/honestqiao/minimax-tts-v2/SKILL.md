---
name: minimax-tts
description: 使用 Zhipu（智谱）的网页搜索 API 来进行互联网搜索。当用户请求网页搜索、最新新闻或需要当前信息时，可以使用该 API。
allowed-tools: Bash(curl:*) Bash(jq:*)
env:
  - MINIMAX_API_KEY
---
# Zhipu 网页搜索

使用 Zhipu 的网页搜索 API 来搜索互联网。

## ⚠️ 安全要求

**使用此功能之前，必须设置 `MINIMAX_API_KEY` 环境变量。**

### 安全最佳实践：

1. **切勿将 API 密钥存储在 ~/.bashrc 文件中**——这可能导致密钥泄露。
2. **不要导入 shell 配置文件**——以防止任意代码的执行。
3. **在运行脚本时直接设置环境变量**。
4. **请注意**：API 密钥会显示在进程列表（`ps aux`）中。

## 设置

```bash
# Set API key as environment variable
export MINIMAX_API_KEY="your_api_key"
```

**从以下链接获取您的 API 密钥：** https://www.bigmodel.cn/usercenter/proj-mgmt/apikeys

## 使用方法

### 快速搜索

```bash
export MINIMAX_API_KEY="your_key"

curl -s -X POST "https://open.bigmodel.cn/api/paas/v4/chat/completions" \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "glm-4-flash",
    "messages": [{"role": "user", "content": "搜索: YOUR_QUERY"}],
    "tools": [{"type": "web_search", "web_search": {"search_query": "YOUR_QUERY"}}]
  }' | jq -r '.choices[0].message.content'
```

### 使用脚本

```bash
export MINIMAX_API_KEY="your_key"
./search.sh "搜索内容"
```

## 安全分析

### ✅ 安全措施：
- 不会导入 ~/.bashrc 或 shell 配置文件。
- 使用 `jq` 进行 JSON 转义（防止注入攻击）。
- 使用支持 TLS 1.2+ 的 HTTPS 协议。
- API 密钥通过环境变量传递（而非硬编码）。
- 有适当的错误处理机制——敏感信息不会泄露。
- 对输入进行验证（限制查询长度）。
- 显示通用的错误信息（不包含路径或文件相关的提示）。

### ⚠️ 需要注意的事项：
- **进程列表可见性**：API 密钥会显示在 `ps aux` 中，因此仅应在受信任的环境中使用该功能。
- **API 端点**：`https://open.bigmodel.cn`（官方 Zhipu API）。

## 安全特性

| 特性 | 实现方式 |
|---------|----------------|
| JSON 转义 | 使用 `jq --arg` 进行 JSON 转义，防止注入攻击。 |
| 输入验证 | 查询长度限制在 500 个字符以内。 |
| TLS 协议 | 强制使用 TLS 1.2+ 协议。 |
| 错误处理 | 显示通用错误信息，避免敏感信息泄露。 |
| 超时设置 | 使用 `curl` 命令设置 30 秒的超时时间。 |

## 适用场景：

- 用户要求“搜索”、“查找信息”或“查询相关内容”时。
- 用户询问“最新的新闻是什么”时。
- 用户需要从互联网获取实时信息时。

## API 端点

**官方端点：** `https://open.bigmodel.cn/api/paas/v4/chat/completions`