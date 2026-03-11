---
name: tapo
description: 通过 [Tapo MCP](https://github.com/mihai-dinculescu/tapo/tree/main/tapo-mcp) 控制 TP-Link Tapo 智能家居设备（灯光、插座、智能灯带）。
metadata:
  {
    "openclaw":
      {
        "emoji": "📦",
        "requires": { "bins": ["mcporter"] },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "mcporter",
              "bins": ["mcporter"],
              "label": "Install mcporter (node)",
            },
          ],
      },
  }
---
# Tapo

使用 `mcporter call tapo.<tool>` 来控制 Tapo 设备。

## 设置

你需要在网络中运行一个 [Tapo MCP](https://github.com/mihai-dinculescu/tapo/tree/main/tapo-mcp) 服务器（使用 HTTP 协议进行通信）。建议使用承载令牌（bearer token）进行身份验证。

1. **添加 Tapo 服务器**：
   ```bash
   mcporter config add tapo http://<TAPO_MCP_IP> \
     --transport http \
     --header "Authorization=Bearer <YOUR_TOKEN>" \
     --scope home
   ```

2. **验证**：
   ```bash
   mcporter list tapo --schema
   ```
   你应该能够看到 `list_devices`、`check_device` 和 `set_device_state` 这些命令。

有关完整的操作步骤、配置管理和故障排除，请参阅 [references/setup.md](references/setup.md)。

## 工具

### list_devices

列出网络中的所有 Tapo 设备。

```bash
mcporter call tapo.list_devices
```

该命令会返回每个设备的 `id`、`name`、`model`、`ip`、`capabilities` 以及（对于电源插排设备）`children`（子设备信息）。

### check_device

验证给定的设备 ID 是否对应于实际的设备。

```bash
mcporter call tapo.check_device id="<DEVICE_ID>" ip="<IP>"
```

### set_device_state

用于开启或关闭设备。系统会先自动执行 `check_device` 命令。

```bash
# Turn on
mcporter call tapo.set_device_state id="<DEVICE_ID>" ip="<IP>" capability='{"OnOff": true}'

# Turn off
mcporter call tapo.set_device_state id="<DEVICE_ID>" ip="<IP>" capability='{"OnOff": false}'
```

## 使用规则

1. 如果你没有最新的设备列表，请务必先运行 `list_devices` 命令。缓存结果的有效时间为 30 分钟。
2. 使用列表中提供的设备 `id` 和 `ip` 值进行操作——切勿猜测或手动复制这些值。
3. 对于电源插排设备（例如 P304M），其子设备会有自己的 `id`。请使用子设备的 `id` 以及父设备的 `ip` 值来进行操作。