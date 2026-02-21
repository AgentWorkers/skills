# AI 账单智能

专为 OpenClaw 设计的实时计费仪表盘，支持对 12 家以上 AI 服务提供商的基于令牌的费用进行精确追踪。

## 🚀 安装
```bash
openclaw skill install https://github.com/fumabot16-max/bill-project
```

## 🛠 使用方式
该功能通过后台收集器进行运行。作为代理，您可以为用户提供以下帮助：
1. **报告使用情况**：读取 `/root/.openclaw/workspace/bill_project/dist/usage.json` 文件以汇总费用支出。
2. **更新余额**：将用户重定向到 `/setup` 页面，或代其更新 `vault.json` 文件。
3. **检查系统运行状态**：确保 `ai-bill` 服务和 `collector.js` 正在运行。

## ⚙️ 配置参数
- **端口**：默认值为 `8003`。
- **计费模式**：`prepaid`（预付费）、`postpaid`（后付费）、`subscribe`（订阅制）、`unused`（未使用）。

## 📂 管理文件
该功能会管理 `app/` 目录下的以下数据文件：
- `app/vault.json`：用户自定义的余额和支付方式信息。
- `app/prices.json`：AI 模型的定价数据。
- `app/cumulative_usage.json`：已过期会话的累计费用记录。
- `app/dist/usage.json`：用于仪表盘的实时使用数据汇总文件。
- `app/debug.log`：收集器的活动日志。

开发者：Tiger Jung 和 Chloe (@fumarole16-afk)。

<!-- 同步触发时间：2026年2月20日星期五 22:36:10 KST -->