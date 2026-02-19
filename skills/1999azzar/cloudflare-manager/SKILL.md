---
name: cloudflare-manager
description: 管理 Cloudflare 的 DNS 记录、隧道（cloudflared）以及零信任（Zero Trust）策略。可用于解析域名、通过隧道暴露本地服务以及更新入站规则。
metadata: {"openclaw":{"requires":{"bins":["python3","cloudflared"],"env":["CLOUDFLARE_API_TOKEN","CLOUDFLARE_ZONE_ID"]},"install":[{"id":"cf-setup","kind":"exec","command":"bash scripts/install.sh"}]}}
---
# Cloudflare Manager

这是一个用于管理 Cloudflare 基础设施和本地隧道入口的标准化系统。

## 先决条件
- **软件要求**：必须安装 `python3` 和 `cloudflared`。
- **凭据**：需要 `CLOUDFLARE_API_TOKEN`（最低权限的 Zone 访问权限）以及 `CLOUDFLARE_ZONE_ID`。

## 设置
1. 在环境变量或本地的 `.env` 文件中配置凭据。
2. 运行 `bash scripts/install.sh` 命令来初始化本地环境。

## 核心工作流程

### 1. DNS 管理
通过 Cloudflare API 添加、列出或删除 DNS 记录。
- **列出 DNS 记录**：`python3 $WORKSPACE/skills/cloudflare-manager/scripts/cf_manager.py list-dns`
- **添加 DNS 记录**：`python3 $WORKSPACE/skills/cloudflare-manager/scripts/cf_manager.py add-dns --type A --name <subdomain> --content <ip>`

### 2. 本地隧道入口设置
更新 `/etc/cloudflared/config.yml` 文件并重启隧道服务。
- **更新隧道设置**：`python3 $WORKSPACE/skills/cloudflare-manager/scripts/cf_manager.py update-ingress --hostname <host> --service <url>`
- **安全提示**：使用 `--dry-run` 选项在应用配置更改前进行预览。

## 安全性与权限控制
- **sudo 使用**：`update-ingress` 命令需要 `sudo` 权限才能写入系统目录并重启 `cloudflared` 服务。
- **最小权限原则**：根据 `references/sudoers.example` 中的示例配置受限的 `sudo` 访问权限。
- **API 令牌隔离**：确保 API 令牌的权限仅限于特定的 Zone。

## 参考资料
- **sudoers 配置示例**：请参阅 [references/sudoers.example](references/sudoers.example)。
- **隧道配置指南**：请参阅 [references/tunnel-guide.md](references/tunnel-guide.md)。