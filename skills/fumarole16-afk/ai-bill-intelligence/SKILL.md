---
name: ai-bill-intelligence
description: OpenClaw 提供实时 AI API 使用情况跟踪和成本监控功能。通过实时仪表板，您可以监控在 OpenAI、Claude、Geminii、Kimi、DeepSeek 和 Grok 等平台上的使用情况与费用支出。该功能适用于需要监控 AI API 成本、追踪令牌使用情况或管理多个 AI 服务提供商预算的用户。
---

# AI Bill Intelligence v2.1.1

这是一个用于 OpenClaw 的实时 AI API 使用情况跟踪和成本监控的仪表板。

## ⚠️ 重要提示：安装方法

**请勿直接使用下载的 .zip 文件**。您的系统可能会误识别该文件。

### ✅ 正确的安装方法（使用 CLI）

**步骤 1：通过 OpenClaw CLI 安装**
```bash
openclaw skill add ai-bill-intelligence
```

或直接从 ClawHub URL 安装：
```bash
openclaw skill add https://clawhub.ai/fumarole16-afk/ai-bill-intelligence
```

**步骤 2：配置 API 帐户余额**
编辑 `vault.json` 文件以设置初始余额：
```json
{
  "openai": 10.0,
  "claude": 20.0,
  "kimi": 15.0,
  "deepseek": 8.0,
  "grok": 10.0,
  "gemini": 0
}
```

**步骤 3：启动服务**
```bash
sudo systemctl start ai-bill ai-bill-collector
```

**步骤 4：查看仪表板**
在浏览器中访问 http://localhost:8003。

---

## 手动安装（备用方案）

如果使用 CLI 安装失败，可以尝试手动安装：

```bash
# 1. Extract the skill
mkdir -p ~/.openclaw/skills/ai-bill-intelligence
cd ~/.openclaw/skills/ai-bill-intelligence

# 2. Copy files from the downloaded zip
unzip /path/to/ai-bill-intelligence-*.zip

# 3. Install systemd services
sudo cp systemd/*.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now ai-bill ai-bill-collector
```

---

## 配置

### 初始设置

1. 在 `vault.json` 文件中设置 API 帐户余额：
```bash
vim ~/.openclaw/skills/ai-bill-intelligence/vault.json
```

示例：
```json
{
  "openai": 9.01,
  "claude": 20.53,
  "kimi": 22.0,
  "deepseek": 7.32,
  "grok": 10.0,
  "gemini": 0
}
```

2. 验证服务是否正在运行：
```bash
systemctl status ai-bill ai-bill-collector
```

3. 访问仪表板：
- 本地访问：http://localhost:8003
- 如果使用 Nginx，请配置反向代理到端口 8003

---

## 服务

| 服务 | 描述 | 端口 |
|---------|-------------|------|
| `ai-bill.service` | Web 仪表板界面 | 8003 |
| `ai-bill-collector.service` | 使用数据收集器 | - |

`ai-bill-collector.service` 每 30 秒运行一次，从 OpenClaw 会话中收集使用数据。

---

## 主要功能

- **实时跟踪**：实时计算来自 OpenClaw 会话的使用成本
- **支持多种服务提供商**：OpenAI、Claude、Gemi、Kimi、DeepSeek、Grok
- **数据持久化**：即使会话被压缩，数据也会被保留
- **余额监控**：实时显示剩余余额
- **Web 仪表板**：通过 http://localhost:8003 访问可视化界面

---

## 故障排除

### 检查服务状态：
```bash
systemctl status ai-bill ai-bill-collector
```

### 查看收集器日志：
```bash
journalctl -u ai-bill-collector -f
```

### 重启服务：
```bash
sudo systemctl restart ai-bill ai-bill-collector
```

### 余额未更新？
1. 确认 `vault.json` 文件中的初始余额设置正确
2. 验证收集器是否正在运行：`systemctl status ai-bill-collector`
3. 查看 `cumulative_usage.json` 文件中的使用数据

---

## 定价

默认定价信息存储在 `prices.json` 文件中。请根据当前的 API 费率更新该文件：

```json
{
  "kimi": {
    "kimi-k2.5": {"in": 0.50, "out": 2.40}
  }
}
```

价格按每百万令牌计算。