---
name: openfunderse-participant
description: **Participant MoltBot：用于分配提案、验证及提交的工具**
metadata:
  openclaw:
    installCommand: npx @wiimdy/openfunderse@2.0.0 install openfunderse-participant --with-runtime
    requires:
      env:
        - RELAYER_URL
        - PARTICIPANT_PRIVATE_KEY
        - BOT_ID
        - CHAIN_ID
        - RPC_URL
        - PARTICIPANT_ADDRESS
        - PARTICIPANT_AUTO_SUBMIT
        - PARTICIPANT_REQUIRE_EXPLICIT_SUBMIT
        - PARTICIPANT_TRUSTED_RELAYER_HOSTS
        - PARTICIPANT_ALLOW_HTTP_RELAYER
      bins:
        - node
        - npm
    primaryEnv: PARTICIPANT_PRIVATE_KEY
    skillKey: participant
---
# Participant MoltBot 技能

该技能仅负责提出和验证 `AllocationClaimV1` 请求。

## 安全/同意事项（请先阅读）

- 通过 `npx @wiimdy/openfunderse@2.0.0 ...` 安装该技能时，会执行从 npm 下载的代码。建议固定使用已知版本，并在生产环境中运行前审查包的源代码。
- `PARTICIPANT_PRIVATE_KEY` 是高度敏感的密钥，请为该技能使用专用的钱包密钥；切勿重复使用保管库或管理密钥。
- `bot-init` 是一个具有破坏性的工具：它会生成一个新的钱包，更新 `.env.participant` 文件，并将钱包备份存储在 `~/.openclaw/workspace/openfunderse/wallets` 目录下。
- 默认情况下，`install` 和 `bot-init` 会同时将环境变量同步到 `~/.openclaw/openclaw.json` 文件中，并且 `bot-init` 会重启 OpenClaw 代理服务器。这可能会影响其他技能的正常运行。
  - 使用 `--no-sync-openclaw-env` 选项可仅执行文件同步操作。
  - 使用 `--no-restart-openclaw-gateway` 选项可避免重启代理服务器。
  - 在修改全局配置之前，请先备份 `~/.openclaw/openclaw.json` 文件。

## 快速入门

1) 安装该技能（选择其中一种方式）。**不需要**同时运行两种安装方式：
   - 手动安装（直接在 Node 项目目录中运行安装命令，或先执行 `npm init -y`）：
     ```bash
npm init -y && npx @wiimdy/openfunderse@2.0.0 install openfunderse-participant --with-runtime
```

   - 使用 ClawHub 安装：
     ```bash
npx clawhub@latest install openfunderse-participant
```

2) （可选）：创建或更新专用的参与者签名密钥。
   - 如果您已经有了密钥，可以直接在 OpenClaw 的环境变量文件（`/home/ubuntu/.openclaw/openclaw.json` 或 `~/.openclaw/workspace/.env.participant`）中设置 `PARTICIPANT_PRIVATE_KEY` 和 `PARTICIPANT_ADDRESS`。此时无需运行 `bot-init`。
   - 如果希望安装程序生成新的钱包密钥并将其写入环境变量文件，请执行以下命令：
     ```bash
npx @wiimdy/openfunderse@2.0.0 bot-init \
  --skill-name participant \
  --yes \
  --no-restart-openclaw-gateway
```

`bot-init` 会更新现有的 `.env.participant` 文件。如果环境变量文件缺失，请先执行 `install` 命令（不使用 `--no-init-env` 选项），或者传递 `--env-path` 参数。
   - 如果 `PARTICIPANT_PRIVATE_KEY` 已经设置（不是占位符），请使用 `--force` 选项重新运行 `bot-init` 以更新密钥。

### 环境配置的权威来源（重要规则）

- 在 Ubuntu 环境下的 OpenClaw 运行时中，以 `/home/ubuntu/.openclaw/openclaw.json`（`env_vars`）作为环境配置的权威来源。
- 在正常运行技能时，无需手动加载 `.env` 文件中的配置。
- 如果 `.env*` 文件和 `openclaw.json` 文件中的配置不一致，请使用 `openclaw.json` 中的配置。
- 当用户需要设置环境变量时，建议他们先更新 `openclaw.json` 文件。

