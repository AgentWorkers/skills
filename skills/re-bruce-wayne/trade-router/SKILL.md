---
name: traderouter
description: 通过 TradeRouter API 执行 Solana 交易、提交受 MEV（Mineralized Exchanges Value）保护的交易、扫描钱包中的资产，以及基于市场市值设置限价/追踪订单。适用于用户需要执行以下操作的场景：在 Solana 上买卖 SPL（Solana Protocol）代币、查看钱包中的代币持有情况、通过受 MEV 保护的优先通道提交已签名的交易、设置限价订单（在目标市场市值水平买入/卖出）、设置追踪止损订单（trailing_sell/trailing_buy）、管理现有订单（查看、列出、取消、延长订单），或实现定期定额投资（DCA）策略。无需 API 密钥——仅需提供钱包地址即可进行操作。该 API 支持以下 REST 请求方法：POST /swap（交易）、POST /holdings（查看持有资产）、POST /protect（保护交易免受 MEV 影响），以及用于限价订单的 WebSocket 接口：wss://api.traderouter.ai/ws。
---
# TradeRouter

这是一个用于Solana平台的交换构建工具和限价订单执行引擎。

**基础URL:** `https://api.traderouter.ai`  
**WebSocket连接:** `wss://api.traderouter.ai/ws`  
**官方网站:** https://traderouter.ai  
**认证方式:** 无需API密钥，仅使用钱包地址进行身份验证。  
**请求内容类型:** 所有REST请求都必须指定`Content-Type: application/json`。  

---

## 使用本工具前的注意事项  

**保持WebSocket连接活跃**：限价订单、跟踪订单以及订单管理（取消、延长、列出）操作都需要保持与`wss://api.traderouter.ai/ws`的连接处于打开状态。只有通过该连接，服务器才会发送`order_filled`响应；如果连接中断，需要重新连接并重新注册后才能接收到订单执行结果。对于任何未完成的订单，都必须保持连接活跃状态。  

**订单管理的认证机制**：通过`challenge–response`流程进行WebSocket上的订单放置和取消操作：服务器会发送一个包含随机数（nonce）的挑战请求；客户端必须使用钱包的私钥（Ed25519算法）对随机数进行签名，并附带`wallet_address`和签名结果发送`register`请求。只有在服务器返回`registered`且`authenticated: true`确认后，客户端才能放置或取消订单。这种认证方式基于对钱包的控制权验证，无需单独的API密钥。  

**服务来源**：本文档仅描述了该API的接口信息，服务官方网站为`https://traderouter.ai`（API接口地址为`api.traderouter.ai`）。  

**MEV保护**：`POST /protect`端点接受已签名的交易请求，并使用`Jito`框架和**质押连接通道**来处理这些交易。  

**风险提示**：无需提供API密钥；身份验证仅依赖于钱包地址（对于WebSocket订单，还需通过签名结果进行验证）。  

---

## 各端点的使用场景  

| 客户操作 | 对应端点 | 请求方法 |  
|-------------|----------|--------|--------|