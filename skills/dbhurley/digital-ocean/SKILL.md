---
name: digital-ocean
description: 通过 DO API 管理 Digital Ocean 的虚拟机（droplets）、域名（domains）以及基础设施。
homepage: https://docs.digitalocean.com/reference/api/
metadata: {"clawdis":{"emoji":"🌊","requires":{"bins":["uv","curl"],"env":["DO_API_TOKEN"]},"primaryEnv":"DO_API_TOKEN"}}
---

# Digital Ocean管理

用于控制Digital Ocean上的虚拟机（Droplets）、域名（Domains）以及基础设施。

## 设置

配置环境变量：
- `DO_API_TOKEN`：您的Digital Ocean API令牌（请在cloud.digitalocean.com/account/api/tokens页面生成）

## 命令行界面（CLI）命令

```bash
# Account info
uv run {baseDir}/scripts/do.py account

# List all droplets
uv run {baseDir}/scripts/do.py droplets

# Get droplet details
uv run {baseDir}/scripts/do.py droplet <droplet_id>

# List domains
uv run {baseDir}/scripts/do.py domains

# List domain records
uv run {baseDir}/scripts/do.py records <domain>

# Droplet actions
uv run {baseDir}/scripts/do.py power-off <droplet_id>
uv run {baseDir}/scripts/do.py power-on <droplet_id>
uv run {baseDir}/scripts/do.py reboot <droplet_id>
```

## 直接使用API（curl）

### 列出虚拟机
```bash
curl -s -H "Authorization: Bearer $DO_API_TOKEN" \
  "https://api.digitalocean.com/v2/droplets" | jq '.droplets[] | {id, name, status, ip: .networks.v4[0].ip_address}'
```

### 获取账户信息
```bash
curl -s -H "Authorization: Bearer $DO_API_TOKEN" \
  "https://api.digitalocean.com/v2/account" | jq '.account'
```

### 列出域名
```bash
curl -s -H "Authorization: Bearer $DO_API_TOKEN" \
  "https://api.digitalocean.com/v2/domains" | jq '.domains[].name'
```

### 创建虚拟机
```bash
curl -s -X POST -H "Authorization: Bearer $DO_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my-droplet",
    "region": "nyc1",
    "size": "s-1vcpu-1gb",
    "image": "ubuntu-22-04-x64"
  }' \
  "https://api.digitalocean.com/v2/droplets"
```

### 重启虚拟机
```bash
curl -s -X POST -H "Authorization: Bearer $DO_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"type":"reboot"}' \
  "https://api.digitalocean.com/v2/droplets/<DROPLET_ID>/actions"
```

### 添加域名
```bash
curl -s -X POST -H "Authorization: Bearer $DO_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "example.com"}' \
  "https://api.digitalocean.com/v2/domains"
```

## 注意事项

- 在执行任何可能破坏系统的数据操作（如关闭虚拟机、删除资源）之前，请务必确认操作的正确性。
- 管理操作需要具备读写权限（即`DO_API_TOKEN`需要具有`read/write`权限）。
- API文档请参考：https://docs.digitalocean.com/reference/api/api-reference/