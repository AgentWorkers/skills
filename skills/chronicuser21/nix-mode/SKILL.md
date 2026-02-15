---
name: nix-mode
description: 在 Nix 模式下处理 Clawdbot 的操作（配置管理、环境检测）。
metadata: {"clawdbot":{"emoji":"❄️","requires":{"bins":["nix","bash"],"envs":["CLAWDBOT_NIX_MODE"]},"install":[]}}
---

# Clawdbot 的 Nix 模式技能

本技能专门用于处理 Clawdbot 在 Nix 模式下的运行相关操作。

## Nix 模式特有的功能

### 环境检测
- 检测 `CLAWDBOT_NIX_MODE` 是否设置为 1
- 识别由 Nix 管理的配置文件路径
- 识别 Nix 特有的错误信息和行为

### 配置管理
- 了解在 Nix 模式下自动安装流程是被禁用的
- 指导用户正确使用 Nix 包管理工具
- 解释某些自我修改功能在 Nix 模式下不可用的原因

### 路径处理
- 识别 Nix 的存储路径
- 理解配置文件目录（config）与状态文件目录（state）之间的区别
- 正确处理 `CLAWDBOT_CONFIG_PATH` 和 `CLAWDBOT_STATE_DIR`

### 故障排除
- 识别与 Nix 相关的故障提示信息
- 指导用户通过 Nix 正确管理依赖关系
- 解释 Nix 模式下“只读”状态的显示机制

## 使用指南

在 Nix 模式下运行时：
1. 不要尝试自动安装依赖项
2. 引导用户使用 Nix 的包管理工具进行依赖项的安装
3. 尊重 Nix 安装的不可变性
4. 提供适用于 Nix 环境的正确配置建议