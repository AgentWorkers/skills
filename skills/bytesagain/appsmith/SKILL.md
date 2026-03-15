---
name: Appsmith
description: "这是一个用于构建管理面板、内部工具和仪表板的平台。该平台能够与25种以上的数据库以及AppSmith、TypeScript、Admin-Dashboard、App-Builder、自动化工具（如CRUD）等工具集成。当您需要使用AppSmith的功能时，可以选用该平台。触发条件为：AppSmith被触发（即AppSmith开始运行或执行相关操作）。"
---
# Appsmith

一个用于构建管理面板、内部工具和仪表板的平台。支持与25种以上的数据库及任何API集成。 ## 命令

- `help` - 提供帮助信息
- `run` - 运行应用程序
- `info` - 显示应用程序信息
- `status` - 显示应用程序状态

## 特点

- 功能基于appsmithorg/appsmith的核心代码实现

## 使用方法

运行任意命令：`appsmith <命令> [参数]`
---
💬 意见反馈与功能请求：https://bytesagain.com/feedback
由BytesAgain提供支持 | bytesagain.com

## 示例

```bash
# Show help
appsmith help

# Run
appsmith run
```

- 运行 `appsmith help` 可查看所有可用命令
- 无需API密钥
- 运行 `appsmith help` 可查看所有命令的详细信息

## 配置

通过设置 `APPSMITH_DIR` 可更改数据目录。默认目录为：`~/.local/share/appsmith/`