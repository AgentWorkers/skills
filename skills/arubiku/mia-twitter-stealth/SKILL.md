---
name: mia-twitter-stealth
description: 利用高级的隐蔽性和反检测技术实现 Twitter/X 的自动化操作
version: 1.0.0
author: MiaBloomx
tags:
  - twitter
  - automation
  - stealth
  - anti-detection
  - social-media
metadata:
  clawdbot:
    emoji: 🕵️‍♀️
---

# Mia Twitter 隐秘操作 🕵️‍♀️

使用先进的隐秘技术实现 Twitter/X 的自动化操作，以避免被机器人检测到。

## 防检测功能

### 1. Playwright 隐秘模式
- 隐藏 `navigator.webdriver`
- 掩盖 Chrome 自动化标志
- 模拟插件和语言设置

### 2. 带界面的模式（Headful Mode）
- 默认设置为 `headless: false`
- 显示真实的浏览器用户界面
- 避免被检测为无界面的自动化脚本

### 3. 人类行为模拟
- 随机输入延迟（50-150 毫秒）
- 模拟鼠标移动
- 随机等待时间
- 自然的滚动行为

### 4. 会话持久化
- 使用 Cookie 存储数据
- 利用 LocalStorage 保存状态
- 保存用户数据到指定目录

### 5. 冷却机制管理
- 监控操作频率
- 实现自动延迟
- 如果被检测到异常行为，24 小时内禁止再次操作

## 使用方法

```bash
# Post tweet
mia-twitter post "Hello world"

# Reply to tweet
mia-twitter reply <tweet-id> "Great post!"

# Like tweets by search
mia-twitter like --search "AI agents" --limit 10

# Follow users
mia-twitter follow --search "founder" --limit 5

# Check notifications
mia-twitter notifications
```

## 安全性限制
- 每小时最多执行 5 次操作
- 每天最多执行 50 次操作
- 每次操作之间需等待 2-5 分钟
- 仅模拟人类真实的使用行为

## 所需环境变量
- `X_AUTH_TOKEN` 环境变量
- `X_CT0` 环境变量
- 需要使用基于 Chromium 的 Playwright 库