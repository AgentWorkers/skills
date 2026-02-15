---
name: ssh-tunnel
description: SSH隧道、端口转发以及远程访问相关技术。这些功能在设置本地/远程/动态端口转发、配置跳板主机、管理SSH密钥、多路复用连接、使用scp/rsync传输文件，或调试SSH连接问题时非常有用。
metadata: {"clawdbot":{"emoji":"🔑","requires":{"bins":["ssh"]},"os":["linux","darwin","win32"]}}
---

# SSH隧道

SSH隧道技术包括端口转发和安全的远程访问功能。本文涵盖了本地/远程/动态端口转发、跳转主机、ProxyCommand命令、连接复用、密钥管理以及连接调试等内容。

## 使用场景

- 通过防火墙访问远程数据库（本地端口转发）
- 将本地开发服务器暴露给远程机器（远程端口转发）
- 使用远程服务器作为SOCKS代理（动态端口转发）
- 通过跳转主机或堡垒主机进行连接
- 管理SSH密钥和代理转发设置
- 安全传输文件（使用scp、rsync命令）
- 调试SSH连接故障

## 端口转发

### 本地端口转发（在本地访问远程服务）

```bash
# Forward local port 5432 to remote's localhost:5432
# Use case: access a remote PostgreSQL database as if it were local
ssh -L 5432:localhost:5432 user@remote-server

# Then connect locally:
psql -h localhost -p 5432 -U dbuser mydb

# Forward to a different host accessible from the remote
# Remote server can reach db.internal:5432, but you can't
ssh -L 5432:db.internal:5432 user@remote-server

# Forward multiple ports
ssh -L 5432:db.internal:5432 -L 6379:redis.internal:6379 user@remote-server

# Run in background (no shell)
ssh -fNL 5432:db.internal:5432 user@remote-server
# -f = background after auth
# -N = no remote command
# -L = local forward
```

### 远程端口转发（在远程机器上访问本地服务）

```bash
# Make your local port 3000 accessible on the remote server's port 8080
ssh -R 8080:localhost:3000 user@remote-server
# On the remote: curl http://localhost:8080 → hits your local :3000

# Expose to all interfaces on the remote (not just localhost)
# Requires GatewayPorts yes in remote sshd_config
ssh -R 0.0.0.0:8080:localhost:3000 user@remote-server

# Background mode
ssh -fNR 8080:localhost:3000 user@remote-server
```

### 动态端口转发（SOCKS代理）

```bash
# Create a SOCKS5 proxy on local port 1080
ssh -D 1080 user@remote-server

# Route browser traffic through the tunnel
# Configure browser proxy: SOCKS5, localhost:1080

# Use with curl
curl --socks5-hostname localhost:1080 https://example.com

# Background mode
ssh -fND 1080 user@remote-server
```

## 跳转主机/堡垒主机

### ProxyJump（最简单的方法，适用于OpenSSH 7.3及以上版本）

```bash
# Connect through a bastion host
ssh -J bastion-user@bastion.example.com target-user@internal-server

# Chain multiple jumps
ssh -J bastion1,bastion2 target-user@internal-server

# With port forward through bastion
ssh -J bastion-user@bastion -L 5432:db.internal:5432 target-user@app-server
```

### ProxyCommand（适用于旧版本系统，功能更灵活）

```bash
# Equivalent to ProxyJump but works on older OpenSSH
ssh -o ProxyCommand="ssh -W %h:%p bastion-user@bastion" target-user@internal-server
```

### 配置跳转主机的SSH设置

```
# ~/.ssh/config

# Bastion host
Host bastion
    HostName bastion.example.com
    User bastion-user
    IdentityFile ~/.ssh/bastion_key

# Internal servers (automatically use bastion)
Host app-server
    HostName 10.0.1.50
    User deploy
    ProxyJump bastion

Host db-server
    HostName 10.0.2.30
    User admin
    ProxyJump bastion
    LocalForward 5432 localhost:5432

# Now just: ssh app-server
# Or: ssh db-server (auto-forwards port 5432)
```

