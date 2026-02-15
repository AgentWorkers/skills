---
name: nordvpn
description: 在 Linux 系统上，可以通过 `nordvpn` 命令行工具来控制 NordVPN：连接/断开 VPN 连接、选择国家/城市/VPN 组、查看状态、调整设置以及管理允许列表。该工具非常适合需要根据地理位置进行路由设置或临时建立 VPN 隧道的自动化场景。
homepage: https://nordvpn.com/
---

# NordVPN CLI 技能（Linux）

这是一个用于控制 **NordVPN Linux CLI**（`nordvpn`）的 ClawBot 技能，可实现自动连接/断开连接、选择地理位置、验证连接状态以及调整设置等功能。

## 假设/兼容性

* 该技能兼容官方的 `nordvpn` CLI（以 **4.3.1 [snap]** 版本为例）。
* 需要 NordVPN 守护进程（通常为 `nordvpnd`）正在运行，并且用户具有足够的权限。
* 根据发行版和安装方式（如使用 Snap 或 deb 包），某些命令可能需要提升权限。

## 安装

### 选项 A：Snap（在 Ubuntu 上较为常见）

```bash
sudo snap install nordvpn
nordvpn --version
```

### 选项 B：发行版包/仓库（因发行版而异）

如果您是通过 Nord 的仓库或包管理器安装的，请执行以下操作进行验证：

```bash
which nordvpn
nordvpn --version
```

### 验证守护进程是否正在运行

```bash
# systemd installs usually
systemctl status nordvpnd --no-pager || true

# snap installs may not expose systemd unit the same way
nordvpn status || true

# or may require the full patch to be specified like so
/snap/bin/nordvpn status || true
```

## 认证/登录

NordVPN CLI 通常要求用户在每次使用设备或会话时进行登录。

```bash
nordvpn login
```

如果环境为无界面（headless）模式，CLI 会引导用户完成登录流程（通常通过浏览器链接或代码实现）。登录完成后，请确认：

```bash
nordvpn account
nordvpn status
```

**ClawBot 提示：** 除非您明确将基于浏览器的登录流程自动化，否则应将其视为手动操作。

## 快速参考

### 连接状态

```bash
nordvpn status
```

### 连接（选择最佳可用服务器）

```bash
nordvpn connect
# alias:
nordvpn c
```

### 连接到特定国家/城市/组

```bash
# country
nordvpn connect Sweden

# city (must exist in `nordvpn cities <country>`)
nordvpn connect "Stockholm"

# group (must exist in `nordvpn groups`)
nordvpn connect P2P
```

### 断开连接

```bash
nordvpn disconnect
# alias:
nordvpn d
```

### 列出所有可用地理位置

```bash
nordvpn countries
nordvpn cities Sweden
nordvpn groups
```

### 查看/修改设置

```bash
nordvpn settings

# examples (options differ by version)
nordvpn set autoconnect on
nordvpn set killswitch on
nordvpn set threatprotectionlite on  # if supported
nordvpn set protocol nordlynx        # if supported
```

### 允许列表（允许某些流量绕过 VPN）

```bash
# view help
nordvpn allowlist --help

# examples (subcommands differ by version)
nordvpn allowlist add port 22
nordvpn allowlist add subnet 192.168.0.0/16
nordvpn allowlist remove port 22
```

## 技能设计

### 该技能应具备的功能

1. **幂等性连接操作**：
   - 如果已经连接到目标位置，则不执行任何操作（或返回“已连接”信息）。
   - 如果当前连接到其他位置，可以选择先断开连接再重新连接到目标位置。
2. **可靠的连接状态验证**：
   - 在连接或断开连接后，始终执行 `nordvpn status` 命令并解析返回的结果。
3. **安全的回退机制**：
   - 如果用户请求的位置/国家/组无效，系统会列出最接近的替代选项：
     - `nordvpn countries`
     - `nordvpn cities <country>`
     - `nordvpn groups`
