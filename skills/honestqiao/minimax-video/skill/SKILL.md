---
name: minimax-video
description: 使用 Zhipu（智谱）的网页搜索 API 来进行互联网搜索。当用户请求网页搜索、最新新闻或需要当前信息时，可以使用该 API。
allowed-tools: Bash(curl:*) Bash(jq:*)
env:
  - MINIMAX_API_KEY
---
# 智谱（Zhipu）网络搜索

使用智谱（Zhipu）的网络搜索API来搜索互联网。

## ⚠️ 安全要求

**使用此功能之前，必须设置`MINIMAX_API_KEY`环境变量。**

### 安全最佳实践：

1. **切勿将API密钥存储在`~/.bashrc`文件中**——这可能导致密钥泄露。
2. **不要导入shell配置文件**——这样可以防止恶意代码的执行。
3. **在运行脚本时直接设置环境变量**。
4. **注意**：API密钥会显示在进程列表（`ps aux`）中。

## 设置

```bash
# Set API key as environment variable
export MINIMAX_API_KEY="your_api_key"
```

**从以下链接获取您的API密钥：** https://www.bigmodel.cn/usercenter/proj-mgmt/apikeys

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
- **不导入`~/.bashrc`或shell配置文件**。
- **使用jq进行JSON转义**（防止注入攻击）。
- **使用TLS 1.2+版本的HTTPS**。
- **API密钥通过环境变量传递**（而非硬编码）。
- **适当的错误处理**——敏感信息不会被泄露。
- **输入验证**（查询长度有限制）。
- **通用错误信息**（不提供路径或文件相关的提示）。

### ⚠️ 需要注意的问题：
- **进程列表可见性**：API密钥会显示在`ps aux`中。
  - 仅应在受信任的环境中使用。
  - 不建议在共享或多用户系统中使用。
- **API端点**：`https://open.bigmodel.cn`（在生产环境中请验证）。
- **密钥权限**：使用具有最小权限的密钥。

## 安全特性

| 特性 | 实现方式 |
|---------|----------------|
| JSON转义 | 使用`jq --arg`进行转义，防止注入攻击。 |
| 输入验证 | 查询长度不超过500个字符。 |
| TLS协议 | 强制使用TLS 1.2+版本。 |
| 错误处理 | 显示通用错误信息，避免泄露敏感信息。 |
| 超时设置 | 使用`curl`命令设置30秒的超时时间。 |

## 使用场景：

- 用户请求“搜索”、“查找信息”或“查询相关内容”。
- 用户询问“最新的新闻是什么”。
- 用户需要从网络上获取当前信息。
- 用户想要了解最近发生的事件。

## API端点

**官方端点：** `https://open.bigmodel.cn/api/paas/v4/chat/completions`

这是智谱（Zhipu）AI的官方API。