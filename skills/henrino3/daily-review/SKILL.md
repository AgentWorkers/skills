---
name: daily-review
version: 1.0.0
description: 全面的每日绩效评估，包括沟通记录、会议分析、输出指标以及专注时间的监控。您的AI绩效教练。
author: henrino3
tags: [productivity, performance, tracking, review, coach]
---

# 日常绩效回顾功能

该功能利用人工智能技术生成全面的每日绩效报告，并提供相应的辅导建议。

## 功能列表

| 功能                | 来源                | 状态                |
|------------------|------------------|------------------|
| 发送的电子邮件       | Gmail API            | ✅                |
| Slack消息             | Slack API            | ✅                |
| X.com上的提及           | Bird CLI             | ✅                |
| 参加的会议             | Fireflies（确认发言者身份）    | ✅                |
| Git提交             | git log             | ✅                |
| 修改的文档             | Google Drive API        | ✅                |
| 屏幕使用时间         | macOS knowledgeC.db       | ✅                |
| ActivityWatch         | AW API             | ✅                |

## 使用方法

```bash
# Run daily review for today
~/clawd/skills/daily-review/scripts/daily-review.sh

# Run for specific date
~/clawd/skills/daily-review/scripts/daily-review.sh 2026-01-15
```

## 示例输出

```
🏆 Daily Performance Review - 2026-01-15
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📬 COMMUNICATION
  • Emails sent: 6
  • Slack messages: 203
  • X.com mentions: 5

📅 MEETINGS (Fireflies - speaker verified)
  • CEO Chat (70 min)
  • Meeting with Perfectos (27 min)
  • US Squad Standup (27 min)
  Total: 3 meetings (~2.0 hrs)

💻 OUTPUT
  • Git commits: 6
  • Docs modified: 20
  • Messages to Ada: 73

⏱️ FOCUS TIME
  Screen Time: 9.7 hrs
  • Atlas: 203min
  • Slack: 163min
  • Telegram: 45min
  
  ActivityWatch: 8.5 hrs
  • Telegram: 120min
  • Ghostty: 90min
  • Chrome: 45min
```

## 系统要求

### 所需API与服务
- **Gmail**: Google Workspace服务账户或gog OAuth认证
- **Slack**: Slack API令牌（用于搜索功能）
- **Fireflies**: 会议记录的API密钥
- **Google Drive**: 用于跟踪文档变更的服务账户

### 所需工具
- **Bird CLI**: 用于处理X.com/Twitter数据（需要auth_token和ct0 cookies）
- **ActivityWatch**: 用于记录用户活动的本地应用程序（http://localhost:5600）

### macOS（用于获取屏幕使用时间）
- 需要通过SSH访问Mac电脑
- 使用`get_screentime.py`脚本查询knowledgeC.db数据库中的数据

## 安装步骤

1. 将该功能复制到您的clawd工作空间：
```bash
cp -r daily-review ~/clawd/skills/
```

2. 安装所需依赖项：
```bash
# Bird CLI (on Mac)
cd ~/Code && git clone https://github.com/steipete/bird.git
cd bird && npm install && npm run build:dist

# ActivityWatch
# Download from https://activitywatch.net/
```

3. 配置相关密钥：
```bash
# Bird (X.com)
cat > ~/clawd/secrets/bird.env << 'EOF'
AUTH_TOKEN=your_auth_token
CT0=your_ct0
EOF

# Fireflies
echo "your_api_key" > ~/clawd/secrets/fireflies.key

# Slack
echo '{"user_token": "xoxp-xxx"}' > ~/clawd/secrets/slack-super-ada.json
```

4. 设置每日09:00自动执行审查任务的cron作业：
```bash
clawdbot cron add --name "daily-review" --schedule "0 9 * * *"
```

## 屏幕使用时间查询

该功能直接从`knowledgeC.db`数据库中获取Mac电脑的屏幕使用时间数据：

```python
SELECT 
  ZVALUESTRING as app,
  SUM(ZENDDATE - ZSTARTDATE) as seconds
FROM ZOBJECT 
WHERE ZSTREAMNAME = '/app/usage' 
AND date(ZSTARTDATE + 978307200, 'unixepoch') = '2026-01-15'
GROUP BY ZVALUESTRING
ORDER BY seconds DESC
```

## Fireflies发言者身份验证

会议的有效性通过检查用户是否实际参与了发言（而不仅仅是被邀请）来确认：

```graphql
{
  transcripts(limit: 30) {
    title dateString duration
    sentences { speaker_name }
  }
}
```

只有`speaker_name`字段中包含用户姓名的会议才会被计入统计范围内。

## 许可证

MIT许可证