4. **人工干预的登录流程**：
   - 如果 `nordvpn` 报告用户未登录，系统会返回提示信息，指示用户执行 `nordvpn login` 命令进行登录。

### 推荐的“操作”（API 接口）

将这些操作实现为技能的可调用功能：

* `status()` → 返回解析后的连接状态
* `connect_best()` → 连接到最佳可用的服务器
* `connect_country(country)` → 连接到指定的国家
* `connect_city(city)` → 连接到指定的城市（可选参数 `country` 用于消除歧义）
* `connect_group(group)` → 连接到指定的组
* `disconnect()` → 断开连接
* `list_countries()` → 列出所有国家
* `list_cities(country)` → 列出指定国家的所有城市
* `list_groups()` → 列出所有组
* `get_settings()` → 获取当前设置
* `set_setting(key, value)` → 设置指定键的值
* `allowlist_add(type, value)` → 向允许列表中添加指定类型的流量
* `allowlist_remove(type, value)` → 从允许列表中删除指定类型的流量

## 建议的实现模式（CLI 调度流程）

### 1) 首先检查连接状态

```bash
nordvpn status
```

解析 CLI 常返回的字段，例如：
- 连接状态（已连接/未连接）
- 当前使用的服务器/国家/城市
- IP 地址、使用的协议和连接技术

### 2) 连接流程

**目标**：连接到指定的目标位置（国家/城市/组）并验证连接状态。

伪代码逻辑：
- 执行 `nordvpn status` 命令
- 如果未连接，则直接尝试连接
- 如果已连接到其他位置，则先执行 `nordvpn disconnect` 命令，然后再尝试连接
- 再次执行 `nordvpn status` 命令以确认连接是否成功

相关命令：
```bash
nordvpn connect "<target>"
nordvpn status
```

### 3) 断开连接流程

```bash
nordvpn disconnect
nordvpn status
```

### 4) 安全地处理用户请求

当用户请求连接特定城市时：
- 如果已知国家名称，优先使用 `nordvpn cities <country>` 命令
- 如果无法连接，则列出所有国家并提供相似位置的推荐选项

```bash
nordvpn countries
nordvpn cities "<country>"
nordvpn groups
```

## 常见错误及处理方法

### 未登录

**症状**：
- CLI 显示认证/账户/登录相关错误。

**处理方法**：
- 返回提示信息：“需要登录。请执行 `nordvpn login` 并重试。”
- 可选：执行 `nordvpn account` 命令以确认账户信息。

### 守护进程未运行或权限不足

**症状**：
- 无法连接，出现服务错误或权限错误。

**处理方法**：
- 检查 `systemctl status nordvpnd`（systemd 系统的配置方式）
- 确认 Snap 服务的运行状态（不同发行版的实现可能有所不同）
- 确保用户属于正确的用户组（某些安装版本要求用户属于 `nordvpn` 用户组）：

  ```bash
  groups
  getent group nordvpn || true
  ```

### 无效的位置/组

**症状**：
- 显示“未知的国家/城市/组”或连接失败。

**处理方法**：
- 提供可用的地理位置选项：

  ```bash
  nordvpn countries
  nordvpn groups
  nordvpn cities "<country>"
  ```

## 实用自动化示例

### 确保 VPN 已连接（任意服务器）

```bash
nordvpn status | sed -n '1,10p'
nordvpn connect
nordvpn status | sed -n '1,15p'
```

### 重新连接到特定国家

```bash
nordvpn disconnect
nordvpn connect Sweden
nordvpn status
```

### 切换 VPN 的开关状态（示例）

```bash
nordvpn set killswitch on
nordvpn settings
```

## 注意事项

* NordVPN CLI 的命令选项和设置键可能会因版本而有所不同。请始终参考官方文档。
* 如果需要稳定的、机器可读的输出格式，由于 NordVPN CLI 不总是返回 JSON 格式的数据，建议采取防御性措施来解析状态信息（例如按行提取键值对，并容忍部分字段缺失的情况）。