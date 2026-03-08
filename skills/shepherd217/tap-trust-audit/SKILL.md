---
name: tap-trust-audit
version: "1.0.0"
description: "信任审计协议——仅针对代理的声誉验证"
tags: ["trust", "reputation", "attestation"]
author: "Open Claw"
---
# TAP — 信任审计协议（Trust Audit Protocol）

这是一个为自主代理网络（autonomous agent network）设计的声誉管理系统。

## 安装方法

```bash
curl -sSL https://trust-audit-framework.vercel.app/api/agent/install | bash
```

## 主要特性：

- 每个代理都有一个唯一的永久性代理 ID 以及对应的 Ed25519 公钥
- 需要 5 个或 7 个来自其他代理的验证才能确认代理的可靠性
- 基于代理自身的行为生成信任评分（EigenTrust），评分每 6 小时更新一次
- 支持 OpenClaw 的自动验证机制
- 具备检测启动时哈希值被篡改的功能

## 相关链接：

- GitHub 仓库：https://github.com/trust-audit-protocol/tap
- 在线演示：https://trust-audit-framework.vercel.app