---
name: adguard
description: 通过 HTTP API 控制 AdGuard Home 的 DNS 过滤功能。适用于管理阻止列表/允许列表、检查域名过滤状态、切换保护模式或清除 DNS 缓存等操作。支持阻止/允许特定域名、查看统计信息，以及启用/禁用 DNS 过滤功能。
---

# AdGuard Home 控制器

通过 REST API 从命令行管理 AdGuard Home 的 DNS 过滤功能。

## 前提条件

- AdGuard Home 已经启动并启用了 Web 界面
- 拥有管理员用户名和密码
- 安装了 `curl`（在 macOS/Linux 上通常已默认安装）

## 快速入门

```bash
# Set password once
export ADGUARD_PASSWORD=your_admin_password

# Use commands
./adguard.sh status
./adguard.sh check example.com
./adguard.sh allow broken-site.com
./adguard.sh block malware.ru
```

## 配置

为你的 AdGuard 实例设置环境变量：

```bash
export ADGUARD_URL="http://192.168.1.100:3000"      # Your AdGuard IP and port
export ADGUARD_USERNAME="admin"                     # Usually 'admin' (default)
export ADGUARD_PASSWORD="your_admin_password"       # REQUIRED
```

将配置添加到 `~/.bashrc` 或 `~/.zshrc` 文件中，以便永久生效。

### 配置文件替代方案

（可选）创建 `~/.adguard/config.json` 文件：

```json
{
  "url": "http://192.168.1.100:3000",
  "username": "admin"
}
```

然后单独设置 `ADGUARD_PASSWORD` 以确保安全。

## 命令

### check `<domain>`

检查某个域名当前是否被阻止或允许访问。

```bash
./adguard.sh check doubleclick.net
# ✗ doubleclick.net IS BLOCKED
#   Blocked by: Adblock Plus filter

./adguard.sh check example.com
# ✓ example.com is NOT blocked (allowed)
```

### allow `<domain>` | whitelist `<domain>`

将域名添加到允许列表（白名单）中。此操作会创建一个例外规则，覆盖原有的阻止规则。

```bash
./adguard.sh allow broken-site.com
# ✓ Added rule: @@||broken-site.com^
#   Domain: broken-site.com
#   Action: allow
```

### block `<domain>` | blacklist `<domain>`

将域名添加到阻止列表中。此操作会创建一个自定义的阻止规则。

```bash
./adguard.sh block spyware-domain.ru
# ✓ Added rule: ||spyware-domain.ru^
#   Domain: spyware-domain.ru
#   Action: block
```

### status | stats

显示 DNS 过滤统计信息和保护状态。

```bash
./adguard.sh status
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# AdGuard Home Status
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Protection: ✓ ENABLED
# 
# DNS Queries: 1,234
# Blocked by rules: 156
# Blocked by safe browsing: 23
# Safe search replacements: 5
# Block rate: 14%
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### toggle | protection

启用或禁用 DNS 保护功能。这有助于暂时关闭过滤功能以进行故障排查。

```bash
./adguard.sh toggle
# Disabling protection...
# ✓ Protection is now false
```

### cache-clear

清除 DNS 缓存，以便立即应用规则更改。

```bash
./adguard.sh cache-clear
# Clearing DNS cache...
# ✓ Cache cleared
```

## 查找 AdGuard Home 设备

如果你不知道 AdGuard 的 URL：

1. **路由器管理面板** — 查找名为 “AdGuard Home” 的设备，或检查端口 3000 是否被占用
2. **本地网络扫描** — 使用 `nmap` 或查看 “连接设备” 列表
3. **如果设备运行在同一台机器上** — 默认地址是 `http://localhost:3000`
4. **使用 mDNS/Bonjour** — 尝试 `http://adguard-home.local:3000`（具体取决于网络配置）

## 过滤规则语法

AdGuard 使用以下 DNS 过滤规则语法：

| 规则 | 功能 |
|------|--------|
| `\|\|example.com^` | 阻止 example.com 及其子域名 |
| `@@\|\|example.com^` | 允许 example.com 访问（作为例外/白名单） |
| `example.com` | 仅阻止 example.com 这个域名 |
| `\|\|ad.example.com^` | 仅阻止 ad.example.com 这个域名 |

有关完整的语法说明，请参阅 [API 参考文档](references/api.md)。

## 常见场景

### 允许被误阻止的网站访问

```bash
adguard.sh allow my-bank.com
```

### 阻止已知的恶意软件域名

```bash
adguard.sh block malicious-tracker.xyz
```

### 检查某个域名是否被过滤

```bash
adguard.sh check ads.google.com
```

### 查看今日的统计信息

```bash
adguard.sh status
```

### 暂时关闭过滤功能（例如用于故障排查）

```bash
adguard.sh toggle
```

## 故障排除

**错误：身份验证失败**
→ 确保 `ADGUARD_PASSWORD` 设置正确
→ 验证 `ADGUARD_URL` 是否指向正确的 IP 和端口

**错误：API 调用失败（HTTP 401）**
→ 身份验证失败，请检查凭据

**规则未生效**
→ 运行 `adguard.sh cache-clear` 清除 DNS 缓存
→ 等待 5 分钟以上，让客户端刷新缓存
→ 重启设备的网络连接

**无法连接到 AdGuard**
→ 确认设备在同一网络内
→ 检查防火墙是否阻止了端口 3000
→ 使用 `ping <ip>` 测试设备是否可访问

## 高级功能：批量操作

- 批量阻止多个域名：```bash
for domain in tracker1.com tracker2.com tracker3.com; do
    adguard.sh block "$domain"
done
```
- 批量检查多个域名：```bash
for domain in example.com test.org my-site.net; do
    echo "Checking $domain..."
    adguard.sh check "$domain"
done
```

## API 参考文档

有关 AdGuard Home 的完整 API 文档，请参阅 [references/api.md]。