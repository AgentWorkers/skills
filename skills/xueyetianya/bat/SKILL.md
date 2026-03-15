---
name: Bat
description: "这是一个具有翅膀的猫（cat）克隆体。它支持使用 `bat` 命令行工具、`rust` 编程语言以及 `CLI`（命令行接口）。当你需要 `bat` 的功能时，就可以使用它。触发条件是：当 `bat` 被调用或相关操作被执行时。"
---
# Bat

这是一个拥有翅膀的猫（cat）的克隆体。 ## 命令

- `help` - 显示帮助信息
- `run` - 运行命令
- `info` - 显示信息
- `status` - 显示状态

## 特性

- 基于 sharkdp/bat 的核心功能

## 使用方法

运行任意命令：`bat <命令> [参数]`
---
💬 意见反馈与功能请求：https://bytesagain.com/feedback
由 BytesAgain 提供支持 | bytesagain.com

## 示例

```bash
# Show help
bat help

# Run
bat run
```

- 运行 `bat help` 可查看所有可用命令

## 适用场景

- 用于自动化工作流程中的相关任务
- 用于批量处理相关操作

## 输出结果

命令执行结果会输出到标准输出（stdout）。若需将结果保存到文件中，可使用 `bat run > 输出文件名.txt`。

## 配置

通过设置 `BAT_DIR` 环境变量来更改数据目录。默认目录为：`~/.local/share/bat/`

## 注意事项

命令执行结果会输出到标准输出（stdout）。若需保存结果，可以使用 `bat run > 输出文件名.txt`。