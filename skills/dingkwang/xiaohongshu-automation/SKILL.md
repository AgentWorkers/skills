---
name: xiaohongshu-automation
description: 这是一个专为小红书（Little Red Book）设计的完整自动化套件，涵盖了长文本发布、评论管理（回复/查看）以及隐藏式登录辅助功能。
author: Dingkang Wang
---
# 小红书自动化套件

本技能包提供了一套工具，用于自动化您的小红书内容创作和社区管理。

## 包含的工具

### 1. 📝 发布内容（xiaohongshu-publish）
- **publish_long_text**：自动发布带有标题和内容的长篇文章。
- 支持“Pro”平台（pro.xiaohongshu.com）。

### 2. 💬 社区管理（xiaohongshu-reply）
- **check_comments**：获取并回复最新的评论。
- **reply_fixed**：替代的回复逻辑。
- **generate_replies**：生成模板回复。

### 3. 🔐 认证
- **login_helper**：使用Playwright实现的隐式登录脚本（独立使用，无需插件）。
- 管理和持久化Cookie。

## 使用方法

### 登录（首次使用）
运行登录辅助工具以获取Cookie：
```bash
python3 skills/xiaohongshu-skill/login_helper.py
```

### 发布文章
```bash
python3 skills/xiaohongshu-skill/xiaohongshu-publish/publish_long_text.py --title "My Title" --content "My Content"
```

## 兼容要求
- Python 3.8及以上版本
- Playwright（需安装：`pip install playwright && playwright install chromium`）