## SSH配置模式

### 基本配置

```
# ~/.ssh/config

# Global defaults
Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3
    AddKeysToAgent yes
    IdentitiesOnly yes

# Named hosts
Host prod
    HostName 203.0.113.50
    User deploy
    IdentityFile ~/.ssh/prod_ed25519
    Port 2222

Host staging
    HostName staging.example.com
    User deploy
    IdentityFile ~/.ssh/staging_ed25519

# Wildcard patterns
Host *.dev.example.com
    User developer
    IdentityFile ~/.ssh/dev_key
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null
```

### 连接复用（重用已建立的SSH连接）

```
# ~/.ssh/config
Host *
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%r@%h-%p
    ControlPersist 600

# First connection opens socket, subsequent connections reuse it
# Much faster for repeated ssh/scp/rsync to same host
```

### 连接复用（ControlMaster模式）

```bash
# Create socket directory
mkdir -p ~/.ssh/sockets

# Manually manage control socket
ssh -O check prod       # Check if connection is alive
ssh -O stop prod        # Close the master connection
ssh -O exit prod        # Close immediately
```

## 密钥管理

### 生成SSH密钥对

```bash
# Ed25519 (recommended — fast, secure, short keys)
ssh-keygen -t ed25519 -C "user@machine" -f ~/.ssh/mykey_ed25519

# RSA 4096 (wider compatibility)
ssh-keygen -t rsa -b 4096 -C "user@machine" -f ~/.ssh/mykey_rsa

# Generate without passphrase (for automation only)
ssh-keygen -t ed25519 -N "" -f ~/.ssh/deploy_key
```

### 部署SSH密钥

```bash
# Copy public key to remote server
ssh-copy-id -i ~/.ssh/mykey_ed25519.pub user@remote-server

# Manual (if ssh-copy-id unavailable)
cat ~/.ssh/mykey_ed25519.pub | ssh user@remote-server "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

### SSH代理

```bash
# Start agent (usually auto-started)
eval "$(ssh-agent -s)"

# Add key to agent
ssh-add ~/.ssh/mykey_ed25519

# Add with expiry (key removed after timeout)
ssh-add -t 3600 ~/.ssh/mykey_ed25519

# List loaded keys
ssh-add -l

# Remove all keys
ssh-add -D

# Agent forwarding (use your local keys on remote hosts)
ssh -A user@remote-server
# On remote: ssh git@github.com  → uses your local key
# SECURITY: only forward to trusted hosts
```

### 文件权限设置

```bash
# SSH is strict about permissions. Fix common issues:
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519          # Private key
chmod 644 ~/.ssh/id_ed25519.pub      # Public key
chmod 600 ~/.ssh/config
chmod 600 ~/.ssh/authorized_keys
```

## 文件传输

### 使用scp命令传输文件

```bash
# Copy file to remote
scp file.txt user@remote:/path/to/destination/

# Copy from remote
scp user@remote:/path/to/file.txt ./local/

# Copy directory recursively
scp -r ./local-dir user@remote:/path/to/

# Through jump host
scp -o ProxyJump=bastion file.txt user@internal:/path/

# With specific key and port
scp -i ~/.ssh/mykey -P 2222 file.txt user@remote:/path/
```

### 通过SSH使用rsync命令传输文件

```bash
# Sync directory (only changed files)
rsync -avz ./local-dir/ user@remote:/path/to/remote-dir/

# Dry run (preview changes)
rsync -avzn ./local-dir/ user@remote:/path/to/remote-dir/

# Delete files on remote that don't exist locally
rsync -avz --delete ./local-dir/ user@remote:/path/to/remote-dir/

# Exclude patterns
rsync -avz --exclude='node_modules' --exclude='.git' ./project/ user@remote:/deploy/

