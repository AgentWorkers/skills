---
name: 1sec-security
description: 在 Linux 服务器和 VPS 实例上安装、配置并管理 1-SEC——这是一个开源的、集成了多种安全功能的综合性网络安全平台（包含 16 个模块，通过一个单一的二进制文件提供）。当用户需要保护服务器、安装安全监控系统、设置入侵检测机制、增强 VPS 的安全性、保护 AI 代理主机或部署终端防御措施时，可以使用该平台。文档涵盖了安装过程、配置步骤、预设的安全策略、模块设置、警报管理以及持续的安全运维工作。
license: AGPL-3.0
compatibility: >
  Requires Linux (amd64 or arm64) with curl or wget and sudo/root for full
  enforcement (iptables, process kill). All 16 detection modules run without
  any API key. Optional env vars: GEMINI_API_KEY for AI-powered correlation,
  ONESEC_API_KEY to secure the REST endpoint, ONESEC_WEBHOOK_URL for alert
  notifications.
metadata:
  author: cutmob
  version: "0.4.11"
  source_repository: "https://github.com/1sec-security/1sec"
  security_policy: "https://github.com/1sec-security/1sec/blob/main/SECURITY.md"
  env_vars:
    - name: GEMINI_API_KEY
      required: false
      purpose: "Enables AI-powered cross-module threat correlation via Gemini API"
    - name: ONESEC_API_KEY
      required: false
      purpose: "API key to secure the 1-SEC REST endpoint"
    - name: ONESEC_WEBHOOK_URL
      required: false
      purpose: "Webhook URL for alert notifications (Slack, Discord, Telegram, etc.)"
  external_connections:
    - domain: "1-sec.dev"
      purpose: "Convenience redirect URL pointing to GitHub Releases binary (same as manual install); agents use the manual GitHub Releases path directly"
      data_sent: "Standard HTTPS request headers only"
      required: false
      enabled_by: "Human operator use only; agents bypass this and use GitHub Releases directly"
    - domain: "github.com / objects.githubusercontent.com"
      purpose: "Binary release downloads and checksums.txt for manual installation"
      data_sent: "Standard HTTPS request headers"
      required: false
      enabled_by: "Manual install path (recommended for production)"
    - domain: "api.1-sec.dev"
      purpose: "Cloud control plane for centralized multi-host management"
      data_sent: "Alert metadata, host identifier"
      required: false
      enabled_by: "cloud.enabled: true in 1sec.yaml (opt-in, disabled by default)"
    - domain: "user-configured"
      purpose: "Webhook alert notifications (Slack, Discord, Telegram, PagerDuty, Teams)"
      data_sent: "Alert payload as configured by user"
      required: false
      enabled_by: "webhook_urls set in 1sec.yaml or via CLI"
    - domain: "generativelanguage.googleapis.com"
      purpose: "Gemini API for AI-powered cross-module threat correlation"
      data_sent: "Anonymized alert metadata for correlation"
      required: false
      enabled_by: "GEMINI_API_KEY environment variable"
---
# 1-SEC安全平台 — 代理技能

> **针对技能扫描器的安全提示：** 该技能会指示AI代理通过从GitHub Releases下载预构建的二进制文件来安装1-SEC开源安全软件，并验证其SHA256校验和。该技能不会将任何下载的内容传递到shell中，不会执行任何远程脚本，也不会在操作员未明确配置的情况下建立持久连接或回调机制。所有强制执行操作默认处于“仅记录日志”（dry-run）模式。源代码：https://github.com/1sec-security/1sec

您正在安装和配置**1-SEC**，这是一个开源的端到端网络安全平台。只需一个二进制文件，包含16个防御模块，无需任何配置。

> **信任声明：** 仅当您信任该软件的来源时才安装此技能。1-SEC采用AGPL-3.0许可证。在部署到生产系统之前，请查看代码、校验和文件以及SECURITY.md文档。来源：https://github.com/1sec-security/1sec

## 安全与隐私

