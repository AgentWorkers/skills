# Web3 Signer API 规范（参考实现）

> **版本**: v1.0.0  
> **目的**: 定义 web3-investor skill 期望的签名服务 API 接口  
> **适用对象**: 签名服务实现者、智能体（Agent）

---

## 设计理念

### 面向智能体设计

本规范的设计目标是**让智能体理解**，而非让程序自动适配。

- 智能体拥有 LLM 能力和编程能力
- 智能体可以阅读文档、理解设计意图、二次修改代码
- 我们提供的是**参考规范**，而非强制标准

### 核心原则

| 原则 | 说明 |
|------|------|
| **无私钥** | 签名服务持有私钥，skill 不持有任何私钥 |
| **状态机** | 所有交易必须经过 `preview → approve → execute` |
| **安全检查** | 余额充足、授权充足、路由有效 |
| **可配置** | API 端点可通过配置文件映射 |

---

## 执行模型

```
┌─────────────────────────────────────────────────────────────┐
│                        Web3 Investor Skill                   │
│                     (运行在 Agent 环境中)                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ REST API 调用
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    本地 Keystore 签名服务                     │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐       │
│  │  Keystore   │   │  签名引擎   │   │  广播服务   │       │
│  │  (私钥存储)  │ → │  (eth_sign) │ → │  (RPC)     │       │
│  └─────────────┘   └─────────────┘   └─────────────┘       │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ 广播交易
                              ▼
                       ┌─────────────┐
                       │  区块链网络  │
                       │ (Base/ETH)  │
                       └─────────────┘
```

**关键点**：
- Skill 只负责生成交易请求，不持有私钥
- 签名服务负责签名和广播
- 两者通过 REST API 通信

---

## 状态机

```
preview ──→ approve ──→ execute
   │           │            │
   │           │            └──→ tx_hash (成功) 或 error (失败)
   │           │
   │           └──→ 需要人工确认
   │
   └──→ simulation_ok: true/false
        risk: { balance, allowance, route }
```

**强制规则**：
- ❌ 不能跳过 `approve` 步骤
- ✅ 必须先 `preview` 验证交易可行性
- ✅ `approve` 需要人工/外部确认

---

## API 端点规范

### 1. 查询余额

```
GET /api/wallet/balances
```

**查询参数**:
- `chain` (可选): 链名称，如 `base`, `ethereum`
- `tokens` (可选): 代币列表，如 `USDC,WETH`

**响应**:
```json
{
  "success": true,
  "balances": [
    {
      "symbol": "USDC",
      "address": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
      "balance": "1000.50",
      "chain": "base"
    },
    {
      "symbol": "ETH",
      "balance": "0.5",
      "chain": "base"
    }
  ]
}
```

---

### 2. 预览交易

```
POST /api/trades/preview
```

**请求**:
```json
{
  "type": "swap",
  "from_token": "USDC",
  "to_token": "WETH",
  "amount": "5",
  "network": "base",
  "slippage_percent": 0.5
}
```

**响应**:
```json
{
  "success": true,
  "preview_id": "550e8400-e29b-41d4-a716-446655440000",
  "simulation_ok": true,
  "rate": "0.00035",
  "estimated_output": "0.00175",
  "gas_estimate": 150000,
  "risk": {
    "balance_sufficient": true,
    "allowance_sufficient": true,
    "route_valid": true,
    "warnings": []
  },
  "transaction": {
    "to": "0x...",
    "value": "0x0",
    "data": "0x..."
  },
  "next_step": "approve"
}
```

**字段说明**:
| 字段 | 类型 | 说明 |
|------|------|------|
| `preview_id` | string | 预览ID，用于后续 approve |
| `simulation_ok` | boolean | 模拟是否成功 |
| `risk` | object | 风险评估结果 |
| `next_step` | string | 下一步操作：`approve` 或 `clarification` |

---

### 3. 批准交易

```
POST /api/trades/approve
```

