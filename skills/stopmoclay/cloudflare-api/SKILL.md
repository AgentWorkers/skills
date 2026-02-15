---
name: cloudflare
description: 连接到 Cloudflare API 以进行 DNS 管理、隧道配置和区域设置。当用户需要管理域名、DNS 记录或创建隧道时，请使用此功能。
read_when:
  - User asks about Cloudflare DNS or domains
  - User wants to create or manage DNS records
  - User needs to set up Cloudflare tunnels
  - User wants to list their Cloudflare zones
metadata:
  clawdbot:
    emoji: "☁️"
    requires:
      bins: ["curl", "jq"]
---

# Cloudflare Skill

该技能用于连接 [Cloudflare](https://cloudflare.com) 的 API，以实现 DNS 管理、隧道配置以及区域设置等功能。

## 设置

### 1. 获取 API 令牌
1. 访问 [dash.cloudflare.com/profile/api-tokens](https://dash.cloudflare.com/profile/api-tokens)
2. 创建一个具有以下权限的 API 令牌：
   - **Zone:Read**：列出域名
   - **DNS:Edit**：管理 DNS 记录
   - **Account:Cloudflare Tunnel:Edit**：管理隧道
3. 复制该令牌。

### 2. 配置
```bash
# Option A: Store in file (recommended)
echo "YOUR_API_TOKEN" > ~/.cloudflare_token
chmod 600 ~/.cloudflare_token

# Option B: Environment variable
export CLOUDFLARE_API_TOKEN="YOUR_API_TOKEN"
```

### 3. 测试连接
```bash
./scripts/setup.sh
```

---

## 命令

### 区域（域名）
```bash
./scripts/zones/list.sh                    # List all zones
./scripts/zones/list.sh --json             # JSON output
./scripts/zones/get.sh example.com         # Get zone details
```

### DNS 记录
```bash
# List records
./scripts/dns/list.sh example.com
./scripts/dns/list.sh example.com --type A
./scripts/dns/list.sh example.com --name api

# Create record
./scripts/dns/create.sh example.com \
  --type A \
  --name api \
  --content 1.2.3.4 \
  --proxied

# Create CNAME
./scripts/dns/create.sh example.com \
  --type CNAME \
  --name www \
  --content example.com \
  --proxied

# Update record
./scripts/dns/update.sh example.com \
  --name api \
  --type A \
  --content 5.6.7.8

# Delete record
./scripts/dns/delete.sh example.com --name api --type A
```

### 隧道
```bash
# List tunnels
./scripts/tunnels/list.sh

# Create tunnel
./scripts/tunnels/create.sh my-tunnel

# Configure tunnel ingress
./scripts/tunnels/configure.sh my-tunnel \
  --hostname app.example.com \
  --service http://localhost:3000

# Get run token
./scripts/tunnels/token.sh my-tunnel

# Delete tunnel
./scripts/tunnels/delete.sh my-tunnel
```

---

## 令牌权限

| 功能          | 所需权限                |
|---------------|----------------------|
| 列出区域        | Zone:Read                |
| 管理 DNS        | DNS:Edit                |
| 管理隧道        | Account:Cloudflare Tunnel:Edit       |

请在 [dash.cloudflare.com/profile/api-tokens](https://dash.cloudflare.com/profile/api-tokens) 处创建 API 令牌。

---

## 常见工作流程

### 将子域名指向服务器
```bash
./scripts/dns/create.sh mysite.com --type A --name api --content 1.2.3.4 --proxied
```

### 为本地服务设置隧道
```bash
# 1. Create tunnel
./scripts/tunnels/create.sh webhook-tunnel

# 2. Configure ingress
./scripts/tunnels/configure.sh webhook-tunnel \
  --hostname hook.mysite.com \
  --service http://localhost:8080

# 3. Add DNS record
TUNNEL_ID=$(./scripts/tunnels/list.sh --name webhook-tunnel --quiet)
./scripts/dns/create.sh mysite.com \
  --type CNAME \
  --name hook \
  --content ${TUNNEL_ID}.cfargotunnel.com \
  --proxied

# 4. Run tunnel
TOKEN=$(./scripts/tunnels/token.sh webhook-tunnel)
cloudflared tunnel run --token $TOKEN
```

---

## 输出格式

| 标志          | 描述                        |
|--------------|---------------------------|
| `--json`       | 来自 API 的原始 JSON 数据           |
| `--table`      | 格式化的表格（默认输出）             |
| `--quiet`      | 最小化输出（仅显示 ID）           |

---

## 故障排除

| 错误信息        | 解决方案                        |
|---------------|-------------------------------------------|
| “未找到 API 令牌”     | 运行设置脚本或设置 `CLOUDFLARE_API_TOKEN`         |
| “401 未经授权”     | 检查令牌是否有效                   |
| “403 禁止访问”     | 令牌缺少所需权限                   |
| “区域未找到”     | 确认域名是否属于您的账户                 |