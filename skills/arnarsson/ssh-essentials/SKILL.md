---
name: ssh-essentials
description: 用于安全远程访问、密钥管理、隧道创建和文件传输的基本SSH命令。
homepage: https://www.openssh.com/
metadata: {"clawdbot":{"emoji":"🔐","requires":{"bins":["ssh"]}}}
---

# SSH基础知识

SSH（安全外壳）用于远程访问和安全文件传输。

## 基本连接

### 连接
```bash
# Connect with username
ssh user@hostname

# Connect to specific port
ssh user@hostname -p 2222

# Connect with verbose output
ssh -v user@hostname

# Connect with specific key
ssh -i ~/.ssh/id_rsa user@hostname

# Connect and run command
ssh user@hostname 'ls -la'
ssh user@hostname 'uptime && df -h'
```

### 交互式使用
```bash
# Connect with forwarding agent
ssh -A user@hostname

# Connect with X11 forwarding (GUI apps)
ssh -X user@hostname
ssh -Y user@hostname  # Trusted X11

# Escape sequences (during session)
# ~. - Disconnect
# ~^Z - Suspend SSH
# ~# - List forwarded connections
# ~? - Help
```

## SSH密钥

### 生成密钥
```bash
# Generate RSA key
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# Generate ED25519 key (recommended)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Generate with custom filename
ssh-keygen -t ed25519 -f ~/.ssh/id_myserver

# Generate without passphrase (automation)
ssh-keygen -t ed25519 -N "" -f ~/.ssh/id_deploy
```

### 管理密钥
```bash
# Copy public key to server
ssh-copy-id user@hostname

# Copy specific key
ssh-copy-id -i ~/.ssh/id_rsa.pub user@hostname

# Manual key copy
cat ~/.ssh/id_rsa.pub | ssh user@hostname 'cat >> ~/.ssh/authorized_keys'

# Check key fingerprint
ssh-keygen -lf ~/.ssh/id_rsa.pub

# Change key passphrase
ssh-keygen -p -f ~/.ssh/id_rsa
```

### SSH代理
```bash
# Start ssh-agent
eval $(ssh-agent)

# Add key to agent
ssh-add ~/.ssh/id_rsa

# List keys in agent
ssh-add -l

# Remove key from agent
ssh-add -d ~/.ssh/id_rsa

# Remove all keys
ssh-add -D

# Set key lifetime (seconds)
ssh-add -t 3600 ~/.ssh/id_rsa
```

## 端口转发与隧道

### 本地端口转发
```bash
# Forward local port to remote
ssh -L 8080:localhost:80 user@hostname
# Access via: http://localhost:8080

# Forward to different remote host
ssh -L 8080:database.example.com:5432 user@jumphost
# Access database through jumphost

# Multiple forwards
ssh -L 8080:localhost:80 -L 3306:localhost:3306 user@hostname
```

### 远程端口转发
```bash
# Forward remote port to local
ssh -R 8080:localhost:3000 user@hostname
# Remote server can access localhost:3000 via its port 8080

# Make service accessible from remote
ssh -R 9000:localhost:9000 user@publicserver
```

### 动态端口转发（SOCKS代理）
```bash
# Create SOCKS proxy
ssh -D 1080 user@hostname

# Use with browser or apps
# Configure SOCKS5 proxy: localhost:1080

# With Firefox
firefox --profile $(mktemp -d) \
  --preferences "network.proxy.type=1;network.proxy.socks=localhost;network.proxy.socks_port=1080"
```

### 后台隧道
```bash
# Run in background
ssh -f -N -L 8080:localhost:80 user@hostname

# -f: Background
# -N: No command execution
# -L: Local forward

# Keep alive
ssh -o ServerAliveInterval=60 -L 8080:localhost:80 user@hostname
```

## 配置

### SSH配置文件（`~/.ssh/config`）
```
# Simple host alias
Host myserver
    HostName 192.168.1.100
    User admin
    Port 2222

# With key and options
Host production
    HostName prod.example.com
    User deploy
    IdentityFile ~/.ssh/id_prod
    ForwardAgent yes
    
# Jump host (bastion)
Host internal
    HostName 10.0.0.5
    User admin
    ProxyJump bastion

Host bastion
    HostName bastion.example.com
    User admin

# Wildcard configuration
Host *.example.com
    User admin
    ForwardAgent yes
    
# Keep connections alive
Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3
```

### 使用配置文件
```bash
# Connect using alias
ssh myserver

# Jump through bastion automatically
ssh internal

# Override config options
ssh -o "StrictHostKeyChecking=no" myserver
```

## 文件传输

