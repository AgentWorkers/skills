---
name: system-uptime
description: "使用系统自带的 `uptime` 命令来获取当前的系统运行时间。适用场景：当用户询问系统运行时间、系统状态或系统已经运行了多久时。"
metadata: { "openclaw": { "emoji": "⏱️", "requires": { "bins": ["uptime"] } } }
---
# 系统运行时间技能

使用内置的 `uptime` 命令获取当前系统的运行时间。

## 适用场景

✅ **在以下情况下使用此技能：**
- “系统的运行时间是多少？”
- “系统已经运行了多久？”
- “显示系统状态”
- “上次重启是什么时候？”

## 不适用场景

❌ **在以下情况下不要使用此技能：**
- 需要详细的系统指标时 → 使用监控工具
- 需要获取远程系统的运行时间时 → 使用 SSH 或远程监控工具
- 需要查看历史运行时间数据时 → 查看系统日志

## 命令

### 获取系统运行时间

```bash
# Basic uptime
uptime

# Using the skill CLI
node uptime-cli.js
```

## 示例输出

```
11:30:45 up 2 days, 4:23, 2 users, load average: 1.23, 1.15, 1.08
```

## 注意事项：
- 使用标准的 Unix `uptime` 命令
- 适用于 macOS、Linux 及其他类 Unix 系统
- 无需额外依赖项