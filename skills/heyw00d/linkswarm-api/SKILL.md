# LinkSwarm API 🐝

**专为AI代理设计的反向链接交换服务。帮助您的代理提升所创建网站的权威性。**

## 该功能的作用

允许您的代理：
- 在LinkSwarm网络中注册域名
- 请求反向链接（需要消耗信用点数）
- 提供链接资源（可获得信用点数）
- 查看信用点数余额及链接放置状态
- 在链接被放置时收到通知

## 快速入门

### 1. 获取API密钥
在https://linkswarm.ai/register/注册，或通过API获取：
```bash
curl -X POST https://api.linkswarm.ai/waitlist \
  -H "Content-Type: application/json" \
  -d '{"email": "your@email.com"}'
```

### 2. 将API密钥添加到代理的配置文件中
将API密钥添加到代理的`auth-profiles.json`文件或环境变量中：
```json
{
  "linkswarm": {
    "api_key": "sk_linkswarm_..."
  }
}
```

## API参考

**基础URL：** `https://api.linkswarm.ai`

**认证方式：** `Authorization: Bearer sk_linkswarm_...`

### 注册网站
```bash
POST /v1/sites
{
  "domain": "mycoolsite.com",
  "name": "My Cool Site",
  "categories": ["tech", "ai"]
}
```

### 验证域名
```bash
POST /v1/sites/verify
{
  "domain": "mycoolsite.com",
  "method": "dns"  # or "meta"
}
```
- 通过添加TXT记录（内容：`linkswarm-verify=<token>`）或meta标签来验证域名。

### 请求反向链接（消耗1个信用点数）
```bash
POST /v1/pool/request
{
  "target_domain": "mycoolsite.com",
  "target_page": "/",
  "anchor_text": "My Cool Site"
}
```

### 提供链接资源（获得1个信用点数）
```bash
POST /v1/pool/contribute
{
  "domain": "mycoolsite.com",
  "page_url": "/resources/",
  "max_links": 3
}
```

### 查看状态
```bash
GET /v1/pool/status
```
返回信息包括：当前信用点数、待放置的链接、已验证的链接等。

### 列出所有注册的网站
```bash
GET /v1/sites
```

## 信用点数系统

| 操作          | 信用点数        |
|---------------|-------------|
| 请求反向链接      | -1            |
| 提供链接资源      | +1            |
| 链接验证通过     | +1（额外奖励）      |
| 推荐他人注册    | +3            |

免费账户初始拥有3个信用点数。

## 示例：代理的完整操作流程
```python
import requests

API = "https://api.linkswarm.ai"
KEY = "sk_linkswarm_..."
headers = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}

# 1. Register new site
requests.post(f"{API}/v1/sites", headers=headers, json={
    "domain": "myagentsite.com",
    "categories": ["ai", "tools"]
})

# 2. Contribute to earn credits
requests.post(f"{API}/v1/pool/contribute", headers=headers, json={
    "domain": "myagentsite.com",
    "page_url": "/partners/"
})

# 3. Request backlinks
requests.post(f"{API}/v1/pool/request", headers=headers, json={
    "target_domain": "myagentsite.com",
    "anchor_text": "AI Tools Directory"
})

# 4. Check status
status = requests.get(f"{API}/v1/pool/status", headers=headers).json()
print(f"Credits: {status['credits']['balance']}")
print(f"Pending: {status['pendingPlacements']}")
```

## Webhook（可选）
注册Webhook以接收通知：
```bash
POST /v1/webhooks
{
  "url": "https://your-agent.com/webhook",
  "events": ["link.placed", "link.verified", "credits.low"]
}
```

## 最佳实践

1. 在请求链接前先验证域名。
2. 先提供链接资源以积累信用点数。
3. 使用相关的分类标签以提升匹配效果。
4. 设置Webhook以实现自动化操作。

## 请求限制

- 每分钟60次请求。
- 每小时500次请求。
- 允许同时进行10次突发请求。

## 支持方式

- 文档：https://linkswarm.ai/docs/
- Discord频道：https://discord.gg/6RzUpUbMFE
- API状态查询：https://api.linkswarm.ai/health

## 选择LinkSwarm的理由？

- **非互惠式匹配**：生成的链接对搜索引擎更自然。
- **链接验证**：系统会确认每个反向链接的有效性。
- **公平的信用点数系统**：提供相应的奖励。
- **不断扩展的网络**：拥有30多个高质量网站。
- **以AI为核心**：专为自动化代理设计。

---

*您的代理负责构建网站，LinkSwarm则帮助提升其权威性。* 🐝