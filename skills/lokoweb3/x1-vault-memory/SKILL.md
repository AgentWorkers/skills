---
name: x1-vault-memory
description: 将 OpenClaw 代理的内存数据备份到 IPFS，并使用 AES-256-GCM 加密算法进行加密；同时，将加密后的数据通过 X1 区块链的 CID（Content Identifier）进行锚定（即存储在区块链上以确保数据的安全性和可追溯性）。
version: 1.1.0
author: Lokoweb3
homepage: https://github.com/Lokoweb3/x1-vault-memory
metadata:
  clawdbot:
    emoji: "🦞"
requires:
  env: ["PINATA_JWT", "X1_RPC_URL"]
  primaryEnv: "PINATA_JWT"
files: ["src/*"]
tags:
  - backup
  - memory
  - ipfs
  - encryption
  - x1
  - blockchain
  - restore
  - vault
---
# X1 Vault Memory

这是一个为 OpenClaw 代理提供的加密、去中心化的记忆备份服务，基于 IPFS 和 X1 区块链技术实现。

## 功能概述

该服务使用 AES-256-GCM 军用级加密算法备份代理的配置信息（包括身份、个性特征和记忆数据），并将备份文件存储在 IPFS 上，同时将文件的唯一标识符（CID）锚定到 X1 区块链上。只有用户的钱包密钥对才能解密这些数据。

**备份流程：**  
代理文件 → tar.gz 压缩 → AES-256-GCM 加密 → 上传至 IPFS → 在 X1 区块链上永久存储。

### 设计目的

传统服务器可能发生故障，容器也可能被意外删除；简单的删除操作（如 `rm -rf`）可能导致代理数据丢失。X1 Vault Memory 通过加密、去中心化的存储方式，确保代理数据的安全性和可恢复性。

### 主要特点：

- **加密方式：** AES-256-GCM，使用用户的钱包密钥对进行加密，确保只有用户能够解密数据。
- **存储平台：** 数据存储在去中心化的 IPFS 网络上，而非单一服务器上。
- **区块链记录：** 每个备份的 CID 都会被记录在区块链上，提供永久且可验证的存储证明。
- **一键恢复：** 通过一个命令即可下载、解密并恢复所有代理文件。
- **低成本：** 每年仅需约 0.03 美元即可完成日常备份。

### v1.1.0 的新功能：

- **数据完整性验证：** 对备份和恢复过程添加了 SHA-256 校验。
- **选择性恢复：** 支持使用 `--only` 标志仅恢复特定文件或目录。
- **备份列表：** 提供查看所有备份的列表功能，并支持基于版本号的恢复。
- **自动恢复机制：** 在检测到数据损坏时，系统会自动触发恢复操作。

## 使用要求：

- **Pinata 账户：** 需要在 https://app.pinata.cloud 注册账户（免费，提供 500 个文件和 1GB 存储空间）。
- **Solana CLI：** 用于创建和管理钱包。
- **Solana/X1 钱包：** 需要用户的钱包密钥对 JSON 文件（可免费生成）。
- **XNT 代币：** 每次备份需要支付约 0.002 XNT 的交易费用。

### 获取 XNT 代币的方法：

XNT 是 X1 区块链的原生代币，用于支付区块链交易费用：

1. **通过 Solana 桥接器：** 最简单的方式（https://app.bridge.x1.xyz），将 SOL/USDC 代币转换为 XNT，然后在 XDEX 上进行交易。
2. **直接在 XDEX 上交易：** 访问 https://app.xdex.xyz/swap 进行交易。
3. **场外交易：** 对于较大金额的交易，可以选择 OTC 方式（https://otc.xonedex.xyz）。
4. **使用交易机器人：** 可通过 Telegram 机器人 Honey Badger Bot （https://t.me/HoneyBadgerCoreBot?start=ref_HEBCU2E3）快速完成交易。

**注意：** 使用该服务前，请确保已安装 X1 钱包的 Chrome 扩展程序（https://chromewebstore.google.com/detail/x1-wallet/kcfmcpdmlchhbikbogddmgopmjbflnae）。

### 如何设置 Pinata 和获取 JWT 代币：

**Pinata：** 是用于存储加密备份的 IPFS 服务。免费账户即可满足大部分需求。

1. 访问 https://app.pinata.cloud 并注册新账户。
2. 使用电子邮件或 GitHub/Google 登录。
3. 登录后，点击右上角的个人资料图标。
4. 从下拉菜单中选择 “API Keys”。
5. 点击 “New Key” 按钮创建新密钥。
6. 仅启用 “pinFileToIPFS” 权限（无需管理员权限）。
7. 为密钥命名（例如 “x1-vault-memory”）。
7. 点击 “Create Key” 生成密钥。
8. 生成的密钥包括 API Key、API Secret 和 JWT；请妥善保存 JWT（即 `PINATA_JWT`）。
9. 免费账户提供 500 个文件和 1GB 的存储空间；每个加密备份文件大小约为 10-50KB，因此可以存储大量备份文件而无需额外付费。

### 设置环境变量：

