---
name: sparkle-vpn
description: **控制 Sparkle VPN**：直接使用 Mihomo Core 启动和停止 VPN 连接。
---
# Sparkle VPN 控制

本技能提供了直接通过 Mihomo 核心来控制 Sparkle VPN 的工具（无需图形用户界面交互）。

## 工具

- `sparkle_vpn_start`：使用 Mihomo 核心和 DirectACCESS 配置文件启动 VPN
- `sparkle_vpn_stop`：停止 VPN 并终止所有相关进程

## 实现方式

直接使用 Mihomo 核心进行操作：
- 配置文件路径：`~/.config/sparkle/profiles/19c48c94cbb.yaml`
- 代理端口：`7890`（HTTP/HTTPS）
- 配置目录：`~/.config/sparkle/`

## 使用方法

启动 VPN：
```bash
bash /home/admin/.openclaw/workspace/skills/sparkle-vpn/scripts/start-vpn.sh
```

停止 VPN：
```bash
bash /home/admin/.openclaw/workspace/skills/sparkle-vpn/scripts/stop-vpn.sh
```