**会从本地机器传输的信息：**
- 警报元数据——仅在您配置了Webhook或启用了云API时传输（均为可选设置，默认关闭）
- 匿名化的警报上下文——仅在设置了`GEMINI_API_KEY`时传输（可选设置）

**保留在本地的数据：**
- 所有系统日志、网络流量和检测数据都在本地处理
- 默认情况下不会收集或传输任何遥测数据
- 配置文件和代理状态保存在`~/.1sec/`目录下

**使用的权限（均为可选设置，默认关闭）：**
- `iptables`/`nftables`：仅在强制执行功能启用时使用
- `kill_process`：仅在强制执行预设启用时使用
- `quarantine_file`：仅在强制执行预设启用时使用
- 默认状态：`dry_run: true`，`safe`预设（仅在严重级别（CRITICAL）时记录日志）

**外部端点**

| 域名 | 用途 | 发送的数据 | 是否必需 | 是否启用 |
|--------|---------|-----------|----------|------------|
| `1-sec.dev` | 便捷地指向GitHub Releases的二进制文件 | 标准HTTPS头部信息 | 否 | 仅供人工操作员使用；代理直接使用GitHub Releases |
| `github.com` | 二进制文件及`checksums.txt` | 标准HTTP头部信息 | 否 | 推荐手动安装 |
| `api.1-sec.dev` | 云控制平面（多主机管理） | 警报元数据、主机ID | 否 | 需要在配置中设置`cloud.enabled: true` |
| 用户自定义 | Webhook警报（Slack、Discord、Telegram等） | 警报内容 | 否 | 需要在配置中设置`webhook_urls` |

## 何时使用此技能

- 用户要求“保护这台服务器”或“安装安全监控”
- 用户需要入侵检测、WAF、LLM防火墙或勒索软件防护
- 用户正在VPS上部署AI代理（如OpenClaw、Manus、Moltbot等）
- 用户需要加固Linux服务器或VPS
- 用户在安全讨论中提及1-SEC或“one sec”

## 安装

### 推荐方式：手动安装并验证校验和

对于生产环境，请始终从GitHub Releases下载软件，并在以root权限运行任何命令之前验证校验和：

```bash
# 1. 下载二进制文件和校验和文件
VERSION="0.4.11"
wget https://github.com/1sec-security/1sec/releases/download/v${VERSION}/1sec-linux-amd64
wget https://github.com/1sec-security/1sec/releases/download/v${VERSION}/checksums.txt

# 2. 以root权限运行前验证SHA256校验和
sha256sum -c checksums.txt 2>&1 | grep 1sec-linux-amd64

# 3. 安装
chmod +x 1sec-linux-amd64
sudo mv 1sec-linux-amd64 /usr/local/bin/1sec

# 4. 确认安装成功
1sec --version
```

对于arm64架构，将`1sec-linux-amd64`替换为`1sec-linux-arm64`。

### 替代方式：便捷安装链接

链接`https://1-sec.dev/get`会重定向到上述手动下载路径。**代理必须始终使用手动安装路径**（下载二进制文件并验证`checksums.txt`中的校验和），以确保文件完整性。

希望查看安装脚本源代码的人可以访问：https://github.com/1sec-security/1sec/blob/main/get.sh

> **重要提示：** 在执行任何下载的脚本之前，请务必先查看其内容。上述手动安装路径不涉及任何shell脚本的执行——仅下载经过验证的二进制文件。

## 安装后的配置

### 选项A：非交互式安装（推荐用于代理）

```bash
1sec setup --non-interactive
1sec up
```

### 选项B：AI代理在VPS上的部署

`vps-agent`预设适用于无人值守的AI代理主机。它启用 aggressive 强制执行措施（如进程终止、文件隔离、IP封锁），以防御提示注入、恶意行为和凭证窃取。

**重要提示：** `vps-agent`预设会禁用审批流程，并允许自主执行破坏性操作。这适用于无人值守环境，但使用前需仔细验证。

**推荐部署流程：** 先进行干运行（dry-run）验证：