**请求**:
```json
{
  "preview_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**响应**:
```json
{
  "success": true,
  "approval_id": "660e8400-e29b-41d4-a716-446655440001",
  "preview_id": "550e8400-e29b-41d4-a716-446655440000",
  "approved_at": "2026-03-05T06:00:00Z",
  "expires_at": "2026-03-05T06:30:00Z"
}
```

---

### 4. 执行交易

```
POST /api/trades/execute
```

**请求**:
```json
{
  "approval_id": "660e8400-e29b-41d4-a716-446655440001"
}
```

**响应**:
```json
{
  "success": true,
  "tx_hash": "0xabcdef1234567890...",
  "explorer_url": "https://basescan.org/tx/0xabcdef1234567890...",
  "network": "base",
  "executed_at": "2026-03-05T06:01:00Z"
}
```

---

### 5. 查询交易状态

```
GET /api/transactions/{tx_hash}
```

**响应**:
```json
{
  "success": true,
  "tx_hash": "0xabcdef1234567890...",
  "status": "confirmed",
  "block_number": 12345678,
  "gas_used": 145000,
  "network": "base"
}
```

---

### 6. 查询授权

```
GET /api/allowances?chain=base&token=USDC
```

**响应**:
```json
{
  "success": true,
  "allowances": [
    {
      "token": "USDC",
      "token_address": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
      "spender": "0x...",
      "spender_name": "Uniswap Router",
      "allowance": "115792089237316195423570985008687907853269984665640564039457584007913129639935",
      "allowance_formatted": "Unlimited"
    }
  ]
}
```

---

### 7. 预览撤销授权

```
POST /api/allowances/revoke-preview
```

**请求**:
```json
{
  "token": "USDC",
  "spender": "0x...",
  "chain": "base"
}
```

**响应**:
```json
{
  "success": true,
  "preview_id": "770e8400-e29b-41d4-a716-446655440002",
  "current_allowance": "115792089237316195423570985008687907853269984665640564039457584007913129639935",
  "next_step": "approve"
}
```

---

## 错误格式

所有错误响应遵循统一格式：

```json
{
  "success": false,
  "error": {
    "code": "E001",
    "message": "Insufficient balance for transaction"
  },
  "diagnostics": "Required: 10 USDC, Available: 5 USDC"
}
```

**错误码定义**:

| 代码 | 说明 |
|------|------|
| E001 | 余额不足 |
| E002 | 授权不足，需要先 approve token |
| E003 | 无有效路由 |
| E004 | 链不在白名单中 |
| E005 | 协议不在白名单中 |
| E006 | 代币不在白名单中 |
| E007 | 超过交易限额 |
| E008 | 模拟失败 |
| E009 | 未批准，无法执行 |
| E010 | API 服务不可用 |
| E999 | 未知错误 |

---

## 配置适配

签名服务实现者可以通过修改 `config/config.json` 来适配不同的 API：

```json
{
  "api": {
    "base_url": "http://localhost:3000/api",
    "endpoints": {
      "balances": "/wallet/balances",
      "preview": "/trades/preview",
      "approve": "/trades/approve",
      "execute": "/trades/execute",
      "status": "/transactions/{tx_hash}",
      "allowances": "/allowances",
      "revoke_preview": "/allowances/revoke-preview"
    }
  }
}
```

---

## 适配指南

如果你的签名服务 API 与本规范不同：

### 方法 1：修改配置文件
修改 `config/config.json` 中的 `endpoints` 映射。

### 方法 2：修改代码
修改 `scripts/trading/trade_executor.py` 中的 `api_request()` 函数。

### 方法 3：实现适配层
在你的签名服务中实现一个适配层，将你的 API 转换为本规范格式。

---

## 安全建议

1. **签名服务应运行在本地**，不暴露到公网
2. **approve 步骤应有确认机制**，可以是：
   - 控制台确认（开发环境）
   - 硬件钱包确认（生产环境）
   - 多签确认（团队环境）
3. **设置交易限额**，防止单笔交易金额过大
4. **白名单机制**，限制可交互的合约地址

---

**维护者**: Web3 Investor Skill Team  
**更新日期**: 2026-03-05