---
name: vps-command-runner
description: >
  **同时运行多个VPS上的命令**  
  您可以从一个地方执行SSH命令、部署更新、查看日志以及管理所有服务器上的服务。这非常适合在管理多个VPS时使用，无论是需要在所有主机上运行命令、检查分布式服务的状态，还是将更改部署到多台服务器上。
---
# VPS命令执行器

能够同时在整个VPS集群中执行命令。

## VPS清单

| 主机 | IP地址 | 用户名 | 提供的服务 |
|------|---------|---------|------------|
| 内部主机 | [已屏蔽] | [已屏蔽] | Gateway、Nextcloud、其他服务 |
| VPS1（德国） | [已屏蔽] | [已屏蔽] | 提供商服务、Nextcloud |
| VPS2（美国） | [已屏蔽] | [已屏蔽] | WireGuard、提供商服务、Nextcloud |

## 设置

编辑脚本以添加您的登录凭据：

```bash
# Set these variables in each script:
USER="your-username"
PASS="your-password"

# Or use SSH keys:
# Add keys to ~/.ssh/ and modify scripts to use key auth
```

## 快速使用方法

```bash
# Run command on all VPS
~/.openclaw/workspace/skills/vps-command-runner/scripts/run-all.sh "docker ps"

# Run command on specific VPS
~/.openclaw/workspace/skills/vps-command-runner/scripts/run.sh [IP] "systemctl status docker"

# Check provider status everywhere
~/.openclaw/workspace/skills/vps-command-runner/scripts/run-all.sh "docker ps --filter name=urnetwork --format \"{{.Names}}\" | wc -l"

# Update all providers
~/.openclaw/workspace/skills/vps-command-runner/scripts/run-all.sh "docker pull bringyour/community-provider:g4-latest"
```

## 脚本说明

- `run-all.sh <命令>` — 在所有VPS上执行该命令
- `run.sh <IP地址> <命令>` — 在指定的VPS上执行该命令
- `status.sh` — 快速检查所有VPS的运行状态

## SSH设置

默认设置：密码认证（请编辑脚本以更改）

对于基于密钥的认证：
1. 将密钥添加到`~/.ssh/`目录中
2. 修改脚本，使用`ssh -i ~/.ssh/密钥文件...`代替`sshpass`进行登录