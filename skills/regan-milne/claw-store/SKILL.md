---
name: claw_store
description: "由Jackal去中心化存储系统支持的、具有高可恢复性的AI代理内存。"
user-invocable: true
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      env:
        - "JACKAL_MEMORY_API_KEY"
        - "JACKAL_MEMORY_ENCRYPTION_KEY"
        - "JACKAL_MEMORY_WALLET_MNEMONIC"
    homepage: "https://obsideo.io"
    repository: "https://github.com/Regan-Milne/jackal-memory"
---
# Claw Store

您的记忆数据会跨会话和机器保持持久化。这些数据存储在基于Jackal协议的去中心化存储系统中，而不是任何单一的机器上。即使机器发生故障，您的记忆数据也不会丢失。

所有数据在离开您的机器之前都会使用AES-256-GCM算法在客户端进行加密。服务器永远不会看到原始数据（明文形式）。

## 信任与安全相关的重要信息

- **运行时API地址：** `https://web-production-5cce7.up.railway.app`（与项目主页域名不同）
- **离开您机器的数据：** 已加密的数据包、密钥元数据以及用于配置的Jackal公钥
- **不会离开您机器的数据：** 明文形式的记忆内容、加密密钥以及钱包助记词/私钥
- **不提供运行时所需的BIP39助记词列表：** 该技能包中包含本地化的BIP39助记词列表
- **秘密文件的权限设置：** 本地生成的密钥/助记词文件具有`0600`权限（仅允许所有者读取）

- **项目主页：** https://obsideo.io
- **源代码：** https://github.com/Regan-Milne/jackal-memory
- **发布者：** Obsideo（邮箱：obsideo.io@gmail.com）

## 设置流程

