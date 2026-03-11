# ClawGears 安全审计技能

## 概述

ClawGears 是一款专为 OpenClaw/MoltBot/ClawdBot 用户在 macOS 上设计的安全审计工具。它可以帮助检测并修复可能使您的 AI 助手暴露在公共互联网中的安全漏洞。

**在以下情况下使用此技能：**
- 用户咨询 OpenClaw 的安全问题
- 用户希望检查他们的 AI 助手是否被暴露
- 用户提到“裸奔”（即系统处于未受保护的状态）或存在安全问题
- 用户希望审计他们的 OpenClaw 配置
- 用户询问 IP 泄露检测的情况

---

## ⚠️ 需求与依赖项

### 所需的系统二进制文件

| 二进制文件 | 用途 |
|--------|---------|
| `python3` | JSON 解析 |
| `curl` | HTTP 请求、IP 检测 |
| `lsof` | 端口和进程检查 |
| `pgrep` / `pkill` | 进程管理 |
| `openssl` | 令牌生成 |
| `socketfilterfw` | macOS 防火墙控制（`/usr/libexec/ApplicationFirewall/socketfilterfw`） |

### 平台

- **仅限 macOS** - 使用 macOS 特定的工具和路径

---

## 📁 访问的文件

### 读取操作

| 路径 | 用途 |
|------|---------|
| `~/.openclaw/openclaw.json` | OpenClaw 配置（令牌、网关设置） |
| `~/.openclaw/logs/` | 网关日志（用于异常检测） |
| `/Library/Application Support/com.apple.TCC/TCC.db` | macOS TCC 数据库（需要完全磁盘访问权限） |
| `~/Library/Application Support/com.apple.TCC/TCC.db` | 用户级别的 TCC 数据库 |

### 写入操作

| 路径 | 用途 |
|------|---------|
| `./history/` | 审计结果存储（JSON、HTML 报告） |
| `./reports/` | 生成的审计报告 |
| `~/.openclaw/openclaw.json` | 配置修复（仅使用 `--fix` 标志） |

---

## 🌐 网络调用

### 外部服务（IP 检测）

| 域名 | 用途 | 发送的数据 |
|--------|---------|-----------|
| `api.ipify.org` | 公共 IP 检测 | 无（GET 请求） |
| `icanhazip.com` | 公共 IP 检测（备用） | 无 |
| `ifconfig.me/ip` | 公共 IP 检测（备用） | 无 |

### 外部服务（泄漏检测）

| 域名 | 用途 | 发送的数据 |
|--------|---------|-----------|
| `openclaw.allegro.earth` | OpenClaw 暴露数据库检查 | 您的公共 IP 地址 |
| `search.censys.io` | Censys 扫描数据库（仅提供链接，手动检查） | 脚本不发送数据 |
| `www.shodan.io` | Shodan 扫描数据库（仅提供链接，手动检查） | 脚本不发送数据 |

---

## 🔐 隐私声明

**在运行此技能之前，请注意：**

1. **IP 传输**：您的公共 IP 地址将被发送到：
   - `api.ipify.org`（或备用服务）进行 IP 检测
   - `openclaw.allegro.earth` 进行暴露数据库检查

2. **本地文件访问**：此技能会读取：
   - 您的 OpenClaw 配置（包括令牌）
   - macOS TCC 权限数据库
   - 网关日志

3. **系统更改**：`interactive-fix.sh` 脚本可以：
   - 修改 OpenClaw 配置
   - 生成新的令牌
   - 重启网关服务
   - 修改防火墙设置时需要 `sudo` 权限

4. **建议**：在运行之前先查看脚本。建议先运行 `quick-check.sh`（仅读取数据）。

---

## 检测到的安全风险

| 风险 | 严重程度 | 描述 |
|------|----------|-------------|
| 网关暴露 | 严重 | 端口绑定到 0.0.0.0，可被互联网访问 |
| 令牌强度低 | 高 | 令牌长度小于 40 个字符 |
| 允许执行敏感命令 | 高 | 允许执行摄像头/屏幕捕获命令 |
| 启用了完全磁盘访问权限 | 中等 | 启用了完全磁盘访问权限 |
| IP 地址出现在泄漏数据库中 | 高 | IP 地址出现在 openclaw.allegro.earth、Censys 或 Shodan 数据库中 |

---

## 快速安全检查

运行一次快速的 5 秒安全审计（仅读取数据，安全无风险）：

```bash
./scripts/quick-check.sh
```

此检查内容包括：
1. 网关是否暴露在网络中
2. 令牌的强度
3. 命令注入防护机制
4. TCC 权限设置
5. 防火墙状态

---

## 全面安全审计

运行一次全面的安全审计：

```bash
./scripts/generate-report.sh --format html --output ./reports
```

---

## IP 泄露检测

检查用户的 IP 地址是否已出现在安全数据库中：

```bash
./scripts/ip-leak-check.sh --all
```

检查以下 3 个数据库：
- `openclaw.allegro.earth` - 专门用于 OpenClaw 的暴露数据库
- **Censys** - 全球范围内的扫描数据库（https://search.censys.io）
- **Shodan** - 物联网和服务扫描数据库（https://www.shodan.io）

---

## 自动修复

**⚠️ 运行前需获得用户明确同意**

自动修复常见的安全问题：

```bash
./scripts/interactive-fix.sh
```

选项：
- `--bind` - 将网关重新绑定到本地主机
- `--token` - 生成新的强令牌
- `--deny` - 将敏感命令添加到禁止列表
- `--restart` - 重启网关服务
- `--all` - 修复所有问题

---

## 工作流程

当用户询问安全问题时：

1. **首先运行快速检查**（仅读取数据）以识别问题：
   ```bash
   ./scripts/quick-check.sh
   ```

2. **如果发现问题**，在修复之前向用户解释风险并征求同意：
   ```bash
   ./scripts/interactive-fix.sh --all
   ```

3. **检查 IP 是否暴露**：
   ```bash
   ./scripts/ip-leak-check.sh --all
   ```

4. **生成报告**以记录检查结果：
   ```bash
   ./scripts/generate-report.sh --format html
   ```

---

## 输出解释

### 快速检查结果

| 符号 | 含义 |
|--------|---------|
| ✅ 通过 | 安全检查通过 |
| ⚠️ 警告 | 建议查看详细信息 |
| ❌ 失败 | 严重问题，立即修复 |

### IP 泄露结果

| 结果 | 应采取的措施 |
|--------|--------|
| IP 地址未出现在数据库中 | 继续监控 |
| IP 地址出现在数据库中 | 紧急：关闭公共访问权限，重新生成令牌 |

---

## 重要提示

1. **始终建议**先运行快速检查（仅读取数据，安全无风险）
2. **在修复之前用简单的语言解释风险**
3. **在运行 `interactive-fix.sh` 之前征求用户的明确同意**
4. **建议定期进行检查**（每周一次或配置更改后）
5. **注意**：目前有超过 220,000 个 OpenClaw 实例被公开暴露

---

## 统计数据

> 目前有超过 220,000 个 OpenClaw 实例被公开暴露，许多 API 密钥已经泄露给黑客数据库。

---

## 相关链接

- GitHub: https://github.com/JinHanAI/ClawGears
- ClawHub: https://clawhub.ai

---

## 许可证

MIT-0（ClawHub 平台许可证）