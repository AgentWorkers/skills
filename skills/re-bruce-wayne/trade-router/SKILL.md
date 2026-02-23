---
name: traderouter
description: 通过 TradeRouter API 执行 Solana 交易、提交受 MEV 保护的交易、扫描钱包中的资产，以及基于市值设置限价/追踪订单。适用于用户需要执行以下操作的场景：在 Solana 上买卖 SPL 代币、查看钱包中的代币持有情况、通过受 MEV 保护的优先通道提交已签名的交易、设置限价订单（在目标市值水平买入/卖出）、设置追踪止损订单（trailing_sell/trailing_buy）、管理现有订单（查看、列出、取消、延长订单），或实现定期定额投资（DCA）策略。无需 API 密钥——仅需提供钱包地址即可进行操作。该 API 支持以下 REST 端点：POST /swap、POST /holdings、POST /protect；同时支持用于提交限价订单的 WebSocket 端点：wss://api.traderouter.ai/ws。
---
# TradeRouter

Solana交易路由器和限价单引擎。

**基础URL:** `https://api.traderouter.ai`
**WebSocket连接:** `wss://api.traderouter.ai/ws`
**官方网站:** https://traderouter.ai
**认证:** 无需API密钥。仅使用钱包地址进行身份验证。
**内容类型:** 所有REST请求都需要`Content-Type: application/json`。

---

## 使用本技能前的注意事项

**维护WebSocket连接:** 下单、追踪订单和订单管理（取消、延长、列出）需要保持与`wss://api.traderouter.ai/ws`的连接打开。服务器仅通过该连接发送`order_filled`信息——如果客户端断开连接，直到重新连接并重新注册后才能收到成交结果。只要还有未完成的限价/追踪订单，就需要保持WebSocket连接活跃，以便接收和执行成交。在断开连接后，请重新连接并重新注册（详见“重新连接”部分）；活跃订单会保存在服务器端。

**订单管理的认证:** WebSocket上的订单放置和取消通过“挑战-响应”流程进行：服务器发送一个带有随机数（nonce）的挑战；客户端必须使用钱包的私钥（Ed25519算法）对随机数进行签名，并发送包含`wallet_address`和Base58签名的`register`请求。只有在服务器返回`registered`且`authenticated: true`后，客户端才能放置或取消订单。这种认证方式是通过签名来验证钱包所有权的。

**服务来源:** 本文档仅描述了API接口。服务网站是`https://traderouter.ai`（API地址为api.traderouter.ai）。

**MEV保护:** `/POST /protect`端点接受已签名的交易，并使用`Jito`和**质押连接通道**来处理这些交易。

**风险:** 无需API密钥；唯一需要的身份验证信息是钱包地址（对于WebSocket订单，还需要通过签名来验证所有权）。

---

## 如何使用不同的端点

| 客户操作 | 对应端点 | 方法 |
|-------------|----------|--------|
| 即时买卖代币 | `POST /swap` → 签名 → `POST /protect` | REST请求 |
| 查看钱包代币余额 | `POST /holdings` | REST请求 |
| 提交已签名的交易（具有MEV保护） | `POST /protect` | REST请求 |
| 下限价单（获利、止损、逢低买入、突破买入） | WebSocket上的`sell`或`buy`操作 | WebSocket请求 |
| 追踪止损（根据市场自动调整） | WebSocket上的`trailing_sell`或`trailing_buy`操作 | WebSocket请求 |
| 管理订单（查看、列出、取消、延长） | WebSocket操作 | WebSocket请求 |
| 定投（DCA，定期小额买入） | WebSocket上的`buy`操作 | WebSocket请求 |