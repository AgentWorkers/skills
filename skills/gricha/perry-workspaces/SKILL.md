---
name: perry-workspaces
description: 在您的 Tailnet 环境中，使用已预安装的 Claude Code 和 OpenCode 工具来创建和管理隔离的 Docker 工作空间。这些工作空间适用于与 Perry 工作空间协同工作、连接编码代理或管理远程开发环境。
---

# Perry Workspaces

Perry Workspaces提供隔离的Docker工作环境，这些工作环境中预先安装了编程代理工具。

## 命令
```bash
perry start <name> --clone git@github.com:user/repo.git  # Create
perry ls                                                  # List
perry stop <name>                                         # Stop
perry remove <name>                                       # Delete
perry shell <name>                                        # Interactive shell
```

## SSH访问
```bash
ssh workspace@<name>        # User is always 'workspace'
ssh workspace@<IP>          # Use IP if MagicDNS fails
```

## 编程代理
- **OpenCode**：通过`http://<workspace>:4096`访问（Web UI）或通过CLI进行连接
- **Claude Code**：在 workspace shell（`perry shell`）中运行`claude`命令

## 项目存储位置
项目会被克隆到`~/<name>`目录中，而不是`/workspace`目录：
```bash
cd ~/my-project  # Correct
```

## 故障排除
- **无法连接**：检查`tailscale status`的状态，使用IP地址而非主机名进行连接
- **SSH连接失败**：用户必须使用`workspace`用户身份，而不是本地用户身份
- **启动缓慢**：通过Web UI查看项目进度