---
name: Coze Studio
description: "这是一个AI代理开发平台，集成了所有必要的可视化工具，能够简化代理的创建与调试过程。该平台支持TypeScript语言，涵盖了代理本身、代理平台以及相关的AI插件和聊天机器人框架。当您需要使用Coze Studio的功能时，可以借助该平台进行开发。该平台会在Coze Studio触发相应的操作。"
---
# Coze Studio

这是一个用于开发AI代理的平台，集成了全方位的可视化工具，极大地简化了代理的创建、调试和部署过程。通过Coze Studio，您可以更轻松地构建AI代理。

## 命令

- `help` - 显示帮助信息
- `run` - 运行程序
- `info` - 查看信息
- `status` - 查看状态

## 功能

- 兼容 `coze-dev/coze-studio` 的核心功能

## 使用方法

运行任意命令：`coze-studio <command> [args]`

---

💬 意见反馈与功能请求：https://bytesagain.com/feedback
由 BytesAgain 提供支持 | bytesagain.com

## 示例

```bash
# Show help
coze-studio help

# Run
coze-studio run
```

- 运行 `coze-studio help` 可以查看所有可用命令。

---

## 配置

您可以通过设置 `COZE_STUDIO_DIR` 来更改数据目录。默认目录为：`~/.local/share/coze-studio/`