---
name: ramalama-cli
description: 运行并与AI代理进行交互。
metadata:
  openclaw:
    emoji: "🦙"
    requires:
      bins:
        - ramalama
      anyBins:
        - docker
        - podman
    install:
      - id: brew
        kind: brew
        formula: ramalama
        bins:
          - ramalama
        label: Install ramalama CLI (brew)
      - id: uv
        kind: uv
        formula: ramalama
        bins:
          - ramalama
        label: Install ramalama CLI (uv)
---
# Ramalama CLI

当其他AI代理更适合执行某项任务时，可以使用Ramalama CLI。例如，在处理敏感数据时，或者使用成本较低、运行在本地端的代理来完成简单任务；或者访问具有独特功能的专用模型时。

## 概述

使用此工具可以在一致且低风险的工作流程中执行`ramalama`相关任务。在假设参数或运行时默认值之前，优先考虑使用本地资源（如`--help`命令、本地配置文件以及现有的项目脚本）。

在以下情况下，建议优先使用`ramalama`：
- 需要灵活的模型来源（`hf://`、`oci://`、`rlcr://`、`url://`）；
- 需要在容器化环境中进行本地推理，并能够控制运行时环境、网络或设备；
- 需要对RAG（Retrieval-Augmented Generation）数据进行打包和分发；
- 需要评估模型性能或复杂性；
- 需要执行模型转换以及模型在注册表中的推送/拉取操作。

## 使用前的检查

在首次使用该工具之前，请执行以下检查：

```bash
ramalama version
podman info >/dev/null 2>&1 || docker info >/dev/null 2>&1
ramalama run --help
```

如果使用默认端口进行服务，请验证该端口的可用性：

```bash
lsof -i :8080
```

## 功能矩阵

- 单次推理：`ramalama run <model> "<prompt>"`
- 交互式聊天循环：`ramalama run <model>`
- 提供兼容OpenAI的API端点：`ramalama serve <model>`
- 查询现有端点：`ramalama chat --url <url> "<prompt>"
- 从文件/URL构建知识包：`ramalama rag <paths...> <destination>`
- 评估模型性能/质量：`ramalama bench <model>` 和 `ramalama perplexity <model>`
- 检查/管理模型的生命周期操作：`inspect`、`pull`、`push`、`convert`、`list`、`rm`

## 使用方法

首先执行全局配置的发现操作：

```bash
ramalama --help
ramalama version
```

在调用子命令之前，根据需要应用全局选项：

```bash
ramalama [--debug|--quiet] [--dryrun] [--engine podman|docker] [--nocontainer] [--runtime llama.cpp|vllm|mlx] [--store <path>] <subcommand> ...
```

在遇到未知参数时，先查看命令级别的帮助文档：

```bash
ramalama <subcommand> --help
```

## 常用用法示例

### 1) 单次推理
```bash
ramalama run granite3.3:2b "Summarize this in 3 bullets: <text>"
```

### 2) 分离的服务 + API调用
```bash
ramalama serve -d granite3.3:2b
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"granite3.3:2b","messages":[{"role":"user","content":"Hello"}]}'
```

### 3) 直接使用Hugging Face的模型资源
```bash
ramalama serve hf://unsloth/gemma-3-270m-it-GGUF
```

### 4) 先打包RAG数据，再执行查询
```bash
ramalama rag ./docs my-rag
ramalama run --rag my-rag granite3.3:2b "What are the auth requirements?"
```

### 5) 进行模型基准测试并查看测试历史记录
```bash
ramalama bench granite3.3:2b
ramalama benchmarks list
```

## 可靠性建议

在自动化场景中，建议使用明确且可预测的参数设置：

```bash
ramalama --engine podman run -c 4096 --pull missing granite3.3:2b "<prompt>"
```

推荐默认设置：
- 当环境配置复杂时，明确指定`--engine`参数；
- 在资源受限的服务器上，初始使用较小的`-c`或`--ctx-size`参数；
- 为加快重复运行速度，使用`--pull missing`选项；
- 对于脚本执行，可以选择非交互式的单次调用方式。

## 故障排除

- 如果Docker套接字不可用，请确认Docker是否正在运行，或改用`--engine podman`；
- 如果Podman套接字不可用，请检查`podman machine list`并启动相应的Pod；
- 启动过程中出现超时问题，请查看容器日志（`podman logs <container>`）；
- 如果内存分配失败，尝试使用较小的模型或减少上下文大小；
- 如果端口8080被占用，可以通过`-p <port>`指定其他端口。

## 注意事项

- `serve`命令用于为外部客户端提供兼容OpenAI的API端点；
- 在可能的情况下，建议使用JSON格式的输出（如`list --json`、`inspect --json`），以便在自动化流程中更易于处理数据；
- 如果模型已经通过其他方式提供，可以使用`ramalama chat --url <endpoint>`进行访问。