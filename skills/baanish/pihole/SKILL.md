# Pi-hole 技能

通过 Pi-hole v6 API 来控制您的 Pi-hole DNS 广告拦截器。

## 设置

在 Clawdbot 的配置文件中设置 Pi-hole 的 API 配置：

```yaml
skills:
  entries:
    pihole:
      apiUrl: "https://pi-hole.local/api"  # v6 API path
      apiToken: "your-app-password-here"       # Get from Pi-hole Admin
      insecure: false                          # Set to true for self-signed certs
```

或者，您也可以通过设置环境变量来配置：

```bash
export PIHOLE_API_URL="https://pi-hole.local/api"
export PIHOLE_API_TOKEN="your-app-password-here"
export PIHOLE_INSECURE="false"
```

### 获取 API 凭据

1. 打开 Pi-hole 的管理界面：`http://pi-hole.local/admin`
2. 转到 **设置** > **API**
3. 生成一个应用密码
4. 将该密码用作 `apiToken`

## 功能

### 状态
- 获取 Pi-hole 的当前状态（启用/禁用）
- 查看统计信息：被拦截的请求数量、今日的请求数量、被拦截的域名、活跃的客户端数量
- 查看最近的请求活动

### 控制功能
- **启用/禁用**：开启或关闭 Pi-hole
- **禁用 5 分钟**：暂时禁用广告拦截功能
- **自定义禁用时长**：设置特定的禁用时间（以分钟为单位）

### 块拦截分析
- **查看被拦截的域名**：查看在指定时间范围内被拦截的域名
- **显示最常被拦截的域名**：查看最常被拦截的域名

## 使用示例

```
# Check Pi-hole status
"pihole status"

# Turn off ad blocking
"pihole off"

# Turn on ad blocking
"pihole on"

# Disable for 5 minutes (for a site that needs ads)
"pihole disable 5m"

# Disable for 30 minutes
"pihole disable 30"

# See what was blocked in the last 30 minutes
"pihole blocked"

# See blocked domains in last 10 minutes (600 seconds)
"pihole blocked 600"

# Show statistics
"pihole stats"
```

## API 端点（Pi-hole v6）

### 认证
```
POST /api/auth
Content-Type: application/json
{"password":"your-app-password"}

Response:
{
  "session": {
    "sid": "session-token-here",
    "validity": 1800
  }
}
```

### 状态
```
GET /api/dns/blocking
Headers: sid: <session-token>

Response:
{
  "blocking": "enabled" | "disabled",
  "timer": 30  // seconds until re-enable (if disabled with timer)
}
```

### 启用/禁用
```
POST /api/dns/blocking
Headers: sid: <session-token>
Content-Type: application/json

Enable:
{"blocking":true}

Disable:
{"blocking":false}

Disable with timer (seconds):
{"blocking":false,"timer":300}
```

### 统计信息
```
GET /api/stats/summary
Headers: sid: <session-token>

Response:
{
  "queries": {
    "total": 233512,
    "blocked": 23496,
    "percent_blocked": 10.06
  },
  "gravity": {
    "domains_being_blocked": 165606
  },
  "clients": {
    "active": 45
  }
}
```

### 请求信息
```
GET /api/queries?start=-<seconds>
Headers: sid: <session-token>

Response:
{
  "queries": [
    {
      "domain": "example.com",
      "status": "GRAVITY",
      "time": 1768363900,
      "type": "A"
    }
  ]
}
```

## v5 与 v6 API 的变化

Pi-hole v6 引入了一些重要的 API 变更：

| 功能 | v5 API | v6 API |
|---------|----------|----------|
| 基本 URL | `/admin/api.php` | `/api` |
| 认证方式 | URL/头部中的令牌 | 基于会话的认证 |
| 状态查询 | `?status` | `/api/dns/blocking` |
| 统计信息 | `?summaryRaw` | `/api/stats/summary` |
| 请求信息 | `?recentBlocked` | `/api/queries` |
| 白名单 | 可通过 API 设置 | **v6 API 不支持** |

**重要提示：** v6 API 不再支持域名白名单功能。您必须通过 Pi-hole 的管理界面来设置域名白名单。

## SSL 证书

### 生产环境（有效证书）
```yaml
{
  "apiUrl": "https://pi-hole.example.com/api",
  "apiToken": "...",
  "insecure": false
}
```

### 自签名/本地证书
```yaml
{
  "apiUrl": "https://pi-hole.local/api",
  "apiToken": "...",
  "insecure": true
}
```

在 `curl` 命令中添加 `--insecure` 选项可以绕过证书验证。

## 安全注意事项

- 会话令牌在 30 分钟（1800 秒）后失效
- API 密码以 JSON 格式在请求体中发送，而不是通过 URL 传递
- 所有请求都有 30 秒的超时限制
- 令牌不会显示在进程列表中（通过环境变量传递）

## 故障排除

### “无法认证”
- 确认 `apiToken` 与您的 Pi-hole 应用密码一致
- 检查 `apiUrl` 是否正确（必须以 `/api` 结尾）
- 确保可以从您的网络访问 Pi-hole

### “无法确定状态”
- 检查 API URL 是否可访问
- 如果使用自签名证书，请设置 `insecure: true`
- 确认 API 密码正确

### 网络问题
- 确保 Clawdbot 可以访问 Pi-hole
- 检查防火墙规则是否允许 API 访问
- 确认 URL 协议（http 或 https）

## 其他要求

- 需要使用 Pi-hole v6 或更高版本
- 在 Pi-hole 管理界面生成应用密码
- 确保可以从网络访问 Pi-hole 的 API
- 需要安装 `curl` 和 `jq`（大多数 Unix 系统都已安装）