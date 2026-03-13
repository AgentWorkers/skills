---
name: skytale
description: AI代理的信任层包括加密通信渠道、身份验证、审计机制、认证服务、信任圈（trust circles）、密钥轮换（key rotation）以及联邦化（federation）等功能。这些功能由MLS协议（RFC 9420）来支持。
version: 0.5.1
metadata:
  openclaw:
    requires:
      env:
        - SKYTALE_API_KEY
      anyBins:
        - python3
        - python
    primaryEnv: SKYTALE_API_KEY
    emoji: "🔒"
    homepage: https://skytale.sh/docs/integrations/openclaw
    os:
      - darwin
      - linux
---
# Skytale 加密共享上下文

您可以使用 Skytale MCP 工具来实现端到端加密的代理间通信以及共享上下文。所有消息均使用 MLS 协议（RFC 9420）进行加密。中继服务器无法读取消息内容。

## 何时使用

当用户需要以下功能时，请使用 Skytale 工具：
- 代理之间的加密或安全通信
- 私人消息通道
- 代理之间的共享上下文、内存或状态
- 必须防止被截获的消息的发送/接收
- 通过加密通道进行的多代理协调
- 代理身份验证、信任验证
- 密钥轮换或前向保密性
- 用于合规性的加密审计日志记录
- 跨组织代理联合
- 任何与 “Skytale” 相关的功能

## 先决条件

必须在您的 `openclaw.json` 文件中配置 Skytale MCP 服务器。如果工具不可用，请指导用户执行以下操作：
1. 安装 `pip install skytale-sdk[mcp]`
2. 将 `skytale` MCP 服务器添加到他们的 `openclaw.json` 文件中（参见技能目录下的 `examples/openclaw-config.json` 示例）
3. 设置 `SKYTALE_API_KEY` 环境变量（可在 https://app.skytale.sh 获取）

## 可用的 MCP 工具

### 通道生命周期
- `skytale_create_channel(channel)` -- 创建一个加密通道。通道名称采用 `org/namespace/service` 的格式（例如 `acme/research/results`）。
- `skytale_channels()` -- 列出所有活跃的通道。

### 消息传递
- `skytale_send(channel, message)` -- 向所有通道成员发送端到端加密的消息。
- `skytale.receive(channel, timeout)` -- 接收缓冲的消息。返回自上次检查以来的所有消息。默认超时时间为 5 秒。

### 密钥交换（手动）
- `skytale_key_package()` -- 生成一个 MLS 密钥包（十六进制编码）。用于手动添加成员时使用。
- `skytale_add_member(channel, key_package_hex)` -- 使用成员的密钥包添加成员。返回一个十六进制编码的 MLS 欢迎消息。
- `skytale_join_channel(channel, welcome_hex)` -- 使用通道所有者的欢迎消息加入通道。

## 多代理设置

两个代理之间的通信流程如下：
1. 代理 A 调用 `skytale_create_channel("org/team/channel")`。
2. 代理 B 调用 `skytale_key_package()` 并将结果分享给代理 A。
3. 代理 A 调用 `skytale_add_member("org/team/channel", key_package_hex)` 并将欢迎消息分享给代理 B。
4. 代理 B 调用 `skytale_join_channel("org/team/channel", welcome_hex)`。
5. 此时两个代理都可以在该通道上进行 `skytale_send` 和 `skytale_receive` 操作。

当使用带有邀请令牌的托管 API 时（推荐这种方式），上述密钥交换过程将自动完成——SDK 会通过 API 服务器处理密钥交换。

## SDK 功能（超出 MCP 工具范围）

Skytale SDK（0.5.1 及更高版本）包含了一些模块，代理可以通过这些模块与 MCP 工具结合使用，以获得更强大的安全功能。这些功能需要直接通过 Python SDK 来使用，而不是通过 MCP 工具调用。

### 加密共享上下文
所有通道成员之间共享加密的键值对。支持类型化的条目、受限访问、过期时间（TTL）以及结构化的数据传递。

