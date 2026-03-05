# macOS 通知阅读器

该工具可读取 macOS 通知中心的数据库，并将最近的通知内容导出为 Markdown 文件。适用于查看错过的通知、记录日常活动或排查通知相关问题。

## 主要功能

- 📱 **多应用支持**：支持微信（WeChat）、Teams、Outlook、Mail、iMessage、Calendar、Reminders 等应用程序的通知。
- ⏰ **时间过滤**：可仅获取过去 N 分钟或 N 小时的通知。
- 📅 **按日期排序的输出**：导出的文件路径格式为 `memory/YYYY-MM-DD/computer_io/notification/`。
- 🤖 **定时任务**：支持自动定期导出通知内容。
- 🔒 **隐私保护**：仅从本地数据库读取数据，不会上传到云端。

## 快速入门

### 1. 授予完整磁盘访问权限（必需）

该工具需要完整磁盘访问权限才能读取 macOS 通知数据库。

```bash
# Verify permission
python3 -c "import os; print('OK' if os.access(os.path.expanduser('~/Library/Group Containers/group.com.apple.usernoted/db2/db'), os.R_OK) else 'FAIL')"
```

如果提示“FAIL”，请按照以下步骤操作：

1. 打开 **系统设置** → **隐私与安全** → **完整磁盘访问权限**。
2. 点击锁形图标并输入密码。
3. 点击 “+” 按钮，同时按下 `Cmd+Shift+G`，输入 `/usr/bin/python3`，然后点击 “打开”。
4. 确保权限开关处于 “开启” 状态。

> **注意**：如果使用虚拟环境，请使用该虚拟环境中的 Python 可执行文件。

### 2. 测试脚本

```bash
# Navigate to the skill directory
cd /path/to/macos-notification-reader

# Read notifications from the last 35 minutes
python3 scripts/read_notifications.py --minutes 35

# Read notifications from the last 24 hours
python3 scripts/read_notifications.py --hours 24

# Limit the number of results
python3 scripts/read_notifications.py --hours 1 --limit 50
```

### 3. 设置定时任务（推荐）

若希望每 30 分钟自动导出一次通知，请设置一个定时任务：

```bash
# Edit crontab
crontab -e

# Add this line (adjust paths as needed):
*/30 * * * * /path/to/macos-notification-reader/scripts/export-notification.sh
```

或者使用 OpenClaw 内置的定时任务功能（如果可用）：

```bash
openclaw cron add --schedule "*/30 * * *" --command "bash /path/to/macos-notification-reader/scripts/export-notification.sh"
```

## 输出格式

脚本会将通知内容以 Markdown 表格格式输出：

```markdown
# macOS Notifications Export
- Date: 2026-03-05
- Timestamp: 20260305-112000
- Total: 15 items

## Notifications

| Time | App | Content |
|------|-----|---------|
| 2026-03-05 11:15:32 | WeChat | Contact Name: Hello message |
| 2026-03-05 10:30:00 | Teams | Meeting reminder: Weekly Standup |
```

## 配置

### 输出目录

默认情况下，通知文件会被保存在以下路径：
```
~/.openclaw/workspace/memory/YYYY-MM-DD/computer_io/notification/
```

如需自定义输出目录，请编辑 `export_notification.sh` 文件并修改 `OUTPUT_DIR` 变量。

### 支持的应用程序

该工具默认支持以下应用程序的通知：

| 应用程序包 ID | 显示名称 |
|-----------|--------------|
| com.tencent.xinWeChat | 微信 |
| com.microsoft.teams2 | Teams |
| com.microsoft.Outlook | Outlook |
| com.apple.mail | Mail |
| com.apple.mobilesms | iMessage |
| com.apple.ical | Calendar |
| com.apple.reminders | Reminders |

如需添加更多应用程序，请编辑 `read_notifications.py` 文件中的 `simplify_app_name()` 函数。

## 限制

- ⚠️ **仅支持 macOS**：该工具仅适用于 macOS 系统。
- ⚠️ **需要完整磁盘访问权限**：必须手动授予该权限（详见上文）。
- ⚠️ **数据保留时间有限**：macOS 会自动删除旧通知，因此该工具只能访问数据库中仍然存在的通知。
- ⚠️ **通知状态**：无法读取用户已明确关闭的通知。

## 文件结构

```
macos-notification-reader/
├── SKILL.md                  # This file
├── _meta.json                # Skill metadata
├── scripts/
│   ├── read_notifications.py # Core script (file output)
│   └── export-notification.sh # Wrapper for cron usage
└── references/
    └── permission-setup.md   # Detailed permission guide
```

## 使用场景

- 📊 **查看错过的通知**：快速查看离开期间错过的通知内容。
- 🔍 **排查通知问题**：检查特定应用程序是否发送了通知。
- 📝 **每日记录**：自动归档通知内容以供后续查看。
- 🤖 **自动化**：通过 Markdown 输出结果与其他工具集成。

## 故障排除

### 出现 “权限被拒绝” 错误

可能是您尚未授予完整磁盘访问权限。请参考 [references/permission-setup.md](references/permission-setup.md) 文档进行设置。

### 出现 “无法找到通知数据库” 错误

- 确保您使用的是 macOS 15.0 或更高版本。
- 检查数据库路径是否正确：
  ```bash
  ls -la ~/Library/Group\ Containers/group.com.apple.usernoted/db2/
  ```

### 通知内容为空

- 可能是 macOS 已删除了旧通知。
- 尝试缩小时间范围（例如，将 `--hours 24` 更改为 `--minutes 10`）。

---

**作者**：OpenClaw 社区  
**版本**：1.0.0  
**适用平台**：macOS 15.0 及以上  
**许可证**：MIT 许可证