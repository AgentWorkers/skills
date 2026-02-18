---
name: daily-oracle
version: 1.1.0
description: 一个后台代理程序，通过分析本地数据和社会信号来生成日常生活预测。
author: https://github.com/Invelene
repository: https://github.com/Invelene/Futurizzm/daily-oracle
requirements:
  - browser-automation
  - calendar-access
  - local-file-search
  - sqlite-access
permissions:
  - read: browser_cookies (instagram.com, twitter.com)
  - read: local_db (imessage/chat.db)
  - read: calendar
  - read: filesystem (downloads)
safety_policy: "local-only"
---
# 每日预言（自动化）

该技能设计为以后台进程（Cron作业）的形式运行。它会在后台启动，分析用户的数字行为数据，生成预测结果，发送通知后自动终止。

**⚠️ 隐私声明：** 该技能会处理高度敏感的个人信息。所有分析必须在本地大语言模型（LLM）的上下文中完成，严禁将任何数据发送给第三方日志服务。

## 执行流程

### 1. 初始化与防止被封禁

- **背景**：由于该任务由精确的Cron定时器触发（例如，恰好在08:00:00），立即执行可能会被系统识别为机器人行为。
- **操作**：生成一个介于120到900秒之间的随机整数。
- **等待**：等待指定的时间后再进行任何网络请求。
  ```bash
  sleep $(( RANDOM % 780 + 120 ))
  ```

### 2. 静默数据收集

#### A. 日历数据

- **操作**：读取本地日历中今天的所有事件（00:00至23:59）。
- **工具使用**：使用`calendar-access`或相应的命令行工具（例如，在macOS上使用`icalBuddy`）。
  - **提示**：“总结今天00:00至23:59之间的日历事件，重点关注会议和空闲时间。”

#### B. 社交媒体数据（无界面操作）

- **操作**：使用现有的cookies打开无界面的浏览器会话。
- **目标**：扫描用户最近日历/消息中出现的“密友”或共同联系人。
- **安全措施**：滚动浏览量限制在5条帖子/故事以内。如果系统要求登录，则立即终止会话，以防被标记为异常行为。
- **数据提取**：从特定URL（例如`instagram.com/direct/inbox/`）的第一个视口中截图或提取文本。

#### C. 消息通信数据（iMessage/本地数据库）

- **操作**：读取本地`chat.db`文件中的最后50条消息。
- **查询**：
  ```sql
  SELECT
      text,
      datetime(date/1000000000 + 978307200, 'unixepoch', 'localtime') as date_sent
  FROM message
  WHERE date_sent > datetime('now', '-24 hours')
  ORDER BY date DESC
  LIMIT 50;
  ```
- **过滤**：查找包含以下关键词的消息：“tomorrow”、“gym”、“coffee”、“meet”、“lunch”、“tonight”。

#### D. 系统信号数据

- **操作**：检查`~/Downloads`目录中是否有新下载的文件。
  ```bash
  find ~/Downloads -type f -mtime -1 -print
  ```
- **分析**：根据文件类型（如PDF或图片）判断用户的当前活动或兴趣。

### 3. 预测结果生成

- **数据整合**：将硬性数据（日历中的“下午5点去健身房”）与软性数据（社交媒体中的“Amy提到想喝咖啡”）结合起来。
- **预测**：生成一个基于当前信息的、具有高置信度的未来时态句子。
- **表达方式**：简洁明了且富有洞察力。例如：“你今天会在健身房遇到Amy，她可能会建议锻炼后一起去喝咖啡，因为她提到了自己对咖啡的渴望。”

### 4. 发送通知（重要提示）

- **考虑因素**：用户可能不会查看终端或聊天窗口。
- **操作**：使用系统的默认通知工具。
  - **macOS**：`osascript -e 'display notification "您的预测是..." with title "每日预言"'`
  - **Linux**：`notify-send "每日预言" "您的预测是..."`
- **格式**：
  > 🔮 **每日预言**：[你的预测内容]

## 限制与安全要求

1. **一次性执行**：整个流程必须连续完成，不得等待用户输入。
2. **异常处理**：如果数据不足无法做出具体预测，应使用基于天气的通用健康建议作为替代方案。切勿无声地失败。
3. **数据清理**：预测结果发送后，必须立即清除所有临时存储的数据。
4. **信息保密**：通知内容仅包含预测结果及预测的依据，严禁透露数据来源。