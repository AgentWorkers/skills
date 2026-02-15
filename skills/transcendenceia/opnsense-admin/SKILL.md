---
name: opnsense-admin
description: 通过 API 和 SSH 管理 OPNsense 防火墙、DNS、IDS/IPS 以及网络配置。适用于以下场景：配置 OPNsense 防火墙、管理 Suricata IDS/IPS、操作 Unbound DNS、创建防火墙规则、备份配置文件、监控网络流量以及排查网络故障。该工具支持基于 API 的自动化操作，同时也支持对 OPNsense 26.1 及更高版本版本执行 SSH 命令。
---

# OPNsense管理

> ⚠️ **免责声明**

> 该工具将授予您对您的防火墙和网络的高权限访问权限。
> 它可以修改防火墙规则、阻止网络流量以及重启关键服务。

> **使用本工具，即表示您：**
> - 是一位负责任的成年人
> - 拥有管理此防火墙的授权
> - 明白错误可能导致您的网络无法正常运行
> - 将以道德和合法的方式使用该工具

> **作者不对因使用本工具而导致的配置错误、访问权限锁定或任何损害承担责任。**

通过API和SSH完成OPNsense防火墙的全面管理。自动化备份、监控安全、管理服务并排查网络问题。

## 功能

- 🔥 **防火墙管理** - 规则、NAT、别名和诊断
- 🛡️ **IDS/IPS（Suricata）** - 监控和管理入侵检测/预防
- 🌐 **DNS（Unbound）** - DNS解析器、黑名单、转发、TLS加密的DNS通信
- 📊 **监控** - 服务状态、流量分析、系统健康状况
- 💾 **自动备份** - 定期备份配置文件
- 🔧 **服务控制** - 通过SSH启动/停止/重启服务
- 🔌 **API集成** - 提供RESTful API接口以实现自动化操作

## 安装

### 先决条件

- OPNsense 26.1或更高版本
- 具有适当权限的API密钥
- SSH访问权限（可选，用于服务管理）

### 快速设置

1. 在OPNsense中生成API凭据：
   ```
   System → Access → Users → API
   ```

2. 配置凭据（选择一种方法）：

   **选项A：环境变量**
   ```bash
   export OPNSENSE_HOST="192.168.1.1"
   export OPNSENSE_KEY="your_api_key"
   export OPNSENSE_SECRET="your_api_secret"
   ```

   **选项B：凭据文件**（推荐）
   ```bash
   mkdir -p ~/.opnsense
   cat > ~/.opnsense/credentials << EOF
   OPNSENSE_HOST=192.168.1.1
   OPNSENSE_PORT=443
   OPNSENSE_KEY=your_api_key
   OPNSENSE_SECRET=your_api_secret
   EOF
   chmod 600 ~/.opnsense/credentials
   ```

## 使用方法

### API辅助脚本

```bash
# Check system status
./scripts/opnsense-api.sh status

# Get firmware information
./scripts/opnsense-api.sh firmware-status

# Check Suricata status
./scripts/opnsense-api.sh suricata-status

# Custom API request
./scripts/opnsense-api.sh get /api/core/system/status
./scripts/opnsense-api.sh post /api/core/firmware/update '{"upgrade":true}'
```

### 配置备份

```bash
# Full backup (with RRD data)
./scripts/backup-config.sh

# Config-only backup (smaller)
./scripts/backup-config.sh --config-only

# Custom directory and retention
./scripts/backup-config.sh --dir /mnt/backups --keep 90
```

### 服务控制

```bash
# Restart DNS resolver
./scripts/service-control.sh unbound restart

# Check Suricata status
./scripts/service-control.sh suricata status

# Reload DHCP configuration
./scripts/service-control.sh dhcpd reload

# Check all services
./scripts/service-control.sh all status
```

## 配置参考

### 环境变量

| 变量 | 默认值 | 说明 |
|----------|---------|-------------|
| `OPNSENSE_HOST` | `192.168.1.1` | OPNsense的IP地址或主机名 |
| `OPNSENSE_PORT` | `443` | HTTPS端口 |
| `OPNSENSE_KEY` | - | API密钥 |
| `OPNSENSE_SECRET` | - | API密钥的密文 |
| `SSH_PORT` | `22` | 用于服务控制的SSH端口 |
| `BACKUP_DIR` | `./backups` | 默认备份目录 |
| `KEEP_DAYS` | `30` | 备份保留天数 |

