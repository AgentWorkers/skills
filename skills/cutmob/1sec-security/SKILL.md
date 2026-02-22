---
name: 1sec-security
description: 在 Linux 服务器和 VPS 实例上安装、配置并管理 1-SEC——这是一个集成了多种安全功能的一体化网络安全平台（包含 16 个模块，以单一二进制文件的形式提供）。当用户需要保护服务器、安装安全监控系统、设置入侵检测机制、增强 VPS 的安全性、保护 AI 代理主机或部署终端防御措施时，可以使用该平台。文档涵盖了安装过程、配置步骤、预设的安全策略、模块配置方法、警报管理以及持续的安全运维流程。
license: AGPL-3.0
compatibility: >
  Requires Linux (amd64 or arm64) with curl or wget. Root or sudo recommended
  for full enforcement (iptables, process kill). Optional: GEMINI_API_KEY env
  var for AI-powered cross-module correlation.
metadata:
  author: cutmob
  version: "0.4.11"
---
# 1-SEC安全平台——代理技能

您正在安装和配置**1-SEC**，这是一个开源的、集成了多种安全功能的综合性网络安全平台。只需一个二进制文件，即可启用16个防御模块，且完全无需进行任何配置。

## 何时使用此技能

- 当用户请求“保护这台服务器”或“安装安全监控系统”时；
- 当用户需要入侵检测、Web应用防火墙（WAF）、大型语言模型（LLM）防火墙或勒索软件防护功能时；
- 当用户需要在虚拟私有服务器（VPS）上部署AI代理（如OpenClaw、Manus、Moltbot等）时；
- 当用户需要加固Linux服务器或VPS的安全性时；
- 当用户在安全相关讨论中提到“1-SEC”或“one sec”时。

## 快速安装

```bash
curl -fsSL https://1-sec.dev/get | sh
```

该命令会检测操作系统和架构类型，下载最新版本，并将其安装到`/usr/local/bin`（或在没有root权限的情况下安装到`~/.local/bin`）。

## 安装后的配置

### 选项A：非交互式配置（推荐用于代理部署）

```bash
# 一次性完成安装和配置
1sec setup --non-interactive

# 启动所有16个模块，无需任何配置
1sec up
```

### 选项B：在VPS上部署AI代理

如果服务器上托管了AI代理，请使用专为AI代理设计的`vps-agent`预设配置。此预设会启用自动升级机制（对未处理的警报进行自动升级）、禁用人工审批流程，并将关键操作标记为`skip_approval`以允许立即响应：

```bash
# 安装
curl -fsSL https://1-sec.dev/get | sh

# 非交互式配置（使用环境变量设置AI代理相关参数）
1sec setup --non-interactive

# 应用vps-agent预设配置（进行模拟运行）
1sec enforce preset vps-agent --dry-run

# 启动代理
1sec up

# 配置通知方式（根据需要选择平台）
# Slack:
1sec config set webhook-url https://hooks.slack.com/services/YOUR/WEBHOOK --template slack
# Discord:
1sec config set webhook-url https://discord.com/api/webhooks/YOUR/WEBHOOK --template discord
# Telegram:
1sec config set webhook-url https://api.telegram.org/botTOKEN/sendMessage --template telegram --param chat_id=CHAT_ID
```

### 选项C：交互式配置

```bash
1sec setup
```

该选项会引导用户完成配置文件的创建、AI代理密钥的设置以及API认证过程的配置。

## 执行策略预设

1-SEC默认使用`dry_run: true`和`safe`预设。

| 预设名称 | 功能描述 |
|---------|-------------|
| `lax`     | 仅记录日志并通过Webhook发送警报，不会阻止或终止恶意活动。|
| `safe`     | 默认配置：仅在严重级别阻止暴力攻击和端口扫描。|
| `balanced`  | 在高风险情况下阻止IP连接并终止相关进程。|
| `strict`    | 在中等及以上风险级别采取更严格的防护措施。|
| `vps-agent` | 专为AI代理部署设计，提供强化的身份验证、LLM防火墙、恶意行为遏制及运行时安全保护等功能。|

推荐的使用顺序：`lax` → `safe` → `balanced` → `strict`。

`vps-agent`预设是独立使用的，适用于AI代理的部署：

```bash
# 应用预设配置
1sec enforce preset balanced

# 查看预设配置的效果（不执行实际操作）
1sec enforce preset strict --show

# 先进行模拟运行以测试配置
1sec enforce preset balanced --dry-run
```

## 常用命令

```bash
1sec up                        # 启动整个安全系统（所有16个模块）
1sec status                    # 查看系统状态
1sec alerts                    # 查看最近收到的警报
1sec alerts --severity HIGH    # 按严重程度筛选警报
1sec modules                   | 查看所有启用的模块
1sec dashboard                 | 查看实时用户界面（TUI）仪表盘
1sec check                     | 进行启动前的诊断检查
1sec doctor                    | 进行系统健康检查并提供修复建议
1sec stop                      | 平稳关闭系统
```