# With specific SSH options
rsync -avz -e "ssh -i ~/.ssh/deploy_key -p 2222" ./dist/ user@remote:/var/www/

# Resume interrupted transfer
rsync -avz --partial --progress large-file.tar.gz user@remote:/path/

# Through jump host
rsync -avz -e "ssh -J bastion" ./files/ user@internal:/path/
```

## 连接调试

### 查看详细连接日志

```bash
# Increasing verbosity levels
ssh -v user@remote       # Basic debug
ssh -vv user@remote      # More detail
ssh -vvv user@remote     # Maximum detail

# Common issues visible in verbose output:
# "Connection refused" → SSH server not running or wrong port
# "Connection timed out" → Firewall blocking, wrong IP
# "Permission denied (publickey)" → Key not accepted
# "Host key verification failed" → Server fingerprint changed
```

### 测试连接是否正常

```bash
# Check if SSH port is open
nc -zv remote-host 22
# or
ssh -o ConnectTimeout=5 -o BatchMode=yes user@remote echo ok

# Check which key the server accepts
ssh -o PreferredAuthentications=publickey -v user@remote 2>&1 | grep "Offering\|Accepted"

# Test config without connecting
ssh -G remote-host   # Print effective config for this host
```

### 常见问题解决方法

```bash
# "WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED"
# Server was reinstalled / IP reassigned
ssh-keygen -R remote-host   # Remove old fingerprint
ssh user@remote-host        # Accept new fingerprint

# "Too many authentication failures"
# SSH agent is offering too many keys
ssh -o IdentitiesOnly=yes -i ~/.ssh/specific_key user@remote

# "Connection closed by remote host"
# Often: MaxSessions or MaxStartups limit on server
# Or: fail2ban banned your IP

# Tunnel keeps dying
# Add keepalive in config or command line:
ssh -o ServerAliveInterval=30 -o ServerAliveCountMax=5 user@remote

# Permission denied despite correct key
# Check remote: /var/log/auth.log or /var/log/secure
# Common: wrong permissions on ~/.ssh or authorized_keys
```

### 强制结束卡住的SSH会话

```
# If SSH session hangs (frozen terminal):
# Type these characters in sequence:
~.          # Disconnect
~?          # Show escape commands
~#          # List forwarded connections
~&          # Background SSH (when waiting for tunnel to close)
# The ~ must be the first character on a new line (press Enter first)
```

## 使用建议

- 尽量使用`~/.ssh/config`文件来配置SSH参数。使用命名主机可以简化配置过程，减少输入错误的风险。
- 推荐使用Ed25519加密算法生成的密钥，因为它们更短、传输速度更快，且安全性相当。
- 启用连接复用功能（`ControlMaster`）可以显著提高连接效率。建议全局启用该功能。
- 对于多文件传输，`rsync`通常比`scp`更高效：它能够处理传输中断、仅传输文件变化内容，并支持压缩。
- 虽然SSH代理（`-A`选项）使用方便，但在不可信的服务器上可能存在安全风险。建议优先使用ProxyJump模式。
- 配置`ServerAliveInterval 60`可以避免因网络问题导致的连接中断。
- 保持`~/.ssh/config`文件的结构清晰，并添加适当的注释，以便后续维护。
- 使用`~.`通配符是结束卡住的SSH会话的唯一方法，而无需关闭终端窗口。

## 其他注意事项

- 使用`~/.ssh/config`文件可以简化SSH配置，提高效率并减少错误。
- Ed25519密钥比RSA密钥更安全、传输速度更快。
- 启用连接复用功能可以显著提升连接效率。
- `rsync`在处理多文件传输时性能优于`scp`，且支持中断处理和压缩。
- 在不可信的服务器上使用SSH代理可能存在安全风险，建议优先使用ProxyJump模式。
- 配置`ServerAliveInterval`可以防止因网络问题导致的连接中断。
- 保持`~/.ssh/config`文件的结构清晰和注释有助于后续维护。