### 常见API端点

| 端点 | 方法 | 功能 |
|----------|--------|---------|
| `/api/core/system/status` | GET | 系统健康状况 |
| `/api/core/firmware/status` | GET | 固件信息 |
| `/api/ids/service/status` | GET | Suricata服务状态 |
| `/api/unbound/diagnostics/stats` | GET | DNS统计信息 |
| `/api/diagnostics/interface/getInterfaceConfig` | GET | 接口配置 |
| `/api/diagnostics/firewall/pfstats` | GET | 防火墙统计信息 |
| `/api/core/backup/backup` | GET | 下载备份文件 |

## 安全最佳实践

1. **SSL证书验证** - 默认启用。仅在开发环境或使用内部网络的自签名证书时，使用`--insecure`或`OPNSENSE_INSECURE=true`选项。
2. **限制API权限** - 为API用户设置最低必要的权限。
3. **安全存储凭据** - 使用文件权限（600）和环境变量。
4. **更改前备份** - 在进行任何更改之前，务必备份配置。
5. **先测试IDS规则** - 在启用IPS阻止功能之前，先在IDS模式下运行Suricata。

### SSL/TLS配置

默认情况下，所有API调用都会验证SSL证书。对于使用有效证书的生产环境，无需进行任何更改。

对于开发环境或使用自签名证书的情况：
```bash
# Option 1: Command line flag
./scripts/opnsense-api.sh --insecure status

# Option 2: Environment variable
export OPNSENSE_INSECURE=true
./scripts/opnsense-api.sh status
```

## 关键概念

### 防火墙规则

- **状态ful过滤** - 默认启用连接跟踪功能。
- **处理顺序**：浮动规则 → 接口组 → 接口规则。
- **操作**：允许（Pass）、阻止（Block，静默丢弃）或拒绝（Reject，并发出警告）。
- **NAT**：在过滤规则之前进行处理。

### Suricata IDS/IPS

- **IDS模式**：仅用于检测（发出警报，不执行阻止操作）。
- **IPS模式**：同时进行检测和阻止（需要手动配置）。
- **最佳实践**：在局域网接口上启用监控，以查看真实的客户端IP地址。
- **规则**：针对新兴威胁、Abuse.ch数据源以及应用程序进行检测。

### Unbound DNS

- **递归解析器**：默认情况下直接查询根服务器。
- **DNSSEC验证**：为增强安全性，默认启用。
- **黑名单**：通过插件阻止基于DNS的广告和跟踪器请求。
- **TLS加密的DNS通信**：加密上行DNS请求。

## 故障排除

### API连接问题

```bash
# Test connectivity
curl -k -u "key:secret" https://opnsense/api/core/system/status

# Check API is enabled in OPNsense
# System → Access → Settings → Enable API
```

### SSH连接问题

```bash
# Test SSH connectivity
ssh -p 22 root@opnsense "echo OK"

# Check SSH is enabled
# System → Administration → Secure Shell
```

### 权限问题

- 确认API密钥具有所需的权限。
- 检查用户是否属于相应的用户组。
- 确保在“系统”→“访问”→“设置”中启用了API功能。

## 版本兼容性

| OPNsense版本 | 本技能版本 | 兼容性 |
|------------------|---------------|--------|
| 26.1及以上 | 1.x | ✅ 兼容 |
| 25.x | 1.x | ⚠️ 可能兼容 |
| 24.x | 1.x | ❌ 未经过测试 |

## 参考文档

- [API指南](references/api-guide.md) - 完整的API认证指南
- [防火墙规则](references/firewall-rules.md) - 规则结构和示例
- [Suricata IPS](references/suricata-ips.md) - IDS/IPS配置
- [Unbound DNS](references/unbound-dns.md) - DNS解析器设置
- [快速参考](references/quick-ref.md) - 命令和文件位置

## 许可证

MIT许可协议 - 详细信息请参阅LICENSE文件。

## 贡献

欢迎在GitHub仓库中提出问题或提交拉取请求。

---

**免责声明**：本技能为非官方开发，与Deciso B.V.或OPNsense项目无关。