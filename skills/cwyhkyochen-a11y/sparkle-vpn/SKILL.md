---
name: sparkle-vpn
description: >
  **使用 Mihomo Core 直接控制 Sparkle VPN：**  
  - 启动/停止 Sparkle VPN  
  - 管理系统代理设置  
  - 查询 VPN 状态  
  - 切换使用不同的 VPN 节点  
  （注：根据文档内容，这些操作都是通过 Mihomo Core 的核心功能直接完成的。）
---
# Sparkle VPN 控制

本技能提供了直接使用 Mihomo 核心来控制 Sparkle VPN 的工具（无需图形界面交互）。

## 工具

### VPN 控制
- `sparkle_vpn_start` - 仅启动 VPN 核心（使用端口 7890，不启用系统代理）
- `sparkle_vpn_start_with_proxy` - 启动 VPN 并启用系统代理
- `sparkle_vpn_stop` - 停止 VPN 并禁用系统代理

### 系统代理管理
- `sparkle_vpn_enable_proxy` - 启用系统代理设置（VPN 必须正在运行）
- `sparkle_vpn_disable_proxy` - 禁用系统代理设置

### 节点管理
- `sparkle_vpn_status` - 查询当前 VPN 状态、活动节点及可用节点列表
- `sparkle_vpn_switch` - 切换到不同的 VPN 节点

## 实现方式

直接使用 Mihomo 核心：
- 配置文件：`~/.config/sparkle/profiles/19c48c94cbb.yaml`
- 代理端口：`7890`（HTTP/HTTPS）
- 配置目录：`~/.config/sparkle/`
- API 端口：`9090`

## 使用示例

- **启用系统代理并启动 VPN：**
  ```bash
sparkle_vpn_start_with_proxy
```

- **不启用系统代理（手动模式）并启动 VPN：**
  ```bash
sparkle_vpn_start
```

- **在 VPN 运行后启用系统代理：**
  ```bash
sparkle_vpn_enable_proxy
```

- **停止 VPN：**
  ```bash
sparkle_vpn_stop
```

- **查询状态：**
  ```bash
sparkle_vpn_status
```

- **切换节点：**
  ```bash
sparkle_vpn_switch "香港-HKG-01-VL"
```

## 常用节点
- **自动选择** - 自动选择最佳节点
- **故障转移** - 备用模式
- **香港-HKG-01-VL** - 香港节点
- **香港-HKG-02-VL** - 香港节点 2
- **香港-HKT-01-VL** - 香港 HKT 节点
- **新加坡-SIN-01-VL** - 新加坡节点
- **日本-TYO-01-VL** - 日本东京节点
- **美国-SJC-01-VL** - 美国圣何塞节点

## 系统代理支持

系统代理设置通过以下方式应用：
- GNOME gsettings（适用于 GNOME/GTK 桌面环境）
- 环境变量保存在 `~/.config/sparkle/proxy.env` 文件中

**在当前终端会话中启用代理：**
```bash
source ~/.config/sparkle/proxy.env
```