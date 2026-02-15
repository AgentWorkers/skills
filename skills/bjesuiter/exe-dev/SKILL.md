---
name: exe-dev
description: 在 exe.dev 上管理持久化虚拟机（Persistent VMs）。您可以创建虚拟机、配置 HTTP 代理、共享访问权限，并设置自定义域名。这些功能适用于在 exe.dev 上使用虚拟机进行托管、开发或运行持久化服务。
author: Benjamin Jesuiter
---

> ⚠️ **警告：** 此功能是由 clawdbot 根据 exe.dev 的 markdown 文档自动生成的，尚未经过测试——请谨慎使用！我计划尽快对其进行测试。 🔜

# exe.dev 虚拟机管理

## 快速命令

| 任务 | 命令 |
|------|---------|
| 列出虚拟机 | `ssh exe.dev ls --json` |
| 创建虚拟机 | `ssh exe.dev new` |
| 将虚拟机设为公共状态 | `ssh exe.dev share set-public <vm>` |
| 更改端口 | `ssh exe.dev share port <vm> <port>` |
| 添加用户 | `ssh exe.dev share add <vm> <email>` |
| 共享链接 | `ssh exe.dev share add-link <vm>` |

## 访问地址

- **虚拟机**: `https://<vmname>.exe.xyz/`
- **Shelley 代理**: `https://<vmname>.exe.xyz:9999/`
- **VSCode**: `vscode://vscode-remote/ssh-remote+<vmname>.exe.xyz/home/exedev`

## 代理配置

默认端口会从 Dockerfile 的 `EXPOSE` 指令中自动选择。如需更改，请使用以下命令：
```bash
ssh exe.dev share port <vmname> <port>
```

可以通过 `https://vmname.exe.xyz:<port>/` 访问 3000-9999 端口的资源。

## 身份验证头部信息

当用户通过 exe.dev 进行身份验证时，会发送以下头部信息：
- `X-ExeDev-UserID` — 用户标识符
- `X-ExeDev-Email` — 用户邮箱

在测试过程中，可以使用 mitmproxy 来注入这些头部信息：
```bash
mitmdump --mode reverse:http://localhost:8000 --listen-port 3000 \
  --set modify_headers='/~q/X-ExeDev-Email/user@example.com'
```

## 自定义域名

- **子域名**: 使用 CNAME 将 `app.example.com` 映射到 `vmname.exe.xyz`
- **顶级域名 (Apex)**: 使用 ALIAS 将 `example.com` 映射到 `exe.xyz`，并使用 CNAME 将 `www` 映射到 `vmname.exe.xyz`

## 完整文档

有关定价、Shelley 代理设置、SSH 密钥配置及常见问题的详细信息，请参阅 [references/exe-dev-vm-service.md](exe-dev-vm-service.md)。