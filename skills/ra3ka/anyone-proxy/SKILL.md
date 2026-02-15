---
name: anyone-proxy
homepage: https://anyone.io
description: 此技能支持IP地址的伪装，并允许用户访问“Anyone Network”中的隐藏服务。它通过使用本地的SOCKS5代理，将请求路由到“Anyone Protocol”VPN网络中。
metadata:
  clawdbot:
    requires:
      packages:
        - "@anyone-protocol/anyone-client"
---

# Anyone Protocol 代理

该技能使 Clawdbot 能够通过 Anyone Protocol 网络路由请求。

## 工作原理

该技能使用 `@anyone-protocol/anyone-client` NPM 包来：
1. 启动一个本地的 SOCKS5 代理服务器（默认端口：9050）
2. 通过 Anyone Network 创建加密通信通道
3. 将流量通过这些通道进行路由
4. 在返回响应时隐藏原始 IP 地址

## 设置

## 安装 anyone-client
```bash
npm install -g @anyone-protocol/anyone-client
```

## 启动代理
```bash
npx @anyone-protocol/anyone-client -s 9050
```

## 使用方法
代理启动后，通过以下方式路由请求：
```bash
# Using curl to verify IP
curl --socks5-hostname localhost:9050 https://check.en.anyone.tech/api/ip
```
```javascript
import { Anon } from "@anyone-protocol/anyone-client";
import { AnonSocksClient } from "@anyone-protocol/anyone-client";

async function main() {
    const anon = new Anon();
    const anonSocksClient = new AnonSocksClient(anon);

    try {
        await anon.start();
        // Wait for circuits to establish
        await new Promise(resolve => setTimeout(resolve, 15000));
        
        const response = await anonSocksClient.get('https://check.en.anyone.tech/api/ip');
        console.log('Response:', response.data);
        
    } catch(error) {
        console.error('Error:', error);
    } finally {
        await anon.stop();
    }
}

main();
```

## 注意事项

- 首次连接时，可能需要最多 30 秒时间来建立通信通道
- 代理在启动后会在后续请求中持续生效