## 执行策略管理

```bash
1sec enforce status            | 查看执行策略的状态
1sec enforce policies          | 查看所有应用的策略配置
1sec enforce history           | 查看策略执行的历史记录
1sec enforce dry-run off       | 禁用模拟运行模式
1sec enforce test <module>      | 模拟警报并预览执行结果
1sec enforce approvals pending    | 查看待人工审批的请求
1sec enforce escalations       | 查看升级机制的运行情况
1sec enforce batching          | 查看警报批量处理的相关信息
1sec enforce chains list        | 查看所有执行的操作链配置
```

## AI分析（可选）

1-SEC的15个基于规则的防御模块在无需API密钥的情况下即可正常工作。如需利用AI进行跨模块间的关联分析，请设置Gemini API密钥：

```bash
# 通过环境变量设置密钥
export GEMINI_API_KEY=your_key_here
1sec up

# 或通过命令行设置密钥
1sec config set-key AIzaSy...

# 为提高性能，可以设置多个API密钥
1sec config set-key key1 key2 key3
```

## 16个防御模块

| 编号 | 模块名称 | 主要功能 |
|------|---------|---------|
| 1    | Network Guardian | 防止DDoS攻击、限制请求速率、评估IP信誉、检测C2信号 |
| 2    | API Fortress | 检查API请求的合法性、发现隐藏的API接口 |
| 3    | IoT & OT Shield | 识别物联网设备特征、检测协议异常及固件完整性 |
| 4    | Injection Shield | 防止SQL注入、XSS攻击、SSRF攻击及命令注入 |
| 5    | Supply Chain Sentinel | 检测供应链安全漏洞（如SBOM攻击）、防范域名抢注行为 |
| 6    | Ransomware Interceptor | 检测加密攻击、识别恶意文件及清除工具 |
| 7    | Auth Fortress | 防止暴力破解、凭证填充攻击及多因素认证疲劳攻击 |
| 8    | Deepfake Shield | 识别深度伪造内容、防止AI钓鱼攻击及BEC攻击 |
| 9    | Identity Fabric | 生成虚假身份信息、防止权限提升 |
| 10   | LLM Firewall | 检测多种类型的提示注入攻击、检测越狱行为及隐藏式注入 |
| 11   | AI Agent Containment | 对AI代理进行沙箱测试、防止权限滥用 |
| 12   | Data Poisoning Guard | 保护训练数据的安全性、验证代码注入行为 |
| 13   | Quantum-Ready Crypto | 确保加密系统的安全性、检查PQC（Post-Quantum Cryptography）兼容性 |
| 14   | Runtime Watcher | 监控运行时安全风险（如FIM攻击、容器逃逸等） |
| 15   | Cloud Posture Manager | 检查云环境的安全配置问题 |
| 16   | AI Analysis Engine | 使用双层Gemini算法进行跨模块关联分析 |

## 配置说明

系统默认支持无需配置的快速启动模式。如需自定义配置，可执行以下命令：

```bash
1sec init                      | 生成配置文件（1sec.yaml）
1sec config --validate         | 验证配置文件的有效性 |
```

关键配置参数包括：`server`、`bus`、`modules`、`enforcement`、`escalation`、`archive`、`cloud`。详细配置说明请参考`references/config-reference.md`。

## Webhook通知

您可以为Slack、Discord、PagerDuty或Microsoft Teams配置警报通知的Webhook地址：

```yaml
# 在1sec.yaml或configs/default.yaml文件中设置：
alerts:
  webhook_urls:
    - "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

**Telegram通知示例：**

```yaml
enforcement:
  policies:
    auth_fortress:
      actions:
        - action: webhook
          params:
            url: "https://api.telegram.org/botYOUR_TOKEN/sendMessage"
            template: "telegram"
            chat_id: "-1001234567890"
```

## Docker部署

```bash
cd deploy/docker
docker compose up -d
docker compose logs -f
```

## 日常操作

安装完成后，可执行以下命令进行日常维护：

```bash
1sec status                    | 快速检查系统状态
1sec alerts                    | 查看最近收到的警报
1sec alerts --severity HIGH    | 按严重程度筛选警报
1sec enforce status            | 查看执行策略的状态
1sec enforce history           | 查看已执行的操作记录
1sec threats --blocked         | 查看当前被阻止的恶意IP地址
1sec doctor                    | 进行系统健康检查并提供修复建议
```

有关完整的操作指南（包括警报处理、误报处理、模块调优、Webhook管理、升级机制配置及故障排除等），请参考`references/operations-runbook.md`。

## 额外参考资料

- `references/operations-runbook.md`：日常操作指南、警报处理、配置调整及故障排除方法
- `references/config-reference.md`：完整的配置参考文档
- `references/vps-agent-guide.md`：VPS代理的详细部署指南
- `scripts/install-and-configure.sh`：自动化安装和配置脚本
```