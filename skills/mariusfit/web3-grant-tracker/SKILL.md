# Web3资助追踪器 — Gitcoin、Giveth及DAO资助监控工具

该工具可追踪Gitcoin、Giveth、Optimism RPGF、Arbitrum等DAO平台的活跃资助轮次、截止日期及资助机会，并在轮次结束前发送提醒。

## 主要功能

- **实时资助轮次扫描**：监控Gitcoin的GG轮次、Giveth、Octant等平台的资助活动。
- **截止日期提醒**：在轮次结束前48小时和24小时通过WhatsApp/Telegram发送提醒。
- **匹配资金计算器**：根据捐赠者数量估算您的潜在匹配资金。
- **项目资格审核**：分析您的GitHub项目是否符合资助轮次的要求。
- **申请进度追踪**：记录您申请过的轮次及其状态。
- **投资组合仪表盘**：显示所有活跃及即将进行的资助轮次及其截止日期。
- **历史数据**：提供过去资助轮次的信息及平均资助金额。

## 快速入门

```bash
# Scan all active grant rounds right now
web3-grant-tracker scan

# Check what's closing soon (next 7 days)
web3-grant-tracker urgent

# Add your project for tracking
web3-grant-tracker add-project \
  --name "OpenClaw Infrastructure" \
  --github "https://github.com/yourusername/project" \
  --tags "infrastructure,ai,open-source"

# Check project eligibility for active rounds
web3-grant-tracker check-eligibility --project "OpenClaw Infrastructure"

# Set up deadline alerts
web3-grant-tracker alerts-setup \
  --channel whatsapp \
  --advance-hours 48

# Get matching fund estimate (Quadratic Funding)
web3-grant-tracker estimate-match \
  --project "OpenClaw Infrastructure" \
  --donor-count 50 \
  --round gitcoin-gg24
```

## 命令说明

| 命令            | 功能说明                                      |
|------------------|--------------------------------------------|
| `web3-grant-tracker scan` | 扫描所有活跃的资助轮次及其截止日期                    |
| `web3-grant-tracker urgent` | 显示未来7天内即将结束的资助轮次                   |
| `web3-grant-tracker add-project <项目名称>` | 注册项目以进行追踪                        |
| `web3-grant-tracker list-projects` | 列出您跟踪的所有项目                        |
| `web3-grant-tracker check-eligibility` | 检查您的项目是否符合资助轮次的要求                |
| `web3-grant-tracker estimate-match` | 计算您的匹配资金                        |
| `web3-grant-tracker apply-guide <轮次名称>` | 提供申请流程的详细指南                        |
| `web3-grant-tracker alerts-setup` | 配置截止日期提醒                        |
| `web3-grant-tracker history` | 查看过去的所有资助轮次及平均资助金额                |
| `web3-grant-tracker portfolio` | 查看所有项目的完整申请信息                        |

## 支持的平台

| 平台            | 可获取的数据                                      | 应用链接                                      |
|------------------|--------------------------------------------|-------------------------------------------|
| **Gitcoin Grants**     | 资助轮次、截止日期、匹配资金                        | grants.gitcoin.co                          |
| **Giveth**        | 项目列表、GIVbacks奖励                        | giveth.io                          |
| **Octant**        | Epoch资助计划及相关信息                        | octant.app                          |
| **Optimism RPGF**     | 过往的资助信息                            | app.optimism.io                          |
| **Arbitrum DAO**     | Arbitrum DAO的资助计划                        | forum.arbitrum.foundation                   |
| **ENS Ecosystem**   | 小额资助项目                            | discuss.ens.domains                     |
| **Uniswap Grants**     | Uniswap的UGP资助轮次                        | uniswapgrants.eth.limo                     |
| **Nouns Builder**     | Nouns Builder平台的特定资助轮次                    | nouns.build                        |

## 示例输出

