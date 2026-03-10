---
name: linux-to-mac-bridge
version: "1.2.1"
description: 适用于 Linux 到 Mac 的封装安装的旧版组合桥接技能。对于使用 macOS CLI 的系统，建议使用较新的 `macos-bridge` 技能；对于使用 Homebrew 的工具，则建议使用 `homebrew-bridge` 技能。
metadata: {"openclaw":{"emoji":"🌉"}}
---
# Linux到Mac的桥接方案

这是一个用于将Mac上的工具集成到Linux环境中的解决方案。

推荐使用以下工具：

- `macos-bridge`：用于`imsg`、`remindctl`、`memo`、`things`、`peekaboo`等工具。
- `homebrew-bridge`：用于`brew`、`gh`以及其他位于`/opt/homebrew/bin`下的工具。

当需要将Mac上的工具作为稳定的Linux命令在Linux环境中使用时，可以使用此方案。

这是针对“如何在Linux环境中使用Mac工具”问题的官方解决方案：

- **不要修改已打包的工具**。
- **不要假装Linux可以运行Mac的二进制文件**。
- **在Linux环境中安装相应的封装程序（wrapper）**。
- **让公共技能依赖于这些封装程序的路径**。
- **确保Linux网关和Mac节点位于同一个可信的局域网内**。

## 适用场景

- `imsg`、`remindctl`、`memo`、`things`、`peekaboo`等工具。
- 需要在Linux环境中使用的Homebrew工具（这些工具位于连接的Mac节点上）。
- 需要在Linux环境中正常运行的封装程序支持的工具。
- 需要实现工具所有权映射和功能报告的场景。
- 在同一局域网内的Linux网关和Mac节点之间的通信。

## 不适用场景

- **需要本地安装的Linux原生工具**。
- **通过互联网路由的Mac主机或不受信任的广域网连接**。
- **任意远程shell访问**。
- **修改OpenClaw的内部代码以支持Mac工具**。

## 系统要求

- Linux网关和Mac节点必须位于同一个可信的局域网或VLAN内。
- Linux网关能够通过SSH连接到对应的Mac节点。
- 远程二进制文件必须具有在Mac上运行的权限。
- 你需要知道每个工具对应的Mac节点。
- Mac节点需要保持开机状态，或者至少需要启用Wake-on-LAN功能（以便远程唤醒）。

## 局域网环境要求

- 该方案适用于家庭实验室或办公室内部的局域网环境：
  - Linux网关和Mac节点位于同一个局域网内。
  - Mac节点使用稳定的RFC1918地址或其他本地地址。
  - 网关和节点之间的SSH连接延迟较低。
- 不需要通过公共互联网来访问Mac节点。

**默认假设**：

- 如果Linux网关无法通过局域网访问Mac节点，那么使用封装程序的方案可能无法正常工作。

**关于Wake-on-LAN的功能**：

- 封装程序的安装脚本可以包含Wake-on-LAN相关的元数据和重试逻辑。
- 如果Mac节点可能处于睡眠状态，可以配置一个唤醒映射表，以便Linux端的封装程序能够发送唤醒信号并自动重试SSH连接。

## 设计原则

- **功能分工**：
  - Linux网关负责管理封装程序。
  - Mac节点负责运行真正的二进制文件并提供操作系统级别的权限。
- **公共技能的访问路径**：依赖于封装程序的路径，而非远程文件的路径。
- **工具的所有权信息**：需要保持透明且可审计。
- **优化目标**：主要针对同一局域网内的节点之间的通信，而非跨公共网络的访问。

## 工作流程

### 1. 生成工具所有权映射

运行以下命令：

```bash
scripts/render-tool-map.sh
```

如果`~/.openclaw/openclaw.json`文件中已经包含了Mac节点的地址信息，系统会自动根据该配置生成一个所有权映射表。在这种情况下，除非发现的信息有误，否则无需再次询问IP地址或SSH用户名。

否则，系统会生成一个可重复使用的初始映射表，例如：
- `imsg -> mac-ops@mac-messages.local`
- `remindctl -> mac-ops@mac-messages.local`
- `gh -> mac-ops@mac-tools.local`

### 2. 安装Mac工具的封装程序

运行以下命令：

```bash
scripts/install-macos-pack.sh \
  --target-dir /home/node/.openclaw/bin \
  --tool imsg \
  --tool remindctl \
  --tool memo \
  --tool gh \
  --openclaw-config /home/node/.openclaw/openclaw.json \
  --wake-map mac-messages.local=AA:BB:CC:DD:EE:FF \
  --wake-map mac-tools.local=11:22:33:44:55:66 \
  --wake-wait 20 \
  --wake-retries 2
```

安装程序会根据提供的配置信息：
- 显式指定工具的所有者（`user@host`）。
- 或者尝试从`openclaw.json`中的`remoteHost`值推断工具的所有者。
- 如果只知道一个`remoteHost`地址，系统会使用该地址作为所有者的默认值。
- 如果可以从`openclaw.json`中确定所有者，系统会避免再次询问用户输入。

这样会在Linux系统中创建相应的封装程序路径，例如：
- `/home/node/.openclaw/bin/imsg`
- `/home/node/.openclaw/bin/remindctl`
- `/home/node/.openclaw/bin/memo`
- `/home/node/.openclaw/bin/gh`

如果配置了Wake-on-LAN功能，生成的封装程序会：
- 首先尝试通过SSH连接。
- 如果连接失败，会发送唤醒信号。
- 等待指定的时间后，再次尝试连接。

### 3. 验证封装程序的安装

运行以下命令：

```bash
scripts/verify-macos-pack.sh --target-dir /home/node/.openclaw/bin
```

该命令会验证封装程序是否已正确安装，并确保可以从Linux网关访问它们。

同时，还会检查每个封装程序是否支持Wake-on-LAN功能。

### 4. 发布公共技能

在发布公共技能时，需要提供Linux环境下的封装程序路径，而非Mac上的二进制文件路径。同时，需要明确指定哪个Mac节点负责运行该工具，并将封装程序作为稳定的API接口。

更多详细信息，请参阅[references/skill-readiness.md](references/skill-readiness.md)。

## 安全规则

- 每个工具只能使用一个封装程序。
- 每个工具必须有一个明确的Mac节点作为所有者。
- 不允许使用通用的远程shell访问机制。
- 不要在技能相关文件中存储任何敏感信息。
- 不允许对核心代码进行修改以强制显示“可用”状态。

## 相关文件

- `scripts/install-wrapper.sh`：为每个远程二进制文件创建一个SSH封装程序。
- `scripts/install-macos-pack.sh`：批量安装常见的Mac工具封装程序，支持从`openclaw.json`配置文件自动检测工具信息及启用Wake-on-LAN功能。
- `scripts/verify-macos-pack.sh`：验证Linux网关上的封装程序，并显示Wake-on-LAN功能的启用状态。
- `scripts/render-tool-map.sh`：打印生成的工具所有权映射表及Wake-on-LAN配置示例。
- `references/skill-readiness.md`：介绍如何在无需修改核心代码的情况下确保公共技能在Linux环境中正常运行。