---
name: quantum-bridge
description: 在 Qiskit（OpenQASM）和 OriginIR 之间转换量子电路；运行 IBC（Inter-Blockchain Communication）多智能体共识协议；验证 OriginIR 的正确性；并通过 Quantum Bridge API 将量子电路提交到实际的量子硬件设备（Wukong 72Q 芯片）上。该功能适用于用户需要转换量子电路、执行量子共识操作、将电路提交到量子硬件设备、检查量子后端系统，或处理 OriginIR/OpenQASM 格式的文件时使用。
---
# 量子桥（Quantum Bridge）

量子桥（Quantum Bridge）允许在不同的量子计算框架之间转换量子电路，并通过 `quantum-api.gpupulse.dev` 上的 Quantum Bridge API 将这些电路在真实的量子硬件上运行。

## 设置（Setup）

需要一个 API 密钥。您可以在 [https://quantum-api.gpupulse.dev](https://quantum-api.gpupulse.dev) 免费获取一个 API 密钥（包含 50 个信用点）。请将密钥存储在适当的位置：

```bash
# In your TOOLS.md or env
QUANTUM_BRIDGE_KEY=qb_...
```

## API 参考（API Reference）

基础 URL：`https://quantum-api.gpupulse.dev/api/v1`
认证方式：`Authorization: Bearer qb_...` 或 `X-API-Key: qb_...`

### 将 QASM 代码转换为 OriginIR 代码（1 个信用点）

```bash
curl -X POST "$BASE/transpile" \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d '{"qasm": "OPENQASM 2.0;\ninclude \"qelib1.inc\";\nqreg q[2];\ncreg c[2];\nh q[0];\ncx q[0],q[1];\nmeasure q[0] -> c[0];\nmeasure q[1] -> c[1];"}'
```

响应格式：
```json
{"originir": "QINIT 2\nCREG 2\nH q[0]\nCNOT q[0], q[1]\n...", "stats": {...}, "credits_charged": 1}
```

### 将 OriginIR 代码转换回 QASM 代码（1 个信用点）

```bash
curl -X POST "$BASE/reverse" \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d '{"originir": "QINIT 2\nCREG 2\nH q[0]\nCNOT q[0], q[1]"}'
```

### 验证 OriginIR 代码（免费）

```bash
curl -X POST "$BASE/validate" \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d '{"originir": "QINIT 2\nH q[0]\nCNOT q[0], q[1]"}'
```

### IBC 共识机制（IBC Consensus，2 个信用点）

这是一种多代理量子共识机制。每个代理都有一个名称和特征向量。

```bash
curl -X POST "$BASE/consensus" \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d '{"agents": [
    {"name": "Scheduler", "features": [0.9, 0.1, 0.3]},
    {"name": "Optimizer", "features": [0.1, 0.9, 0.2]},
    {"name": "Monitor",   "features": [0.7, 0.3, 0.5]}
  ], "threshold": 0.3}'
```

响应内容包括共识结果、冲突情况、相似性矩阵以及量子计算的时序信息。

### 将量子电路提交到硬件（5–10 个信用点）

可以选择将电路提交到云模拟器（5 个信用点）或真实的 Wukong 72 量子比特芯片（10 个信用点）上执行。

```bash
curl -X POST "$BASE/submit" \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d '{"qasm": "OPENQASM 2.0;...", "backend": "wukong", "shots": 1000}'
```

响应格式：
```json
{"task_id": "task_...", "status": "queued", "poll_url": "/api/v1/submit/task_..."
```

可以通过 `/api/v1/submit/task_...` 获取任务执行进度。

### 查看任务结果（免费）

```bash
curl "$BASE/submit/task_..." -H "Authorization: Bearer $KEY"
```

### 检查账户余额（免费）

```bash
curl "$BASE/balance" -H "Authorization: Bearer $KEY"
```

### 列出可用的后端（需要认证）

```bash
curl "$BASE/backends" -H "Authorization: Bearer $KEY"
```

### 支持的量子门（无需认证）

```bash
curl "$BASE/gates"
```

## 支持的量子门

支持 20 多种量子门的转换：
- H (Hadamard)
- X (XOR)
- Y (YOR)
- Z (ZOR)
- S (SNOT)
- T (TNOT)
- I (Identity)
- RX (RNOT)
- RY (RYNOT)
- RZ (RZNOT)
- U2 (U2)
- U3 (U3)
- CNOT (CNOT)
- CZ (CNOT)
- SWAP (SWAP)
- CR (CNOT)
- Toffoli (Toffoli)
- CSWAP (CSWAP)
- DAGGER (Dagger)
- BARRIER (Barrier)
- MEASURE (Measure)

## 使用模式（Usage Patterns）

**为用户转换量子电路：**
1. 获取用户的 QASM 代码输入。
2. 向 `/transpile` 端点发送 POST 请求。
3. 接收转换后的 OriginIR 代码和相关的统计信息。

**在真实量子硬件上运行电路：**
1. 向 `/submit` 端点发送 POST 请求，并指定后端为 `wukong`。
2. 获取任务 ID (`task_id`)。
3. 定期访问 `/submit/<task_id>` 查看任务进度，直到状态变为 `completed`。
4. 获取量子计算的测量结果。

**多代理共识：**
1. 收集所有代理的名称和特征向量。
2. 向 `/consensus` 端点发送 POST 请求。
3. 获取共识结果（包括共识组、冲突情况以及各代理之间的相似性得分）。

## 信用点费用（Credit Costs）

| 端点 | 所需信用点 |
|--------|---------|
| transpile | 1       |
| reverse | 1       |
| validate | 0       |
| consensus | 2       |
| submit (simulator) | 5       |
| submit (wukong) | 10       |

## 定价方案（Pricing）

- 免费账户：50 个信用点
- 入门级账户：500 个信用点 — 5 美元（USDC）
- 专业级账户：5,000 个信用点 — 25 美元（USDC）
- 企业级账户：50,000 个信用点 — 100 美元（USDC）

支付方式：使用 Solana 上的 USDC（详情请联系我们）。