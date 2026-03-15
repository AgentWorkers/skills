---
name: Boilerplates
description: "这是我的个人模板集合。在这里，你可以找到各种模板以及用于 Python、Ansible、Docker、Docker-Compose、Kubernetes 和 Packer 的配置文件。当你需要使用这些模板功能时，可以随时使用它们。触发条件：boilerplates。"
---
# 模板集（Boilerplates）

这是我的个人模板集合，其中包含了各种工具和技术的模板及配置文件。

## 命令（Commands）
- `help` - 显示帮助信息
- `run` - 运行指定命令
- `info` - 显示命令的详细信息
- `status` - 显示命令的运行状态

## 功能（Features）
- 该模板集的核心功能来源于 ChristianLempa/boilerplates

## 使用方法（Usage）
要运行任意命令，请使用以下格式：
```
boilerplates <command> [args]
```

---

💬 意见反馈与功能请求：https://bytesagain.com/feedback
本项目由 BytesAgain 提供支持 | bytesagain.com

## 示例（Examples）
```bash
# Show help
boilerplates help

# Run
boilerplates run
```

- 运行 `boilerplates help` 可以查看所有可用的命令。

## 输出结果（Output）
命令的输出结果会直接显示在标准输出（stdout）中。若需保存输出结果，可以使用以下命令：
```
boilerplates run > output.txt
```