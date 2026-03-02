---
name: web5-cli
description: >
  **使用说明：**  
  当使用 Web5 CLI 工具进行去中心化身份管理（Decentralized Identity, DID）、CKB 钱包操作、DID 管理以及 PDS 数据操作时，请参考以下说明。
---
# Web5 CLI

## 概述
Web5 CLI 是一个用于与 Web5 基础设施交互的命令行工具。它提供了密钥管理、CKB 钱包操作、DID（去中心化身份）生命周期管理以及 PDS（个人数据存储）交互等功能。

## 安装
```bash
npm install -g web5-cli
```

## 命令

| 命令 | 功能 | 子命令 |
|---------|---------|-----------------|
| `keystore` | DID 签名密钥管理 | new, import, clean, get, sign, verify |
| `wallet` | CKB 钱包操作 | new, import, clean, get, send-tx, check-tx, balance |
| `did` | CKB 上的 DID 生命周期管理 | build-create-tx, build-destroy-tx, build-update-didkey-tx, build-update-handle-tx, build-transfer-tx, list |
| `pds` | PDS 服务器交互 | check-username, get-did-by-username, create-account, delete-account, login, write, repo, records, blobs, export, import |

## 快速参考

### 密钥管理
```bash
web5-cli keystore new                                    # Create new keypair
web5-cli keystore import --sk <hex>                      # Import private key
web5-cli keystore get                                    # Get DID key
web5-cli keystore sign --message <hex>                   # Sign message
web5-cli keystore verify --message <hex> --signature <hex>  # Verify signature
```

### 钱包操作
```bash
web5-cli wallet new                                      # Create CKB wallet
web5-cli wallet import --sk <hex>                        # Import wallet
web5-cli wallet get                                      # Get CKB address
web5-cli wallet balance                                  # Check balance
web5-cli wallet send-tx --tx-path <path>                 # Send transaction
web5-cli wallet check-tx --tx-hash <hash>                # Check tx status
```

### DID 管理
```bash
web5-cli did build-create-tx --username <name> --pds <url> --didkey <key> --output-path <path>
web5-cli did build-destroy-tx --args <args> --output-path <path>
web5-cli did build-update-didkey-tx --args <args> --new-didkey <key> --output-path <path>
web5-cli did list --ckb-addr <address>                   # List DID cells
```

### PDS 操作
```bash
web5-cli pds check-username --username <name>
web5-cli pds get-did-by-username --username <name>
web5-cli pds create-account --pds <url> --username <name> --didkey <key> --did <did> --ckb-address <addr>
web5-cli pds login --pds <url> --didkey <key> --did <did> --ckb-address <addr>
web5-cli pds write --pds <url> --accessJwt <jwt> --didkey <key> --did <did> --rkey <key> --data <json>
web5-cli pds repo --pds <url> --did <did>
web5-cli pds records --pds <url> --did <did> --collection <nsid> [--limit N] [--cursor <cursor>]
web5-cli pds export --pds <url> --did <did> --data-file <path> [--since <cid>]
web5-cli pds import --pds <url> --did <did> --accessJwt <jwt> --data-file <path>
```

## 配置

- **密钥库（Keystore）**：私钥存储在 `~/.web5-cli/signkey` 文件中
- **钱包（Wallet）**：私钥存储在 `~/.web5-cli/ckb-sk` 文件中
- **网络（Network）**：通过 `CKB_NETWORK` 环境变量设置（`ckb_testnet` 或 `ckb`）

## 输出格式
所有命令的输出均为 JSON 格式，便于 AI 代理和脚本解析。

## 常见工作流程

### 创建账户
1. `web5-cli keystore new` - 创建签名密钥
2. `web5-cli wallet new` - 创建 CKB 钱包（需要超过 450 个测试网 CKB）
3. `web5-cli did build-create-tx ...` - 构建 DID 创建交易
4. `web5-cli wallet send-tx --tx-path <tx-file>` - 提交交易
5. `web5-cli wallet check-tx --tx-hash <hash>` - 确认交易已提交
6. 等待 30 秒
7. `web5-cli pds create-account ...` - 创建 PDS 账户

### 写入数据
1. `web5-cli pds login ...` - 获取访问令牌
2. `web5-cli pds write ...` - 使用访问令牌写入数据

## 安全注意事项
- 由于这是一个用于技术验证的工具，私钥以明文形式存储
- 请勿在生产环境中使用
- 这是一个用于 AI 代理驱动的 Web5 交互的概念验证方案

## 其他说明
- `--pds` 参数后面不需要添加 `https://` 前缀，只需提供主机名
- 每个账户只能属于一个 PDS

## 公共信息
可用的 PDS 地址：
- `web5.bbsfans.dev`
- `web5.ccfdao.dev`

可写入 PDS 的数据结构包括：
- 用户资料
- BBS 的帖子
- BBS 的评论
- BBS 的点赞
- BBS 的回复
- DAO 的回复
- DAO 的提案
- DAO 的点赞

```
{
  $type: 'app.dao.reply'
  proposal: string    // 提案的uri
  to?: string   // 对方did（可选，有就是回复某人）
  text: string  // 评论内容
  parent?: string  // 父评论的uri（可选，用于回复评论）
}
```