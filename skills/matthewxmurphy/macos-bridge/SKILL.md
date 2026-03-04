---
name: macos-bridge
description: 通过安装专门为同一局域网（LAN）设计的SSH封装程序，可以将Mac上使用的工具（如imsgr, remindctl, memo, things, peekaboo等）连接到Linux OpenClaw网关。这些封装程序支持可选的“Wake-on-LAN”（网络唤醒）功能，并具备自动发现OpenClaw配置的能力。
---
# macOS Bridge

当需要将 Linux 上的 OpenClaw 网关暴露为稳定的 Linux 命令时，可以使用此技能。

此技能适用于那些本质上依赖于 macOS 的工具：

- `imsg`
- `remindctl`
- `memo`
- `things`
- `peekaboo`

该技能不会试图让 Linux 模拟这些二进制文件的运行方式，而是会安装专门的 Linux 封装程序，这些程序通过 SSH 调用对应的 macOS 工具。

## 适用场景

- 同局域网内的 Linux 网关与 Mac 节点之间的通信
- 需要 macOS 权限或数据访问的 macOS 工具
- 需要在 Linux 上保持真实性的工具（即不能伪装成 Linux 本地的工具）
- 从现有的 OpenClaw 配置中自动发现远程主机（`remoteHost`）
- 当 Mac 处于睡眠状态时，支持通过 Wake-on-LAN 功能唤醒 Mac

## 不适用场景

- 以 Homebrew 为中心的 Linux 扩展方案（主要目标是暴露 `/opt/homebrew/bin` 中的工具）
- 需要本地安装的 Linux 本机工具
- 修补 OpenClaw 内部代码，以便仅在 Linux 上显示为绿色的 macOS 工具
- 需要通过广域网（WAN）连接的远程 Mac 或不可信任的远程 Mac

## 使用要求

- Linux 网关和 Mac 节点必须位于同一个受信任的局域网或 VLAN 中
- Linux 网关能够通过 SSH 连接到对应的 Mac 节点
- 远程二进制文件必须已经存在，并且具有所需的 macOS 权限
- 如果需要远程恢复功能，Mac 需要保持唤醒状态（支持 Wake-on-LAN）

## 工作流程

### 1. 生成工具所有权映射

运行：

```bash
scripts/render-tool-map.sh /home/node/.openclaw/openclaw.json
```

如果 OpenClaw 配置中已经包含了相应的 `remoteHost` 信息，系统会首先自动生成工具所有权映射。

### 2. 安装 macOS 包

示例：

```bash
scripts/install-macos-pack.sh \
  --target-dir /home/node/.openclaw/bin \
  --tool imsg \
  --tool remindctl \
  --tool memo \
  --openclaw-config /home/node/.openclaw/openclaw.json \
  --wake-map mac-node.local=AA:BB:CC:DD:EE:FF \
  --wake-wait 20 \
  --wake-retries 2
```

安装程序会按以下顺序解析主机信息：
- 显式指定的 `--map tool=user@host`
- OpenClaw 配置中匹配的 `remoteHost`
- `--default-host user@host`
- 如果只存在一个唯一的 `remoteHost`，则使用该主机
- 如果 OpenClaw 配置已经确定了工具的所有者，则不再询问主机信息

### 3. 验证安装结果

运行：

```bash
scripts/verify-macos-pack.sh --target-dir /home/node/.openclaw/bin
```

## 设计原则

- Linux 系统负责管理封装程序的路径
- macOS 系统负责管理实际的二进制文件及相应的操作系统权限
- 公开的工具接口应基于封装程序的路径，而不是远程二进制文件的路径
- 工具的所有权信息必须明确且可审计

## 相关文件

- `scripts/install-wrapper.sh`：为远程二进制文件创建一个 SSH 封装程序
- `scripts/install-macos-pack.sh`：批量安装 macOS 工具的封装程序，并支持自动发现及可选的 Wake-on-LAN 功能
- `scripts/verify-macos-pack.sh`：验证已安装的封装程序包
- `scripts/render-tool-map.sh`：打印自动生成的工具所有权映射或备用映射
- `references/skill-readiness.md`：封装程序相关功能的发布规则