---
name: mac-ai-optimizer
version: 1.0.0
description: 优化 macOS 以适应 AI 工作负载（OpenClaw、Docker、Ollama）。通过禁用后台服务、减少用户界面开销、配置 Docker 限制以及启用 SSH 远程管理，可以将一台 8GB 内存的 Mac 转变为性能接近 16GB 的高效 AI 服务器节点。
tags: ["macos", "optimization", "docker", "ai-server", "memory", "openclaw", "ollama"]
metadata: {"openclaw":{"emoji":"🖥️","requires":{"os":"darwin"}}}
---
# Mac AI 优化工具

本工具用于优化 macOS 系统，以适应 AI 工作负载（如 OpenClaw、Docker、Ollama 等）。它可以将一台配置为 8GB 内存的 Mac 转变为性能接近 16GB 的 AI 服务器节点，适用于代理任务（Agent tasks）。

## 工具列表

### optimize_memory
通过禁用 Spotlight 索引、Siri、照片分析等功能，将 macOS 的空闲内存从约 6GB 降低到约 2.5GB。

使用方法：`"Optimize this Mac's memory for AI workloads"`  

### reduce_ui
通过禁用动画效果、透明度设置以及 Dock 动画，降低 GPU 和 RAM 的使用率。

使用方法：`"Reduce UI overhead on this Mac"`  

### docker_optimize
配置 Docker Desktop 的资源限制，防止其消耗所有可用内存，确保 CPU、RAM 和交换空间（swap）的使用达到平衡状态。

使用方法：`"Optimize Docker for this Mac"`  

### enable_ssh
启用远程登录（SSH）功能，以便能够远程管理这台 Mac 作为 AI 计算节点。

使用方法：`"Enable SSH on this Mac"`  

### system_report
显示当前的内存使用情况、CPU 使用率、交换空间使用情况以及正在运行的服务数量，有助于确定需要优化的方面。

使用方法：`"Show system resource report"`  

### full_optimize
依次执行所有优化步骤：系统报告 -> 内存优化 -> 用户界面优化 -> Docker 配置 -> SSH 启用。通过一条命令即可将 Mac 转变为 AI 服务器节点。

使用方法：`"Full optimize this Mac for OpenClaw"`  

## 使用场景
- 当用户需要优化 Mac 以适应 AI 工作负载时。
- 当 Mac 的 RAM 仅剩 8GB 时，希望提升其运行 AI 应用程序的性能。
- 当希望将一台 Mac Mini 转变为 AI 服务器时。
- 当需要减少内存使用量，以改善 Docker 的运行效率时。
- 当希望将 Mac 配置为远程 AI 节点时。  

## 示例提示：
- "优化这台 Mac 以运行 OpenClaw 应用程序。"
- "我的 Mac 只有 8GB 内存，希望提升其运行 AI 应用程序的性能。"
- "将这台 Mac Mini 转变为 AI 服务器。"
- "减少内存使用量，以优化 Docker 的运行效果。"
- "将这台 Mac 配置为远程 AI 节点。"