---
name: OpenExec
slug: openexec
version: 0.1.10
category: infrastructure/governance/execution
runtime: python
entrypoint: main:app
requires_network: false  # No outbound HTTP/RPC calls during execution. Inbound HTTP only.
modes:
  - demo
  - clawshield
env:
  required: none
  optional:
    - OPENEXEC_MODE
    - CLAWSHIELD_PUBLIC_KEY
    - CLAWSHIELD_TENANT_ID
    - OPENEXEC_ALLOWED_ACTIONS
    - OPENEXEC_DB_URL
description: 这是一个基于源代码分发的确定性执行服务，具有固定的依赖关系（即依赖项在编译时就已经确定）。该服务仅能在经过签名验证的批准文件（ClawShield模式）的驱动下运行，并会生成可验证的执行记录。该服务不会发起任何出站HTTP请求或治理相关的操作；同时，也不会在运行时安装任何软件包或进行动态下载。
---
# OpenExec — 受管控的确定性执行服务（技能）

OpenExec 是一个可运行的、受管控的执行服务。它**仅**执行那些已经获得批准的操作。

它既不是代理程序，也不是策略引擎，也不会自行授权。

在签名验证或执行过程中，OpenExec **不会**进行任何出站 HTTP 请求、RPC 调用或治理操作。所有验证过程都是完全离线的。默认情况下，OpenExec 使用本地的 SQLite 数据库（`sqlite:///openexec.db`）；只有当操作员通过 `OPENEXEC_DB_URL` 明确配置时，才会进行数据库的网络 I/O 操作。

---

## 安装

```bash
pip install -r requirements.txt
```

## 在本地运行

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 5000
```

---

## 端点

* `GET /` → 服务信息（部署健康检查）
* `GET /health` → 健康状态、运行模式、限制级别
* `GET /ready` → 准备就绪状态检查
* `GET /version` → 版本元数据
* `POST /execute` → 确定性执行已批准的操作
* `POST /receipts/verify` → 验证收据哈希的完整性

---

## 运行模式

### 1) 示范模式（默认模式，免费）

无需外部管控机制，也不需要环境变量。

**示范模式仍然遵循以下规则：**
- 确定性执行
- 防止重放（确保每个操作的唯一性）
- 生成收据

---

### 2) ClawShield 模式（生产/业务模式）

需要由 ClawShield 发行的**已签名批准文件**。OpenExec 会使用配置的公钥离线验证 Ed25519 签名。

**如果签名验证失败，执行将被拒绝。**

> 注意：ClawShield 的治理服务可通过 [https://clawshield.forgerun.ai/](https://clawshield.forgerun.ai/) 获取。OpenExec 在运行时不会访问该链接，仅用于参考。

---

## 环境变量

所有环境变量都是**可选的**。在示范模式下，OpenExec 可以在没有任何配置的情况下运行。

| 变量 | 默认值 | 说明 |
|----------|---------|-------------|
| `OPENEXEC_MODE` | `demo` | 执行模式：`demo` 或 `clawshield` |
| `CLAWSHIELD_PUBLIC_KEY` | （无） | 用于签名验证的 PEM 编码的 Ed25519 公钥 |
| `CLAWSHIELD_TENANT_ID` | （无） | 多租户隔离的租户标识符 |
| `OPENEXEC_ALLOWED Actions` | （无） | 允许执行的操作列表（以逗号分隔）。如果未设置，则允许所有注册的操作 |
| `OPENEXEC_DB_URL` | `sqlite:///openexec.db` | 用于存储执行记录的数据库 URL |

---

## 90 秒快速入门（示范模式）

1. 启动服务器：

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 5000
```

2. 检查服务健康状况：

```bash
curl http://localhost:5000/health
```

3. 执行一个示范性操作：

```bash
curl -X POST http://localhost:5000/execute \
  -H "Content-Type: application/json" \
  -d '{
    "action":"echo",
    "payload":{"msg":"hello"},
    "nonce":"unique-1"
  }'
```

4. 尝试重放操作（结果相同，不会重新执行）：

```bash
curl -X POST http://localhost:5000/execute \
  -H "Content-Type: application/json" \
  -d '{
    "action":"echo",
    "payload":{"msg":"hello"},
    "nonce":"unique-1"
  }'
```

---

## 收据

每次执行都会生成一个收据哈希。收据是**证据**，而非日志。

**验证收据的方法：**

```bash
curl -X POST http://localhost:5000/receipts/verify \
  -H "Content-Type: application/json" \
  -d '{"exec_id":"<id>","result":"<result_json>","receipt":"<hash>"}'
```

---

## 该技能的功能

- 接受结构化的执行请求
- 强制执行已批准的操作
- 对每次执行生成可验证的收据
- 在 ClawShield 模式下：在执行前验证已签名的批准文件
- 支持通过环境变量设置允许执行的操作列表

## 该技能不支持的功能

- 定义策略
- 授予权限
- 自主做出决策
- 无视治理决定
- 在执行过程中进行出站 HTTP 请求或治理操作
- 提供操作系统级别的沙箱环境或容器隔离

---

## 安全边界说明

OpenExec 在应用层强制执行执行边界，不提供操作系统级别的沙箱保护。在将 OpenExec 部署到容器化环境、虚拟机隔离环境或强化安全性的环境中时，应确保操作不会影响到生产系统。

OpenExec 实现了权限分离机制，但它本身并不构成一个沙箱环境。

---

## 架构概述（三层分离）

* **OpenExec** — 确定性执行适配器
* **ClawShield** — 管理与批准流程（SaaS 服务）：[https://clawshield.forgerun.ai/](https://clawshield.forgerun.ai/)
* **ClawLedger** — 监证账本（可选集成）

各层都是可替换的，任何一层都无法独立运行。

---

## 安全文档

完整的 security 模型、威胁假设以及生产环境强化检查指南请参阅 [SECURITY.md](SECURITY.md)。

该技能的设计目的是将以下功能分离：
- 执行逻辑的管控（由 OpenExec 负责）
- 基础设施的隔离（由操作员负责）

### 执行安全性保障

OpenExec：
- 不会动态加载代码
- 不会将用户输入视为代码进行评估
- 使用静态的处理程序注册表
- 不会在运行时安装软件包
- 不会从远程获取执行逻辑