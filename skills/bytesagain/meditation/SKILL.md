---
name: meditation
version: 1.0.0
author: BytesAgain
license: MIT-0
tags: [meditation, tool, utility]
---

# 冥想

这是一个用于辅助冥想的工具包，提供引导式冥想会话计时器、呼吸练习、情绪记录、连续冥想次数统计、环境音效以及冥想会话历史记录等功能。

## 命令

| 命令 | 描述 |
|---------|-------------|
| `meditation start` | [开始冥想，持续 [分钟]] |
| `meditation breathe` | [执行特定的呼吸模式] |
| `meditation mood` | [输入 1-10 之间的数字，表示当前的情绪状态（1-10 分为 1-10 分的焦虑程度）] |
| `meditation streak` | [记录连续冥想的次数] |
| `meditation history` | [查看所有冥想会话的历史记录] |
| `meditation sounds` | [播放指定的环境音效] |

## 使用方法

```bash
# Show help
meditation help

# Quick start
meditation start [minutes]
```

## 示例

```bash
# Example 1
meditation start [minutes]

# Example 2
meditation breathe [pattern]
```

- 输入 `meditation help` 可查看所有可用命令。

---
*由 BytesAgain 提供支持 | bytesagain.com*
*反馈与功能请求：https://bytesagain.com/feedback*

## 使用场景

- 从终端快速执行冥想任务
- 用于自动化流程中

## 输出结果

所有输出结果会显示在标准输出（stdout）中。可以使用 `meditation run > output.txt` 将输出内容保存到文件中。

## 使用场景

- 从终端快速执行冥想任务
- 用于自动化流程中