---
name: clawguardian
description: OpenClaw代理的多层安全架构中的一层。该层能够在提示注入、数据泄露尝试、工具滥用以及社会工程攻击到达模型之前进行拦截。它与OpenClaw内置的安全限制功能协同工作，以实现深度防御。
version: 2.4.5
homepage: https://github.com/bluemax30001/guardian
metadata:
  openclaw:
    requires:
      bins:
        - python3
      env:
        required: []
        optional:
          - GUARDIAN_WORKSPACE
          - GUARDIAN_CONFIG
          - OPENCLAW_WORKSPACE
          - OPENCLAW_CONFIG_PATH
        never_required:
          - STRIPE_SECRET_KEY
          - STRIPE_WEBHOOK_SECRET
    permissions:
      - read_workspace
      - write_workspace
      - shell_optional
      - network_optional
    optional_capabilities:
      - name: dashboard_http_server
        description: "Local HTTP dashboard on port 8080 (serve.py). Disabled by default. Start manually or via systemd — never auto-starts on install."
        enabled_by_default: false
        how_to_enable: "python3 scripts/serve.py --port 8080"
      - name: billing_stripe
        description: "Pro tier Stripe billing integration. Completely inactive unless STRIPE_* env vars are set. Safe to ignore for free tier."
        enabled_by_default: false
        how_to_enable: "Set pro_tier.enabled=true in config.json and set STRIPE_* env vars"
      - name: webhook_integration
        description: "Inbound webhook endpoint for external threat reports. Disabled by default."
        enabled_by_default: false
        how_to_enable: "Configure webhook section in config.json"
      - name: cron_jobs
        description: "Periodic scanning cron jobs. Opt-in only — run onboard.py --setup-crons explicitly."
        enabled_by_default: false
        how_to_enable: "python3 scripts/onboard.py --setup-crons"
    install_transparency:
      activation_marker: ".guardian-activate-pending written by install.sh. Delete this file to prevent auto-onboarding on next OpenClaw load."
      data_egress: "None by default. All scan data stays in local guardian.db. Webhooks and HTTP server are opt-in."
      credentials: "No credentials required. Stripe keys only needed for optional Pro billing."
      audit_exports: "audit_exports/ directory is excluded from all published packages (.clawhubignore). Never shipped."
      definitions: "definitions/*.json contain threat-detection regex patterns — these are detection signatures, not attack payloads. Equivalent to antivirus virus definition databases."
---
# Guardian

**OpenClaw代理的多层安全体系中的其中一层**

真正的代理安全需要多层防护：OpenClaw内置的限制机制和审批流程用于控制代理的“行为”；而Guardian则负责控制代理“看到的内容”——在恶意输入到达模型之前对其进行拦截。

Guardian提供基于签名的预模型扫描功能，能够检测提示注入、凭证窃取尝试、工具滥用行为以及社会工程攻击。但它本身并不是一个完整的安全解决方案。应将其与OpenClaw的工具白名单、审批流程以及沙箱执行机制结合使用，以实现深度防御。

Guardian提供了两种扫描模式：

- **实时预扫描**：在每条消息到达模型之前对其进行检查。
- **批量扫描**：定期扫描工作区文件和对话记录。

所有扫描数据都存储在本地。可以通过`scripts/onboard.py --setup-crons`命令进行Cron任务的设置（可选）。

扫描结果会保存在SQLite数据库（`guardian.db`）中。

## 安装

```bash
cd ~/.openclaw/skills/guardian
./install.sh
```

## 安装机制及注意事项
该软件包包含可执行脚本（包括`install.sh`）和Python模块。在生产环境中运行之前，请务必先仔细阅读`install.sh`脚本。`install.sh`负责完成本地设置和验证；辅助脚本`onboard.py`用于Cron任务的配置（可选）。

## 上线检查清单
1) 可选：`python3 scripts/onboard.py --setup-crons`（用于设置Cron任务）
2) `python3 scripts/admin.py status`（确认系统是否正常运行）
3) `python3 scripts/admin.py threats`（确认签名库是否已加载；应显示0或blocked状态）
4) 可选：根据您的环境配置`config.json`中的`scan_paths`和`threshold`参数。

