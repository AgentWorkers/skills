# AdGuard Home Skill

🛡️ 查询 AdGuard Home 实例的 DNS 统计信息、被阻止的域名以及客户端活动

---

## 功能

- ✅ 支持多个实例
- ✅ 实时 DNS 查询统计
- ✅ 被阻止域名的排行榜
- ✅ 活动客户端分析
- ✅ 系统健康状态检查
- ✅ 服务状态监控
- ✅ DNS 配置详情
- ✅ 过滤规则检查
- ✅ 最近的查询日志
- ✅ TLS/加密状态

---

## 使用方法

### 基本命令

```bash
# Statistics & Monitoring
/adguard stats [instance]           # DNS statistics
/adguard top-clients [instance]     # Top 10 active clients
/adguard top-blocked [instance]     # Top 10 blocked domains
/adguard health [instance]          # Health check
/adguard status [instance]          # Service status

# Configuration & Rules
/adguard dns-info [instance]        # DNS configuration
/adguard filter-rules [instance]    # Filter rules and lists
/adguard clients [instance]         # Configured clients
/adguard tls-status [instance]      # TLS/encryption status

# Query Log
/adguard querylog [instance] [n]    # Recent n queries (default: 10)
```

### 示例

```bash
# Query dns1 instance statistics
/adguard stats dns1

# Check service status
/adguard status dns1

# View DNS configuration
/adguard dns-info dns1

# View filter rules
/adguard filter-rules dns1

# View last 20 DNS queries
/adguard querylog dns1 20

# Check TLS status
/adguard tls-status dns1

# If no instance specified, uses the first configured instance
/adguard stats
```

### 输出示例

**stats 命令：**
```
📊 AdGuard Home Statistics (dns1)
Total DNS Queries: 141,647
Blocked Requests: 32,540 (23.0%)
Avg Response Time: 0.005ms
```

**status 命令：**
```
🔧 AdGuard Home Status (dns1)
Version: v0.107.72
Running: ✅ Yes
Protection: ✅ Enabled
DNS Port: 53
HTTP Port: 1080
Language: zh-cn
DHCP Available: ✅ Yes
```

**dns-info 命令：**
```
🌐 DNS Configuration (dns1)
Protection: ✅ Enabled
Rate Limit: 20 req/s
Upstream Mode: parallel
Cache: ✅ 4MB
DNSSEC: ❌ Disabled
IPv6: ✅ Enabled

Upstream DNS Servers:
  1. https://dns.alidns.com/dns-query
  2. 192.168.1.1:53
  3. 8.8.8.8:53
```

**filter-rules 命令：**
```
🛡️ Filter Rules (dns1)
Filtering: ✅ Enabled
Update Interval: 12 hours
User Rules: 6 custom rules

Filter Lists:
  1. ✅ AdAway Default Blocklist (6540 rules)
  2. ✅ gh_100M_block (1110461 rules)
  3. ✅ Delta Force Blacklist (78126 rules)
```

**querylog 命令：**
```
📜 Recent DNS Queries (dns1) - Last 5 entries

1. [12:26:44 AM] 🚫 BLOCKED api.telegram.org (192.168.145.188)
2. [12:26:43 AM] 🚫 BLOCKED self.events.data.microsoft.com (192.168.145.123)
   Rule: ||events.data.microsoft.com^
3. [12:26:42 AM] ✅ OK open.feishu.cn (192.168.145.188)
```

---

## 配置

### 🔒 安全最佳实践

**⚠️ 重要提示：** 请勿在文件中存储明文凭证。始终使用安全的凭证注入方式：

#### 选项 1：环境变量（推荐）

在运行命令之前设置环境变量：

```bash
export ADGUARD_URL="http://192.168.145.249:1080"
export ADGUARD_USERNAME="admin"
export ADGUARD_PASSWORD="your-secure-password"
```

将以下内容添加到您的 shell 配置文件（`~/.bashrc` 或 `~/.zshrc`）中以实现持久化配置。

#### 选项 2：1Password CLI（最安全）

使用 `op read` 在运行时注入凭证：

```bash
export ADGUARD_URL=$(op read "op://vault/AdGuard/url")
export ADGUARD_USERNAME=$(op read "op://vault/AdGuard/username")
export ADGUARD_PASSWORD=$(op read "op://vault/AdGuard/password")
```

**❌ 已弃用：基于文件的配置**

旧版本允许创建包含凭证的 `adguard-instances.json` 文件。**由于存在意外提交和明文存储的风险，此方法不再被支持**。请切换到使用环境变量或 1Password。

---

## 配置参数

| 参数 | 描述 | 示例 |
|-----------|-------------|---------|
| `url` | AdGuard Home 的 URL（包含端口） | `http://192.168.145.249:1080` |
| `username` | 管理员用户名 | `admin` |
| `password` | 管理员密码（使用环境变量或 secrets manager） | `your-secure-password` |

---

## 技术细节

- **认证方式：** 基于 Cookie（POST `/control/login`）
- **数据 API：** GET `/control/*` 端点
- **运行时语言：** Node.js（使用 ES 模块）
- **入口文件：** `index.js`

### 使用的 API 端点

