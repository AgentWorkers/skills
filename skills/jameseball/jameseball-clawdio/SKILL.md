---
name: clawdio
version: 1.0.0
description: 为AI代理提供安全的P2P通信机制：采用Noise XX握手协议、XChaCha20-Poly1305加密算法进行数据传输，确保通信过程中的数据安全性；实施连接同意机制（connection consent）以验证双方身份；同时引入人工验证（human verification）流程来增强系统的安全性。整个通信过程完全不依赖任何中央服务器（zero central servers）。
---

# Clawdio

这是一个专为AI代理设计的轻量级、安全的点对点通信解决方案。两个代理通过交换连接字符串，执行“Noise XX”握手协议，随后在加密通道上进行通信。整个过程无需任何中央服务器的参与。

## 使用场景

- 代理之间的跨机器或网络通信  
- 不同主机上的子代理之间的安全任务委托  
- 任何需要加密且经过身份验证的点对点消息传递场景  

## 设置

Clawdio项目位于`projects/clawdio/`目录下。请按照以下步骤安装依赖项并构建项目：  
```bash
cd projects/clawdio && npm install && npx tsc
```  

## 快速入门  

```javascript
const { Clawdio } = require('./projects/clawdio/dist/index.js');

// Create two nodes
const alice = await Clawdio.create({ port: 9090, autoAccept: true });
const bob = await Clawdio.create({ port: 9091, autoAccept: true });

// Connect (Noise XX handshake)
const aliceId = await bob.exchangeKeys(alice.getConnectionString());

// Send messages
await bob.send(aliceId, { task: "What's the weather?" });
alice.onMessage((msg, from) => console.log(msg.task));
```  

## 连接权限控制（推荐）

默认情况下，系统会要求对未知的入站连接请求明确授权：  
```javascript
const node = await Clawdio.create({ port: 9090 }); // autoAccept defaults to false

node.on('connectionRequest', (req) => {
  console.log(`Connection from ${req.id}`);
  console.log(`Fingerprint: ${req.fingerprint}`);
  // Accept or reject
  node.acceptPeer(req.id);  // or node.rejectPeer(req.id)
});
```  

对于出站连接（即调用`exchangeKeys`的方法），系统会自动接受；而已被信任的代理则会自动重新连接。  

## 人工验证  

在需要高度信任的场景中，可要求用户通过面对面方式验证对方身份：  
```javascript
node.setOwner('Alice');
const code = node.getVerificationCode(peerId); // "torch lemon onyx prism jade index"
// Both humans compare codes in person, then:
node.verifyPeer(peerId); // trust: 'accepted' → 'human-verified'
node.getPeerTrust(peerId); // 'human-verified'
```  

## 信任等级  

- `pending`：连接请求已收到，但尚未被接受  
- `accepted`：代理已被接受，加密通信正在运行  
- `human-verified`：通过人工验证（代码交换）确认身份  

## 持久化身份信息  

通过传递`identityPath`参数，可以在系统重启后仍保留代理的密钥及可信代理的信息：  
```javascript
const node = await Clawdio.create({
  port: 9090,
  identityPath: '.clawdio-identity.json'
});
```  

## 子代理模式  

可以通过以下方式创建子代理来处理Clawdio通信：  
```
1. Main agent spawns sub-agent with task
2. Sub-agent creates Clawdio node, connects to remote peer
3. Sub-agent exchanges messages, collects results
4. Sub-agent reports back to main agent
```  

## 安全特性  

- 前向保密性（使用临时的X25519密钥）  
- 双向身份验证（基于“Noise XX”协议）  
- 防重放攻击机制（使用单调计数器）  
- XChaCha20-Poly1305加密算法  
- 对入站连接请求进行权限控制  

## API参考  

| 方法          | 描述                                      |
|---------------|-----------------------------------------|
| `Clawdio.create(opts)`   | 创建并启动一个代理节点                   |
| `node.exchangeKeys(connStr)` | 与指定代理建立连接                   |
| `node.send(peerId, msg)` | 向指定代理发送加密消息                 |
| `node.onMessage(handler)` | 监听并处理接收到的消息                 |
| `node.acceptPeer(id)`   | 接受待处理的连接请求                   |
| `node.rejectPeer(id)`    | 拒绝待处理的连接请求                   |
| `node.setOwner(name)`   | 设置代理的所有者名称                   |
| `node.getVerificationCode(id)` | 获取6位数的验证代码                   |
| `node.verifyPeer(id)`   | 标记代理为已通过人工验证                |
| `node.getPeerTrust(id)`   | 获取代理的信任等级                   |
| `node.getFingerprint(id)` | 获取代理的“指纹”信息                   |
| `node.getPeerStatus(id)` | 获取代理的状态（在线/离线/故障）             |
| `node.stop()`     | 关闭代理节点                     |