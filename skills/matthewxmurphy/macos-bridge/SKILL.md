---
name: macos-bridge
version: 0.6.2
description: 通过安装专门的、支持同一局域网（LAN）的SSH封装工具，可以将Mac上使用的工具（如imsgr, remindctl, memo, things, peekaboo等）连接到Linux上的OpenClaw网关。这些封装工具支持可选的“Wake-on-LAN”（通过网络信号唤醒设备）功能、自动发现可用通道的功能，以及在OpenClaw配置失败时的备用方案。
metadata: {"openclaw":{"emoji":"🍎"}}
---
# macOS 桥接（macOS Bridge）

当需要将 Linux 上的 OpenClaw 网关暴露为稳定的 Linux 命令时，可以使用此技能。

此技能适用于那些本质上依赖于 macOS 的工具：

- `imsg`
- `remindctl`
- `memo`
- `things`
- `peekaboo`

该技能不会试图让 Linux 模拟这些二进制文件为本地文件；而是会安装专门的 Linux 容器（wrapper），这些容器通过 SSH 调用 macOS 上的相应程序。

如果 `openclaw.json` 中禁用了相关功能，请勿强制使用此桥接功能。

如果该功能已启用且 Linux 上已经存在可用的本地二进制文件，也是可以接受的。在这种情况下，只有当需要使用 macOS 上的实现时，才应使用此技能。

## 适用场景

- 同局域网的 Linux 网关与 Mac 节点之间的通信
- 需要 macOS 权限或数据访问的 macOS 工具
- 需要在 Linux 上保持真实性的容器化工具
- 从 `channels.*.enabled` 文件中自动选择启用的通道
- 从现有的 OpenClaw 配置中自动发现远程主机（`remoteHost`）
- 当 Mac 进入睡眠状态时，可选的唤醒功能（Wake-on-LAN）

## 不适用场景

- 以 Homebrew 为中心的 Linux 扩展方案（主要目标是暴露 `/opt/homebrew/bin` 中的工具）
- 需要本地安装的 Linux 原生工具
- 修补 OpenClaw 内部机制，以便仅在 Linux 上显示仅适用于 macOS 的工具
- 通过广域网（WAN）连接的或不受信任的远程 Mac

## 其他要求

- Linux 网关和 Mac 节点必须位于同一个受信任的局域网或 VLAN 中
- Linux 网关能够通过 SSH 连接到对应的 Mac 节点
- 远程二进制文件必须存在，并且具有所需的 macOS 权限
- 如果需要远程恢复功能（Wake-on-LAN），则 Mac 必须保持唤醒状态

## 工作流程

### 1. 生成工具所有权映射（Generate Tool Ownership Map）

运行以下命令：

```bash
scripts/render-tool-map.sh /home/node/.openclaw/openclaw.json
```

如果 OpenClaw 配置中已经启用了依赖于 macOS 的功能，此命令会首先生成一个自动检测到的工具所有权映射。

### 2. 安装 macOS 容器包（Install macOS Pack）

示例：

```bash
scripts/install-macos-pack.sh \
  --target-dir /home/node/.openclaw/bin \
  --openclaw-config /home/node/.openclaw/openclaw.json \
  --default-host agent2@192.168.88.12 \
  --wake-map mac-node.local=AA:BB:CC:DD:EE:FF \
  --wake-wait 20 \
  --wake-retries 2
```

当未提供 `--tool` 或 `--map` 参数时，安装程序会自动选择 OpenClaw 配置中已启用的工具进行安装。

安装程序按以下顺序解析主机：
- 明确指定的 `--map tool=user@host`
- OpenClaw 配置中匹配的 `remoteHost`
- 默认值 `--default-host user@host`
- 如果只存在一个唯一的 `remoteHost`，则自动选择该主机
- 如果 OpenClaw 配置已经确定了工具的所有者，则不再询问主机信息

### 3. 验证容器包（Verify the Pack）

运行以下命令：

```bash
scripts/verify-macos-pack.sh \
  --target-dir /home/node/.openclaw/bin \
  --openclaw-config /home/node/.openclaw/openclaw.json
```

当提供了 `--openclaw-config` 参数时，验证过程仅检查已启用的依赖于 macOS 的功能，而不会将所有支持的工具都视为必需安装的。

## 设计原则

- Linux 负责管理容器的路径
- macOS 负责管理实际的二进制文件及操作系统权限
- 公开的工具功能依赖于容器的路径，而非远程二进制文件的路径
- 工具的所有权信息必须保持透明且可审计

## 相关文件

- `scripts/install-wrapper.sh`：为远程二进制文件创建一个 SSH 容器
- `scripts/install-macos-pack.sh`：批量安装依赖于 macOS 的工具容器，并支持自动发现及可选的唤醒功能
- `scripts/verify-macos-pack.sh`：验证安装的容器包
- `scripts/render-tool-map.sh`：打印自动检测到的或备用的工具所有权映射
- `references/skill-readiness.md`：关于容器化工具的发布规则