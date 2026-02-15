---
name: flaresolverr
description: 绕过 Cloudflare 的保护机制——在 `curl` 或 `summarize` 命令遇到 403 错误，或者 Cloudflare 对请求进行拦截时使用此方法。
metadata:
  {
    "openclaw":
      {
        "emoji": "🛡️",
        "requires": { "bins": ["curl", "jq"], "env": ["FLARESOLVERR_URL"] },
        "primaryEnv": "FLARESOLVERR_URL",
      },
  }
---

# FlareSolverr — 用于绕过Cloudflare保护的工具

当直接使用`curl`请求失败（返回403错误或遇到Cloudflare的验证页面）时，可以使用FlareSolverr来绕过Cloudflare的保护。

## 设置

1. **运行FlareSolverr**（建议使用Docker）：

```bash
docker run -d --name flaresolverr -p 8191:8191 ghcr.io/flaresolverr/flaresolverr:latest
```

2. **设置环境变量**：

```bash
export FLARESOLVERR_URL="http://localhost:8191"
```

3. **验证设置是否正确**：

```bash
curl -s "$FLARESOLVERR_URL/health" | jq '.'
# Expected: {"status":"ok","version":"3.x.x"}
```

## 使用场景

- 当直接使用`curl`请求时遇到403 Forbidden错误
- 出现Cloudflare的验证页面（如JavaScript验证、验证码、提示“正在检查您的浏览器”）
- 由于机器人检测机制而被阻止的自动化请求
- 遭遇速率限制或反爬虫措施

## 工作流程

1. **首先尝试直接使用`curl`请求**（这种方式更快且更简单）
2. **如果请求被阻止**，使用FlareSolverr获取所需的cookies和用户代理（user-agent）信息
3. **在后续请求中重用会话信息**（可选，以提高性能）

## 基本用法

### 发送简单的GET请求

```bash
curl -X POST "$FLARESOLVERR_URL/v1" \
  -H "Content-Type: application/json" \
  -d '{
    "cmd": "request.get",
    "url": "https://example.com/protected-page",
    "maxTimeout": 60000
  }' | jq '.'
```

### 响应结构

```json
{
  "status": "ok",
  "message": "Challenge solved!",
  "solution": {
    "url": "https://example.com/protected-page",
    "status": 200,
    "headers": {},
    "response": "<html>...</html>",
    "cookies": [
      {
        "name": "cf_clearance",
        "value": "...",
        "domain": ".example.com"
      }
    ],
    "userAgent": "Mozilla/5.0 ..."
  },
  "startTimestamp": 1234567890,
  "endTimestamp": 1234567895,
  "version": "3.3.2"
}
```

### 提取页面内容

```bash
curl -s -X POST "$FLARESOLVERR_URL/v1" \
  -H "Content-Type: application/json" \
  -d '{
    "cmd": "request.get",
    "url": "https://example.com/protected-page"
  }' | jq -r '.solution.response'
```

### 提取cookies

```bash
curl -s -X POST "$FLARESOLVERR_URL/v1" \
  -H "Content-Type: application/json" \
  -d '{
    "cmd": "request.get",
    "url": "https://example.com"
  }' | jq -r '.solution.cookies[] | "\(.name)=\(.value)"'
```

## 会话管理

会话功能允许用户在多次请求中重用浏览器上下文（包括cookies和用户代理信息），从而提高请求效率。

### 创建会话

```bash
curl -s -X POST "$FLARESOLVERR_URL/v1" \
  -H "Content-Type: application/json" \
  -d '{"cmd": "sessions.create"}' | jq -r '.session'
```

### 在请求中使用会话信息

```bash
curl -s -X POST "$FLARESOLVERR_URL/v1" \
  -H "Content-Type: application/json" \
  -d '{
    "cmd": "request.get",
    "url": "https://example.com/page1",
    "session": "SESSION_ID"
  }' | jq -r '.solution.response'
```

### 列出所有活动的会话

```bash
curl -s -X POST "$FLARESOLVERR_URL/v1" \
  -H "Content-Type: application/json" \
  -d '{"cmd": "sessions.list"}' | jq '.sessions'
```

### 销毁会话

```bash
curl -s -X POST "$FLARESOLVERR_URL/v1" \
  -H "Content-Type: application/json" \
  -d '{
    "cmd": "sessions.destroy",
    "session": "SESSION_ID"
  }'
```

## 发送POST请求

```bash
curl -s -X POST "$FLARESOLVERR_URL/v1" \
  -H "Content-Type: application/json" \
  -d '{
    "cmd": "request.post",
    "url": "https://example.com/api/endpoint",
    "postData": "key1=value1&key2=value2",
    "maxTimeout": 60000
  }' | jq '.'
```

对于发送JSON格式的POST数据：

```bash
curl -s -X POST "$FLARESOLVERR_URL/v1" \
  -H "Content-Type: application/json" \
  -d '{
    "cmd": "request.post",
    "url": "https://example.com/api/endpoint",
    "postData": "{\"key\":\"value\"}",
    "headers": {
      "Content-Type": "application/json"
    }
  }' | jq '.'
```