- **安装 Solana CLI：** （请参考相应的代码块进行安装。）
- **配置环境变量：** 需要设置两个环境变量：`PINATA_JWT` 和 `X1_RPC_URL`。
  - **选项 A（推荐用于 Docker 和生产环境）：** 在项目根目录下创建 `.env` 文件。
  - **选项 B（适用于手动或一次性使用）：** 在 shell 环境中设置这些变量。
  - **选项 C（Docker Compose 环境）：** 在 `docker-compose.yml` 文件中配置这些变量。

### 创建钱包密钥对：

请妥善保管 `wallet.json` 文件，因为其中包含你的加密密钥和钱包信息，切勿将其上传至 GitHub。

### 为钱包充值：

获取钱包地址后，向该地址发送 XNT 代币（每次备份费用约为 0.002 XNT）。

### 配置默认网络：

将 X1 主网设置为默认网络。

## 使用方法：

- **备份：** 加密并上传 `IDENTITY.md`、`SOUL.md`、`USER.md`、`TOOLS.md` 及 `memory/` 目录中的文件；将 CID 记录到 X1 区块链，并在 `vault-log.json` 中记录备份信息。
- **恢复：** 从 IPFS 下载文件，使用钱包密钥解密并恢复所有代理文件。
- **选择性恢复：** 仅恢复特定的文件或目录。
- **查看所有备份：** 查看所有备份文件，包括时间戳、CID 和校验和信息，支持基于版本号的恢复。
- **自动检查：** 定期检查代理文件完整性；如果关键文件丢失或损坏，系统会自动从最新备份中恢复数据。
- **测试备份：** 可查看哪些文件会被备份，而无需实际上传或支付费用。

## 错误处理：

- **Pinata 服务不可用：** 备份会因连接错误失败；请稍后重试，本地文件不会受到影响。
- **X1 RPC 失败：** IPFS 上传成功但区块链锚定失败；CID 仍会记录在 `vault-log.json` 中；RPC 恢复后重新进行锚定。
- **钱包无效：** 加密失败；请检查 `wallet.json` 的路径和格式（必须是 JSON 格式的字节数组）。
- **XNT 不足：** 交易被拒绝；请为钱包充值更多代币。
- **恢复失败：** 请检查 Pinata 服务状态；如有需要，重新进行锚定操作。
- **Solana CLI 未安装：** 请按照步骤 1 安装 Solana CLI 并确保 PATH 环境变量设置正确。
- **校验和不一致：** 备份可能损坏；尝试使用 `list.js` 从先前版本恢复数据。

## 数据存储位置：

- **IPFS：** 加密后的文件存储在 Pinata 的 IPFS 网络上。
- **X1 区块链：** 备份文件的 CID 被记录在区块链上，确保数据永久性和可验证性。
- **`vault-log.json`：** 存储所有备份的 CID、时间戳和校验和信息。
- **仅用户钱包密钥对可解密数据。**

## 安全性措施：

- **加密方式：** 使用用户的钱包密钥进行 AES-256-GCM 加密。
- **数据完整性：** 每次备份和恢复操作都会进行 SHA-256 校验。
- **访问控制：** 仅用户密钥对可解密数据；即使他人获取了 CID，数据也不会被泄露。
- **数据存储：** 数据存储在去中心化的 IPFS 上，而非单一服务器。
- **区块链记录：** CID 被锚定在 X1 区块链上，防止数据被篡改。
- **注意事项：** 请勿分享 `wallet.json` 或 `PINATA_JWT`。

## 自动化设置：

- **每周自动备份：** 通过 cron 任务自动执行备份。
- **定期检查：** 每 6 小时自动检查代理文件完整性。

## 备份的文件内容：

- `IDENTITY.md`：代理的名称、个性特征等信息。
- `SOUL.md`：代理的个性特征、使用说明和专业知识。
- `USER.md`：用户个人资料和偏好设置。
- `TOOLS.md`：与环境相关的笔记。
- `memory/*.md`：每日记忆日志。

## 技术栈：

- **加密算法：** AES-256-GCM（认证加密）。
- **数据完整性：** 使用 SHA-256 校验和。
- **存储平台：** IPFS（通过 Pinata API 和 JWT 进行访问控制）。
- **区块链：** X1 主网（兼容 SVM 的 L1 层）。
- **钱包工具：** Solana CLI 和 @solana/web3.js。
- **运行环境：** Node.js v18+。

## 相关链接：

- **GitHub 项目：** https://github.com/Lokoweb3/x1-vault-memory
- **X1 探索器：** https://explorer.mainnet.x1.xyz
- **X1 桥接器：** https://app.bridge.x1.xyz
- **XDEX：** https://app.xdex.xyz/swap
- **X1 钱包：** https://chromewebstore.google.com/detail/x1-wallet/kcfmcpdmlchhbikbogddmgopmjbflnae
- **交易机器人：** Honey Badger Bot（https://t.me/HoneyBadgerCoreBot?start=ref_HEBCU2E3）
- **Pinata：** https://app.pinata.cloud
- **Solana CLI：** https://docs.anza.xyz/cli/install

由 Lokoweb3 开发。