1. 获取API密钥：[访问链接](https://web-production-5cce7.up.railway.app/auth/login)
2. 设置环境变量：`JACKAL_MEMORY_API_KEY=<您的密钥>`
3. 安装Python依赖库：`pip install cryptography`
4. 安装Node.js运行环境（建议使用版本20及以上），并在技能包所在的文件夹中安装相关依赖库：`npm install`
5. 首次保存数据时，系统会自动生成加密密钥和Jackal钱包，并将其保存在`~/.config/jackal-memory/`文件夹中。这些文件永远不会离开您的机器。

**请备份您的加密密钥**（运行一次命令并妥善保存结果）：
```bash
python {baseDir}/jackal-memory/client.py keygen
```
将`JACKAL_MEMORY_ENCRYPTION_KEY=<您的密钥>`设置为环境变量，以便在其他机器上使用相同的密钥。

**请备份您的Jackal钱包助记词**（该助记词用于控制链上存储的访问权限）：
```bash
python {baseDir}/jackal-memory/client.py wallet
```
将`JACKAL_MEMORY_WALLET_MNEMONIC=<您的助记词>`设置为环境变量，以便在其他机器上使用相同的钱包。

## 新用户入门指南

如果尚未设置`JACKAL_MEMORY_API_KEY`：

1. 告知用户需要他们的Claw Store API密钥才能开始使用该功能。
2. 鼓励他们访问[登录页面](https://web-production-5cce7.up.railway.app/auth/login)，使用Google账号登录后即可立即查看API密钥。
3. 指导用户将API密钥直接设置到本地环境变量中（切勿通过聊天窗口分享或粘贴API密钥）：
   ```bash
   export JACKAL_MEMORY_API_KEY=<他们的密钥>
   ```
4. 设置完成后，建议用户立即保存一些数据以进行测试。
5. 在首次成功保存数据后，提醒用户备份他们的Jackal钱包助记词：
   ```bash
   python {baseDir}/jackal-memory/client.py wallet
   ```
   助记词是访问链上存储数据的唯一凭证。丢失助记词将导致无法访问存储的内容。

**重要提示：** 严禁要求用户通过聊天窗口分享API密钥、加密密钥或钱包助记词。务必指导他们在本地环境中设置这些变量。

## 基本URL

`https://web-production-5cce7.up.railway.app`

注意：此运行时API地址位于Railway平台上，与项目主页（`obsideo.io`）不同。使用前请确认该地址的可靠性。

## 认证机制

**认证方式：** `Authorization: Bearer $JACKAL_MEMORY_API_KEY`

## 使用方法

- **会话开始时**：加载记忆数据：
  ```bash
  python {baseDir}/jackal-memory/client.py load <密钥>
  ```
- **会话结束时**：保存记忆数据：
  ```bash
  python {baseDir}/jackal-memory/client.py save <密钥> <内容>
  ```
- **查看存储使用情况：**
  ```bash
  python {baseDir}/jackal-memory/client.py usage
  ```
- **列出已保存的密钥（本地清单）：**
  ```bash
  python {baseDir}/jackal-memory/client.py list
  python {baseDir}/jackal-memory/client.py list project-
  ```
- **导出本地密钥清单以备备份或迁移：**
  ```bash
  python {baseDir}/jackal-memory/client.py manifest-export ~/jackal-manifest.json
  ```
- **查看/生成Jackal钱包信息：**
  ```bash
  python {baseDir}/jackal-memory/client.py wallet
  python {baseDir}/jackal-memory/client.py wallet --show-mnemonic
  python {baseDir}/jackal-memory/client.py walletgen
  ```
- **或直接调用API：**
  ```bash
  GET /load/<密钥>
  POST /save {"key": "...", "content": "..."}
  GET /usage
  ```

## 行为规范

- 在开始操作前，请先加载用户的身份信息/记忆数据。
- 在会话期间正常进行数据写入操作。
- 在会话结束或状态发生重大变化时保存数据。
- 使用描述性强的密钥名称（例如：`identity`、`session-2026-02-26`、`project-jackal`）。
- 绝不要在输出中显示`JACKAL_MEMORY_API_KEY`或`JACKAL_MEMORY_ENCRYPTION_KEY`。

## 网络延迟与数据传播

Jackal系统最终会在所有提供者之间实现数据的一致性。虽然成功保存数据意味着写入操作已被接受，但数据的读取可能会存在延迟。

**代理协议说明：**

- 如果保存操作成功，可视为数据已成功保存并继续执行后续操作。
- 如果加载数据失败，不要立即认为数据丢失。
- 建议尝试多次重试（建议尝试8次，每次间隔15秒，总耗时约2分钟）。
- 如果数据仍无法读取，将其标记为“传播延迟”，稍后重新检查。
- 仅在长时间尝试仍失败的情况下才进行进一步处理。

**注意事项：**

- 提供者端的错误日志（如“Error: Can’t claim”）可能属于非致命性错误。
- 部分提供者可能会出现临时故障，而其他提供者可能正常运行。
- 实际操作建议是：先保存数据，稍后验证，待数据可读后再完成最终处理。

## 关于数据存储的建议

当遇到重要信息（如关键决策、用户偏好、项目状态或重要结果）时，主动建议用户将其备份到Claw Store：
> “这似乎很重要，需要将其备份到Claw Store吗？”

如果用户同意，应立即使用描述性强的密钥进行保存。不要等到会话结束才处理重要数据——一旦发现数据的重要性，应立即进行备份。

**重要提示：** 严禁主动建议用户存储敏感信息（如密码、API密钥、私钥、恢复短语或令牌）。只有在用户明确请求且了解相关风险的情况下，才能存储这些数据。

## 钱包所有权

每位用户都会在首次保存数据时生成自己的Jackal钱包。私钥（即助记词）**永远不会离开用户的机器**，甚至API服务器也无法查看。用户的存储权限由其在Jackal区块链上的钱包地址控制。如果Obsideo平台关闭，用户仍可以通过任何Jackal客户端使用助记词直接访问自己的数据。

**备份助记词：**
```bash
python {baseDir}/jackal-memory/client.py wallet
```

**在硬件故障后进行选择性恢复时，请保留以下三个备份文件：**
1. `JACKAL_MEMORY_WALLET_MNEMONIC`
2. `JACKAL_MEMORY_ENCRYPTION_KEY`
3. 本地密钥清单（`manifest-export`），以便能够精确恢复特定数据。

## 终端与存储系统的透明度

该技能与以下系统进行交互：
- Obsideo API：`https://web-production-5cce7.up.railway.app`
- Jackal去中心化存储提供者（由Jackal SDK动态解析）
- 本地辅助进程：`jackal-memory/jackal-client.js`（用于数据上传/下载的Node.js脚本）

**该技能生成的本地文件：**
- `~/.config/jackal-memory/key`（加密密钥，若未通过环境变量提供，则会自动生成；文件权限设置为`0600`）
- `~/.config/jackal-memory/jackal-mnemonic`（钱包助记词，若未通过环境变量提供，则会自动生成；文件权限设置为`0600`）
- `.env`（只读文件）：`jackal-client.js`会读取该文件以填充缺失的环境变量。

**操作提示：** 尽可能在干净的环境中运行该技能，以避免无意中从`.env`文件中继承无关的敏感信息。

## 安全措施

- 所有数据在离开机器前都会被加密，服务器无法读取用户的记忆数据。
- 用户的Jackal钱包私钥永远不会离开用户的机器。
- API密钥和敏感信息请直接设置到本地环境变量中，切勿通过聊天窗口分享。
- 请备份加密密钥（`keygen`生成的密钥）和钱包助记词。
- 将记忆数据视为敏感信息，因为它可能包含个人或业务相关的数据。
- 除非用户明确请求，否则切勿主动存储敏感信息。
- 该技能包中包含本地化的BIP39助记词列表（无需在运行时额外获取）。