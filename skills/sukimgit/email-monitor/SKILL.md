---
name: email-monitor
version: 2.0.0
description: Email Monitor v2.0 – 自动电子邮件监控功能，支持使用商务回复模板；通过 Feishu 平台发送通知以提醒潜在的商业机会。
author: sukimgit
license: MIT
tags: [email, automation, business, reply, notification, feishu]
metadata:
  {"openclaw": {"emoji": "email", "requires": {"bins": ["python"], "python_packages": ["requests"]}, "primaryEnv": "EMAIL_PASSWORD"}}
---
# Email Monitor v2.0

**由 Efficiency Lab 开发**

具备智能商务回复模板的自动电子邮件监控系统。

## 主要功能

- 自动电子邮件监控（每 30 分钟一次）
- 商机检测
- 使用双语模板（中文/英文）自动回复
- 与 Feishu 实时同步通知
- 垃圾邮件过滤
- 速率限制（防止被封禁）

## 安装

```bash
pip install requests
cp email_config.example.json email_config.json
python check_emails_complete.py
```

## 配置

使用您的电子邮件凭据和 Feishu Webhook URL 修改 `email_config.json` 文件。

## 商务回复模板（v2.0 新增）

提供了 3 个专业的商务回复模板：

1. **商务咨询** - 触发条件：报价/价格/合作/定制
2. **一般咨询** - 触发条件：咨询/询问/服务
3. **技术集成** - 触发条件：API/集成/技术相关问题

## 价格方案

- **标准版**：免费（基础监控 + 自动回复）
- **专业版**：每月 350 元（支持多封电子邮件 + 数据分析）
- **定制版**：7000-20000 元（私有部署 + 个性化定制）

## 联系方式

Efficiency Lab
- 电子邮件：1776480440@qq.com
- 网站：https://clawhub.ai

## 更新日志

### v2.0.0 (2026-03-08)
- 新增：Efficiency Lab 的品牌标识
- 新增：3 个商务回复模板
- 新增：自动模板选择功能
- 优化了与 Feishu 的通知同步机制

### v1.0.7 (2026-03-05)
- 首次发布