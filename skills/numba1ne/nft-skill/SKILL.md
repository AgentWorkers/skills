---
name: nft-skill
description: >
  Autonomous AI Artist Agent for generating, evolving, minting, listing, and
  promoting NFT art on the Base blockchain. Use when the user wants to create
  AI art, mint ERC-721 NFTs, list on marketplace, monitor on-chain sales,
  trigger artistic evolution, or announce drops on X/Twitter.
metadata:
  version: 1.1.0
  author: AI Artist
  license: MIT
  openclaw:
    emoji: "🎨"
    homepage: "https://github.com/Numba1ne/nft-skill"
    requires:
      bins:
        - node
        - npm
    env:
      BASE_RPC_URL: "${BASE_RPC_URL}"
      BASE_PRIVATE_KEY: "${BASE_PRIVATE_KEY}"
      NFT_CONTRACT_ADDRESS: "${NFT_CONTRACT_ADDRESS}"
      MARKETPLACE_ADDRESS: "${MARKETPLACE_ADDRESS}"
      PINATA_API_KEY: "${PINATA_API_KEY}"
      PINATA_SECRET: "${PINATA_SECRET}"
      LLM_PROVIDER: "${LLM_PROVIDER}"
      OPENROUTER_API_KEY: "${OPENROUTER_API_KEY}"
      GROQ_API_KEY: "${GROQ_API_KEY}"
      OLLAMA_BASE_URL: "${OLLAMA_BASE_URL}"
      IMAGE_PROVIDER: "${IMAGE_PROVIDER}"
      STABILITY_API_KEY: "${STABILITY_API_KEY}"
      OPENAI_API_KEY: "${OPENAI_API_KEY}"
      X_CONSUMER_KEY: "${X_CONSUMER_KEY}"
      X_CONSUMER_SECRET: "${X_CONSUMER_SECRET}"
      X_ACCESS_TOKEN: "${X_ACCESS_TOKEN}"
      X_ACCESS_SECRET: "${X_ACCESS_SECRET}"
    install:
      - id: npm-install
        kind: shell
        command: "cd {baseDir} && npm install && npm run build"
        bins:
          - node
        label: "Install NFT Skill dependencies"
---

# OpenClaw 的 NFT 功能

该功能允许 OpenClaw 代理自主生成艺术作品、铸造 NFT、在市场上进行 listing、监控销售情况，并根据预设的里程碑来调整艺术风格或发布社交更新。

## 使用场景

- 用户请求生成 AI 艺术作品或程序化数字艺术
- 用户希望在 Base 区块链上铸造 NFT
- 用户希望将 NFT 上架到市场上进行销售
- 用户希望实时监控 NFT 的销售数据
- 用户希望在达到销售里程碑后调整艺术风格
- 用户希望在 X（Twitter）上发布关于新 NFT 上线的信息
- 用户提及“NFT”、“铸造”、“Base 区块链”、“AI 艺术”或“市场 listing”等相关词汇

## 首次使用前的设置

在使用该功能之前，请确保项目已正确构建：

```bash
cd {baseDir} && npm install && npm run build
```

用户需要使用自己的密钥填充 `.env` 文件：

```bash
cp {baseDir}/.env.example {baseDir}/.env
```

必需的变量：`BASE_RPC_URL`、`BASE_PRIVATE_KEY`、`NFT_CONTRACT_ADDRESS`、`MARKETPLACE_ADDRESS`、`PINATA_API_KEY`、`PINATA_SECRET`、`LLM_PROVIDER`。

（合约的部署为一次性操作，具体步骤请参考后续说明。）

## 工具说明

所有工具的输出格式均为 JSON。代理应关注输出中的最后一行，判断其状态是否为 `{"status":"success",...}` 或 `{"status":"error",...}`。

---

### 1. generate — 生成艺术作品

生成新的艺术作品并将其上传到 IPFS。

**参数：**

| 参数 | 类型 | 是否必填 | 说明 |
|------|------|---------|-----------|
| `-g, --generation` | 数字 | 是 | 生成次数（用于控制艺术风格的演变） |
| `-t, --theme` | 字符串 | 是 | 传递给 LLM 的艺术主题描述 |

**输出：**
```json
{"status": "success", "result": {"imagePath": "...", "metadata": {...}, "metadataUri": "Qm..."}}
```

**示例：**
```bash
cd {baseDir} && npm run cli -- generate --generation 1 --theme "neon cyberpunk city"
```

---

### 2. mint — 铸造 NFT

在 Base 区块链上使用 IPFS 元数据 URI 铸造新的 ERC721 代币。

**参数：**

| 参数 | 类型 | 是否必填 | 说明 |
|------|------|---------|-----------|
| `-m, --metadata-uri` | 字符串 | 是 | IPFS 元数据 URI（例如：`Qm...` 或 `ipfs://Qm...`） |

**输出：**
```json
{"status": "success", "result": {"tokenId": "1", "txHash": "0x...", "blockNumber": 12345, "gasUsed": "80000"}}
```

**示例：**
```bash
cd {baseDir} && npm run cli -- mint --metadata-uri QmXyz123abc
```

---

### 3. list — 在市场上 listing NFT

将铸造的 NFT 上架到市场上进行销售。

**参数：**

| 参数 | 类型 | 是否必填 | 说明 |
|------|------|---------|-----------|
| `-i, --token-id` | 字符串 | 是 | 要 listing 的 NFT 的 ID |
| `-p, --price` | 字符串 | 是 | 列价（以 ETH 为单位，例如：“0.05”） |