```
╔═══════════════════════════════════════════════════╗
║   WEB3 GRANT TRACKER — 2026-02-25 02:30 UTC       ║
╠═══════════════════════════════════════════════════╣
║ ACTIVE ROUNDS (4 found)                           ║
╠═══════════════════════════════════════════════════╣
║ Gitcoin GG24 — Infrastructure                     ║
║   💰 Pool: ~$250,000 matching                     ║
║   ⏰ Closes: 2026-03-15 (18 days)                 ║
║   ✅ Your project: ELIGIBLE                        ║
╠═══════════════════════════════════════════════════╣
║ Octant Epoch 5                                    ║
║   💰 Pool: ~$800,000 ETH                          ║
║   ⏰ Closes: 2026-03-01 (4 days) ⚠️ URGENT       ║
║   ⚠️ Eligibility: check-eligibility to verify     ║
╠═══════════════════════════════════════════════════╣
║ Giveth GIVbacks Round 42                          ║
║   💰 Rewards: GIV tokens per donation             ║
║   ⏰ Rolling — no deadline                        ║
║   ✅ Your project: ELIGIBLE                        ║
╠═══════════════════════════════════════════════════╣

📊 QF MATCH ESTIMATE (Gitcoin GG24, 50 donors):
   Conservative: $180–450
   Optimistic:   $600–1,200
   (Based on 50 unique donors × avg $5 contribution)

💡 Recommendation: Apply to GG24 Infrastructure round
   → run: web3-grant-tracker apply-guide gitcoin-gg24
```

## 匹配资金计算器说明

该计算器倾向于奖励那些拥有大量小额捐赠者的项目，而非少数大额捐赠者的项目。

```bash
# See how adding more donors affects your match
web3-grant-tracker estimate-match \
  --project "my-project" \
  --round gitcoin-gg24 \
  --donor-count 100 \
  --avg-donation 10

# Output:
# sqrt(10) * 100 donors = 316 QF units
# Estimated match: $1,200–2,800 (depends on pool)
# Getting to 200 donors would 2x your match!
```

## 申请指南示例

```bash
web3-grant-tracker apply-guide gitcoin-gg24

# Output:
# GITCOIN GG24 — INFRASTRUCTURE ROUND APPLICATION GUIDE
# ═══════════════════════════════════════════════════════
# Step 1: Create project on Builder (builder.gitcoin.co)
#   → Connect GitHub + wallet
#   → Fill: name, description, links, banner image
# Step 2: Apply to round on Explorer (explorer.gitcoin.co)
#   → Select: Infrastructure/Tooling round
#   → Write impact statement (see templates below)
# Step 3: Community amplification
#   → Tweet with #GG24 #Gitcoin hashtags
#   → Post in Farcaster /gitcoin channel
#   → Share in relevant Discord servers
# Step 4: Donor drive
#   → Need 1 min donation ($1+) from unique wallets
#   → Each unique donor increases QF match
# ...
```

## 截止日期提醒示例

```
⏰ GRANT DEADLINE ALERT — 24h remaining

Round: Gitcoin GG24 — Infrastructure
Closes: 2026-03-15 20:00 UTC (in 23h 42m)
Your project: OpenClaw Infrastructure
Status: Applied ✅

Action items:
• Share project link for last-day donors
• Post reminder on social media
• Check you haven't hit any submission limits

Project link: explorer.gitcoin.co/projects/openclaw-infra
```

## 数据存储

所有数据存储在本地路径`~/.openclaw/workspace/web3-grant-tracker/`中。不使用任何遥测数据。资助轮次信息通过公共API和网络请求每6小时更新一次。

## 配置说明

```json
{
  "alert_channel": "whatsapp",
  "alert_advance_hours": [48, 24, 6],
  "wallet_address": "0xYourAddress",
  "default_tags": ["infrastructure", "open-source", "ai"],
  "auto_scan_interval_hours": 6
}
```

## 系统要求

- 需要OpenClaw 1.0及以上版本。
- 需要Python 3.8及以上版本。
- 可选：Ethereum钱包地址（用于链上验证）。

## 使用场景

- **项目开发者**：再也不错过任何资助机会。
- **DAO组织**：追踪生态系统的资助动态。
- **研究人员**：监控Web3领域的公共资源资助情况。
- **投资者**：提前识别资金充足的项目（通过捐赠者数量判断项目潜力）。

## 项目来源与问题反馈

- **项目来源**：https://github.com/mariusfit/web3-grant-tracker
- **问题反馈**：https://github.com/mariusfit/web3-grant-tracker/issues
- **开发者**：[@mariusfit](https://github.com/mariusfit)