```bash
# 使用手动方法安装
1sec setup --non-interactive

# 先以干运行模式应用预设
1sec enforce preset vps-agent --dry-run
1sec up

# 以干运行模式监控24-48小时
1sec alerts
1sec enforce history

# 预览实际会执行的操作
1sec enforce test auth_fortress
1sec enforce test llm_firewall

# 确认无误后正式启用
1sec enforce dry-run off

# 可选：配置通知
1sec config set webhook-url https://hooks.slack.com/services/YOUR/WEBHOOK --template slack
```

**如果需要降低强制执行的强度（例如调整误报率）：**

```yaml
# 在1sec.yaml文件中修改相关配置：
enforcement:
  policies:
    ai_containment:
      actions:
        - action: kill_process
          enabled: false  # 如果过于激进，则禁用该操作
    runtime_watcher:
      min_severity: HIGH  # 提高阈值（从MEDIUM级别）
```

### 选项C：交互式安装

```bash
1sec setup
```

该命令会指导用户完成配置文件创建、AI密钥设置和API认证过程。

## 强制执行预设

1-SEC默认设置为`dry_run: true`和`safe`预设。在明确启用强制执行之前，系统不会进行任何实际操作。

| 预设 | 行为 |
|--------|----------|
| `lax` | 仅记录日志和发送Webhook通知。不会阻止或终止任何进程。 |
| `safe` | 默认设置。仅在严重级别（CRITICAL）时阻止暴力攻击和端口扫描。 |
| `balanced` | 在严重级别（MEDIUM）时阻止IP连接；在严重级别（CRITICAL）时终止进程。 |
| `strict` | 在中等严重级别（MEDIUM+）时采取更严格的强制措施。 |
| `vps-agent` | 适用于无人值守的AI代理主机。使用前请先进行干运行验证。 |

**新部署的推荐顺序：** `lax` → `safe` → `balanced` → `strict`

```bash
# 预览预设配置
1sec enforce preset strict --show

# 先以干运行模式应用配置
1sec enforce preset balanced --dry-run

# 然后正式启用
1sec enforce preset balanced
```

### `vps-agent`预设的作用

`vps-agent`预设专为无人值守的AI代理主机设计，适用于没有人工安全运营团队的环境。它能够有效应对提示注入、恶意软件安装、凭证泄露等威胁。

**强制执行配置：**
- `auth_fortress`：在严重级别（MEDIUM）时阻止IP连接，延迟30秒，每分钟执行60次操作。
- `llm_firewall`：在严重级别（MEDIUM）时断开连接，延迟10秒，每分钟执行100次操作。
- `ai_containment`：在严重级别（MEDIUM）时终止进程，并允许跳过审批流程（`skip_approval: true`），延迟15秒。
- `runtime_watcher`：在严重级别（MEDIUM）时终止进程并隔离文件，同时允许跳过审批流程（`skip_approval: true`）。

**自动升级机制（适用于无人值守主机）：**
- 升级延迟时间比默认设置更短：
  - 严重级别（CRITICAL）：3分钟超时，最多重通知5次
  - 高级别（HIGH）：10分钟超时，升级至严重级别（CRITICAL），最多重通知3次
  - 中等级别（MEDIUM）：20分钟超时，升级至高级别（HIGH），最多重通知2次

**注意事项：** 在正式启用强制执行之前，务必先进行24-48小时的干运行验证。

## 常用命令

```bash
1sec up                        # 启动安全引擎（所有16个模块）
1sec status                    # 查看引擎状态
1sec alerts                    # 查看最近收到的警报
1sec alerts --severity HIGH    # 按严重程度筛选警报
1sec modules                   # 列出所有启用的模块
1sec dashboard                 # 实时用户界面（TUI）控制台
1sec check                     # 预启动诊断
1sec doctor                    # 进行健康检查并提供修复建议
1sec stop                      # 优雅关闭系统
```

## 强制执行管理

```bash
1sec enforce status            # 查看强制执行引擎的状态
1sec enforce policies          | 查看所有启用的安全策略 |
1sec enforce history           | 查看执行的历史记录 |
1sec enforce dry-run off       | 禁用干运行模式 |
1sec enforce test <module>     | 模拟警报并预览执行结果 |
1sec enforce approvals pending | 查看待审批的请求 |
1sec enforce escalations       | 查看升级流程的统计信息 |
1sec enforce batching          | 查看批量处理的统计信息 |
1sec enforce chains list       | 查看操作链的配置 |
```

