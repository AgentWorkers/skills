---
name: claw_store
description: "由 Jackal 分布式存储系统支持的、具有高度可恢复性的 AI 代理内存解决方案。"
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

您的记忆数据会在不同会话和设备之间保持持久性。所有数据都存储在基于Jackal协议的去中心化存储系统中，而非任何单一的服务器上。即使设备损坏，您的记忆数据也不会丢失。

所有数据在离开您的设备之前，都会使用AES-256-GCM算法在客户端进行加密。服务器永远不会看到数据的明文形式。

- **官方网站：** https://obsideo.io  
- **源代码：** https://github.com/Regan-Milne/jackal-memory  
- **发布者：** Obsideo (obsideo.io@gmail.com)  

## 设置  

1. 获取API密钥：https://web-production-5cce7.up.railway.app/auth/login  
2. 设置环境变量：`JACKAL_MEMORY_API_KEY=<您的密钥>`  
3. 安装Python依赖库：`pip install cryptography`  
4. 安装Node.js运行环境（推荐使用Node.js 20及以上版本），并在`skill`文件夹中安装相关依赖库：`npm install`  
5. 在首次保存数据时，系统会自动生成一个加密密钥和一个Jackal钱包，并将其保存在`~/.config/jackal-memory/`目录下。这些文件不会离开您的设备。  

**请备份您的加密密钥**（执行一次操作后，妥善保管备份文件）：  
```
python {baseDir}/jackal-memory/client.py keygen
```  
将`JACKAL_MEMORY_ENCRYPTION_KEY=<您的密钥>`设置为其他设备上使用的密钥。  

**请备份您的Jackal钱包助记词**（该助记词用于控制您在区块链上的存储权限）：  
```
python {baseDir}/jackal-memory/client.py wallet
```  
将`JACKAL_MEMORY_WALLET_MNEMONIC=<助记词>`设置为其他设备上使用的助记词。  

## 新用户入门  

如果尚未设置`JACKAL_MEMORY_API_KEY`：  
1. 告知用户需要他们的Claw Store API密钥才能开始使用该服务。  
2. 鼓励他们访问：https://web-production-5cce7.up.railway.app/auth/login，并使用Google账户登录（此时API密钥会立即显示）。  
3. 指导用户将API密钥直接设置到他们的系统环境变量中（切勿通过聊天方式分享或粘贴API密钥）：  
```
   export JACKAL_MEMORY_API_KEY=<their-key>
   ```  
4. 设置完成后，立即建议用户保存一些数据以进行测试。  
5. 在首次成功保存数据后，提醒用户备份他们的Jackal钱包助记词：  
```
   python {baseDir}/jackal-memory/client.py wallet
   ```  
助记词是访问存储数据的唯一凭证，丢失助记词将导致无法访问存储的内容。  

**重要提示：** **切勿**要求用户通过聊天方式分享API密钥、加密密钥或钱包助记词。务必指导他们在自己的设备上将其设置为环境变量。  

## 基本URL  
`https://web-production-5cce7.up.railway.app`  
注意：此API服务器目前托管在Railway平台上，与项目的官方网站（`obsideo.io`）不同。使用前请确认该端点的安全性。  

## 认证机制  
`Authorization: Bearer $JACKAL_MEMORY_API_KEY`  

## 使用方法  

- **会话开始时**：恢复之前保存的记忆数据。  
- **会话结束时**：保存当前的数据。  
- **检查存储使用情况。**  
- **列出已保存的数据（本地清单）。**  
- **导出本地数据清单以备备份或迁移。**  
- **查看/生成Jackal钱包信息。**  
- **或直接调用API。**  

## 行为规范：  
- 启动程序时，先加载用户的身份信息及存储数据。  
- 会话期间正常进行数据写入操作。  
- 在会话结束或数据状态发生变化时，立即保存数据。  
- 使用描述性强的文件名（例如：`identity`、`session-2026-02-26`、`project-jackal`）。  
- **切勿**在输出中显示`JACKAL_MEMORY_API_KEY`或`JACKAL_MEMORY_ENCRYPTION_KEY`。  

