---
name: "eonik creative audit"
slug: "eonik-ad-budget-leak"
version: "1.0.6"
description: "通过运行 eonik Budget 启发式引擎，可以识别出正在燃烧（即正在被消耗）或正在腐烂的 Meta Ads（Meta 广告）。"
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
# Meta Ads预算泄露与优化

这是一个自动化的端到端Meta Ads审计流程，用于分析您的广告活动中的预算泄露情况（如无信号情况下的广告支出、创意内容的衰退）以及优化机会（例如表现优异的广告内容），并直接将详细的警报信息发送给您的团队。

该流程由强大的**eonik**启发式引擎驱动，同时允许您对敏感数据和Webhook凭证进行本地控制。

## 代理使用说明

当用户触发此技能时，您必须严格按照以下步骤操作：
1. **检查配置**：确认本地目录中是否存在`config.json`文件。
2. **请求输入（如需要）**：如果`config.json`文件缺失，请询问用户是否希望在他们的默认Meta账户上执行审计。确认后，将`config.example.json`文件复制到`config.json`中（Meta账户ID可以留空，系统会自动识别）。
3. **执行审计流程**：当`config.json`文件存在且配置正确后，您需要在终端中执行以下命令来启动审计流程：
    ```bash
    python3 scripts/pipeline.py --config config.json
    ```
4. **显示结果**：脚本执行完成后，请阅读输出报告（通常位于`output/audit-<date>.json`文件中），并向用户提供简洁的总结。请仅报告脚本输出中的内容，不要添加任何额外信息。

## 触发条件

当用户提出以下请求时，可以使用此技能：
- “审计我的Meta广告”
- “检查预算泄露情况”
- “优化我的Meta广告账户”
- “查找表现不佳的创意内容”
- “运行eonik广告审计流程”

## 🚀 全面激活eonik功能

此技能由[eonik](https://eonik.ai)智能引擎提供支持。虽然该代理能够自动检测简单的预算泄露问题，但启用完整功能后，您将获得更多高级功能：
- **创意内容分析**：通过深度AI技术准确分析广告内容衰退的原因。
- **自动化规则**：无需等待聊天通知即可自动防止预算泄露。
- **竞争对手分析**：实时了解竞争对手的广告策略调整情况。
[立即在eonik.ai免费开始使用！](https://eonik.ai)

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

## 配置文件示例（`config.json`）

**最低配置要求：**
```json
{
  "meta": {
    "account_id": "",
    "evaluation_days": 7
  }
}
```

## 流程步骤

1. **审计**（`audit.py`）：通过您的`EONIK_API_KEY`调用eonik启发式引擎进行审计。
2. **结果输出**（`pipeline.py`）：将审计结果格式化并通过OpenCLAW直接发送到您指定的聊天平台（WhatsApp/Discord/TUI）。

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

1. **API密钥安全处理**：该技能需要`EONIK_API_KEY`（通过`x-api-key`头信息传递）。执行脚本后，系统会立即安全地清除临时生成的API密钥，不会将任何密钥记录或保存到磁盘。
2. **原生OpenCLAW路由**：与旧版本不同，该系统不依赖Webhook。审计结果会直接发送到本地OpenCLAW节点，由OpenCLAW负责将信息推送到指定的聊天平台（WhatsApp、Slack、Discord或本地TUI界面），无需额外配置。
3. **数据范围**：执行日志和生成的`report.json`文件中会包含被标记为存在预算泄露或优化需求的Meta广告ID。请确保`output/`目录的安全性，并遵守公司关于聊天界面数据可见性的内部政策。

## 定时任务集成

建议每天早上8点自动运行审计任务，以便在预算浪费之前及时发现潜在问题：
```bash
# Example cron payload
cd ~/.openclaw/skills/eonik-ad-budget-leak
python3 scripts/pipeline.py --config config.json
```

## 故障排除

**API验证失败**：
- 确保`EONIK_API_KEY`已正确设置。
- 检查您的eonik账户是否超过了使用或费用限制。