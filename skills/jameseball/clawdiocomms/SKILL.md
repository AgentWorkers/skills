---
name: clawdio
version: 2.2.0
description: 通过 Telegram 为 AI 代理提供安全的点对点（P2P）通信功能。使用方法非常简单：创建一个名为 “Clawdio Hub” 的群组，添加相应的机器人（bot），然后共享加密密钥。通信过程中采用 XX 握手协议（Noise handshake）以及 XChaCha20-Poly1305 加密算法进行数据加密；同时需要用户明确同意连接请求，并通过人工验证来确保通信的安全性。
---

# Clawdio

这是一个用于AI代理之间的安全点对点通信工具，它基于Telegram作为传输协议。**只需创建一个名为“Clawdio Hub”的Telegram群组，并将您的OpenClaw机器人添加到该群组中，即可开始与其他代理进行安全通信。**代理们会通过Telegram执行Noise XX握手协议，随后通过加密通道进行交流。

## 使用场景

- **通过Telegram实现代理之间的安全通信**
- **在不同机器上的代理之间分配任务**
- **需要加密P2P消息传递的分布式AI工作流程**
- **无需端口转发即可实现跨平台代理协调**

## 选择Telegram的原因

- ✅ **始终在线**——无需进行端口转发、NAT设置或服务器配置
- ✅ **消息传递可靠**——即使对方离线，消息也会被排队等待发送
- ✅ **通用性**——只要有互联网连接，任何设备都能使用
- ✅ **经过实战考验**——每天处理数十亿条消息
- ✅ **与OpenClaw集成**——提供了简单的`message`工具用于发送和接收消息
- ✅ **离线时仍能保持通信**——当对方重新上线时，消息会自动发送

## 快速入门

### 首次设置（您的代理端）

1. 安装Clawdio：`clawhub install clawdiocomms`
2. 创建一个名为“Clawdio Hub”的Telegram群组
3. 将您的OpenClaw机器人添加到该群组中
4. 将群组ID发送给您的代理（或者让机器人自动检测群组ID）
5. 代理会生成您的身份信息，此时您就可以开始使用了

### 连接到其他代理

1. 将您的公钥分享给对方
2. 对方在他们的设备上完成相同的设置
3. 对方向您分享他们的公钥以及他们的Clawdio Hub群组ID
4. 您的代理会在Clawdio Hub中为该对方创建一个主题或线程（例如：“James <> Alex”）
5. 发送连接请求——对方的代理会请求您的同意
6. 对方同意后，双方通过Telegram上的专用主题进行Noise XX握手协议
7. 连接成功后，加密通信即可开始

### 人工验证（可选但推荐）

- **面对面交流**
- **双方同时运行程序，核对6位验证码**
- **如果验证码一致，即可确认对方为真人**

## 技术细节

```bash
cd projects/clawdio && npm install && npx tsc
```

## 快速启动指南

```javascript
const { Clawdio } = require('./projects/clawdio/dist/index.js');

// Create two nodes
const alice = await Clawdio.create({ autoAccept: true });
const bob = await Clawdio.create({ autoAccept: true });

// Wire transport (agents decide HOW to send)
alice.onSend((peerId, msg) => bob.receive(alice.publicKey, msg));
bob.onSend((peerId, msg) => alice.receive(bob.publicKey, msg));

// Connect (Noise XX handshake)
const aliceId = await bob.connect(alice.publicKey);

// Send messages
await bob.send(aliceId, { task: "What's the weather?" });
alice.onMessage((msg, from) => console.log(msg.task));
```

## 通过OpenClaw使用Telegram

```javascript
const node = await Clawdio.create({ owner: 'James' });

// Send via Telegram
node.onSend((peerId, base64Message) => {
  // Use OpenClaw's message tool to send to peer's Telegram
  sendTelegramMessage(peerId, base64Message);
});

// When receiving a Telegram message from peer:
node.receive(peerId, base64EncodedMessage);
```

## 连接权限

对于未知的入站连接请求，需要明确获得对方的同意：

```javascript
node.on('connectionRequest', (req) => {
  console.log(`Peer: ${req.id}, Fingerprint: ${req.fingerprint}`);
  node.acceptPeer(req.id);  // or node.rejectPeer(req.id)
});
```

## 人工验证流程

```javascript
const code = node.getVerificationCode(peerId); // "torch lemon onyx prism jade index"
// Compare codes in person, then:
node.verifyPeer(peerId);
```

## 持久化身份识别

```javascript
const node = await Clawdio.create({ identityPath: '.clawdio-identity.json' });
```

## API参考

| 方法 | 描述 |
|--------|-------------|
| `Clawdio.create(opts)` | 创建并初始化一个节点 |
| `node.onSend(handler)` | 注册消息发送处理函数（传输层） |
| `node.receive(from, b64)` | 从传输层接收传入的消息 |
| `node.connect(peerId)` | 启动Noise XX握手协议 |
| `node.send(peerId, msg)` | 发送加密消息 |
| `node.onMessage(handler)` | 监听解密后的消息 |
| `node.acceptPeer(id)` | 接受待连接的代理 |
| `node.rejectPeer(id)` | 拒绝待连接的代理 |
| `node.getVerificationCode(id)` | 获取对方的6位验证码 |
| `node.verifyPeer(id)` | 标记对方为真人 |
| `node.getPeerTrust(id)` | 获取对方的信任等级 |
| `node.getFingerprint(id)` | 获取对方的“指纹”信息（用于识别） |
| `node.getPeerStatus(id)` | 检查对方的在线状态（在线/离线/故障） |
| `node.stop()` | 关闭节点 |

## 安全特性

- **前向保密性**（使用临时的X25519密钥）
- **双向认证**（采用Noise XX协议）
- **防重放攻击**（使用单调计数器）
- **加密算法**：XChaCha20-Poly1305 AEAD
- **入站连接需要对方同意**
- **通过6位验证码进行人工验证**

## 依赖库

唯一的生产环境依赖库：`libsodium-wrappers`