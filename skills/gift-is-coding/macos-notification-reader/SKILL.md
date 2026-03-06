# macOS 通知阅读器

该工具能够读取 macOS 通知中心的数据库，并将最近的通知导出为 Markdown 文件。同时支持通过过滤和定时发送来自动生成工作通知摘要。

## 主要功能

- 📱 **多应用支持**：微信、Teams、Outlook、Mail、iMessage、日历、提醒事项等
- ⏰ **时间筛选**：仅获取过去 N 分钟或 N 小时的通知
- 📅 **按日期排序的输出**：导出文件路径为 `memory/YYYY-MM-DD/computer_io/notification/`
- 🤖 **定时任务**：支持自动定期导出通知
- 📊 **工作通知摘要**：自动筛选与工作相关的通知（来自 Teams/Outlook）并生成摘要
- 🔒 **隐私保护**：仅从本地数据库读取数据，不上传到云端

## 快速入门

### 1. 授予完整磁盘访问权限（必需）

该工具需要完整磁盘访问权限才能读取 macOS 通知数据库。

```bash
# Verify permission
python3 -c "import os; print('OK' if os.access(os.path.expanduser('~/Library/Group Containers/group.com.apple.usernoted/db2/db'), os.R_OK) else 'FAIL')"
```

如果返回 `FAIL`，请按照以下步骤操作：

1. 打开 **系统设置** → **隐私与安全** → **完整磁盘访问**
2. 点击 🔒 锁形图标并输入密码
3. 点击 **+**，按下 `Cmd+Shift+G`，输入 `/usr/bin/python3`，然后点击 **打开**
4. 确保权限开关处于 **开启** 状态

> **注意**：如果使用虚拟环境，请使用该虚拟环境中的 Python 可执行文件。

### 2. 测试脚本

```bash
# Navigate to the skill directory
cd /path/to/macos-notification-reader

# Basic: Read notifications from the last 35 minutes
python3 scripts/read_notifications.py --minutes 35

# Basic: Read notifications from the last 24 hours
python3 scripts/read_notifications.py --hours 24

# Advanced: Generate work notification summary (every 30 min)
bash scripts/work-summary.sh
```

### 3. 设置定时任务（推荐）

#### 选项 A：每 30 分钟导出一次通知

```bash
# Edit crontab
crontab -e

# Add this line:
*/30 * * * * /path/to/macos-notification-reader/scripts/export-notification.sh
```

#### 选项 B：每 30 分钟生成工作通知摘要

此选项会筛选与工作相关的通知（来自 Teams/Outlook）并生成摘要：

```bash
crontab -e

# Add this line:
*/30 * * * * /path/to/macos-notification-reader/scripts/work-summary.sh
```

或者使用 OpenClaw 自带的定时任务功能：

```bash
openclaw cron add --name "Work Notification Summary" --every "30m" --message "Run work-summary.sh"
```

## 脚本说明

| 脚本 | 功能 |
|--------|---------|
| `read_notifications.py` | 从数据库中读取原始通知 |
| `export_notification.sh` | 将所有通知导出为 Markdown 格式 |
| `work-summary.sh` | 筛选工作相关通知并生成摘要 |

## 工作通知摘要功能

`work-summary.sh` 脚本的主要功能包括：

1. **筛选工作相关应用**：识别来自 Teams 和 Outlook 的工作相关通知
2. **提取待办事项**：从通知内容中提取待办任务
3. **生成摘要**：创建结构化的 Markdown 报告
4. **保存路径**：`memory/YYYY-MM-DD/computer_io/notification/work-summary-YYYYMMDD-HHMMSS.md`

### 输出格式说明

```markdown
# 工作通知摘要
- Lookback: 过去 35 分钟
- 总工作通知: 5 条

## 渠道分布
- Teams: 3
- Outlook: 2

## 待处理事项（自动提取）
- [时间] (app) 消息内容摘要

## 最近工作通知（去重后）
- [时间] (app) 消息内容
```

## 输出目录

默认情况下，导出的文件会保存在以下路径：
```
~/.openclaw/workspace/memory/YYYY-MM-DD/computer_io/notification/
```

如需自定义输出目录，请修改脚本中的 `OUTPUT_DIR` 变量。

## 支持的应用程序

该工具默认支持以下应用程序：

| 应用程序包 ID | 显示名称 |
|-----------|--------------|
| com.tencent.xinWeChat | 微信 |
| com.microsoft.teams2 | Teams |
| com.microsoft.Outlook | Outlook |
| com.apple.mail | Mail |
| com.apple.mobilesms | iMessage |
| com.apple.ical | 日历 |
| com.apple.reminders | 提醒事项 |

如需添加更多应用程序，请修改 `read_notifications.py` 文件中的 `simplify_app_name()` 函数。

## 限制事项

- ⚠️ **仅支持 macOS**：该工具仅适用于 macOS 系统
- ⚠️ **需要完整磁盘访问权限**：必须手动授予该权限（详见上文）
- ⚠️ **通知保留时间有限**：macOS 会自动删除旧通知（通常为 3-7 天）
- ⚠️ **已关闭的通知无法读取**：无法读取已被用户关闭的通知

## 文件结构

```
macos-notification-reader/
├── SKILL.md                       # This file
├── _meta.json                     # Skill metadata
├── scripts/
│   ├── read_notifications.py      # Core script (file output)
│   ├── export-notification.sh     # Basic export wrapper
│   └── work-summary.sh            # Work notification summary (NEW)
└── references/
    └── permission-setup.md        # Detailed permission guide
```

## 使用场景

- 📊 **查看错过的通知**：查看您在离开时错过的通知
- 🔍 **排查通知问题**：检查特定应用程序是否发送了通知
- 📝 **每日日志记录**：自动归档通知内容
- 💼 **工作汇总**：每 30 分钟生成一次工作通知摘要
- 🤖 **自动化集成**：通过 Markdown 格式与其他工具集成

## 故障排除

### 出现 “权限被拒绝” 错误

请确保已授予完整磁盘访问权限。详情请参考 [references/permission-setup.md](references/permission-setup.md)。

### 出现 “无法找到通知数据库” 错误

- 确保使用的是 macOS 15.0 或更高版本
- 检查文件路径：`ls -la ~/Library/Group\Containers/group.com.apple.usernoted/db2/`

### 通知内容为空

- 可能是 macOS 自动删除了旧通知
- 尝试缩小时间筛选范围：使用 `--minutes 10` 参数来减少查询时间范围

---

**作者**：OpenClaw 社区  
**版本**：1.1.0  
**平台**：macOS 15.0 及以上  
**许可证**：MIT 许可证