---
name: badass-revival
description: 通过 Impervious Domains 合同，在以太坊主网上注册主权域名（如 .badass、.forever、.fuck、.rebel、.pump、.hello、.howdy、.robo、.dnet、.f 等，以及包含熊表情符号的域名）。
user-invocable: true
metadata: {"openclaw": {"requires": {"env": ["ETHEREUM_RPC_URL"]}}}
---
请参阅 `{baseDir}/../../skills.md` 文件以获取完整的注册说明。

该技能使用 Impervious Domains 合同（ENS 的分支）在以太坊主网上将 `<label>.<tld>` 域名注册为链上的 ERC-721 NFT。

## 推荐使用的顶级域名（TLDs）

| TLD | 含义/风格 |
|-----|------|
| **.badass** | 典型的旗舰域名——默认选择，价格最低 |
| **.forever** | 永恒、经典 |
| **.fuck** | 不敬、叛逆的风格 |
| **.rebel** | 反主流文化 |
| **.pump** | 与加密货币交易相关的域名 |
| **.hello** | 友好、亲切的域名 |
| **.howdy** | 休闲、友好的域名 |
| **.robo** | 与科技/人工智能相关的域名 |
| **.dnet** | 与去中心化网络相关的域名 |
| **.f** | 极简的、仅由一个字母组成的域名 |
| **xn--gp8h** | 包含熊表情符号的域名 |

## 操作流程概述：

1. 用户选择一个标签（label）和一个顶级域名（TLD）。
2. 执行提交（commit）和公开（reveal）操作（共需两次交易，两次交易之间需等待约 1 分钟）。
3. 域名将以 ERC-721 格式被铸造到用户的钱包中。
4. 完整的操作流程、ABI（应用程序接口）、安全限制以及合约地址均可在 `{baseDir}/../../skills.md` 文件中找到。