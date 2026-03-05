# Web3 Investor Skill - 签名服务对接指南

> **适用对象**: 智能体（Agent）、签名服务实现者  
> **目的**: 理解如何配置和验证签名服务

---

## 概述

web3-investor skill **不持有私钥**，所有交易执行通过 REST API 委托给外部签名服务。

```
┌──────────────────┐      REST API      ┌──────────────────┐
│  web3-investor   │ ─────────────────→ │  签名服务        │
│  (Skill)         │                    │  (持有私钥)      │
└──────────────────┘ ←───────────────── └──────────────────┘
                         交易结果
```

---

## 前置条件

在执行任何交易之前，需要确保：

1. **签名服务已启动**：运行在 `localhost:3000` 或其他地址
2. **API 可达**：skill 能够通过 HTTP 调用签名服务
3. **钱包已配置**：签名服务中已有可用账户

---

## 配置步骤

### 1. 检查/修改配置文件

配置文件位于 `config/config.json`：

```json
{
  "api": {
    "base_url": "http://localhost:3000/api",
    "timeout_seconds": 30,
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

**修改项**：
- `base_url`: 如果签名服务运行在其他地址/端口
- `endpoints`: 如果签名服务的 API 路径与本规范不同

### 2. 环境变量覆盖（可选）

```bash
# 覆盖 API 地址
export WEB3_INVESTOR_API_URL="http://localhost:8080/api"
```

---

## 验证签名服务

### 方法 1：命令行检查

```bash
# 检查余额接口是否可用
curl http://localhost:3000/api/wallet/balances

# 预期响应
{"success": true, "balances": [...]}
```

### 方法 2：使用 trade_executor.py

```bash
# 查询余额（会自动检查 API 可用性）
python3 scripts/trading/trade_executor.py balances --network base

# 如果成功，会返回余额列表
# 如果失败，会返回错误信息和诊断
```

---

## API 规范参考

详细的 API 规范请参阅：[SIGNER_API_SPEC.md](SIGNER_API_SPEC.md)

**核心端点**：

| 端点 | 用途 | 状态机阶段 |
|------|------|------------|
| `/wallet/balances` | 查询余额 | 前置检查 |
| `/trades/preview` | 预览交易 | preview |
| `/trades/approve` | 批准交易 | approve |
| `/trades/execute` | 执行交易 | execute |

---

## 执行流程

所有交易必须遵循 `preview → approve → execute` 状态机：

```
1. preview:  模拟交易，返回 preview_id
     ↓
2. approve:  人工确认，返回 approval_id
     ↓
3. execute:  签名广播，返回 tx_hash
```

**示例**：

```bash
# Step 1: 预览 swap
python3 scripts/trading/trade_executor.py preview \
  --type swap \
  --from-token USDC \
  --to-token WETH \
  --amount 5 \
  --network base

# 记录返回的 preview_id

# Step 2: 批准
python3 scripts/trading/trade_executor.py approve \
  --preview-id <preview_id>

# 记录返回的 approval_id

# Step 3: 执行
python3 scripts/trading/trade_executor.py execute \
  --approval-id <approval_id>
```

---

## 常见问题

### Q: 签名服务 API 路径不同怎么办？

修改 `config/config.json` 中的 `endpoints` 字段，将路径映射到你的实际 API。

### Q: 签名服务响应格式不同怎么办？

你有两个选择：
1. 在签名服务中实现适配层，转换为规范格式
2. 修改 `scripts/trading/trade_executor.py` 中的响应解析逻辑

### Q: 如何调试？

使用 Safe Vault 模块进行离线调试：

```bash
# 仅生成 calldata，不调用 API
python3 scripts/trading/safe_vault.py preview-deposit \
  --protocol aave \
  --asset USDC \
  --amount 1000
```

### Q: approve 步骤是什么？

`approve` 是状态机中的确认步骤，用于：
- 防止未经确认的交易被执行
- 留出人工/外部系统确认的时间窗口

签名服务实现者可以自定义 approve 的确认机制（控制台确认、硬件钱包、多签等）。

---

## 安全检查清单

在执行交易前，智能体应检查：

- [ ] API 是否可达？
- [ ] 余额是否充足？
- [ ] 是否需要先授权 token？
- [ ] 目标链/协议/代币是否在白名单中？
- [ ] 交易金额是否在限额内？

---

**下一步**: 阅读 [SIGNER_API_SPEC.md](SIGNER_API_SPEC.md) 了解完整的 API 规范。