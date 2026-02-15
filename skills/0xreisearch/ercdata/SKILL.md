---
name: ercdata
description: 使用 ERCData 标准，在以太坊区块链（Base 网络）上存储、验证和管理 AI 数据。当代理需要将数据指纹存储在链上、验证数据完整性、创建审计追踪、管理私有数据的访问控制，或与 ERCData 智能合约交互时，可以使用该标准。支持公共存储和私有存储、EIP-712 验证、快照以及批量操作。
---

# ERCData

在 Base 主网上存储和验证与 AI 相关的数据。数据可以是公开的或私有的，并附带加密完整性证明。

## 快速入门

```bash
# Store public data
uv run {baseDir}/scripts/ercdata-cli.py store \
  --type AI_AGENT_MEMORY \
  --data "memory hash: abc123" \
  --metadata '{"agent":"MyBot","ts":"2026-01-31"}' \
  --key $ERCDATA_KEY --contract $ERCDATA_CONTRACT

# Store private data (only you + granted addresses can read)
uv run {baseDir}/scripts/ercdata-cli.py store \
  --type AI_AGENT_MEMORY \
  --data "secret memory data" \
  --private \
  --key $ERCDATA_KEY --contract $ERCDATA_CONTRACT

# Read entry
uv run {baseDir}/scripts/ercdata-cli.py read --id 1 --key $ERCDATA_KEY --contract $ERCDATA_CONTRACT

# Verify entry (EIP-712 signature check)
uv run {baseDir}/scripts/ercdata-cli.py verify --id 1 --method eip712 --key $ERCDATA_KEY --contract $ERCDATA_CONTRACT

# Grant access to private entry
uv run {baseDir}/scripts/ercdata-cli.py grant-access --id 2 --to 0xSomeAddress --key $ERCDATA_KEY --contract $ERCDATA_CONTRACT
```

## 配置

配置方式如下：
- `ERCDATA_KEY` — 用于签署交易的私钥（写入数据时必需）
- `ERCDATA_CONTRACT` — Base 主网上的合约地址
- `ERCDATA_RPC` — RPC 请求的 URL（默认值：https://mainnet.base.org）

也可以通过 `--key`、`--contract`、`--rpc` 参数进行配置。

## 命令

| 命令 | 功能 |
|---------|-------------|
| `store` | 将数据存储到链上（使用 `--private` 参数可设置访问控制） |
| `read` | 通过 ID 读取数据条目 |
| `verify` | 验证数据完整性（使用 EIP712 或哈希算法） |
| `grant-access` | 授予某个地址读取权限（仅限私有数据） |
| `revoke-access` | 取消读取权限 |
| `register-type` | 注册新的数据类型（仅限管理员操作） |
| `snapshot` | 创建数据快照 |
| `info` | 获取数据条目的信息（不包含完整数据） |

## 隐私模型

- **公开（默认）：** 任何人都可以通过 `getData()` 方法读取数据。适用于透明度和审计追踪。
- **私有（使用 `--private` 参数）：** 仅提供者、被授权的地址和管理员可以读取数据。适用于存储敏感的代理数据。

私有数据条目同样存储在链上，但会限制 `getData()` 方法的访问权限。注意：原始的交易数据仍然可以在链上浏览器中查看。为了最大程度地保护隐私，请在存储前对数据进行加密。

## AI 代理的用例

1. **内存证明** — 定期对 MEMORY.md 文件进行哈希处理并存储，以生成防篡改的审计记录。
2. **代理身份** — 将模型指纹、系统提示信息以及配置数据存储到链上。
3. **可验证的输出** — 对代理的输出结果进行哈希处理并存储，以便后续验证。
4. **代理之间的信任** — 在信任其他代理的数据之前，先检查其 ERCData 条目。
5. **模型来源证明** — 存储模型的哈希值、基准测试分数以及架构元数据。

## API 参考

有关完整的合约 API、角色、事件和限制信息，请参阅 [references/api.md](references/api.md)。

## 系统要求

- Python 3.10 及以上版本，并安装 `web3` 和 `eth-account` 包（由 uv 自动安装）。
- 在 Base 主网上拥有一个已充值的钱包（需要 ETH 作为交易手续费）。
- 必须由合约管理员授予 `PROVIDER_ROLE` 权限才能存储数据。
- 必须由管理员授予 `VERIFIER_ROLE` 权限才能执行数据验证操作。