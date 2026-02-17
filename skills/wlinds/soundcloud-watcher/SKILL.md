---
name: soundcloud-watcher
description: 监控您的 SoundCloud 账户，跟踪艺术家的新作品发布，并在收到新粉丝或点赞时收到通知。
metadata:
  display_name: SoundCloud Watcher
  homepage: https://github.com/wlinds/OpenClaw-SoundCloud-Watcher
  tags:
    - soundcloud
    - music
    - notifications
    - openclaw-plugin
---
# SoundCloud 监控工具

此技能可将您的 OpenClaw 代理与 SoundCloud 账户连接起来。

**功能包括：**
- 检查设置状态和账户信息
- 监控特定艺术家的新作品发布
- 收到关于粉丝和点赞的通知
- 作为 Cron 作业在后台静默运行

| 命令 | 描述 |
|---------|-------------|
| `/soundcloud-setup` | 显示设置说明和配置状态 |
| `/soundcloud-status` | 显示监控状态和账户信息 |
| `/soundcloud-check` | 立即进行检查（输出详细信息） |
| `/soundcloud-cron` | 自动化检查（无更新时静默运行） |
| `/soundcloud-add <username>` | 监控指定的艺术家（用户名用空格分隔） |
| `/soundcloud-remove <username>` | 停止监控指定的艺术家 |
| `/soundcloud-list` | 列出所有被监控的艺术家 |

## 安装

```bash
openclaw plugins install @akilles/soundcloud-watcher
openclaw plugins enable soundcloud-watcher
openclaw gateway restart
```

## 配置

创建文件 `~/.openclaw/secrets/soundcloud.env`：

```
SOUNDCLOUD_CLIENT_ID=your_client_id
SOUNDCLOUD_CLIENT_SECRET=your_client_secret
MY_USERNAME=your_soundcloud_username
```

然后在聊天界面中执行相应操作：

```
/soundcloud-setup
/soundcloud-status
```

若需自动化执行，请添加以下 Cron 作业：

```bash
openclaw cron add --name "soundcloud-check" \
  --every 6h \
  --isolated \
  --message "Run /soundcloud-cron and forward any updates to me."
```