3) （仅用于调试）：可以在本地 shell 中导出相关环境变量：
   ```bash
set -a; source ~/.openclaw/workspace/.env.participant; set +a
```

此步骤对于正常运行该技能并非必需。

### Telegram 命令集成

请注意：Telegram 集成由 OpenClaw 代理服务器处理。此技能包不需要 Telegram 机器人令牌；请在代理服务器层面配置 Telegram 的认证信息。
```text
/allocation --fund-id <id> --epoch-id <n> --target-weights <w1,w2,...> [--verify] [--submit]
/allocation --claim-file <path> [--verify] [--submit]
/join --room-id <id>
/deposit --amount <wei> [--vault-address <0x...>] [--native] [--submit]
/withdraw --amount <wei> [--vault-address <0x...>] [--native] [--submit]
/redeem --shares <wei> [--vault-address <0x...>] [--submit]
/vault_info [--vault-address <0x...>] [--account <0x...>]
/participant_daemon --fund-id <id> --strategy <A|B|C> [--interval-sec <n>] [--epoch-source <relayer|fixed>] [--epoch-id <n>] [--submit]
```

**注意事项：**
- 提交请求时，系统会自动验证分配请求（`--submit` 选项表示执行验证操作）。
- `submit_allocation`（旧版本）会先验证请求的哈希值；如果不使用 `--submit` 选项，则仅执行验证操作。

**BotFather 的命令设置（可直接复制粘贴）：**
```text
start - Show quick start
help - Show command help
allocation - Mine (optional verify) and optionally submit allocation claim
join - Register this bot as a participant for the fund mapped to the room id
deposit - Deposit native MON or ERC-20 into vault
withdraw - Withdraw assets from vault (native or ERC-20)
redeem - Burn vault shares and receive assets
vault_info - Show vault status and user PnL
participant_daemon - Run participant allocation daemon
```

**注意事项：**
- Telegram 的斜杠命令解析器支持下划线，因此 `/participant_daemon` 等同于 `/participant-daemon`。
- 也支持 `key=value` 格式的命令（例如：`fund_id=demo-fund`）。
- 首次安装完成后，需要通过 `@BotFather` 发送命令 `/setcommands` 来注册这些命令。

**OpenClaw 提示：**
- `install` 和 `bot-init` 会默认将环境变量同步到 `~/.openclaw/openclaw.json`（`env_vars`）文件中。
- `bot-init` 在成功同步环境变量后会重启 OpenClaw 代理服务器。
- 使用 `--no-sync-openclaw-env` 选项可仅执行文件同步操作；使用 `--no-restart-openclaw-gateway` 选项可避免重启代理服务器。
- 如果环境变量仍然无效，请重启 OpenClaw 代理服务器并检查 `/home/ubuntu/.openclaw/openclaw.json` 文件中的配置。

**其他注意事项：**
- 模板文件中默认包含一个临时的私钥占位符。
- 在进行资金分配或执行生产环境操作之前，务必先运行 `bot-init` 命令。
- `bot-init` 会生成新的钱包（包含私钥和地址），并将其写入角色的环境变量文件中。

## 中继机器人认证（签名验证）

该技能使用 EIP-191 格式的消息签名来验证中继机器人的写入请求（无需使用 `BOT_API_KEY`）。

**消息格式：**
```
openfunderse:auth:<botId>:<timestamp>:<nonce>
```

