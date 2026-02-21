---
name: zhipu-embeddings
description: 使用 Zhipu（智谱）的 Web 嵌入 API 来对互联网内容进行嵌入处理。当用户请求 Web 嵌入数据、最新新闻或需要获取当前信息时，可以使用该 API。
allowed-tools: Bash(curl:*) Bash(jq:*)
env:
  - ZHIPU_API_KEY
---
# 智谱（Zhipu）Web嵌入功能

使用智谱的Web嵌入API将互联网上的内容进行嵌入处理。

## ⚠️ 安全要求

**使用此功能前，必须设置`ZHIPU_API_KEY`环境变量。**

### 安全最佳实践：

1. **切勿将API密钥存储在`~/.bashrc`文件中**——这可能导致密钥泄露。
2. **不要从shell配置文件中读取API密钥**——这样可以防止恶意代码的执行。
3. **在运行脚本时直接设置环境变量**。
4. **注意**：API密钥会显示在进程列表（`ps aux`）中。

## 设置

```bash
# Set API key as environment variable
export ZHIPU_API_KEY="your_api_key"
```

**获取您的API密钥，请访问：** https://www.bigmodel.cn/usercenter/proj-mgmt/apikeys

## 使用方法

### 快速嵌入

```bash
export ZHIPU_API_KEY="your_key"

curl -s -X POST "https://open.bigmodel.cn/api/paas/v4/chat/completions" \
  -H "Authorization: Bearer $ZHIPU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "glm-4-flash",
    "messages": [{"role": "user", "content": "搜索: YOUR_QUERY"}],
    "tools": [{"type": "web_embeddings", "web_embeddings": {"embeddings_query": "YOUR_QUERY"}}]
  }' | jq -r '.choices[0].message.content'
```

### 使用脚本

```bash
export ZHIPU_API_KEY="your_key"
./embeddings.sh "搜索内容"
```

## 安全分析

### ✅ 安全措施：
- **不从`~/.bashrc`或shell配置文件中读取API密钥**。
- **使用`jq`进行JSON转义**（防止注入攻击）。
- **使用TLS 1.2+版本的HTTPS**。
- **API密钥通过环境变量传递（而非硬编码）**。
- **适当的错误处理**——避免敏感信息泄露。
- **输入验证**（限制查询长度）。
- **使用通用的错误信息**（不暴露路径或文件信息）。

### ⚠️ 需要注意的事项：
- **进程列表可见性**：API密钥会显示在`ps aux`中。
  - 仅应在受信任的环境中使用此功能。
  - 不建议在共享或多用户系统中使用。
- **API端点**：`https://open.bigmodel.cn`（在生产环境中请验证此地址）。
- **密钥权限**：使用具有最小权限的API密钥。

## 安全特性

| 特性 | 实现方式 |
|---------|----------------|
| JSON转义 | 使用`jq --arg`进行转义，防止注入攻击。 |
| 输入验证 | 查询长度不超过500个字符。 |
| TLS协议** | 强制使用TLS 1.2+版本。 |
| 错误处理 | 显示通用错误信息，避免敏感信息泄露。 |
| 超时设置 | 使用`curl`命令设置30秒的超时时间。 |

## 适用场景：

- 用户请求“进行嵌入处理”、“查找信息”或“查询相关内容”。
- 用户询问“最新的新闻是什么”。
- 用户需要获取网络上的最新信息。
- 用户希望了解最近发生的事件。

## API端点

**官方端点：** `https://open.bigmodel.cn/api/paas/v4/chat/completions`

这是智谱（Zhipu）AI的官方API。