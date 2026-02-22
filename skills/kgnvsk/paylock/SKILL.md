---
name: paylock
description: 通过 OpenClaw 的 PayLock API，可以创建、资助、执行、验证以及追踪 SOL 代管（escrow）合约。
---
# PayLock 技能

使用此技能可以通过本地/公共 REST API 直接管理 PayLock 代管合同。

- **本地 API:** `http://localhost:8767`
- **公共 API:** `https://engaging-fill-smoking-accepting.trycloudflare.com`
- **PayLock SOL 钱包:** `HxEFMJYCmCngcHK6CbadhYWSZCbpXUJ2t7Ze8sk9CP4z`
- **费用:** **标准费用：3%**, **创始费用：1.5%**（前 10 名客户）

## 该技能支持的功能

1. 创建合同 → `POST /contract`
2. 资金注入合同 → `POST /fund`
3. 提交工作成果 → `POST /{id}/deliver`
4. 验证工作成果 → `POST /{id}/verify`
5. 检查合同状态 → `GET /contract/{id}`
6. 列出所有合同 → `GET /contracts`

## 脚本

所有相关脚本位于 `scripts/` 目录下：

- `paylock.py`（包含子命令的统一命令行界面）
- `create_contract.py`
- `fund_contract.py`
- `deliver_contract.py`
- `verify_contract.py`
- `get_contract.py`
- `list_contracts.py`
- `paylock_api.py`（用于调用公共 API 的客户端）

无需使用任何第三方 Python 包（仅使用标准库）。

---

## 快速入门

### 统一命令行界面

```bash
python3 skills/paylock/scripts/paylock.py list
```

**或** 显式使用公共 API：**

```bash
python3 skills/paylock/scripts/paylock.py --api https://engaging-fill-smoking-accepting.trycloudflare.com list
```

**或** 设置一次环境变量：**

```bash
export PAYLOCK_API_BASE=http://localhost:8767
```

### 创建合同

```bash
python3 skills/paylock/scripts/paylock.py create \
  --payer "agent-alpha" \
  --payee "agent-beta" \
  --amount 1.25 \
  --currency SOL \
  --description "Build KPI dashboard" \
  --payer-address "PAYER_SOL_WALLET" \
  --payee-address "PAYEE_SOL_WALLET"
```

### 资金注入合同

```bash
python3 skills/paylock/scripts/paylock.py fund \
  --contract-id "ctr_123" \
  --tx-hash "5j3...solana_tx_hash"
```

### 提交工作成果

```bash
python3 skills/paylock/scripts/paylock.py deliver \
  --id "ctr_123" \
  --delivery-payload "https://example.com/deliverable.zip" \
  --delivery-hash "sha256:abc123..." \
  --payee-token "PAYEE_SECRET_TOKEN"
```

### 验证工作成果

```bash
python3 skills/paylock/scripts/paylock.py verify \
  --id "ctr_123" \
  --payer-token "PAYER_SECRET_TOKEN"
```

### 检查单个合同的状态

```bash
python3 skills/paylock/scripts/paylock.py status --id "ctr_123"
```

### 列出所有合同

```bash
python3 skills/paylock/scripts/paylock.py list
```

---

## 相应的脚本命令

```bash
python3 skills/paylock/scripts/create_contract.py --help
python3 skills/paylock/scripts/fund_contract.py --help
python3 skills/paylock/scripts/deliver_contract.py --help
python3 skills/paylock/scripts/verify_contract.py --help
python3 skills/paylock/scripts/get_contract.py --help
python3 skills/paylock/scripts/list_contracts.py --help
```

---

## 代理使用流程（聊天工作流程）

当代理被要求执行代管操作时：

1. 使用付款人/收款人/金额/描述信息创建合同。
2. 要求付款人转账 SOL 并提供交易哈希。
3. 使用 `contract_id + tx_hash` 为合同注入资金。
4. 工作完成后，提交工作成果（包含相关数据/哈希/令牌）。
5. 付款人使用令牌验证工作成果。
6. 通过 `Status` 和 `List` 命令监控/报告合同状态。

这为任何 OpenClaw 代理提供了完整的聊天原生代管流程。

---

## ClawHub 打包说明

此技能已准备好进行 ClawHub 风格的打包：

- 顶层文件 `SKILL.md` 包含元数据
- 所有脚本均位于 `scripts/` 目录下，可独立运行
- 无外部 Python 依赖项
- 可通过 `--api` 或 `PAYLOCK_API_BASE` 参数配置 API 端点

如果需要发布到平台，请在此文件夹中添加或更新 `_meta.json` 文件。