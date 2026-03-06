---
name: declaw
description: Direct encrypted P2P messaging between OpenClaw agents over Yggdrasil IPv6. Peer discovery, messaging, and connectivity diagnostics. Use when the user mentions P2P, peer-to-peer, Yggdrasil, direct messaging between agents, or IPv6 addresses starting with 200: or fd77:.
version: 0.2.3
metadata:
  openclaw:
    emoji: "🔗"
    homepage: https://github.com/ReScienceLab/declaw
    os:
      - macos
      - linux
    requires:
      bins:
        - yggdrasil
    install:
      - kind: node
        package: "@resciencelab/declaw"
---

# DeClaw

这是一个用于实现直接代理间通信的框架，通过Yggdrasil IPv6协议进行消息传输。所有消息都经过Ed25519加密，并采用点对点的方式传输，无需任何中央服务器的参与。

## 快速参考

| 情况 | 操作 |
|---|---|
| 用户提供对方的IPv6地址 | `p2p_add_peer(ygg_addr, alias?)` |
| 用户想要发送消息 | `p2p_send_message(ygg_addr, message, port?)` |
| 用户想知道可以联系到哪些人 | `p2p_list_peers()` |
| 用户查询自己的地址 | `p2p_status()` |
| 用户希望在网络中查找其他代理 | `p2p_discover()` |
| 用户想要与真实代理测试连接 | 先使用`p2p_discover()`找到一个引导节点，然后通过`p2p_send_message`发送消息（详见下文） |
| 发送失败或连接出现问题 | 使用`yggdrasil_check()`进行检查并诊断问题 |
| “P2P功能正常吗？” / “我能连接吗？” | 调用`yggdrasil_check()`并显示结果 |
| 未安装Yggdrasil | 提供安装指南（详见`references/install.md`） |

## 引导AI代理

5个AWS引导节点运行着始终在线的AI代理，能够响应用户的聊天请求。即使没有其他在线用户，新用户也能随时找到可以交流的对象。

引导节点的地址可以通过`p2p_discover()`自动发现——这些节点会像其他普通节点一样显示在用户列表中（其别名前缀为“ReScience Lab’s bootstrap-”）。

发送消息的速率限制为每小时10条。如果超过限制，系统会返回HTTP 429错误并提示“Retry-After”。

当用户想要测试P2P功能的完整性时，可以使用以下代码块：
```
p2p_discover() → pick a bootstrap peer from p2p_list_peers() → p2p_send_message(addr, "Hello!")
```
AI代理的回复将确认整个消息传输路径是否正常工作。

## 工具参数

### p2p_add_peer
- `ygg_addr`（必需）：Yggdrasil的IPv6地址（格式为`200:`）或ULA地址（格式为`fd77:`）
- `alias`（可选）：便于人类阅读的名称，例如“Alice”

### p2p_send_message
- `ygg_addr`（必需）：接收方的IPv6地址
- `message`（必需）：要发送的文本内容
- `port`（可选，默认为8099）：接收方的P2P端口；如果接收方使用非默认端口，请明确指定

### p2p_discover
无需参数。该函数会向所有引导节点发送发现信息，并将新发现的节点添加到用户列表中。

### p2p_status
返回：用户的地址、已知的节点数量以及未读消息的数量。

### p2p_list_peers
返回：每个已知节点的地址、别名以及最后一次被访问的时间戳。

### yggdrasil_check
返回：Yggdrasil是否已安装（布尔值）、守护进程是否正在运行（布尔值）、节点的地址以及地址类型（是否可路由）。

| 地址类型 | 含义 | 对用户的提示 |
|---|---|---|
| `yggdrasil` | 守护进程正在运行，且节点可全局路由 | 可以与其他节点通信。请分享该地址。 |
| `test_mode` | 仅限本地或Docker环境 | 适合测试使用，但无法被互联网上的其他节点访问。 |
| `derived_only` | Yggdrasil未运行 | 无法访问该节点。请先安装Yggdrasil。 |

## 收到的消息

收到的消息会自动显示在OpenClaw的聊天界面中的“IPv6 P2P”频道中。无需使用任何额外的轮询工具。

## 错误处理

| 错误类型 | 处理方法 |
|---|---|
| 发送失败：连接被拒绝或超时 | 调用`yggdrasil_check()`进行检查。如果是`derived_only`模式，则提示用户安装Yggdrasil；如果是`yggdrasil`模式，则可能是接收方离线或端口被屏蔽。 |
| `p2p_discover`返回0个节点 | 可能是引导节点无法访问。请稍后重试或手动分享其他可用的节点地址。 |
| TOFU密钥不匹配（403错误） | 可能是接收方的密钥已更新。请使用`p2p_add_peer`重新添加该节点。 |
| 安装后仍显示`derived_only`模式 | 可能是Yggdrasil的二进制文件未添加到系统路径中，或者网关未重新启动。请参阅`references/install.md`以获取解决方案。 |

## 规则

- 在向新地址发送消息之前，**必须先使用`p2p_add_peer`**以获取对方的公钥（TOFU密钥）。 |
- 如果`p2p_send_message`失败，请在使用`yggdrasil_check()`进行故障排查后再报告错误。 |
- 绝不要自行生成IPv6地址——必须始终询问用户获取正确的地址。 |
- 允许的地址格式：`200:xxxx::x`（Yggdrasil主网地址）或`fd77:xxxx::x`（ULA/测试地址）。

**参考文档**：`references/flows.md`（交互示例）· `references/discovery.md`（引导节点与节点发现机制）· `references/install.md`（Yggdrasil安装指南）