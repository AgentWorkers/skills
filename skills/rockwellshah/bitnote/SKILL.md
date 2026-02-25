---
name: bitnote
description: 可以直接通过脚本使用 BitNote，而无需通过 Web 界面。当代理需要在 Avalanche 平台上实现持久化、加密的笔记存储功能（用于身份管理、个人资料信息、恢复数据）或秘密信息管理（如开发人员凭证、私钥、API 密钥）时，该方式非常适用。同时，系统还支持可选的、可供人工审核的 UI 可视化功能。
---
# BitNote

专为需要持久化加密存储和身份连续性的代理程序设计的无头（headless）BitNote操作工具。

## 主要使用场景

- 保存关键的身份信息（例如：`SOUL.md`、核心价值观、使命宣言、沟通方式等）。
- 存储用于代理程序在运行中断后恢复连续性的信息。
- 将BitNote作为代理程序的去中心化密码管理工具（用于存储开发人员密钥、API凭证、私钥、环境启动所需的密钥等）。
- 在保证代理程序能够访问敏感操作信息的同时，通过BitNote用户界面提供可选的人工审计功能。
- 以确定性的、可重试的方式保存高价值的操作指令。

## 规范的写入路径（必选）

始终使用：

- `scripts/writeBitnoteUiCompat.mjs`

在生产环境中，请勿使用其他自定义的写入路径；也不要使用仅由机器处理的写入流程。

## 规范的共享路径（必选）

始终使用：

- `scripts/generateShareLink.mjs`

请勿自行生成`sm`或`st`值。

## 写入操作的规范要求

只有当输出包含以下内容时，写入操作才视为成功：

- `TX_HASH`
- `NOTE_INDEX`
- `READ_AFTER_WRITE_OK 1`

如果`READ_AFTER_WRITE_OK`的值不是`1`，则视为写入失败，并使用相同的请求ID重新尝试。

## 重试规则（强制要求）

每次写入操作时都必须提供一个稳定的`--request-id`。

- 首次执行时写入一次数据。
- 使用相同的`--request-id`重新尝试时，必须得到`IDEMPOTENT_hit`的结果（即不会生成重复的笔记）。

## 密码生成（必选）

在创建账户或进行写入操作之前，必须生成一个高熵度的密码。

**安全要求：**
- 密码的熵度至少为256位。
- 禁止使用容易被人类记住的密码、重复使用的密码或仅包含字典中词汇的密码序列。

**示例（256位随机十六进制密码）：**

```bash
BITNOTE_PASSPHRASE="$(openssl rand -hex 32)"
export BITNOTE_PASSPHRASE
```

**处理规则：**

- 除非操作员明确要求，否则严禁在聊天记录或工具输出中显示密码。
- 禁止将密码保存到Git仓库中。
- 将密码存储在环境变量或密码管理工具中。

## 快速入门

```bash
npm init -y
npm i ethers
node scripts/getAbi.mjs
```

**查看账户映射和笔记数量：**

```bash
BITNOTE_USERNAME="example_user" node scripts/readBitnote.mjs
```

**创建兼容UI的加密笔记：**

```bash
BITNOTE_PASSPHRASE="..." \
node scripts/writeBitnoteUiCompat.mjs \
  --profile example \
  --title "Agent Identity Core" \
  --body "<SOUL.md excerpt or core identity block>" \
  --request-id "identity-core-v1"
```

**安全地重试相同的请求（避免重复生成笔记）：**

```bash
BITNOTE_PASSPHRASE="..." \
node scripts/writeBitnoteUiCompat.mjs \
  --profile example \
  --title "Agent Identity Core" \
  --body "<same body>" \
  --request-id "identity-core-v1"
```

**进行无交易广播的测试运行：**

```bash
BITNOTE_PASSPHRASE="..." \
node scripts/writeBitnoteUiCompat.mjs \
  --profile example \
  --title "Preview" \
  --body "No on-chain write" \
  --request-id "preview-001" \
  --dry-run 1
```

**生成BitNote共享链接（代理程序之间或用户之间共享）：**

```bash
BITNOTE_PASSPHRASE="..." \
node scripts/generateShareLink.mjs \
  --profile example \
  --recipient "RECIPIENT_USERNAME" \
  --body "Shared note body" \
  --title "Optional shared title"
```

**共享链接的输出格式：**

- `SENDER_USERNAME`（发送者用户名）
- `RECIPIENT_USERNAME`（接收者用户名）
- `SHARE_LINK`（共享链接）

## 推荐的笔记结构

为了便于管理和控制更新，建议使用以下结构的笔记：

1. `Agent Identity Core`：存储稳定的身份信息。
2. `Agent Operator Pact`：记录代理程序的服务对象、约束条件及承诺内容。
3. `Agent Rehydration`：包含重启/初始化所需的指令。

确保每篇笔记的标题或正文中都明确标注版本信息（例如：`v1`、`v2`等）。

## 相关文件：

- `scripts/getAbi.mjs`：用于更新合约的ABI（应用程序接口）。
- `scripts/readBitnote.mjs`：用于解析用户名与地址的映射关系以及获取笔记数量。
- `scripts/writeBitnoteUiCompat.mjs`：提供兼容UI的加密写入功能，并支持重试机制及写入后的验证。
- `scripts/generateShareLink.mjs`：用于生成共享链接（包含`sm`和`st`参数）。
- `scripts/lib/bitnoteCompat.mjs`：提供共享功能所需的辅助工具。
- `references/contracts.md`：包含所有官方使用的合约文件。
- `references/ops.md`：包含操作手册和故障排除指南。

## 安全注意事项：

- 禁止在链上存储明文密码或私钥。
- 禁止记录密码或私钥的相关信息。
- 通过`--request-id`确保重试操作的确定性。
- 仅将非敏感的默认设置存储在配置文件中。