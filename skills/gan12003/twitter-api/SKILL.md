---
name: twitter-agent-skill
description: "基于Cookie的Twitter/X自动化工具包（用于OpenClaw代理程序），支持时间线查看、通知接收、内容发布以及关注操作。"
metadata:
  openclaw:
    emoji: "🐦"
    requires:
      bins: ["python", "git"]
---
# twitter-agent-skill

## 概述
这是一个异步的 Twitter/X 客户端及脚本工具，依赖于 `auth_token` 和 `ct0` cookies（无需官方 API 密钥）。支持以下功能：
- 获取个人主时间线内容及摘要（`scripts/timeline_summary.py`）。
- 获取通知信息并分析通知信号（`scripts/fetch_notifications.py`, `scripts/analyze_signal.py`）。
- 通过环境变量驱动的账户标签实现自动发帖和关注操作（`scripts/post_custom_tweet.py`, `scripts/follow_account.py`）。
- 提供完整的异步客户端功能（`twitter_api/`），包含处理推文、用户、关系、私信等数据的模块。

## 设置方法
1. 使用 `pip install -r requirements.txt`（Python 3.10 及以上版本）安装所需依赖库。
2. 将 `.env.example` 文件复制到 `.env` 文件中，并根据实际登录会话填写相应的 `auth_token` 和 `ct0` 值。
3. 从仓库根目录运行相关脚本，例如：
   ```
   python scripts/timeline_summary.py
   python scripts/post_custom_tweet.py account_a "hello"
   python scripts/follow_account.py thenfter07
   ```

## 注意事项
- 环境变量名称为通用格式（如 `ACCOUNT_A_AUTH_TOKEN` 等）；可根据需要进行重命名，并调整脚本中的 `ACCOUNT_ENV` 字典。
- 请遵守 Twitter/X 的服务条款，避免发送垃圾信息。
- 该工具专为 GanClaw 的社交操作设计，但结构较为通用，其他代理也可以直接使用。