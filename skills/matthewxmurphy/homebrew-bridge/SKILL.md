---
name: homebrew-bridge
version: "0.6.1"
description: 通过在 Linux OpenClaw 网关上安装特定配置的 SSH 封装层（这些封装层支持同一局域网内的通信），可以暴露 Mac 上的 Homebrew 工具（如 `brew`、`gh` 以及其他位于 `/opt/homebrew/bin` 目录下的 CLI 工具）。这些封装层还提供了可选的“Wake-on-LAN”功能以及自动发现 OpenClaw 配置的功能。
metadata: {"openclaw":{"emoji":"🍺"}}
---
# Homebrew Bridge

当真正需要的是通过 Linux OpenClaw 网关来访问 Mac 机器上的 Homebrew 工具链时，可以使用此技能。

该技能适用于 `/opt/homebrew/bin/<tool>` 目录下的工具封装程序，例如：

- `brew`
- `gh`
- 其他通过 Homebrew 安装的 CLI 工具（这些工具需要从 Mac 机器上进行访问）

## 适用场景

- 需要通过 Mac 机器运行由 Homebrew 支持的工具的 Linux 网关
- 需要依赖 `brew`、`gh` 或其他 Homebrew CLI 的工具封装程序
- 同一局域网内的 Mac 机器（这些机器上已经安装了真正的 Homebrew 工具）
- 当仅知道一个 Mac 机器的所有者时，可以通过 OpenClaw 配置实现自动主机发现

## 不适用场景

- 本质上是 Mac 系统自带的工具或需要特定权限的 CLI（如 `imsg`、`remindctl`）
- 需要在 Linux 系统上直接安装的 Linux 原生工具
- 需要通过广域网进行远程连接的 Mac 机器

## 前提条件

- Linux 网关和拥有该 Homebrew 工具的 Mac 机器位于同一个受信任的局域网或 VLAN 中
- Linux 网关能够通过 SSH 连接到拥有该工具的 Mac 机器
- 要使用的工具存在于该 Mac 机器的 `/opt/homebrew/bin/<tool>` 目录下
- 该 Mac 机器在工作期间保持开机状态，或者支持通过局域网唤醒功能（Wake-on-LAN）

## 工作流程

### 1. 生成工具所有权映射

运行以下命令：

```bash
scripts/render-tool-map.sh /home/node/.openclaw/openclaw.json
```

该命令会输出由系统推断出的或作为备用的 Homebrew 工具所有者信息。

### 2. 安装 Homebrew 工具封装程序

示例：

```bash
scripts/install-homebrew-pack.sh \
  --target-dir /home/node/.openclaw/bin \
  --tool brew \
  --tool gh \
  --tool claude \
  --default-host mac-ops@mac-node.local \
  --wake-map mac-node.local=AA:BB:CC:DD:EE:FF \
  --wake-wait 20 \
  --wake-retries 2
```

主机解析顺序如下：
- 显式指定 `--map tool=user@host`
- 使用默认值 `--default-host user@host`
- 如果 OpenClaw 配置中只检测到一个远程主机，则使用该主机地址 `remoteHost`
- 如果 OpenClaw 配置已经确定了所有者信息，则不再重复询问主机地址

### 3. 验证工具封装程序的安装情况

运行以下命令：

```bash
scripts/verify-homebrew-pack.sh --target-dir /home/node/.openclaw/bin
```

## 设计规范

- Linux 系统负责管理工具封装程序的路径
- Mac 机器负责保存实际的 `/opt/homebrew/bin` 中的二进制文件
- 公共使用的技能依赖于工具封装程序的路径，而非 Mac 机器上的实际二进制文件路径
- 每个工具的封装程序名称必须保持明确

## 相关文件

- `scripts/install-wrapper.sh`：为远程二进制文件创建一个 SSH 封装程序
- `scripts/install-homebrew-pack.sh`：批量安装 Homebrew 支持的工具封装程序
- `scripts/verify-homebrew-pack.sh`：验证已安装的工具封装程序
- `scripts/render-tool-map.sh`：输出工具与主机之间的映射关系
- `references/skill-readiness.md`：关于 Homebrew 支持的工具封装程序的发布规范