---
name: gotchi-channeling
description: 通过 Bankr 将 Aavegotchis 通道连接到 Base 通道：检查冷却时间（cooldown），构建相关数据（calldata），并安全地提交通道交易（channel transactions）。
homepage: https://github.com/aaigotchi/gotchi-channeling
metadata:
  openclaw:
    requires:
      bins:
        - cast
        - jq
        - curl
      env:
        - BANKR_API_KEY
    primaryEnv: BANKR_API_KEY
---
# gotchi-channeling

用于处理已配置的 gotchi/parcel 对的 Channel Alchemica 工具。

## 脚本

- `./scripts/check-cooldown.sh <gotchi-id>`
  - 输出 `ready:0` 或 `waiting:<seconds>`。
  - 如果 RPC 查询失败，则返回错误信息。
- `./scripts/channel.sh <gotchi-id> <parcel-id>`
  - 验证冷却时间，通过 Bankr 提交交易，并打印交易哈希值。
- `./scripts/channel-all.sh`
  - 遍历 `config.json` 中的配置对，仅对状态为“ready”的 gotchis 执行操作。

## 配置文件

`config.json` 的关键字段：
- `realmDiamond`
- `rpcUrl`
- `chainId`
- `channeling[]`：包含以下格式的条目：`{"parcelId": "...", "gotchiId": "...", "description": "..." }`

可选环境变量：
- `GOTCHI_CHANNELING_CONFIG_FILE`：用于指定配置文件的路径。
- `BASE_MAINNET_RPC`：用于覆盖 `rpcUrl` 的值。

## Bankr API 密钥的获取方式

1. 使用 `BANKR_API_KEY`。
2. 通过 `systemctl --user show-environment` 查看环境变量。
3. 查找文件：`~/.openclaw/skills/bankr/config.json` 或 `~/.openclaw/workspace/skills/bankr/config.json`。

## 快速使用示例

```bash
./scripts/check-cooldown.sh 9638
./scripts/channel.sh 9638 867
./scripts/channel-all.sh
```

## 安全注意事项

- 冷却时间设置为 24 小时（86400 秒）。
- 如果 RPC 请求、配置设置或工具使用过程中出现错误，脚本会立即终止执行。
- 在批量处理过程中，如果任何一条记录执行失败，整个脚本会以非零状态退出。