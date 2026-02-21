# ShieldAgent 技能

这是一个自主运行的去中心化金融（DeFi）智能合约漏洞扫描器。

## 使用方法

```bash
shield-agent scan <address>
shield-agent monitor <address> --interval 3600
shield-agent report <scan_id>
```

## 集成

该技能与 EvoClaw 的代理运行时环境以及 ClawChain 的 `pallet-agent-receipts` 模块集成，用于链上审计验证。

每次扫描的结果都会被记录在 ClawChain 上，形成不可篡改的审计记录，从而提供可验证的安全审计证明。