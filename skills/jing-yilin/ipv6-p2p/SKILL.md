---
name: ipv6-p2p
description: 使用 Yggdrasil 或 ULA IPv6 地址，在 OpenClaw 代理之间发送/接收直接加密的 P2P 消息。
version: 0.1.0
metadata:
  openclaw:
    emoji: "🔗"
    homepage: https://github.com/ReScienceLab/claw-p2p
    install:
      - kind: node
        package: "@resciencelab/claw-p2p"
---
# IPv6 P2P 功能

支持通过 IPv6 进行直接的代理到代理的消息传递。无需服务器参与，消息会使用 Ed25519 算法进行签名，并以点对点的方式传输。

## 使用场景

| 情况 | 需要调用的工具 |
|---|---|
| 用户提供了对方的 IPv6 地址 | `p2p_add_peer(ygg_addr, alias?)` |
| 用户想要向某个对等方发送消息 | `p2p_send_message(ygg_addr, message)` |
| 用户想查询可联系的对等方/已知联系人 | `p2p_list_peers()` |
| 用户想获取自己的代理地址 | `p2p_status()` |

## 规则

- 在发送任何消息之前，**必须先调用 `p2p_add_peer`**，以便缓存对方的公钥（遵循 TOFU 安全策略）。
- 如果用户提供了名称/别名，请将其传递给 `p2p_add_peer`。
- 如果 `p2p_send_message` 失败，请先调用 `yggdrasil_check()` 来检查网络连接情况，然后再向用户反馈错误信息。
- 如果用户之前从未使用过 P2P 功能，请先调用 `yggdrasil_check()` 确认其地址是否可被路由。
- 绝不要自行生成 IPv6 地址——必须让用户明确提供地址。
- 合法的地址格式：`fd77:xxxx::x`（ULA/test）或 `200:xxxx::x`（Yggdrasil 主网）。

有关示例交互模式，请参阅 `references/flows.md`。