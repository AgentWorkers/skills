---
name: cloudflare-manager
description: 管理 Cloudflare 的 DNS 记录、隧道（cloudflared）以及零信任（Zero Trust）策略。适用于用户需要“指向某个域名”、“暴露本地主机（localhost）”或“阻止特定 IP 地址”的场景。
---

# Cloudflare Manager

## 配置
需要以下环境变量（位于 `.env` 文件中）：

| 变量 | 说明 | 是否必需？ |
| :--- | :--- | :--- |
| `CLOUDFLARE_API_TOKEN` | 具有 Zone.DNS 权限的 API 令牌 | 是 |
| `CLOUDFLARE_ZONE_ID` | 需要管理的区域 ID | 是 |

**旧版本支持**：也支持使用 `CF_API_TOKEN` 和 `CF_ZONE_ID`。

## 安装
本功能需要依赖 Python 库（`requests`、`PyYAML`）。运行安装脚本以创建本地虚拟环境：
```bash
./scripts/install.sh
```

## 使用方法
- **适用角色**：云工程师（Cloud Engineer）。
- **触发条件**：执行“创建 DNS 记录”（Create DNS record）、“设置隧道”（Setup tunnel）或“开放端口 3000”（Expose port 3000）等操作。
- **输出结果**：以 JSON 格式返回状态信息或 CLI 命令的执行结果。

### 命令
#### `scripts/cf_manager.py`
这是主要的 CLI 工具。请使用 `venv python` 来运行该脚本。

**语法**：
```bash
.venv/bin/python3 scripts/cf_manager.py [OPTIONS] <COMMAND>
```

**选项**：
- `--dry-run`：模拟操作，不实际应用任何更改（不修改 DNS 或 Ingress 设置）。

**示例**：
```bash
# List DNS Records
.venv/bin/python3 scripts/cf_manager.py list-dns

# Add DNS Record
.venv/bin/python3 scripts/cf_manager.py add-dns --type A --name subdomain --content 1.2.3.4

# Update Ingress (Tunnel)
.venv/bin/python3 scripts/cf_manager.py update-ingress --hostname app.example.com --service http://localhost:3000
```

## 安全性与权限
- **API 令牌权限**：遵循“最小权限原则”（Principle of Least Privilege）。仅为特定区域创建具有 `Zone:DNS:Edit` 和 `Zone:Settings:Edit` 权限的 API 令牌。避免使用全局 API 密钥。
- **高级操作**：
  - `update-ingress` 命令会修改 `/etc/cloudflared/config.yml` 文件并重启服务。
  - **sudo 权限**：运行 `tee` 和 `systemctl` 命令需要 `sudo` 权限。
- **权限限制**：切勿授予完整的 `sudo` 权限。请参考 `references/sudoers.example` 中的示例，将 `sudo` 权限限制在仅必要的命令上。
- **安全措施**：使用 `--dry-run` 选项预览配置更改，避免将更改写入磁盘或重启服务。

## 功能概述
1. **DNS 管理**：添加、编辑和删除 A/CNAME 记录。
2. **隧道管理**：配置 Cloudflare 隧道（需要 `sudo` 权限）。
3. **安全设置**：管理访问策略和 WAF 规则。

## 参考资料
- [隧道使用指南](references/tunnel-guide.md)