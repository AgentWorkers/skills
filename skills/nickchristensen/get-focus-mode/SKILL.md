---
name: get-focus-mode
description: 获取当前的 macOS 焦点模式
---

# 获取当前激活的 macOS 专注模式

返回当前激活的 macOS 专注模式的名称。

## 使用方法

```bash
~/clawd/skills/get-focus-mode/get-focus-mode.sh
```

## 输出结果

将专注模式的名称输出到标准输出（stdout）：
- "No Focus" - 专注模式未启用
- "Office" - 办公模式已激活
- "Sleep" - 睡眠模式已激活
- "Do Not Disturb" - 防打扰模式已激活

## 系统要求

- 必须使用 macOS 操作系统
- 需要安装 `jq` 工具