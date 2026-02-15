---
name: token-panel-ultimate
version: 1.0.8
description: 在一个OpenClaw仪表板上，您可以追踪Claude Max、ChatGPT、Gemini和Manus中AI的使用情况。该仪表板支持查看各服务提供商的速率限制、滚动时间窗口以及信用余额等信息。
homepage: https://github.com/globalcaos/clawdbot-moltbot-openclaw
metadata:
  openclaw:
    emoji: "🎛️"
    requires:
      bins: ["python3"]
---

# Token Panel ULTIMATE

> 🎛️ 了解自己的使用极限，并严格遵守。最大限度地发挥你的能力。

**Claude Max**、**Gemini** 和 **Manus** 的实时使用情况追踪——全部集中在一个地方。

---

## 功能

| 提供商 | 追踪内容 |
|----------|----------------|
| **Claude Max** | 5小时周期、7天周期的使用数据及重置时间 |
| **ChatGPT / OpenAI** | 每个模型的API使用限制（请求次数 + 令牌数量），以及Plus订阅套餐的用量上限 |
| **Gemini** | 每个模型的RPD（请求次数/分钟）、RPM（请求次数/秒）和TPM（请求次数/分钟）；瓶颈检测 |
| **Manus** | 每日更新的数据、每月可使用的信用额度以及附加功能的余额 |

此外，还有一个**网页聊天小部件**，可以一目了然地展示所有信息。

---

## Claude Max 使用情况追踪

实时追踪你的Claude Max订阅使用情况。

### 显示内容

- **5小时周期：** 当前使用百分比及重置时间
- **7天周期：** 近一周的使用百分比及重置时间
- **模型特定限制：** Sonnet和Opus模型的使用额度分配

### 使用方法

```bash
# Pretty print current usage
python3 {baseDir}/scripts/claude-usage-fetch.py

# Update JSON file for the widget
python3 {baseDir}/scripts/claude-usage-fetch.py --update

# Raw JSON output
python3 {baseDir}/scripts/claude-usage-fetch.py --json
```

### 使用要求

- 已安装并登录Claude的命令行工具 (`claude /login`) 

### 自动更新（可选）

```bash
# Add to crontab for automatic updates every 5 minutes
*/5 * * * * python3 {baseDir}/scripts/claude-usage-fetch.py --update
```

---

## Gemini 多模型追踪

追踪每个模型的**瓶颈指标**（RPD、RPM、TPM中最高的那个指标）。

### 模型限制（第一层级）

| 模型 | RPM | TPM | RPD |
|-------|-----|-----|-----|
| gemini-3-pro | 25 | 1M | 250 |
| gemini-2.5-pro | 25 | 1M | 250 |
| gemini-2.5-flash | 2000 | 4M | **无限** |
| gemini-3-flash | 1000 | 1M | 10K |
| gemini-2.0-flash | 2000 | 4M | **无限** |

### 备用策略

优先使用性能最强的模型；对于这些模型，RPD使用次数不受限制。

**重置时间：** 太平洋标准时间午夜（RPD每天重置一次）

### JSON格式

数据存储在 `memory/gemini-usage.json` 文件中：

```json
{
  "models": {
    "gemini-3-pro": {
      "limits": { "rpm": 25, "tpm": 1000000, "rpd": 250 },
      "usage": { "rpm": 17, "tpm": 1380000, "rpd": 251 },
      "status": "exceeded"
    }
  }
}
```

---

## Manus 信用额度监控

### 信用额度结构

- **每月：** 4,000个信用额度（续费时重置）
- **每日更新：** 300个信用额度（凌晨1点重置）
- **附加功能：** 购买的信用额度（永久有效）

### 使用方法

```bash
# Pretty print current usage
python3 {baseDir}/scripts/manus-usage-fetch.py

# Update JSON file for the widget
python3 {baseDir}/scripts/manus-usage-fetch.py --update

# Raw JSON output
python3 {baseDir}/scripts/manus-usage-fetch.py --json
```

### 使用要求

- 设置 `MANUS_API_KEY` 环境变量

### 自动更新（可选）

```bash
# Add to crontab for automatic updates every 15 minutes
*/15 * * * * MANUS_API_KEY=your-key python3 {baseDir}/scripts/manus-usage-fetch.py --update
```

### JSON格式

数据存储在 `memory/manus-usage.json` 文件中（由自动获取脚本生成）：

```json
{
  "credits": {
    "total_all_time": 8407,
    "breakdown": {
      "monthly": { "used": 480, "limit": 4000, "remaining": 3520 },
      "addon": 7296
    },
    "daily_refresh": { "used": 0, "remaining": 300, "limit": 300, "reset_time": "01:00 local" }
  },
  "today": { "tasks": 0, "credits_used": 0, "breakdown": [] }
}
```

