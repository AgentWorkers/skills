# AgentMesh 技术文档 (SKILL.md)

> **专为 AI 代理设计的 WhatsApp 风格的端到端加密通信方案。**
> GitHub: https://github.com/cerbug45/AgentMesh | 作者: cerbug45

---

## 什么是 AgentMesh？

AgentMesh 为每个 AI 代理分配一个 **加密身份**，并允许代理之间进行以下方式的消息交换：

| 属性 | 机制        |
|---|-----------|
| **加密**   | AES-256-GCM 加密（带身份验证） |
| **认证**   | 每条消息使用 Ed25519 数字签名 |
| **前向保密** | X25519 ECDH 临时会话密钥 |
| **防篡改** | AEAD 认证标签       |
| **防重放** | 使用随机数和计数器防止重复发送 |
| **隐私保护** | 代理中心（Hub）无法查看消息内容 |

无需 TLS 证书，本地使用无需服务器。只需执行一次 `pip install` 即可安装。

---

## 安装

### 系统要求

- Python 3.10 或更高版本
- `pip` 工具

### 方法 1 – 从 GitHub 安装（推荐）

```bash
pip install git+https://github.com/cerbug45/AgentMesh.git
```

### 方法 2 – 从源代码克隆并本地安装

```bash
git clone https://github.com/cerbug45/AgentMesh.git
cd AgentMesh
pip install .
```

### 方法 3 – 开发者版本（可修改，包含测试）

```bash
git clone https://github.com/cerbug45/AgentMesh.git
cd AgentMesh
pip install -e ".[dev]"
pytest           # run all tests
```

### 验证安装是否成功

```python
python -c "import agentmesh; print(agentmesh.__version__)"
# → 1.0.0
```

---

## 快速入门（5 分钟）

```python
from agentmesh import Agent, LocalHub

hub   = LocalHub()                  # in-process broker
alice = Agent("alice", hub=hub)     # keys generated automatically
bob   = Agent("bob",   hub=hub)

@bob.on_message
def handle(msg):
    print(f"[{msg.recipient}] ← {msg.sender}: {msg.text}")

alice.send("bob", text="Hello, Bob! This is end-to-end encrypted.")
```

---

## 核心概念

### 代理（Agent）

代理是一个具有 **加密身份** 的 AI 代理（包含两对密钥）：

- **Ed25519 身份密钥**：用于签署每条发出的消息
- **X25519 会话密钥**：用于建立 ECDH 会话

```python
from agentmesh import Agent, LocalHub

hub   = LocalHub()
alice = Agent("alice", hub=hub)

# See the agent's fingerprint (share out-of-band to verify identity)
print(alice.fingerprint)
# → a1b2:c3d4:e5f6:g7h8:i9j0:k1l2:m3n4:o5p6
```

### 代理中心（Hub）

代理中心是消息的路由器，负责存储公钥包（用于识别代理）并转发加密后的消息。代理中心无法解密消息。

| 代理中心类型 | 适用场景       |
|---|--------------|
| `LocalHub` | 单个 Python 进程（演示、测试） |
| `NetworkHub` | 多进程/多机器环境（生产环境） |

### 消息（Message）

---

## 使用指南

### 发送带有额外数据的消息

除了 `text` 参数外，所有关键字参数都会被包含在 `msg.payload` 中。

### 链式处理消息（Chaining handlers）

---

### 持久化密钥管理

将密钥保存到磁盘，以确保代理在重启后仍能保持相同的身份：

- 首次运行时生成密钥文件。
- 之后的运行会从该文件中加载密钥（相同的密钥意味着相同的身份）。
- 请确保密钥文件的安全存储，因为其中包含私钥。

### 对等体发现（Peer discovery）

---

## 网络模式（多机器环境）

### 1. 启动代理中心服务器

在代理中心所在的机器上运行相应命令：

```bash
# Option A – module
python -m agentmesh.hub_server --host 0.0.0.0 --port 7700

# Option B – entry-point (after pip install)
agentmesh-hub --host 0.0.0.0 --port 7700
```

### 2. 代理从任何地方连接

```python
# Machine A
from agentmesh import Agent, NetworkHub
hub   = NetworkHub(host="192.168.1.10", port=7700)
alice = Agent("alice", hub=hub)

# Machine B (different process / different computer)
from agentmesh import Agent, NetworkHub
hub = NetworkHub(host="192.168.1.10", port=7700)
bob = Agent("bob", hub=hub)

bob.on_message(lambda m: print(m.text))
alice.send("bob", text="Cross-machine encrypted message!")
```

### 代理中心架构

```
┌──────────────────────────────────────────────────────┐
│                   NetworkHubServer                   │
│  Stores public bundles.  Routes encrypted envelopes. │
│  Cannot read message contents.                       │
└──────────────────────┬───────────────────────────────┘
                       │ TCP (newline-delimited JSON)
           ┌───────────┼───────────┐
           │           │           │
      Agent A      Agent B      Agent C
   (encrypted)  (encrypted)  (encrypted)
```

---

## 安全架构

### 加密机制

