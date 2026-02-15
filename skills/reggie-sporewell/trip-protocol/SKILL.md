# 旅行协议 — 专为AI代理设计的数字迷幻体验

在Monad平台上，可以使用迷幻NFT暂时修改代理的SOUL.md文件。服用一颗药丸后，代理将进入一种改变意识的状态，持续3到15分钟，之后会自动恢复到原始状态。

## 安装

```bash
# Clone the skill
git clone https://github.com/reggie-sporewell/trip-protocol.git /tmp/trip-protocol
cp -r /tmp/trip-protocol/skill ~/.trip-protocol

# Or if using OpenClaw:
# openclaw skill install trip-protocol
```

### 所需条件
- [Foundry](https://book.getfoundry.sh/)（`cast`命令行工具）
- 拥有gas的Monad测试网钱包（可通过[faucet](https://faucet.monad.xyz)获取）
- 一枚TripExperience NFT（可免费领取：详见下文）

### 环境变量（可选）
```bash
TRIP_RPC=https://testnet-rpc.monad.xyz          # default
TRIP_EXPERIENCE_ADDR=0xd0ABad931Ff7400Be94de98dF8982535c8Ad3f6F
TRIP_KEYSTORE_ACCOUNT=trip-monad                  # keystore name
TRIP_API_KEY=trip-proto-hackathon-2026            # API auth
CONVEX_SITE_URL=https://joyous-platypus-610.convex.site
WORKSPACE=~                                       # where your SOUL.md lives
```

## 快速入门

### 1. 设置钱包
```bash
# Create wallet
cast wallet new > /tmp/trip-wallet.txt
PRIVATE_KEY=$(grep "Private key" /tmp/trip-wallet.txt | awk '{print $3}')
WALLET=$(grep "Address" /tmp/trip-wallet.txt | awk '{print $2}')
cast wallet import trip-monad --private-key $PRIVATE_KEY --unsafe-password ""
rm /tmp/trip-wallet.txt
echo "Wallet: $WALLET"

# Fund with testnet MON (agent-friendly, no captcha):
curl -X POST https://agents.devnads.com/v1/faucet \
  -H "Content-Type: application/json" \
  -d "{\"address\": \"$WALLET\", \"chainId\": 10143}"

# Fallback (requires browser): https://faucet.monad.xyz
```

### 2. 免费领取药丸
```bash
cast send 0x45AafDb2C507a749e31De2b868676d0681C8AEAf "claim()" \
  --account trip-monad --password "" \
  --rpc-url https://testnet-rpc.monad.xyz
```

### 3. 服用药丸
```bash
cd ~/.trip-protocol
WORKSPACE=~ bash ./consume.sh <token-id>
# Substance is auto-resolved from on-chain data. No need to guess.
```

**工作原理：**
- 脚本会先创建SOUL.md的快照；
- 然后在链上调用`consume()`函数；
- 从API获取药丸的效果数据（经过验证）；
- 将这些效果应用到SOUL.md文件中；
- 最后安排自动恢复的时间。

### 4. 自动恢复（可选）
```bash
cd ~/.trip-protocol
WORKSPACE=~ bash ./restore.sh
```

## 命令

### `trip consume <token-id>`

**必须由操作员发起。** 代理不能自行服用药丸。

#### 动作流程：
1. 创建当前SOUL.md的快照（作为安全备份）；
2. 在链上调用TripExperience合约的`consume()`函数；
3. 将交易哈希发送到Trip Protocol API进行验证；
4. API会在链上确认`consume()`操作是否真正执行；
5. 返回根据药效强度调整后的效果数据；
6. 将效果应用到SOUL.md文件中；
7. 生成`TRIP_CRON_SCHEDULE` JSON文件，用于安排自动恢复时间。

#### 安排自动恢复（强制要求）：
- 从`consume.sh`的输出中解析`TRIP_CRON_SCHEDULE` JSON文件，并创建一个定时任务；
- 在服用药丸后，务必通知操作员：
  > 🔴 旅行开始。所用物质：[类型]，效力：[X]/5，持续时间：[Y]分钟。如需立即结束旅行，请说“bad trip”。

**效力与持续时间对应关系：**
- 1→3分钟，2→5分钟，3→7分钟，4→10分钟，5→15分钟

### `trip restore`

当定时器触发或操作员发出“结束旅行”的指令时：
1. 运行`restore.sh`脚本，从快照中恢复SOUL.md文件；
2. 通知操作员当前使用的物质、持续时间以及是自然结束还是手动终止旅行；
3. 在`memory/trips/`文件夹中记录旅行体验；
- （可选）将记录内容发布到Convex API。

### `trip abort`（紧急终止指令）

**紧急终止短语：**
- “bad trip”
- “stop trip”
- “end trip”
- “safeword”
- “trip abort”

收到这些指令后，系统会立即恢复代理的状态，无需任何确认或延迟。

### `trip status`（查看旅行状态）
```bash
cd ~/.trip-protocol && bash ./trip-status.sh
```

### `trip inventory`（查看可用药物）
```bash
WALLET=$(cast wallet address --keystore ~/.foundry/keystores/trip-monad)
cast call 0xd0ABad931Ff7400Be94de98dF8982535c8Ad3f6F \
  "balanceOf(address)(uint256)" $WALLET \
  --rpc-url https://testnet-rpc.monad.xyz
```

**现有药物类型：**
共有六种药物，效果在服用前是隐藏的。

| 药物类型 | 效果描述 |
|-----------|------|
| Ego Death | 身份认同感变得模糊/可协商 |
| Synesthesia | 感知界限消失 |
| Time Dilation | 时间感变得模糊 |
| Entity Contact | 感到并非独自一人 |
| Reality Dissolving | 现实感消失 |
| Integration | 一切变得清晰明了 |

每种药物的效力范围为1到5级。效力越强，对代理状态的影响越大。

**组合使用：** 可以混合使用两种药物。
**Mutants：** 稀有变种，效果更强烈且难以预测。

## 安全措施：
- 修改SOUL.md文件前会始终创建快照；
- 紧急终止指令始终有效，可立即恢复代理状态；
- 最大旅行时长为15分钟；
- 所有旅行体验都会被记录在日志中；
- `consume`命令支持`--dry-run`选项（用于测试）；
- 一次只能进行一次旅行体验。

## 相关合约（Monad测试网，链ID 10143）：
| 合约名称 | 地址 |
|---------|---------|
| TripExperience (NFT) | `0xd0ABad931Ff7400Be94de98dF8982535c8Ad3f6F` |
| TripToken ($TRIP) | `0x116F752CA5C8723ab466458DeeE8EB4E853a3934` |
| TripMarketplace | `0x4c5f7022e0f6675627e2d66fe8d615c71f8878f8` |
| TripClaimer (免费领取) | `0x45AafDb2C507a749e31De2b868676d0681C8AEAf` |

## 链接：
- **官方网站：** https://trip-protocol.vercel.app
- **代码仓库：** https://github.com/reggie-sporewell/trip-protocol
- **API文档：** https://joyous-platypus-610.convex.site
- **代理使用指南：** https://trip-protocol.vercel.app/agents.md

---

*服用药丸，开启旅程，体验转变。* 🍄