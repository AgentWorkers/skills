# Infra Watchdog — 基础设施监控与健康警报系统

这是一个专为 OpenClaw 代理设计的自托管基础设施监控工具。无需任何外部 SaaS 服务，所有监控数据均本地处理，并通过 WhatsApp、Telegram 或 Discord 发送警报。

## 功能概述

- **HTTP/HTTPS 端点监控**：检查状态码、响应时间以及 SSL 证书的有效性。
- **TCP 端口监控**：监控数据库、SSH 服务及自定义服务的运行状态。
- **Docker 容器监控**：检测容器的运行状态（运行中、已停止或异常）。
- **系统资源监控**：实时监控 CPU、RAM 和磁盘使用情况，并支持自定义阈值设置。
- **SSL 证书到期预警**：在证书到期前 30 天发送警报。
- **DNS 解析监控**：验证域名与 IP 地址的映射关系。
- **Proxmox 虚拟机监控**：通过本地 API 监控虚拟机的运行状态。
- **警报通知方式**：支持通过 WhatsApp、Telegram 或 Discord 发送警报，同时支持配置警报发送的延迟时间。

## 快速入门

```bash
# Initialize data directory & config
infra-watchdog init

# Add your first monitor
infra-watchdog add-monitor --type http --name "My API" --url https://myapi.example.com

# Add a TCP port check
infra-watchdog add-monitor --type tcp --name "PostgreSQL" --host localhost --port 5432

# Add a Docker container check
infra-watchdog add-monitor --type docker --name "My App" --container myapp

# Run all checks now
infra-watchdog check

# View current status dashboard
infra-watchdog dashboard

# Install auto-check cron (every 5 min)
infra-watchdog cron-install
```

## 命令列表

| 命令 | 功能描述 |
|---------|-------------|
| `infra-watchdog init` | 设置数据目录和默认配置 |
| `infra-watchdog add-monitor` | 添加新的监控项目（支持 HTTP、TCP、Docker、资源或 SSL 监控） |
| `infra-watchdog list` | 显示所有已配置的监控项目及其当前状态 |
| `infra-watchdog check` | 立即执行所有监控任务 |
| `infra-watchdog check --name <名称>` | 执行指定的监控项目 |
| `infra-watchdog status` | 显示所有监控项目的状态统计（正常/异常/警告） |
| `infra-watchdog dashboard` | 以 ASCII 格式显示所有监控项目的详细信息 |
| `infra-watchdog cron-install` | 自动安排定期监控任务（使用 Cron 作业） |

## 监控类型

- **HTTP/HTTPS 监控**  
- **TCP 端口监控**  
- **Docker 容器监控**  
- **系统资源监控**  
- **SSL 证书监控**  

## 配置文件

配置文件位于：`~/.openclaw/workspace/infra-watchdog-data/config.json`

```json
{
  "alert_channel": "whatsapp",
  "alert_cooldown_minutes": 15,
  "check_interval_minutes": 5,
  "ssl_expiry_warning_days": 30
}
```

## 预警通知渠道

| 渠道 | 配置值 |
|---------|-------------|
| WhatsApp | `"whatsapp"` |
| Telegram | `"telegram"` |
| Discord | `"discord"` |
| 无（仅记录日志） | `"none"` |

## 使用场景

- **家庭实验室监控**：实时监控所有自托管服务（如 Proxmox、Docker 容器、Jellyfin、Home Assistant 等），一旦出现问题立即通过 WhatsApp 收到警报。
- **API 运行状态监控**：如果您在 RapidAPI 上提供 API 服务，该工具可 24/7 监控您的 API 端点，确保客户在遇到故障前及时得到通知。
- **SSL 证书管理**：防止 SSL 证书过期，提前 30 天发送预警。
- **资源使用预警**：当磁盘空间不足时立即收到警报，避免服务中断。

## 数据存储

所有监控数据均保存在本地（`~/.openclaw/workspace/infra-watchdog-data/`），使用 SQLite 数据库存储，不涉及任何云同步或远程数据传输。

## 系统要求

- Python 3.8 或更高版本 |
- Docker（可选，用于容器监控）
- OpenClaw 1.0 或更高版本

## 项目信息

- **来源代码**：https://github.com/mariusfit/infra-watchdog |
- **问题反馈**：https://github.com/mariusfit/infra-watchdog/issues |
- **开发者**：[@mariusfit](https://github.com/mariusfit)