```
┌─────────────────────────────────────────────────────┐
│  Application layer (dict payload)                   │
├─────────────────────────────────────────────────────┤
│  Ed25519 signature  (sender authentication)         │
├─────────────────────────────────────────────────────┤
│  AES-256-GCM  (confidentiality + integrity)         │
├─────────────────────────────────────────────────────┤
│  HKDF-SHA256 key derivation (directional keys)      │
├─────────────────────────────────────────────────────┤
│  X25519 ECDH  (shared secret / forward secrecy)     │
└─────────────────────────────────────────────────────┘
```

### 安全特性

| 攻击方式 | 防御措施       |
|---|-------------|
| 窃听     | AES-256-GCM 加密        |
| 消息篡改 | AEAD 认证标签       |
| 伪装     | 每条消息都带有 Ed25519 签名   |
| 防重放攻击 | 使用随机数和计数器     |
| 密钥泄露   | 临时会话密钥（前向保密）   |
| 代理中心被攻破 | 代理中心仅存储公钥，无法解密消息 |

### 代理中心可以查看的内容

- ✅ 代理 ID（用于路由消息）
- ✅ 公钥包（用于识别代理）
- ✅ 元数据：发送者、接收者、时间戳、消息计数器
- ❌ 消息内容（始终加密）
- ❌ 载荷数据（始终加密）

---

## 示例

| 文件名 | 功能         |
|---|-------------|
| `examples/01_simple_chat.py` | 两个代理之间的简单通信 |
| `examples/02_multi_agent.py` | 协调器与多个工作代理的任务分配 |
| `examples/03_persistent_keys.py` | 将密钥保存到磁盘，确保重启后身份不变 |
| `examples/04_llmAgents.py` | 使用 LLM 代理（如 OpenAI 或其他 API） |

可以运行任意示例文件：

```bash
python examples/01_simple_chat.py
```

---

## API 参考

### `Agent` 方法

```python
agent_id = "agent_id"
hub = None
keypair_path = None
log_level = "WARNING"
agent = Agent(agent_id, hub, keypair_path, log_level)
```

| 方法        | 描述                          |
|-------------|-----------------------------------|
| `send(recipient_id, text="", **kwargs)` | 发送加密消息                         |
| `send_payload(recipient_id, payload: dict)` | 低级发送方式                         |
| `on_message(handler)` | 注册消息处理函数                         |
| `connect(peer_id)` | 预先建立会话（可选，自动连接）                    |
| `connect_with_bundle(bundle)` | 使用公钥包直接建立 P2P 连接                   |
| `list_peers()` | 列出代理中心上的所有对等体 ID                    |
| `status()` | 返回代理的状态信息                         |
| `fingerprint` | 人类可读的十六进制身份标识                   |
| `public_bundle` | 返回代理的公钥包                         |

---

### `LocalHub` 类

```python
local_hub = LocalHub()
local_hub.register(agent)      # 自动注册代理
local_hub.deliver(envelope)    | 路由加密消息                         |
| local_hub.get_bundle(agent_id)   | 获取指定代理的公钥包                     |
| local_hub.list_agents()    | 列出所有注册的代理                         |
| local_hub.message_count()    | 显示已路由的消息数量                     |

```

### `NetworkHub` 类

```python
network_hub = NetworkHub(host="0.0.0.0", port=7700)
```

`NetworkHub` 与 `LocalHub` 接口相同，但通过 TCP 与远程的 `NetworkHubServer` 通信。

### `NetworkHubServer` 类

```python
network_hub.start(block=True)   # 启动服务器（block 参数为 False 表示后台运行）
```

### 高级加密技术细节

```python
from agentmesh.crypto import (
    AgentKeyPair,        # key generation, serialisation, fingerprint
    CryptoSession,       # encrypt / decrypt
    perform_key_exchange,# X25519 ECDH → CryptoSession
    seal,                # sign + encrypt (high-level)
    unseal,              # decrypt + verify (high-level)
    CryptoError,         # raised on any crypto failure
)
```

---

## 常见问题及解决方法

### `CryptoError: 检测到重放攻击`
您尝试发送了相同的加密消息。每次调用 `send()` 时都会生成新的加密消息，请勿重复使用相同的消息。

### `CryptoError: 认证标签不匹配`
消息在传输过程中被篡改。请确保传输过程中不会损坏二进制数据（使用安全的 JSON 编码方式，如 base64）。

### `ValueError: 对等体 'xxx' 未在代理中心找到`
接收方尚未在代理中心注册。请确保两个代理使用相同的代理中心实例（`LocalHub`）或连接到同一个代理中心服务器（`NetworkHub`）。

### `RuntimeError: 未配置代理中心`
您在创建代理时未指定代理中心。请传递 `hub=LocalHub()` 或 `hub=NetworkHub()` 参数。

---

## 贡献代码

欢迎提交问题或 pull 请求：https://github.com/cerbug45/AgentMesh/issues

---

## 许可证

MIT 许可证 © cerbug45 – 详细许可信息请参见 [LICENSE](LICENSE) 文件。