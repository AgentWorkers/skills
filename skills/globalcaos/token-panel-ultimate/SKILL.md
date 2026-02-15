---
name: token-panel-ultimate
version: 1.0.5
description: 多提供商使用跟踪功能：支持在同一个仪表板中监控Claude Max、Gemini和Manus等AI代理的使用情况。
homepage: https://clawhub.com/skills/token-panel-ultimate
metadata:
  openclaw:
    emoji: "🎛️"
    requires:
      bins: ["python3"]
---

# Token Panel ULTIMATE

> 🎛️ 了解自己的使用限制，并严格遵守它们。最大限度地发挥你的能力。

**Claude Max**、**Gemini** 和 **Manus** 的实时使用情况追踪——全部集中在一个地方。

---

## 功能

| 提供商 | 追踪内容 |
|----------|----------------|
| **Claude Max** | 5小时周期、7天周期的使用数据及重置时间 |
| **Gemini** | 每个模型的 RPD/RPM/TPM 数据及瓶颈检测 |
| **Manus** | 每日更新的数据、每月的信用额度以及附加功能的余额 |

此外，还提供了一个 **网页聊天小部件**，可以一目了然地查看所有信息。

---

## Claude Max 使用情况追踪

实时追踪你的 Claude Max 订阅使用情况。

### 显示内容

- **5小时周期**：滚动显示的使用百分比及重置时间
- **7天周期**：每周的使用百分比及重置时间
- **模型特定的限制**：Sonnet 和 Opus 的使用额度分配

---

### 使用要求

- 已安装并登录 Claude Code CLI (`claude /login`)

### 自动更新（可选）

---

## Gemini 多模型追踪

追踪每个模型的 **瓶颈指标**（RPD、RPM、TPM 中的最高值）。

### 模型限制（第一层级）

| 模型 | RPM | TPM | RPD |
|-------|-----|-----|-----|
| gemini-3-pro | 25 | 1M | 250 |
| gemini-2.5-pro | 25 | 1M | 250 |
| gemini-2.5-flash | 2000 | 4M | **∞** |
| gemini-3-flash | 1000 | 1M | 10K |
| gemini-2.0-flash | 2000 | 4M | **∞** |

### 备用策略

优先使用性能最强的模型；对于 RPD 指标达到上限的模型，提供无限使用额度作为保障。

**重置时间**：太平洋标准时间午夜（RPD 每日重置）

### JSON 格式

数据存储在 `memory/gemini-usage.json` 文件中：

---

## Manus 信用额度监控

### 信用额度结构

- **每月**：4,000 信用额度（续费时重置）
- **每日更新**：300 信用额度（凌晨 1:00 重置）
- **附加功能**：购买的信用额度（永久有效）

### 使用要求

- 设置 `MANUS_API_KEY` 环境变量

### 自动更新（可选）

---

### JSON 格式

数据存储在 `memory/manus-usage.json` 文件中（由自动获取脚本生成）：

---

## 预算管理功能

将相关设置添加到你的 SOUL.md 文件中：

---

## 代理自我检查功能

---

## 网页聊天小部件

这是一个使用 Tampermonkey 的用户脚本，可以在 OpenClaw 的网页聊天中显示实时使用情况。

### 安装方法

#### 1. 安装 Tampermonkey

| 浏览器 | 安装链接 |
|---------|------|
| Chrome | [Chrome Web Store](https://chrome.google.com/webstore/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobfkfo) |
| Firefox | [Firefox Add-ons](https://addons.mozilla.org/en-US/firefox/addon/tampermonkey/) |
| Edge | [Edge Add-ons](https://microsoftedge.microsoft.com/addons/detail/tampermonkey/iikmkjmpaadaobahmlepeloendndfphd) |
| Safari | [Mac App Store](https://apps.apple.com/app/tampermonkey/id1482490089) |

#### 2. 创建新脚本

1. 点击 Tampermonkey 图标 → **“创建新脚本...”**
2. 删除所有默认内容
3. 复制 `{baseDir}/scripts/budget-panel-widget.user.js` 文件的内容
4. 将其粘贴到 Tampermonkey 中
5. 按 **Ctrl+S** 保存

#### 3. 刷新网页聊天界面

访问 `http://localhost:18789` 并刷新页面。小部件将显示在页面的左下角。

### 故障排除

- **小部件未显示？** 确保 Tampermonkey 已启用
- **显示使用率为 0%？** 先运行 `claude-usage-fetch.py --update`
- **出现 MIME 错误？** 全面重启系统：`openclaw gateway stop && openclaw gateway start`

---

## 相关文件

---

## 网关插件

为了实现完整集成，我们的 OpenClaw 分支中提供了 **budget-panel** 网关插件：

**仓库地址：** [github.com/globalcaos/clawdbot-moltbot-openclaw](https://github.com/globalcaos/clawdbot-moltbot-openclaw)

该插件提供以下功能：
- `budget_usage` 网关方法，用于获取实时数据
- 自动读取 JSON 文件
- 支持多提供者的数据聚合

将插件安装到 OpenClaw 的 `extensions/budget-panel/` 目录下。

---

## 相关技能

- **shell-security-ultimate**：命令安全加固功能
- **agent-memory-ultimate**：带有使用日志的内存管理系统

---

## 致谢

本工具由 **Oscar Serra** 在 **Claude**（Anthropic）的帮助下开发完成。

*开发于 2026 年 2 月的一个深夜编程会议期间。*