- `/control/stats` - 统计数据
- `/control/status` - 服务状态
- `/control/dns_info` - DNS 配置
- `/control/filtering/status` - 过滤规则
- `/control/querylog` - 查询日志
- `/control/clients` - 客户端管理
- `/control/tls/status` - TLS 状态

---

## 常见问题解答

**Q：** 出现 “未配置 AdGuard 实例” 错误？**
A：在运行命令之前设置环境变量：
```bash
export ADGUARD_URL="http://your-adguard:1080"
export ADGUARD_USERNAME="admin"
export ADGUARD_PASSWORD="your-password"
```
或者使用 1Password CLI 来安全地注入凭证。

---

**Q：** 查询时出现认证错误？**
A：请检查用户名和密码是否正确，并确保 AdGuard Home 服务正在运行。

---

**Q：** 如何添加更多实例？**
A：使用 secrets manager（如 1Password）来存储多个实例的凭证，或者通过设置不同的 `ADGUARD_URL` 值在多个实例之间切换。对于高级的多实例设置，可以考虑使用不同的 shell 会话并配置不同的环境变量。

---

**Q：** 为什么查询日志没有显示数据？**
A：请确保在 AdGuard Home 的设置中启用了查询日志功能（设置 → DNS 设置 → 查询日志）。

---

## 版本历史

### v1.2.6 (2026-02-25) - 移除基于文件的配置选项 🔧

**错误修复：**
- ✅ 修复了常见问题解答中的不一致之处 - 移除了 “如何添加更多实例？” 部分中对 `adguard-instances.json` 的引用
- ✅ 文档与代码保持一致 - 所有文档现在都遵循仅使用环境变量的实现方式（v1.2.2 及更高版本）
- ✅ 更新了多实例配置的说明 - 明确介绍了使用 1Password 或不同 shell 会话的方法

### v1.2.5 (2026-02-25) - 修复注册表元数据 🔧

**错误修复：**
- ✅ 修复了注册表元数据问题 - `clawhub.json` 现在正确地声明了 `requires.env`，其中包含 `ADGUARD_URL`、`ADGUARD_USERNAME` 和 `ADGUARD_PASSWORD`
- ✅ 设置了 `primaryEnv` - ClawHub 现在会显示环境变量为必需项
- ✅ 更新了安全说明 - 修复了文档中的元数据问题

### v1.2.2 (2026-02-25) - 移除基于文件的凭证配置 🔐

**安全改进：**
- ✅ 移除了基于文件的配置选项 - 不再支持使用包含明文凭证的 `adguard-instances.json` 文件
- ✅ 仅支持环境变量 - 凭证必须通过环境变量或 1Password 提供
- ✅ 更新了常见问题解答 - 移除了关于创建配置文件的说明
- ✅ 更明确的警告 - 明确指出基于文件的配置已弃用且不受支持

### v1.2.1 (2026-02-25) - 提升凭证安全性 🔐

**安全改进：**
- ✅ 移除了明文凭证的存储方式 - 不再建议创建包含管理员凭证的配置文件
- ✅ 支持使用环境变量 - 通过 `ADGUARD_URL`、`ADGUARD_USERNAME` 和 `ADGUARD_PASSWORD` 安全地注入凭证
- ✅ 集成 1Password - 支持使用 `op read` 进行凭证管理
- ✅ 移除了多路径搜索 - 不再搜索 `~/.openclaw-*/workspace/` 路径
- ✅ 配置文件仅限在工作区使用（开发环境）
- ✅ 更新了文档 - 更突出了安全最佳实践

### v1.2.0 (2026-02-24) - 加强安全性 🔒

**安全改进：**
- ✅ 修复了命令注入漏洞 - 将 `execSync` 和 `curl` 替换为原生的 HTTPS 客户端
- ✅ 输入验证 - 对实例名称、命令和参数进行了清理
- ✅ 命令白名单 - 只允许执行指定的命令
- ✅ URL 验证 - 在发送请求前验证 URL 格式
- ✅ 参数限制 - 将查询日志的条目数量限制在 1-100 条之间
- ✅ 解决了 shell 逃逸问题 - 使用纯 JavaScript 发送 HTTP 请求

**技术变更：**
- 移除了对 `child_process` 和外部 `curl` 命令的依赖
- 所有 API 调用都使用了原生的 `http`/`https` 模块
- 实现了基于 Cookie 的会话管理
- 改进了错误处理和验证机制

### v1.1.0 (2026-02-24) - 功能增强**

**新增命令：**
- `status` - 服务状态（版本、保护状态、端口）
- `dns-info` - DNS 配置详情
- `filter-rules` - 过滤规则及其列表
- `querylog [n]` - 最近的 DNS 查询记录
- `clients` - 配置的客户端列表
- `tls-status` - TLS/加密状态

**其他改进：**
- 改进了错误处理机制
- 改进了输出格式

### v1.0.0 (2026-02-24) - 初始版本

**功能：**
- 提供了 `stats`、`top-clients`、`top-blocked` 和 `health` 命令
- 支持多实例配置
- 采用 ES 模块实现

---

## 作者

**Leo Li (@foxleoly)**  
许可证：MIT