## 高级选项

### 自定义用户代理（user-agent）

```bash
curl -s -X POST "$FLARESOLVERR_URL/v1" \
  -H "Content-Type: application/json" \
  -d '{
    "cmd": "request.get",
    "url": "https://example.com",
    "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
  }' | jq '.'
```

### 自定义请求头（request headers）

```bash
curl -s -X POST "$FLARESOLVERR_URL/v1" \
  -H "Content-Type: application/json" \
  -d '{
    "cmd": "request.get",
    "url": "https://example.com",
    "headers": {
      "Accept-Language": "en-US,en;q=0.9",
      "Referer": "https://google.com"
    }
  }' | jq '.'
```

### 支持代理服务器（proxy）

```bash
curl -s -X POST "$FLARESOLVERR_URL/v1" \
  -H "Content-Type: application/json" \
  -d '{
    "cmd": "request.get",
    "url": "https://example.com",
    "proxy": {
      "url": "http://proxy.example.com:8080"
    }
  }' | jq '.'
```

### 下载二进制文件内容

```bash
curl -s -X POST "$FLARESOLVERR_URL/v1" \
  -H "Content-Type: application/json" \
  -d '{
    "cmd": "request.get",
    "url": "https://example.com/file.pdf",
    "download": true
  }' | jq -r '.solution.response' | base64 -d > file.pdf
```

## 错误处理

- **`"status": "error"`**：请求失败（请查看`message`字段以获取详细信息）
- **`"status": "timeout"`**：超时（请增加`maxTimeout`值）
- **`"status": "captcha"`**：需要手动输入验证码（这种情况较少见，通常可以自动解决）

### 检查请求状态

```bash
curl -s -X POST "$FLARESOLVERR_URL/v1" \
  -H "Content-Type: application/json" \
  -d '{"cmd": "request.get", "url": "https://example.com"}' | \
  jq -r '.status'
```

## 示例用法

### 绕过Cloudflare并提取数据

```bash
# Step 1: Fetch page through FlareSolverr
RESPONSE=$(curl -s -X POST "$FLARESOLVERR_URL/v1" \
  -H "Content-Type: application/json" \
  -d '{
    "cmd": "request.get",
    "url": "https://example.com/protected-page"
  }')

# Step 2: Check if successful
STATUS=$(echo "$RESPONSE" | jq -r '.status')
if [ "$STATUS" != "ok" ]; then
  echo "Failed: $(echo "$RESPONSE" | jq -r '.message')"
  exit 1
fi

# Step 3: Extract and parse HTML
echo "$RESPONSE" | jq -r '.solution.response'
```

### 处理多页面请求时的会话管理

```bash
# Create session
SESSION=$(curl -s -X POST "$FLARESOLVERR_URL/v1" \
  -H "Content-Type: application/json" \
  -d '{"cmd": "sessions.create"}' | jq -r '.session')

# Page 1
curl -s -X POST "$FLARESOLVERR_URL/v1" \
  -H "Content-Type: application/json" \
  -d "{\"cmd\": \"request.get\", \"url\": \"https://example.com/page1\", \"session\": \"$SESSION\"}" | \
  jq -r '.solution.response'

# Page 2 (reuses cookies from page 1)
curl -s -X POST "$FLARESOLVERR_URL/v1" \
  -H "Content-Type: application/json" \
  -d "{\"cmd\": \"request.get\", \"url\": \"https://example.com/page2\", \"session\": \"$SESSION\"}" | \
  jq -r '.solution.response'

# Cleanup
curl -s -X POST "$FLARESOLVERR_URL/v1" \
  -H "Content-Type: application/json" \
  -d "{\"cmd\": \"sessions.destroy\", \"session\": \"$SESSION\"}"
```

## 健康检查（health check）

```bash
curl -s "$FLARESOLVERR_URL/health" | jq '.'
```

## 性能优化建议

- **对于同一域名的多次请求，尽量使用会话功能以重用cookies和浏览器上下文**
- **对于响应速度较慢的网站，增加`maxTimeout`值（默认为60000毫秒）**
- **尽可能直接使用`curl`请求（因为FlareSolverr会因为浏览器开销而降低请求速度）**
- **请求完成后及时销毁会话以释放系统资源**

## 限制与注意事项

- **相比直接使用`curl`，FlareSolverr的请求速度较慢**（因为它需要启动无头浏览器）
- **资源消耗较大**（会限制同时进行的请求数量）
- **可能无法解决所有类型的验证码**（大多数Cloudflare验证机制都能被绕过）
- **响应内容仅包含HTML，不支持客户端JavaScript的执行**

## 最佳实践

- **始终优先尝试直接使用`curl`请求**
- **在处理多页面请求时使用会话功能**
- **根据网站响应速度设置合适的`maxTimeout`值**
- **请求完成后及时清理会话信息**
- **优雅地处理错误（务必检查`status`字段）
- **合理控制请求频率，避免对FlareSolverr或目标网站造成负担**