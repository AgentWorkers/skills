---
name: pomodoro
description: 当用户希望通过终端运行定时专注训练（Pomodoro 技巧）时，请使用此技能。
---

# Pomodoro 计时器

## 使用场景

- 当用户需要开始一个专注工作时段、设置计时器或使用 Pomodoro 工作法时。

## 工作原理

首先执行 25 分钟的专注工作时间，然后休息 5 分钟。完成 4 个这样的工作周期后，再进行 15 分钟的长时间休息。

## 开始一个工作周期

```bash
echo "🍅 Focus started at $(date +%H:%M)" && sleep 1500 && osascript -e 'display notification "Time for a break!" with title "Pomodoro"' && echo "Break time at $(date +%H:%M)"
```

## 自定义工作时长（分钟）

```bash
MINS=15 && echo "Focus: ${MINS}m started at $(date +%H:%M)" && sleep $((MINS * 60)) && echo "Done at $(date +%H:%M)"
```

## 记录已完成的工作周期

```bash
echo "$(date +%Y-%m-%d) $(date +%H:%M) - 25min focus" >> ~/pomodoro.log
```

## 查看今天的工作记录

```bash
grep "$(date +%Y-%m-%d)" ~/pomodoro.log 2>/dev/null || echo "No sessions today."
```