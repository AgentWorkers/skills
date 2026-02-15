---
description: 使用简单的命令来设置和管理 SSH 隧道、端口转发以及 SOCKS 代理。
---

# 端口转发器

用于设置和管理 SSH 隧道及端口转发功能。

**适用场景**：创建 SSH 隧道、转发端口或配置 SOCKS 代理时使用。

## 必备条件

- OpenSSH 客户端（`ssh`）
- 可选：`autossh`（用于创建持久性隧道）
- 不需要 API 密钥

## 使用说明

### 本地端口转发
将远程服务访问方式设置为本地服务：
```bash
# Forward local:8080 → remote:80
ssh -fNL 8080:localhost:80 user@remote-host

# Access a service behind a jump host
ssh -fNL 5432:db-server:5432 user@jump-host

# Bind to all interfaces (not just localhost)
ssh -fNL 0.0.0.0:8080:localhost:80 user@remote-host
```

### 远程端口转发
在远程主机上暴露本地服务：
```bash
# Expose local:3000 on remote:9000
ssh -fNR 9000:localhost:3000 user@remote-host
```

### 动态 SOCKS 代理
将所有网络流量路由通过远程主机：
```bash
ssh -fND 1080 user@remote-host
# Configure browser: SOCKS5 proxy → localhost:1080
```

### SSH 配置参数说明

| 参数 | 含义 |
|------|---------|
| `-f` | 验证身份后在后台运行 |
| `-N` | 不执行远程命令（仅建立隧道） |
| `-L` | 本地端口转发 |
| `-R` | 远程端口转发 |
| `-D` | 动态 SOCKS 代理 |
| `-o ServerAliveInterval=60` | 每 60 秒发送一次心跳请求 |
| `-o ExitOnForwardFailure=yes` | 如果端口绑定失败则终止连接 |

### 管理命令
```bash
# List active SSH tunnels
ps aux | grep 'ssh -[fN]' | grep -v grep

# Test if a forwarded port works
nc -zv localhost 8080
curl -s http://localhost:8080

# Kill a specific tunnel
kill <PID>

# Kill all SSH tunnels
pkill -f 'ssh -fN'
```

### 使用 `autossh` 创建持久性隧道
```bash
# Auto-reconnect on failure
autossh -M 0 -fNL 8080:localhost:80 user@remote-host \
  -o "ServerAliveInterval=30" \
  -o "ServerAliveCountMax=3"

# As a systemd service
# Create /etc/systemd/system/ssh-tunnel.service
```

## 隧道状态输出格式
用于显示隧道状态的信息：
```
## 🔌 Active SSH Tunnels
| PID | Type | Local | Remote | Host | Status |
|-----|------|-------|--------|------|--------|
| 1234 | Local | :8080 | :80 | server1 | 🟢 Active |
| 5678 | SOCKS | :1080 | — | proxy1 | 🟢 Active |
```

## 注意事项

- **端口已被占用**：可以使用 `lsof -i :8080` 或 `ss -tlnp | grep 8080` 检查。
- **连接中断**：添加 `-o ServerAliveInterval=60 -o ServerAliveCountMax=3` 以保持连接。或使用 `autossh`。
- **权限问题**：确保 SSH 密钥已正确配置（检查 `~/.ssh/config`）。
- **远程端口转发被阻止**：服务器的 `/etc/ssh/sshd_config` 文件中需要设置 `GatewayPorts yes`。
- **隧道可用但服务无响应**：可能是远程服务仅监听本地地址（localhost）。

## 安全提示

- **切勿将敏感端口转发到 `0.0.0.0`**（除非有特殊需求），否则会导致所有网络接口均可访问该端口。
- 使用 SSH 密钥进行身份验证，避免使用密码。
- 对不需要的服务器禁用远程端口转发功能。
- 定期监控活跃的隧道，避免长时间未使用的隧道成为安全风险。