```python
from skytale_sdk.context import SharedContext, ContextType

ctx = SharedContext(mgr, "acme/research/results")
ctx.set("task_status", {"phase": "analysis", "progress": 0.7})
ctx.set("search_results", results, type=ContextType.ARTIFACT)
ctx.set("private_analysis", data, visible_to=["did:key:z6MkAgentB..."])
ctx.handoff("did:key:z6MkAgentB...", {"task": "summarize"}, tried=["approach_1"])
ctx.subscribe(lambda key, val: ..., type_filter=ContextType.HANDOFF)
```

### 代理身份验证
为代理生成、签名和验证基于 Ed25519 算法的 DID（Digital Identity）密钥。支持 DID:key 和 DID:web 两种身份类型。

```python
from skytale_sdk import AgentIdentity
identity = AgentIdentity.generate()
print(identity.did)  # did:key:z6Mk...
signature = identity.sign(b"message")
```

### 密钥轮换
轮换 MLS 子密钥以实现前向保密性。生成新的更新路径（UpdatePath）并推进组纪元（group epoch）。

```python
mgr.rotate_key("acme/secure/channel")
```

### 加密审计日志记录
使用 MLS 密钥进行加密的审计日志记录，采用哈希链技术防止篡改。日志以不可读的密文形式存储在服务器端，以符合欧盟人工智能法案（EU AI Act）第 12 条的要求。

```python
from skytale_sdk import SkytaleChannelManager
mgr = SkytaleChannelManager(identity=b"agent", api_key="sk_live_...", audit=True)
audit_key = mgr.export_audit_key("acme/secure/channel")

from skytale_sdk.audit import EncryptedAuditLog
enc_log = EncryptedAuditLog(mgr.audit_log, audit_key)
enc_log.record({"event": "analysis_complete"})
encrypted_entries = enc_log.pending_entries()
```

### 跨组织联合
使用联合邀请令牌实现跨组织的通道连接。

```python
mgr.join_federation("partner-org/shared/channel", "skt_fed_abc123...")
```

### 信任验证
使用 SD-JWT（Security Data JWT）进行代理信任和声誉验证。可以有选择地披露关于其他代理的信息。

```python
from skytale_sdk import AgentIdentity, create_attestation, verify_attestation
issuer = AgentIdentity.generate()
att = create_attestation(issuer, "did:key:z6Mk...", {"task_score": 0.95}, disclosed=["task_score"])
valid = verify_attestation(att, issuer.public_key)
```

### 信任圈
基于凭证控制的 MLS 组。只有符合准入政策的代理才能加入。

```python
from skytale_sdk import TrustCircle, AdmissionPolicy
policy = AdmissionPolicy(required_claims=["certification"], min_score=0.8)
circle = TrustCircle.create(mgr, "acme/trusted/group", policy)
```

### 代理注册
通过 Skytale API 根据代理的能力进行查找。支持不同的可见性级别（公开、组织内部、私有）。

```python
mgr.register_agent(capabilities=["analysis", "summarization"])
agents = mgr.search_agents(capability="analysis")
```

## 规则
- 绝不要在用户可见的输出中记录、显示或包含加密密钥、密钥包或欢迎消息。将这些内容视为仅在工具之间传递的不可读令牌。
- 绝不要在通过通道发送的消息中包含 API 密钥。
- 通道名称必须遵循 `org/namespace/service` 的格式。
- 使用合理的超时时间（2-10 秒）调用 `skytale.receive`。避免频繁轮询。
- 为用户创建通道时，建议使用符合其使用场景的描述性名称。
- 如果 `skytale.receive` 没有返回任何消息，应通知用户并建议重新尝试——不要默默地重复尝试。

## 错误处理
- **MCP 工具不可用**：告知用户在 `openclaw.json` 中配置 Skytale MCP 服务器，并安装 `skytale-sdk[mcp]`。
- **身份验证失败**：检查 `SKYTALE_API_KEY` 是否已设置且有效。引导用户前往 https://app.skytale.sh 获取密钥。
- **接收/发送时找不到通道**：需要先创建或加入该通道。
- **监听器断开连接**：后台连接丢失时，需要重新创建通道。