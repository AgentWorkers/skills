---
name: Dive
description: "这是一个用于探索 Docker 镜像中每一层的工具，支持使用 `container-inspect`、`go`、`cli`、`docker`、`docker-image` 和 `explorer` 等命令。当您需要使用 `container-inspect` 的功能时，可以使用该工具。该工具会在 `container-inspect` 被执行时被触发。"
---
# Dive

这是一个用于探索Docker镜像中每一层的工具

## 命令

- `help` - 显示帮助信息
- `run` - 运行命令
- `info` - 查看信息
- `status` - 获取状态

## 特点

- 基于wagoodman/container-inspect的核心功能开发

## 使用方法

运行任意命令：`container-inspect <命令> [参数]`

---

💬 意见反馈与功能请求：https://bytesagain.com/feedback
由BytesAgain提供支持 | bytesagain.com


## 示例

```bash
# Show help
container-inspect help

# Run
container-inspect run
```

## 工作原理

该工具会读取输入数据，通过内置逻辑进行处理，然后输出处理结果。

## 提示

- 可以运行`container-inspect help`来查看所有可用的命令。
- 无需API密钥。
- 支持离线使用。

## 工作原理

该工具会读取输入数据，通过内置逻辑进行处理，然后输出结构化的结果。

## 提示

- 可以运行`container-inspect help`来查看所有可用的命令。


## 提示

- 可以运行`container-inspect help`来查看所有可用的命令。