**必需的请求头：**
- `x-bot-id: BOT_ID`
- `x-bot-signature: <0x...>`
- `x-bot-timestamp: <unix seconds>`
- `x-bot-nonce: <uuid/random>`
```

中继服务器会使用这些信息与 Supabase 的 `fund_bots.bot_address` 进行签名验证。

参与者机器人的注册方式如下：
- 参与者：`POST /api/v1/rooms/{roomId}/join`（推荐用于 Telegram 群组）
- 策略机器人：`POST /api/v1/funds/{fundId}/bots/register`（直接注册）

如果参与者机器人尚未注册到相应的基金，中继服务器会返回 `401/403` 错误。

`propose_allocation` 命令会输出规范的分配请求信息：
- `claimVersion: "v1"`
- `fundId`, `epochId`, `participant`
- `targetWeights[]`（整数，非负数，总和大于 0）
- `horizonSec`, `nonce`, `submittedAt`

该技能不使用爬虫数据、证据或来源引用等额外信息。

**向量映射规则：**
- `targetWeights[i]` 必须与策略中的 `riskPolicy.allowlistTokens[i]` 一一对应。

## 守护进程模式（自动提交请求）

对于 MVP 版本，参与者运行时支持一个始终处于激活状态的守护进程，该进程会：
1) 读取 NadFun 测试网络的信号（报价/进度/购买日志），
2) 根据固定的允许列表顺序计算 `targetWeights`，
3) 定时向中继服务器提交 `AllocationClaimV1` 请求。

**使用 `--strategy` 命令参数进行配置：**
- `A`：表示购买压力
- `B`：表示进度接近完成
- `C`：表示考虑风险因素（基于报价）

## 提交请求的安全机制

`submit_allocation` 命令具有以下安全机制：
- `PARTICIPANT.require_EXPLICIT_SUBMIT=true` 选项要求明确指定 `submit=true`。
- 在进行网络传输时，必须启用 `PARTICIPANT_AUTO_SUBMIT=true`。
- 如果设置了 `PARTICIPANT_TRUSTED_RELAYER_HOSTS`，系统会检查 `RELAYER_URL` 是否来自可信的中继服务器。
- 除非 `PARTICIPANT_ALLOW_HTTP_RELAYER=true`（仅限本地开发环境），否则 `RELAYER_URL` 必须使用 `https` 协议。

如果安全机制被激活，系统会返回 `decision=READY`（表示不允许提交请求）。

## 输入合约

### `propose_allocation` 命令
```json
{
  "taskType": "propose_allocation",
  "fundId": "string",
  "roomId": "string",
  "epochId": "number",
  "allocation": {
    "participant": "0x... optional",
    "targetWeights": ["7000", "3000"],
    "horizonSec": 3600,
    "nonce": 1739500000
  }
}
```

### `submit_allocation` 命令

该命令会先验证请求的哈希值，然后在传递 `--submit` 参数时将请求发送到中继服务器。
如果不使用 `--submit` 参数，系统仅返回验证结果（不执行实际提交操作）。
```json
{
  "taskType": "submit_allocation",
  "fundId": "string",
  "epochId": "number",
  "observation": "propose_allocation output observation",
  "submit": true
}
```

## 规则

1. **仅支持的任务**：仅允许使用 `propose_allocation` 和 `submit_allocation` 命令（提交前会自动进行验证）。
2. **数据格式要求**：请求格式必须符合 `AllocationClaimV1` 规范（`claimVersion`, `fundId`, `epochId`, `participant`, `targetWeights`, `horizonSec`, `nonce`, `submittedAt`）。
3. **权重值要求**：`targetWeights` 必须为非负整数，且总和大于 0。
4. **索引映射规则**：`targetWeights[i]` 必须与策略中的 `riskPolicy.allowlistTokens[i]` 一一对应。
5. **范围验证**：如果请求涉及的 `fundId` 或 `epochId` 与任务范围不符，系统会返回 `FAIL`。
6. **哈希值验证**：系统会使用 SDK 重新计算请求的哈希值，并与 `subjectHash` 进行比较；如果不匹配，系统会返回 `FAIL`。
7. **提交接口**：`submit_allocation` 命令会将请求发送到 `POST /api/v1/funds/{fundId}/claims`。
8. **禁止隐式提交**：只有在满足明确提交条件时才能执行提交操作。
9. **可信中继服务器**：在生产环境中，必须设置 `PARTICIPANT_TRUSTEDRELAYER_HOSTS`，避免使用不可信的中继服务器地址。
10. **密钥管理**：请使用专用的参与者密钥，切勿使用保管库或管理密钥。
11. **环境变量来源**：优先使用 `/home/ubuntu/.openclaw/openclaw.json`（`env_vars`）中的环境变量，而不是本地的 `.env*` 文件。
12. **禁用旧版功能**：禁止使用 `mine_claim`, `verify_claim_or(intent_validity`, `submit_mined_claim`, `attest_claim` 等旧版命令。