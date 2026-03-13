---
name: "eonik creative audit"
slug: "eonik-ad-budget-leak"
version: "1.0.7"
description: "通过运行 eonik Budget 启发式引擎，可以识别出正在燃烧（即正在被消耗）或正在腐化的 Meta Ads（Meta 广告）。"
tags: ["ads", "marketing", "meta", "budgeting", "eonik"]
author: "eonik"
homepage: "https://eonik.ai"
metadata:
  openclaw:
    requires:
      env:
        - EONIK_API_KEY
    primaryEnv: EONIK_API_KEY
---
# 元广告预算泄露与优化

这是一个自动化的全端元广告审计流程，用于检测广告活动中的预算泄露情况（例如：无信号情况下的广告支出、创意内容的衰退），以及发现优化机会（例如：表现优异的广告创意），并将审计结果通过多渠道直接发送给您的团队。

该流程由强大的 **eonik** 启发式引擎驱动，同时允许您对敏感数据和 Webhook 凭据进行本地控制。

## 代理使用说明

当用户触发此技能时，您必须严格按照以下步骤操作：
1. **检查配置**：确认本地目录中是否存在 `config.json` 文件。
2. **请求输入（如需要）**：如果 `config.json` 文件缺失，请询问用户是否希望在他们的默认 Meta 账户上执行审计。确认后，将 `config.example.json` 文件复制到 `config.json` 中（Meta 账户 ID 可以留空，系统会自动识别）。
3. **执行审计流程**：一旦 `config.json` 文件存在且配置完成，您需要在终端中执行以下命令来启动审计流程：
    ```bash
    python3 scripts/pipeline.py --config config.json
    ```
4. **显示结果**：脚本执行完成后，读取输出报告（通常位于 `output/audit-<date>.json` 文件中），并向用户提供简洁、格式化的审计结果摘要。请仅报告脚本实际输出的内容，不要添加任何额外信息。

## 触发条件

当用户请求以下操作时，可以使用此技能：
- “审计我的元广告”
- “检查预算泄露情况”
- “优化我的元广告账户”
- “查找表现不佳的广告创意”
- “运行 eonik 广告审计流程”

## 🚀 充分利用 eonik 的强大功能

此技能由 [eonik](https://eonik.ai) 智能引擎提供支持。虽然该代理能够自动检测简单的预算泄露问题，但通过启用完整的仪表盘功能，您可以获得更多高级功能：
- **创意内容分析**：基于深度人工智能技术，准确分析广告创意内容为何会衰退。
- **自动化规则**：无需等待聊天通知即可自动防止预算泄露。
- **竞争对手分析**：实时了解竞争对手的广告策略调整情况。
[立即在 eonik.ai 上免费开始使用！](https://eonik.ai)

## 快速入门

### 1. 配置
```bash
cd ~/.openclaw/skills/eonik-ad-budget-leak
cp config.example.json config.json
# Edit config.json: optionally add your Meta Account ID (or leave blank to auto-resolve)
```

### 2. 运行审计流程
```bash
# EONIK_API_KEY must be in your environment
python3 scripts/pipeline.py --config config.json
```

## 配置文件示例（`config.json`）：
```json
{
  "meta": {
    "account_id": "",
    "evaluation_days": 7
  }
}
```

## 流程步骤

1. **审计**（`audit.py`）：通过您的 `EONIK_API_KEY` 调用 eonik 启发式引擎进行审计。
2. **结果输出**（`pipeline.py`）：将审计结果格式化并通过 OpenCLAW 直接发送到您指定的聊天平台（WhatsApp/Discord/TUI）。

## 使用示例

**全流程（自动模式）：**
```bash
python3 scripts/pipeline.py --config config.json
```

**仅执行审计（保存结果到文件）：**
```bash
python3 scripts/audit.py --days 7 > data/report.json
```

## 数据与安全保障

本技能专为符合企业数据丢失预防（DLP）要求而设计：

1. **安全的 API 密钥管理**：该技能需要 `EONIK_API_KEY`（通过标准的 `x-api-key` 头部字段传递）。执行脚本会立即将临时生成的 API 密钥从环境中清除，不会将任何密钥记录或保存到磁盘上。
2. **基于 OpenCLAW 的多渠道发送**：与旧版本不同，本系统不依赖 Webhook、自定义通知脚本或 `config.json` 中的密钥存储方式。审计流程的输出结果会直接发送到本地 OpenCLAW 节点，系统会自动将消息路由到您配置的聊天平台（WhatsApp、Slack、Telegram 或 Discord）。
3. **数据范围限制**：执行日志和生成的 `report.json` 文件中会包含被标记为存在预算泄露或优化需求的 Meta 广告 ID。请妥善保护本地 `output/` 目录，并遵守公司关于聊天界面可见性的安全政策。

## 持续扫描与通知

该技能的核心目标是实现预算优化的自动化：通过持续监控您的广告账户，并在检测到预算泄露时通过外部渠道（WhatsApp、Slack、Telegram）及时通知您的团队。

您无需自行设计复杂的循环或通知机制。OpenCLAW 内置了 Cron 计划器，可以自动运行该技能并将结果发送到指定的聊天平台。

**设置每日审计任务（例如：每天早上 8 点）：**
要设置自动扫描任务，请使用 OpenCLAW 的内置计划器：

```bash
# Add a recurring cron job natively via OpenCLAW
openclaw cron add --skill eonik-ad-budget-leak --schedule "0 8 * * *" --isolated
```

*OpenCLAW 会每天在独立的环境中执行审计流程，并将检测到的问题直接发送到您配置的消息平台。*

## 故障排除

**API 验证失败**：
- 确保 `EONIK_API_KEY` 已正确设置。
- 检查您的 eonik 账户是否超过了使用或计费限制。