### 首次加载/自动激活
`install.sh`执行完成后，它会在工作区根目录下创建`.guardian-activate-pending`文件（路径为`~/.openclaw/workspace/.guardian-activate-pending`）。当OpenClaw下次加载时，会自动触发`onboard.py`以完成激活流程。激活完成后，该文件会被删除。如果您希望手动进行上线配置，可以直接删除该文件（`rm ~/.openclaw/workspace/.guardian-activate-pending`）。

## 扫描范围与隐私保护
Guardian会扫描配置的工作区路径以检测威胁。根据`scan_paths`的设置，扫描范围可能包括工作区中的其他技能配置文件。如果处理敏感文件，请在`config.json`中设置更严格的扫描路径。

## 发布前的安全检查流程
在进行任何`clawhub publish`操作之前，请先运行以下命令：

```bash
python3 scripts/pre_publish_check.py
```

如果检查结果显示非零错误代码，**请勿发布**，直到问题得到解决。该检查会忽略`.clawhubignore`文件中的路径，并阻止可能泄露敏感信息的文件（例如长度超过24个字符的十六进制字符串，以及`audit_exports/*.json`文件）。

## 快速入门

```bash
# Check status
python3 scripts/admin.py status

# Scan recent threats
python3 scripts/guardian.py --report --hours 24

# Full report
python3 scripts/admin.py report
```

## 管理命令

```bash
python3 scripts/admin.py status          # Current status
python3 scripts/admin.py enable          # Enable scanning
python3 scripts/admin.py disable         # Disable scanning
python3 scripts/admin.py threats         # List detected threats
python3 scripts/admin.py threats --clear # Clear threat log
python3 scripts/admin.py dismiss INJ-004 # Dismiss a signature
python3 scripts/admin.py allowlist add "safe phrase"
python3 scripts/admin.py allowlist remove "safe phrase"
python3 scripts/admin.py update-defs     # Update threat definitions
```

在命令后添加`--json`参数可获取机器可读的输出结果。

## Python API

```python
from core.realtime import RealtimeGuard

guard = RealtimeGuard()
result = guard.scan_message(user_text, channel="telegram")
if guard.should_block(result):
    return guard.format_block_response(result)
```

## 环境变量
- `GUARDIAN_WORKSPACE`（可选的工作区配置路径）
- `OPENCLAW_WORKSPACE`（可选的OpenClaw工作区配置路径）
- `GUARDIAN_CONFIG`（可选的Guardian配置文件路径）
- `OPENCLAW_CONFIG_PATH`（可选的OpenClaw配置文件路径）

## 配置
请编辑`config.json`文件：

| 设置 | 描述 |
|---|---|
| `enabled` | 启用/禁用Guardian的开关 |
| `severity_threshold` | 阻止行为的严重程度阈值：`low` / `medium` / `high` / `critical` |
| `scan_paths` | 需要扫描的路径列表（`["auto"]`表示扫描所有常见文件夹） |
| `db_path` | SQLite数据库路径（默认为`<workspace>/guardian.db`） |

## 工作原理
Guardian从`definitions/*.json`文件中加载威胁签名信息。每个签名都包含一个ID、正则表达式模式、严重程度等级和类别。系统会将传入的文本与所有有效的签名进行匹配。符合配置严重程度阈值的请求会被阻止并记录到数据库中。

支持的威胁类型包括：提示注入、凭证窃取尝试、工具滥用行为以及社会工程攻击手段。

### 来源信任等级
Guardian会根据消息的来源渠道和类型为其分配信任等级。共有四个等级：
- **0 – 内部来源**（Cron任务、工作区文件、系统提示）：永远不会被阻止；
- **1 – 所有者来源（Telegram）**：会被标记以供审核，但不会被阻止；
- **2 – 半可信来源（电子邮件、未知来源）**：只有当威胁等级达到70分或以上时才会被阻止；
- **3 – 外部来源（Webhook）**：在威胁等级达到50分或以上时就会被阻止。
消息的来源类型会影响实际的信任等级：系统生成的消息会使信任等级略微偏向“内部”级别，而工具生成的消息则会使信任等级略微偏向“外部”级别。这样可以避免对内部或Cron生成的合法内容产生误判（例如，日志输出或文档中可能包含类似注入攻击的短语）。