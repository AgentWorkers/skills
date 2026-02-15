---
name: npm-proxy
description: 管理 Nginx Proxy Manager（NPM）的主机、证书和访问列表。当用户需要添加新域名、将域名指向某个服务器/端口、启用 SSL 或检查代理主机的状态时，可以使用该功能。
---

# NPM 代理技能

通过 Nginx 代理管理器（NPM）的 REST API 进行管理。

## 配置

设置以下环境变量：
- `NPM_URL`：您的 NPM 实例的 URL（例如：`https://npm.example.com`）
- `NPM_EMAIL`：您的 NPM 管理员邮箱
- `NPM_PASSWORD`：您的 NPM 管理员密码

## 使用方法

```bash
# List all proxy hosts
python scripts/npm_client.py hosts

# Get details for a specific host
python scripts/npm_client.py host <host_id>

# Enable/Disable a host
python scripts/npm_client.py enable <host_id>
python scripts/npm_client.py disable <host_id>

# Delete a host
python scripts/npm_client.py delete <host_id>

# List certificates
python scripts/npm_client.py certs
```

## 工作流程

### 添加新的代理主机
要添加新的主机，可以直接使用 `curl` 命令（当前脚本较为简单）。
`POST /api/nginx/proxy-hosts` 的示例请求数据：
```json
{
  "domain_names": ["sub.example.com"],
  "forward_scheme": "http",
  "forward_host": "192.168.1.10",
  "forward_port": 8080,
  "access_list_id": 0,
  "certificate_id": 0,
  "ssl_forced": false,
  "meta": {
    "letsencrypt_email": "",
    "letsencrypt_agree": false,
    "dns_challenge": false
  },
  "advanced_config": "",
  "locations": [],
  "block_exploits": true,
  "caching_enabled": false,
  "allow_websocket_upgrade": true,
  "http2_support": true,
  "hsts_enabled": false,
  "hsts_subdomains": false
}
```

### 启用 SSL（Let's Encrypt）
1. 使用 `certs` 命令列出现有的证书。
2. 使用 `certificate_id` 和 `ssl_forced: true` 参数更新主机配置。