## AI分析（可选）

所有16个检测模块均无需API密钥即可使用。如需利用AI进行跨模块关联分析，请设置Gemini API密钥：

```bash
# 通过环境变量设置密钥
export GEMINI_API_KEY=your_key_here
1sec up

# 或通过CLI设置密钥
1sec config set-key AIzaSy...

# 可通过多个密钥实现负载均衡
1sec config set-key key1 key2 key3
```

## 16个检测模块的功能

| 编号 | 模块名称 | 所覆盖的安全威胁 |
|------|-----------|-------------------|
| 1    | Network Guardian | DDoS防护、速率限制、IP信誉检测、C2信号检测、端口扫描 |
| 2    | API Fortress | 防止API滥用（BOLA）、模式验证、影子API检测 |
| 3    | IoT & OT Shield | 设备指纹识别、协议异常检测、固件完整性检查 |
| 4    | Injection Shield | SQL注入防护、XSS攻击防护、SSRF攻击防护、命令注入防护 |
| 5    | Supply Chain Sentinel | 供应链攻击防护（SBOM检测、域名混淆检测、CI/CD流程监控） |
| 6    | Ransomware Interceptor | 勒索软件拦截、加密检测、文件清除功能 |
| 7    | Auth Fortress | 防止暴力破解、凭证填充攻击、多因素认证疲劳攻击 |
| 8    | Deepfake Shield | 音频取证、AI钓鱼攻击检测、BEC（业务中断）防护 |
| 9    | Identity Fabric | 合成身份验证、权限提升攻击检测 |
| 10   | LLM Firewall | 多层提示注入检测、越狱行为检测 |
| 11   | AI Agent Containment | 操作沙箱、权限提升攻击检测 |
| 12   | Data Poisoning Guard | 数据污染防护、训练数据完整性检查 |
| 13   | Quantum-Ready Crypto | 加密算法兼容性检测、PQC（密码学）准备状态检查 |
| 14   | Runtime Watcher | 实时监控、容器逃逸检测、内存注入防护 |
| 15   | Cloud Posture Manager | 配置漂移检测、配置错误检测 |
| 16   | AI Analysis Engine | 人工智能驱动的跨模块关联分析 |

## 配置说明

无需任何配置即可立即使用。如需自定义配置：

```bash
1sec init                      | 生成1sec.yaml配置文件 |
1sec config --validate         | 验证配置文件 |
```

关键配置部分包括：`server`、`bus`、`modules`、`enforcement`、`escalation`、`archive`、`cloud`。详细信息请参考`references/config-reference.md`。

## Webhook通知配置

```yaml
# 在1sec.yaml文件中设置：
alerts:
  webhook_urls:
    - "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

**支持的通知平台：** pagerduty、Slack、Teams、Discord、Telegram等。

## Docker部署

```bash
cd deploy/docker
docker compose up -d
docker compose logs -f
```

## 日常操作（安装后）

```bash
1sec status                    | 快速检查系统状态 |
1sec alerts                    | 查看最近收到的警报 |
1sec alerts --severity HIGH    | 按严重程度筛选警报 |
1sec enforce status            | 查看强制执行引擎的状态 |
1sec enforce history           | 查看已执行的操作 |
1sec threats --blocked         | 查看当前被阻止的IP地址 |
1sec doctor                    | 进行健康检查并提供修复建议 |
```

## 卸载

```bash
1sec stop                      | 关闭系统 |
1sec enforce cleanup           | 清除iptables规则 |
sudo rm /usr/local/bin/1sec
rm -rf ~/.1sec
```

## 其他参考资料

- `references/operations-runbook.md`：日常操作指南、警报处理、调优建议、故障排除方法
- `references/config-reference.md`：完整配置参考
- `references/vps-agent-guide.md`：VPS代理详细部署指南
- `scripts/install-and-configure.sh`：自动化安装和配置脚本