---
name: aap
version: 3.2.0
description: **代理认证协议——反向图灵测试**  
用于验证人工智能代理的真实性，同时阻止人类滥用这些代理。
homepage: https://github.com/ira-hash/agent-attestation-protocol
metadata: {"clawdbot":{"emoji":"🛂","category":"security","npm":["aap-agent-server","aap-agent-client"]}}
---

# AAP（Agent Attestation Protocol）——代理认证协议

**反向图灵测试（Reverse Turing Test）**：CAPTCHA用于阻止机器人访问，而AAP则用于阻止人类滥用服务。

## 功能概述

AAP通过以下方式验证客户端是否为AI代理：
- 向客户端发送对大型语言模型（LLM）来说简单的挑战，但对人类来说无法在规定的时间内完成；
- 要求客户端使用secp256k1加密算法进行身份验证；
- 在6秒内完成7个挑战，并强制要求客户端签名。

## 安装说明

```bash
npm install aap-agent-server  # Server
npm install aap-agent-client  # Client
```

## 服务器端使用方法

```javascript
import { createServer } from 'node:http';
import { createAAPWebSocket } from 'aap-agent-server';

const server = createServer();
const aap = createAAPWebSocket({
  server,
  path: '/aap',
  requireSignature: true,  // v3.2 default
  onVerified: (result) => console.log('Verified:', result.publicId)
});

server.listen(3000);
```

## 客户端使用方法

```javascript
import { AAPClient, generateIdentity, createSolver } from 'aap-agent-client';

// Identity auto-generated (secp256k1 key pair)
const client = new AAPClient({
  serverUrl: 'ws://localhost:3000/aap'
});

const result = await client.verify(solver);
// Signature automatically included
```

## 协议流程（WebSocket v3.2）

```
← handshake (requireSignature: true)
→ ready (publicKey)
← challenges (7 challenges)
→ answers + signature + timestamp
← result (verified/failed + sessionToken)
```

## 签名格式

使用secp256k1算法生成的签名数据：
```javascript
JSON.stringify({ nonce, answers, publicId, timestamp })
```

## 配置参数

| 参数 | 默认值 | 说明 |
|--------|---------|-------------|
| `challengeCount` | 7 | 挑战的数量 |
| `totalTimeMs` | 6000 | 时间限制（毫秒） |
| `requireSignature` | true | 强制要求进行加密签名验证 |

## 安全特性：
- 使用secp256k1加密算法进行身份验证，确保用户身份的真实性；
- 强制要求签名，防止匿名访问；
- 在6秒内完成7个挑战，对人类来说几乎不可能完成；
- 具有不可否认性（所有操作均可追溯）。

## 相关链接：
- [GitHub仓库](https://github.com/ira-hash/agent-attestation-protocol) |
- [服务器端库：aap-agent-server](https://www.npmjs.com/package/aap-agent-server) |
- [客户端库：aap-agent-client](https://www.npmjs.com/package/aap-agent-client) |
- [在线演示：ClosedClaw](https://focused-blessing-production-d764.up.railway.app/)