### SCP（安全复制）
```bash
# Copy file to remote
scp file.txt user@hostname:/path/to/destination/

# Copy file from remote
scp user@hostname:/path/to/file.txt ./local/

# Copy directory recursively
scp -r /local/dir user@hostname:/remote/dir/

# Copy with specific port
scp -P 2222 file.txt user@hostname:/path/

# Copy with compression
scp -C large-file.zip user@hostname:/path/

# Preserve attributes (timestamps, permissions)
scp -p file.txt user@hostname:/path/
```

### SFTP（安全FTP）
```bash
# Connect to SFTP server
sftp user@hostname

# Common SFTP commands:
# pwd          - Remote working directory
# lpwd         - Local working directory
# ls           - List remote files
# lls          - List local files
# cd           - Change remote directory
# lcd          - Change local directory
# get file     - Download file
# put file     - Upload file
# mget *.txt   - Download multiple files
# mput *.jpg   - Upload multiple files
# mkdir dir    - Create remote directory
# rmdir dir    - Remove remote directory
# rm file      - Delete remote file
# exit/bye     - Quit

# Batch mode
sftp -b commands.txt user@hostname
```

### 通过SSH进行Rsync
```bash
# Sync directory
rsync -avz /local/dir/ user@hostname:/remote/dir/

# Sync with progress
rsync -avz --progress /local/dir/ user@hostname:/remote/dir/

# Sync with delete (mirror)
rsync -avz --delete /local/dir/ user@hostname:/remote/dir/

# Exclude patterns
rsync -avz --exclude '*.log' --exclude 'node_modules/' \
  /local/dir/ user@hostname:/remote/dir/

# Custom SSH port
rsync -avz -e "ssh -p 2222" /local/dir/ user@hostname:/remote/dir/

# Dry run
rsync -avz --dry-run /local/dir/ user@hostname:/remote/dir/
```

## 安全最佳实践

### 加强SSH安全性
```bash
# Disable password authentication (edit /etc/ssh/sshd_config)
PasswordAuthentication no
PubkeyAuthentication yes

# Disable root login
PermitRootLogin no

# Change default port
Port 2222

# Use protocol 2 only
Protocol 2

# Limit users
AllowUsers user1 user2

# Restart SSH service
sudo systemctl restart sshd
```

### 连接安全
```bash
# Check host key
ssh-keygen -F hostname

# Remove old host key
ssh-keygen -R hostname

# Strict host key checking
ssh -o StrictHostKeyChecking=yes user@hostname

# Use specific cipher
ssh -c aes256-ctr user@hostname
```

## 故障排除

### 调试
```bash
# Verbose output
ssh -v user@hostname
ssh -vv user@hostname  # More verbose
ssh -vvv user@hostname  # Maximum verbosity

# Test connection
ssh -T user@hostname

# Check permissions
ls -la ~/.ssh/
# Should be: 700 for ~/.ssh, 600 for keys, 644 for .pub files
```

### 常见问题
```bash
# Fix permissions
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub
chmod 644 ~/.ssh/authorized_keys

# Clear known_hosts entry
ssh-keygen -R hostname

# Disable host key checking (not recommended)
ssh -o StrictHostKeyChecking=no user@hostname
```

## 高级操作

### 跳转主机（ProxyJump）
```bash
# Connect through bastion
ssh -J bastion.example.com user@internal.local

# Multiple jumps
ssh -J bastion1,bastion2 user@final-destination

# Using config (see Configuration section above)
ssh internal  # Automatically uses ProxyJump
```

### 多路复用
```bash
# Master connection
ssh -M -S ~/.ssh/control-%r@%h:%p user@hostname

# Reuse connection
ssh -S ~/.ssh/control-user@hostname:22 user@hostname

# In config:
# ControlMaster auto
# ControlPath ~/.ssh/control-%r@%h:%p
# ControlPersist 10m
```

### 执行命令
```bash
# Single command
ssh user@hostname 'uptime'

# Multiple commands
ssh user@hostname 'cd /var/log && tail -n 20 syslog'

# Pipe commands
cat local-script.sh | ssh user@hostname 'bash -s'

# With sudo
ssh -t user@hostname 'sudo command'
```

## 提示

- 使用SSH密钥而非密码
- 对于经常访问的主机，使用`~/.ssh/config`文件进行配置
- 谨慎启用SSH代理转发（存在安全风险）
- 使用ProxyJump访问内部网络
- 保持SSH客户端和服务器的更新
- 使用fail2ban等工具防止暴力攻击
- 监控`/var/log/auth.log`以检测可疑活动
- 使用端口敲击（port knocking）或VPN增强安全性
- 安全地备份SSH密钥
- 为不同用途使用不同的密钥

## 文档资料

官方文档：https://www.openssh.com/manual.html
手册页：`man ssh`、`man ssh_config`、`man sshd_config`