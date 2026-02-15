---
name: lightning
description: 使用 LNI（Lightning Node Interface）发送和接收 Bitcoin Lightning 支付。支持 LND、CLN、Phoenixd、NWC 以及托管服务（Strike、Blink、Speed）。
user-invocable: true
metadata: {"clawdbot":{"emoji":"⚡"}}
---

# Lightning (⚡)

使用 LNI 在 Lightning Network 上发送和接收比特币。

*开发于 🤠 德克萨斯州 ❤️ [PlebLab](https://pleblab.dev)*

![Lightning — 从聊天界面发送比特币。](https://files.catbox.moe/cjnf01.png)

---

> ⚠️ **请务必先阅读此警告** ⚠️
>
> **将资金权限授予机器人是极其危险的。**
>
> - 仅使用您能够承受损失的 **小额资金** 进行操作
> - **绝对不要** 在可通过聊天界面被外部访问的机器人上启用此功能
> - 本功能仅限 **个人/内部使用**
> - 机器人可以代表您进行支付——请将您的账户凭证视为现金一样谨慎对待
> - 从小额交易开始，彻底测试后再谨慎使用

## 支持的后端

| 后端 | 类型 | BOLT11 | BOLT12 | LNURL |
|---------|------|--------|--------|-------|
| CLN | 自托管 | ✅ | ✅ | ✅ |
| LND | 自托管 | ✅ | ⚠️ | ✅ |
| Phoenixd | 自托管 | ✅ | ✅ | ✅ |
| NWC | Nostr Wallet | ✅ | ❌ | ✅ |
| Spark | Breez SDK | ✅ | ❌ | ✅ |
| Strike | 托管服务 | ✅ | ❌ | ✅ |
| Blink | 托管服务 | ✅ | ❌ | ✅ |
| Speed | 托管服务 | ✅ | ❌ | ✅ |

## 命令

| 命令 | 描述 |
|---------|-------------|
| `/lightning` | 显示钱包信息和余额 |
| `/lightning invoice <金额> [备注]` | 创建支付请求 |
| `/lightning pay <收款地址> <金额>` | 进行支付（支持 BOLT11/BOLT12/LNURL/地址） |
| `/lightning confirm <收款地址> <金额>` | 确认并发送支付 |
| `/lightning decode <支付请求>` | 解码支付请求详情 |
| `/lightning history [数量]` | 列出最近的交易记录 |
| `/lightning contacts` | 列出保存的收款人信息 |
| `/lightning add <名称> <收款地址>` | 保存新的收款人信息 |

## 支持的支付目的地

`pay` 命令可自动识别以下支付方式：
- **BOLT11**: `lnbc10u1p5...`
- **BOLT12**: `lno1pg...`（仅支持 CLN/Phoenixd）
- **Lightning 地址**: `user@domain.com`
- **LNURL**: `lnurl1...`
- **保存的收款人信息**: 如 `topher`

## 安装

### 1. 下载 LNI 二进制文件

```bash
cd ~/workspace/skills/lightning
npm run download
```

从 [GitHub 仓库](https://github.com/lightning-node-interface/lni/releases) 下载适用于您平台的预编译二进制文件。

### 2. 配置后端

创建 `~/.lightning-config.json` 文件：

**CLN (Core Lightning):**
```json
{
  "backend": "cln",
  "url": "https://your-cln-node:3010",
  "rune": "your-rune-token",
  "acceptInvalidCerts": true
}
```

**LND:**
```json
{
  "backend": "lnd",
  "url": "https://your-lnd-node:8080",
  "macaroon": "hex-encoded-admin-macaroon",
  "acceptInvalidCerts": true
}
```

**Phoenixd:**
```json
{
  "backend": "phoenixd",
  "url": "http://127.0.0.1:9740",
  "password": "your-phoenixd-password"
}
```

**NWC (Nostr Wallet Connect):**
```json
{
  "backend": "nwc",
  "nwcUri": "nostr+walletconnect://..."
}
```

**Spark (Breez SDK):**
```json
{
  "backend": "spark",
  "apiKey": "your-breez-api-key",
  "mnemonic": "your 12 word seed",
  "storageDir": "/home/clawd/lightning-data",
  "network": "mainnet"
}
```

#### 配置新的 Spark 钱包

如果用户还没有 Spark 钱包，请按照以下步骤操作：

**步骤 1: 生成 12 个单词的助记词**

使用 LNI 的内置工具生成助记词：
```js
const lni = require('./lib/lni_js.node');
const mnemonic = lni.generateMnemonic();
console.log(mnemonic);
```
⚠️ 请用户 **安全地备份他们的助记词**——这是他们资金的安全保障。

**步骤 2: 请求 Breez API 密钥**

用户需要从 Breez 获取 API 密钥以使用无节点（Nodeless, Spark）SDK：

1. 访问：https://breez.technology/request-api-key/#contact-us-form-sdk
2. 填写您的 **电子邮件地址** 并选择 **Nodeless (Greenlight)** 实现方式
3. 提交表格——Breez 会通过电子邮件发送 API 密钥

**步骤 3: 获取 API 密钥**

提交表格后，询问用户：
> “您是否配置了电子邮件相关的技能（例如 ProtonMail）？如果需要，我可以帮您在收件箱中查找 Breez API 密钥。”

如果用户同意，使用相应的电子邮件技能来查找并提取 API 密钥。

**步骤 4: 创建配置文件**

获取助记词和 API 密钥后，编辑 `~/.lightning-config.json` 文件：
```json
{
  "backend": "spark",
  "apiKey": "<breez-api-key>",
  "mnemonic": "<12-word-seed>",
  "storageDir": "/home/clawd/lightning-data",
  "network": "mainnet"
}
```

**步骤 5: 连接并验证**
```js
const node = new lni.SparkNode(config);
await node.connect();
const info = await node.getInfo();
```

**Strike/Blink/Speed (托管服务):**
```json
{
  "backend": "strike",
  "apiKey": "your-api-key"
}
```

### Tor 支持（SOCKS5 代理）

通过 Tor 连接到您的节点以增强隐私保护，或访问使用 `.onion` 地址的节点。

**要求：**
1. **Tor 必须在本地运行**——在您的机器上安装并启动 Tor 服务
2. 您的节点必须可以通过 Tor 访问（无论是通过 `.onion` 地址还是普通网络）

**安装 Tor:**
```bash
# macOS
brew install tor && brew services start tor

# Ubuntu/Debian
sudo apt install tor && sudo systemctl start tor

# Arch
sudo pacman -S tor && sudo systemctl start tor
```

**配置 SOCKS5 代理:**

在任意后端配置文件中添加 `socks5Proxy` 选项：
```json
{
  "backend": "cln",
  "url": "http://your-node.onion:3010",
  "rune": "your-rune-token",
  "socks5Proxy": "socks5h://127.0.0.1:9050"
}
```

**常用代理地址:**
| 服务 | 地址 |
|---------|---------|
| Tor 守护进程 | `socks5h://127.0.0.1:9050` |
| Tor 浏览器 | `socks5h://127.0.0.1:9150` |

> 💡 请使用 `socks5h://`（而非 `socks5://`），以确保 `.onion` 地址通过 Tor 进行解析。

## 示例

```bash
# Check balance
/lightning

# Create invoice
/lightning invoice 1000 "Coffee payment"

# Pay Lightning Address
/lightning pay nicktee@strike.me 100

# Pay BOLT12 offer
/lightning pay lno1pg... 50

# Save & pay contact
/lightning add topher lno1pg...
/lightning pay topher 69
```

## 相关文件

- `~/.lightning-config.json` - 后端配置信息
- `~/.lightning-contacts.json` - 保存的收款人信息

## 安全提示

- **切勿共享助记词、API 密钥等敏感信息**
- 仅在可信网络中使用 `acceptInvalidCerts` 选项来处理自签名证书
- `contacts` 文件仅包含收款人信息，不包含任何敏感数据

## 致谢

本功能基于 [LNI](https://github.com/lightning-node-interface/lni)（Lightning Node Interface）开发。