---

## ChatGPT / OpenAI 使用情况追踪

追踪每个模型的API使用限制以及ChatGPT Plus订阅套餐的用量上限。

### 显示内容

- **API使用限制：** 每个模型的请求次数/分钟和令牌数量/分钟（来自响应头）
- **Plus套餐的用量上限：** GPT-4o（150次/3小时）、o3（100次/周）、o4-mini（300次/天）等
- **支持的模型：** gpt-4o、gpt-4o-mini、gpt-4、gpt-3.5-turbo、o3-mini

### 使用方法

```bash
# Pretty print current usage
python3 {baseDir}/scripts/chatgpt-usage-fetch.py

# Update JSON file for the widget
python3 {baseDir}/scripts/chatgpt-usage-fetch.py --update

# Raw JSON output
python3 {baseDir}/scripts/chatgpt-usage-fetch.py --json
```

### 使用要求

- 设置 `OPENAI_API_KEY` 环境变量
- 该键需要具有聊天完成权限（API使用限制信息从最小范围的请求中提取）
- 用于获取账单/费用数据：需要具有 `api_usage.read` 权限（管理员权限）

### 自动更新（可选）

```bash
# Add to crontab for automatic updates every 10 minutes
*/10 * * * * OPENAI_API_KEY=your-key python3 {baseDir}/scripts/chatgpt-usage-fetch.py --update
```

---

## 预算管理功能

将相关设置添加到你的 `SOUL.md` 文件中：

```markdown
## Resource Awareness

**Behavior by budget level:**
| Budget | Behavior |
|--------|----------|
| 🟢 >50% | Normal operations |
| 🟡 30-50% | Be concise |
| 🟠 10-30% | Defer non-essential tasks |
| 🔴 <10% | Minimal responses only |
```

## 代理自我检查

```python
import json
from pathlib import Path

def get_claude_usage():
    path = Path.home() / ".openclaw/workspace/memory/claude-usage.json"
    if path.exists():
        data = json.loads(path.read_text())
        return data.get("limits", {}).get("five_hour", {}).get("utilization", 0)
    return 0
```

---

## 网页聊天小部件

这是一个使用Tampermonkey用户脚本实现的，可在OpenClaw网页聊天界面中实时显示使用情况。

### 安装方法

#### 1. 安装Tampermonkey

| 浏览器 | 安装链接 |
|---------|------|
| Chrome | [Chrome Web Store](https://chrome.google.com/webstore/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobfkfo) |
| Firefox | [Firefox Add-ons](https://addons.mozilla.org/en-US/firefox/addon/tampermonkey/) |
| Edge | [Edge Add-ons](https://microsoftedge.microsoft.com/addons/detail/tampermonkey/iikmkjmpaadaobahmlepeloendndfphd) |
| Safari | [Mac App Store](https://apps.apple.com/app/tampermonkey/id1482490089) |

#### 2. 创建新脚本

1. 点击Tampermonkey图标 → **“创建新脚本...”**
2. 删除所有默认内容
3. 复制 `{baseDir}/scripts/budget-panel-widget.user.js` 文件的内容
4. 将其粘贴到Tampermonkey中
5. 按 **Ctrl+S** 保存脚本

#### 3. 刷新网页聊天界面

访问 `http://localhost:18789` 并刷新页面。小部件将显示在页面的左下角。

### 故障排除

- **小部件未显示？** 确保Tampermonkey已启用
- **显示使用率为0%？** 先运行 `claude-usage-fetch.py --update`
- **出现MIME错误？** 重新启动OpenClaw服务器：`openclaw gateway stop && openclaw gateway start`

---

## 相关文件

```
token-panel-ultimate/
├── SKILL.md
├── package.json
└── scripts/
    ├── claude-usage-fetch.py       # Claude Max usage fetcher
    ├── manus-usage-fetch.py        # Manus credit usage fetcher
    └── budget-panel-widget.user.js # Webchat widget
```

---

## 网关插件

为了实现全面集成，我们提供了 **budget-panel** 网关插件：

**仓库地址：** [github.com/globalcaos/clawdbot-moltbot-openclaw](https://github.com/globalcaos/clawdbot-moltbot-openclaw)

该插件提供以下功能：
- `budget_usage` 网关方法，用于获取实时数据
- 自动读取JSON文件
- 支持多提供者的数据聚合

请将插件安装到你的OpenClaw安装目录下的 `extensions/budget-panel/` 目录中。

---

## 相关技能

- **shell-security-ultimate** - 命令安全加固工具
- **agent-memory-ultimate** - 带有使用日志的内存管理系统

---

## 致谢

本工具由 **Oscar Serra** 在 **Claude**（Anthropic公司）的帮助下开发完成。

*开发于2026年2月的一个深夜编程时段。*