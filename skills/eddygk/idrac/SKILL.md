---
name: idrac
description: >
  通过 iDRAC Redfish API（iDRAC 8/9）监控和管理 Dell PowerEdge 服务器。
  适用场景：
  - 检查服务器的硬件状态、健康状况或温度
  - 查询 CPU、内存、存储/RAID 的详细信息
  - 监控系统传感器（风扇、电压、温度）
  - 执行电源操作（状态切换、开机/关机、优雅重启、强制重启）
  - 查看 BIOS/固件版本或系统库存信息
  - 查看系统事件日志（SEL）或生命周期控制器日志
  - 获取硬件库存信息或序列号
  所需工具：curl、jq。可选工具：1Password CLI（用于身份验证）。
  配置文件：
  - ~/.config/idrac-skill/config（用户自定义配置文件）
  - ~/.idrac-credentials（缓存的身份验证凭据，权限设置为 600）
  网络连接：
  - 仅连接到用户配置的 iDRAC IP 地址
  - 使用 HTTPS 协议进行连接；对于自签名证书，TLS 验证功能被禁用。
  辅助脚本：
  - scripts/idrac.sh（与本技能相关的辅助脚本）
  注意：
  - 该技能依赖于 curl 和 jq 工具来执行网络请求和数据处理操作。
  - 如果使用 1Password CLI，需要将其配置文件（~/.idrac-credentials）添加到系统的环境变量中。
metadata: { "openclaw": { "emoji": "🖥️", "requires": { "bins": ["curl", "jq"] }, "os": ["darwin", "linux"] } }
---
# iDRAC 技能

通过 iDRAC Redfish API 监控和管理 Dell PowerEdge 服务器。

## 首次设置

在 `~/.config/idrac-skill/config` 文件中创建一个配置文件：

```bash
mkdir -p ~/.config/idrac-skill
cat > ~/.config/idrac-skill/config <<'EOF'
# iDRAC connection settings
IDRAC_IP="<your-idrac-ip>"

# Credential source: "1password" | "file" | "env"
CREDS_SOURCE="file"

# For CREDS_SOURCE="1password":
#   OP_ITEM="<1password-item-name>"
#
# For CREDS_SOURCE="file":
#   Create ~/.idrac-credentials with contents: username:password
#   chmod 600 ~/.idrac-credentials
#
# For CREDS_SOURCE="env":
#   Export IDRAC_USER and IDRAC_PASS
EOF
```

## 认证

该辅助脚本支持三种凭证来源：

| 来源 | 配置 | 工作原理 |
|--------|--------|--------------|
| **1. 密码** | `OP_ITEM="item-name"` | 通过 `op` CLI 获取用户名和密码，并将其缓存到 `~/.idrac-credentials` 文件中 |
| **文件** | （默认） | 读取 `~/.idrac-credentials` 文件（格式：`user:pass`，权限设置为 600） |
| **环境变量** | — | 使用 `$IDRAC_USER` 和 `$IDRAC_PASS` 环境变量 |

## 辅助脚本

位置：`scripts/idrac.sh`（相对于此技能目录）

```bash
idrac.sh test            # Test connectivity and authentication
idrac.sh status          # System summary (model, power, CPU, memory)
idrac.sh health          # Health checks (temps, fans, power)
idrac.sh power           # Current power state
idrac.sh inventory       # Full hardware inventory
idrac.sh logs            # Recent system event log entries (last 10)
idrac.sh thermal         # Detailed temperature and fan status
idrac.sh storage         # RAID/disk status
idrac.sh reset-types     # Available power reset types
```

## 工作流程

1. 从 `~/.config/idrac-skill/config` 文件中加载配置。
2. （如果需要）动态加载凭证。
3. 确定操作类型：
   - **只读操作**（状态、健康状况、日志、库存信息）→ 直接执行。
   - **破坏性操作**（关机、重启、BIOS 更改）→ 先获取用户确认。
4. 通过 curl 和基本认证（或会话令牌）查询 Redfish API。
5. 使用 jq 解析 JSON 数据。
6. 以自然语言的形式向用户展示查询结果。
7. **切勿在响应中泄露凭证信息**。

## 终端点参考

有关原始 Redfish API 终端点的详细信息（系统信息、温度、存储、网络、日志、电源操作、BIOS、固件、会话认证、Dell OEM 属性）：

→ 请参阅 [references/endpoints.md](references/endpoints.md)

## 安全注意事项

- **切勿记录或显示凭证信息** — 使用 `--silent` 选项并将输出传递给 jq 工具进行处理。
- **凭证文件的权限必须设置为 600 (`chmod 600 ~/.idrac-credentials`)**。
- **禁用 TLS 验证**（使用 `-k` 选项）—— iDRAC 使用自签名证书（适用于私有网络）。
- **电源操作具有破坏性**—— 在执行关机/重启操作前必须获取用户确认。

## 兼容性

该脚本兼容 Dell iDRAC 8（Redfish 1.0–1.4）和 iDRAC 9（Redfish 1.6+）。支持从第 13 代（R630/R730）到当前版本的 PowerEdge 服务器。具体版本信息请参阅终端点参考文档。

**注意：** iDRAC 8 的 API 响应可能需要 5–10 秒才能完成一次调用。`test` 命令会连续执行 4 次调用（总共约 30–40 秒），请相应地设置执行超时时间。iDRAC 9 的响应速度明显更快。