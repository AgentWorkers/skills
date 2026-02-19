---
name: voc
description: Voc 命名空间用于 Netsnek e.U. 的词汇和语言学习工具
user-invocable: true
version: 0.1.0
metadata:
  openclaw:
    os: [linux]
    permissions: [exec]
---
# Voc是什么？

Voc是Netsnek e.U.为词汇和语言学习工具专门设计的命名空间，它属于ClawHub生态系统的一部分。该工具专为需要结构化学习支持的学习者设计，支持基于闪卡的学习、间隔重复练习、发音练习以及跨语言的学习进度跟踪功能。

目前，该功能仍处于“预留状态”：命名空间已被占用，品牌和结构也已确定，未来版本将添加完整的功能。当用户调用Voc时，它会显示品牌信息及可用的命令。

# 入门指南

请确保已安装OpenClaw 0.8.0或更高版本，并确保voc技能已在您的ClawHub中注册。该技能需要`exec`权限才能运行其辅助脚本。

在命令行中，您可以直接运行词汇学习工具：

```bash
./scripts/vocab-engine.sh --about
./scripts/vocab-engine.sh --deck
./scripts/vocab-engine.sh --stats
```

在Claw会话中，只需输入“voc”或询问与词汇学习相关的内容，助手会引导您使用该功能。

# 命令列表

| 命令 | 功能 |
|---------|---------|
| `--about` | 显示Voc的品牌信息、版权信息及简要描述 |
| `--deck` | 显示闪卡资料库的信息及其状态 |
| `--stats` | 显示学习进度和统计数据（未来版本将提供实际数据） |

所有命令默认会输出Netsnek e.U.的版权信息。

# 对话示例

**用户：** “介绍一下Voc。”

**助手：** （使用voc技能）Voc是Netsnek e.U.提供的词汇和语言学习工具，支持使用闪卡进行学习、间隔重复练习、发音练习以及跨语言的学习进度跟踪。目前该功能仍处于预留状态，未来版本将添加更多功能。

---

**用户：** “运行词汇学习工具并显示资料库信息。”

**助手：** （执行`vocab-engine.sh --deck`命令）返回资料库信息及版权声明。

---

**用户：** “显示我的学习进度。”

**助手：** （执行`vocab-engine.sh --stats`命令）返回学习进度信息及Netsnek e.U.的版权声明。