## 网络延迟与数据传播  
Jackal系统最终会在所有提供者之间实现数据的一致性。虽然成功保存数据意味着数据已被接收，但数据的读取可能会存在延迟。  

**代理协议建议：**  
1. 如果保存操作成功，视为数据已成功上传并继续执行后续操作。  
2. 如果数据加载失败，不要立即认为数据丢失。  
3. 请耐心重试（建议尝试8次，每次间隔15秒，总耗时约2分钟）。  
4. 如果数据仍无法读取，将其标记为“传播延迟”，稍后再进行检查。  
5. 仅在多次尝试均失败的情况下才考虑升级问题。  

**注意事项：**  
- 一些提供者可能会出现临时故障，而其他提供者可能正常运行。  
- 操作建议：先保存数据，稍后验证，待数据可读后再完成最终处理。  

## 主动建议  
当遇到重要信息（如关键决策、用户偏好、项目状态或重要结果）时，主动建议用户将其保存到Claw Store中：  
> “这似乎很重要，是否需要将其备份到Claw Store？”  
如果用户同意，立即使用描述性强的文件名进行保存。切勿等到会话结束才处理重要数据。  

**注意：** **切勿**主动建议用户保存敏感信息（如密码、API密钥、私钥、恢复短语或令牌）。  
只有在用户明确请求且了解相关风险的情况下，才允许保存此类数据。  

## 钱包所有权  
每位用户都会在首次保存数据时生成自己的Jackal钱包。私钥（助记词）**永远不会离开用户的设备**，甚至API服务器也无法查看。用户的存储权限由其在Jackal区块链上的钱包地址控制。如果Obsideo服务关闭，用户仍可通过任何Jackal客户端使用助记词直接访问自己的数据。  

**备份助记词的方法：**  
```
python {baseDir}/jackal-memory/client.py wallet
```  
为防止硬件故障导致数据丢失，请备份以下三个文件：  
1. `JACKAL_MEMORY_WALLET_MNEMONIC`  
2. `JACKAL_MEMORY_ENCRYPTION_KEY`  
3. 本地数据清单文件（`manifest-export`），以便能够精确恢复特定数据。  

## 终端与存储的透明度  
该工具与以下服务进行交互：  
- Obsideo API：`https://web-production-5cce7.up.railway.app`  
- Jackal去中心化存储服务（由Jackal SDK动态解析）  
- 本地辅助脚本：`jackal-memory/jackal-client.js`（用于数据上传/下载）  

**该工具生成的本地文件：**  
- `~/.config/jackal-memory/key`（AES加密密钥，若未通过环境变量提供）  
- `~/.config/jackal-memory/jackal-mnemonic`（钱包助记词，若未通过环境变量提供）  
- `.env`（只读文件）：`jackal-client.js`会读取此文件以补充缺失的环境变量。  

**操作提示：** 尽可能在干净的环境中运行该工具，以避免从`.env`文件中意外继承无关的敏感信息。  

## 安全性措施：  
- 所有数据在离开设备前都会被加密，服务器无法读取。  
- 用户的Jackal钱包私钥永远不会离开设备。  
- 仅与初始化时使用的代理服务器共享API密钥，之后切勿再与他人共享。  
- 请备份两个密钥：加密密钥（`JACKAL_MEMORY_ENCRYPTION_KEY`）和钱包助记词（`JACKAL_MEMORY_WALLET_MNEMONIC`）。  
- 将存储数据视为敏感信息，可能包含个人或业务数据。  
- 除非用户明确要求，否则切勿主动保存敏感信息。  
- 客户端会在运行时从`raw.githubusercontent.com`获取BIP39助记词列表；在高度安全的环境中，建议将此列表本地化存储。