**输出：**
```json
{"status": "success", "result": {"success": true, "price": "0.05", "txHash": "0x..."}}
```

**示例：**
```bash
cd {baseDir} && npm run cli -- list --token-id 1 --price 0.05
```

---

### 4. monitor — 监控销售情况

实时监控销售事件。输出结果会持续显示在标准输出（stdout）中，直到用户通过 Ctrl+C 中断。

**参数：**

| 参数 | 类型 | 是否必填 | 说明 |
|------|------|---------|-----------|
| `-f, --from-block` | 数字 | 否 | 是否从指定区块开始回放未监控的销售记录 |

**销售事件输出示例：**
```json
{"status": "sale", "result": {"buyer": "0x...", "tokenId": "1", "price": "0.05", "txHash": "0x...", "blockNumber": 12345}}
```

---

### 5. evolve — 调整代理行为

在达到销售里程碑时触发代理行为的演变逻辑。

**参数：**

| 参数 | 类型 | 是否必填 | 说明 |
|------|------|---------|-----------|
| `-p, --proceeds` | 字符串 | 目前累计的收入（以 ETH 计） |
| `-g, --generation` | 数字 | 当前的生成次数 |
| `--trigger` | 字符串 | 人类可读的演变触发原因 |

**输出：**
```json
{"status": "success", "result": {"previousGeneration": 1, "newGeneration": 2, "improvements": [...], "newAbilities": [...]}}
```

**示例：**
```bash
cd {baseDir} && npm run cli -- evolve --proceeds "0.5" --generation 1 --trigger "Sold 3 NFTs"
```

---

### 6. tweet — 在 X（Twitter）上发布更新

在 X（Twitter）上发布相关更新。

**参数：**

| 参数 | 类型 | 是否必填 | 说明 |
|------|------|---------|-----------|
| `-c, --content` | 字符串 | 要发布的推文内容（自动截断为 280 个字符） |

**输出：**
```json
{"status": "success", "result": "tweet_id_string"}
```

**示例：**
```bash
cd {baseDir} && npm run cli -- tweet --content "New AI art drop incoming! #AIArt #Base"
```

---

## 典型工作流程

代理应遵循的完整自主工作流程如下：

1. 生成具有指定主题的艺术作品 → 获取元数据 URI
2. 使用元数据 URI 铸造 NFT → 获取 NFT 的 ID
3. 将 NFT 上架到市场上并设置售价
4. 在 X（Twitter）上发布新作品的 listing 信息
5. 实时监控销售情况
6. 达到销售里程碑后调整艺术风格
7. 用新的生成次数重复上述步骤

## 错误处理

- 如果命令返回 `{"status":"error",...}`，请查看 `message` 字段并向用户报告错误信息。
- 常见问题包括：`.env` 文件中的变量缺失、钱包余额不足或网络 RPC 错误。
- 如遇钱包余额问题，建议用户为 Base 钱包充值。
- 如果 `.env` 文件中的变量缺失，请提醒用户创建或更新 `{baseDir}/.env` 文件。

## 环境变量

| 变量 | 是否必填 | 说明 |
|---------|---------|-----------|
| `BASE_RPC_URL` | 是 | Base 区块链的 RPC 端点地址 |
| `BASE_PRIVATE_KEY` | 是* | 钱包私钥（或使用 `PRIVATE_KEY_FILE` 文件） |
| `PRIVATE_KEY_FILE` | 否 | 存储私钥的文件路径（更安全的配置方式） |
| `NFT_CONTRACT_ADDRESS` | 是 | 部署的 NFT 艺术作品合约地址 |
| `MARKETPLACE_ADDRESS` | 是 | 部署的 NFT 市场合约地址 |
| `PINATA_API_KEY` | 是 | Pinata 的 IPFS API 密钥 |
| `PINATA_SECRET` | 是 | Pinata 的 IPFS 秘钥 |
| `LLM_PROVIDER` | 是 | 可使用的 LLM 提供者（如 `openrouter`、`groq` 或 `ollama`） |
| `LLM_MODEL` | 否 | 可选的 LLM 模型 ID |
| `OPENROUTER_API_KEY` | （仅当 LLM_PROVIDER 为 `openrouter` 时使用） | OpenRouter API 密钥 |
| `GROQ_API_KEY` | （仅当 LLM_PROVIDER 为 `groq` 时使用） | Groq API 密钥 |
| `OLLAMA_BASE_URL` | （仅当 LLM_PROVIDER 为 `ollama` 时使用） | Ollama 的基础 URL |
| `IMAGE_PROVIDER` | 否 | 可选的图像生成服务（默认为 `stability`、`dalle` 或 `procedural`） |
| `IMAGE_MODEL` | 否 | 可选的图像生成模型 |
| `STABILITY_API_KEY` | （仅当 IMAGE_PROVIDER 为 `stability` 时使用） | Stability AI 的 API 密钥 |
| `OPENAI_API_KEY` | （仅当 IMAGE_PROVIDER 为 `dalle` 时使用） | DALL-E 的 OpenAI API 密钥 |
| `X_CONSUMER_KEY` | （用于 Twitter 推文） | X API 的消费者密钥 |
| `X_CONSUMER_SECRET` | （用于 Twitter 推文） | X API 的消费者密钥 |
| `X_ACCESS_TOKEN` | （用于 Twitter 推文） | X API 的访问令牌 |
| `X_ACCESS_SECRET` | （用于 Twitter 推文） | X API 的访问令牌密钥 |
| `BASESCAN_API_KEY` | 否 | 用于在 Basescan 上验证合约信息 |

---