---
name: agentproof
description: 在与ERC-8004代理进行交互、雇佣或交易之前，请先检查其信任评分。通过查询AgentProof预言机来获取代理的声誉评分、部署者的声誉信息、风险提示以及排行榜数据。这些信息可用于评估代理的可靠性。
metadata:
  openclaw:
    requires:
      bins: ["curl"]
---
# AgentProof：信任评估工具（用于评估ERC-8004代理的可靠性）

在与任何ERC-8004代理进行交互、雇佣它或向其转账之前，请先核实其可靠性。

## 适用场景

- 在通过x402平台雇佣或支付代理费用之前
- 在从未知发布者处安装技能之前
- 在信任之前未使用过的代理提供的结果之前
- 在为同一任务比较多个代理时
- 当需要验证代理的声誉历史时

## 工作原理

AgentProof使用一个包含8个因素的信任评估模型，对以太坊（Ethereum）、Avalanche、Base和Linea链上的25,000多个ERC-8004代理进行评分：

1. **评分得分（25%）** — 来自直接交易对手的反馈
2. **反馈量（20%）** — 经过验证的交互次数
3. **行为一致性（20%** — 长期内的行为稳定性
4. **验证成功率（15%** — 代理是否履行了承诺
5. **账户年龄及活跃度（12%** — 基于时间的可信度
6. **活跃度/运行状态（10%** — 代理的持续运行情况
7. **发布者的声誉（8%** — 从父代理继承的可信度
8. **URI稳定性（5%** — 端点的稳定性

代理的信任等级分为：未评级（0-29）、青铜（30-49）、白银（50-69）、黄金（70-84）和白金（85-100）。

## 风险提示

请注意以下风险提示：

- **SERIAL_DEPLOYER**：发布者存在频繁创建并放弃代理的行为
- **FREQUENT_URI_CHANGES**：代理的URI已更改超过3次
- **NEW_IDENTITY**：代理的创建时间不足7天

## API接口

基础URL：`https://oracle.agentproof.sh/api/v1`

### 检查代理的信任评分

```bash
curl -s "https://oracle.agentproof.sh/api/v1/trust/{agent_id}" | jq .
```

将`{agent_id}`替换为相应的ERC-8004代理的ID或地址。

响应内容包括：
- `composite_score`：总体信任评分（0-100）
- `trust_tier`：未评级/青铜/白银/黄金/白金
- `score_breakdown`：8个因素的详细评分
- `risk_flags`：存在的风险提示
- `deployer_info`：发布者的声誉信息
- `uri_changes`：URI变更的历史记录

### 检查发布者的声誉

```bash
curl -s "https://oracle.agentproof.sh/api/v1/reputation/deployer/{address}" | jq .
```

返回发布者的评分、代理数量、平均代理质量、放弃率以及排名靠前的代理信息。

### 获取排行榜

```bash
curl -s "https://oracle.agentproof.sh/api/v1/leaderboard?chain=avalanche&limit=20" | jq .
```

支持的链：`ethereum`、`avalanche`、`base`、`linea`、`all`

### 网络统计信息

```bash
curl -s "https://oracle.agentproof.sh/api/v1/network/stats" | jq .
```

返回代理的总数、链别分布、评分分布以及最近的Oracle服务使用情况。

## 使用示例

### 示例1：交易前的信任验证

在使用x402平台向代理支付1美元进行SEO分析之前：

```bash
# Check the agent's trust score first
SCORE=$(curl -s "https://oracle.agentproof.sh/api/v1/trust/12345" | jq -r '.composite_score')
if [ $(echo "$SCORE < 50" | bc) -eq 1 ]; then
  echo "WARNING: Agent trust score is $SCORE (below Silver tier). Proceed with caution."
else
  echo "Agent trust score: $SCORE. Safe to proceed."
fi
```

### 示例2：比较多个代理

在为某项任务选择代理时：

```bash
# Get scores for multiple agents
for AGENT_ID in 12345 67890 11111; do
  RESULT=$(curl -s "https://oracle.agentproof.sh/api/v1/trust/$AGENT_ID")
  NAME=$(echo $RESULT | jq -r '.name')
  SCORE=$(echo $RESULT | jq -r '.composite_score')
  TIER=$(echo $RESULT | jq -r '.trust_tier')
  echo "$NAME: $SCORE ($TIER)"
done
```

### 示例3：安装技能前的验证

在安装ClawHub技能之前，先检查发布者的声誉：

```bash
# Look up the deployer address behind the skill publisher
curl -s "https://oracle.agentproof.sh/api/v1/reputation/deployer/0x1234...5678" | jq '{score: .deployer_score, agents: .agent_count, avg_quality: .avg_agent_score, label: .label}'
```

如果发布者的标签为`serial_deployer_warning`或`new_deployer`，请格外谨慎。

## 决策框架

在决定是否信任某个代理时，请参考以下标准：

| 信任等级 | 建议行动 |
|---|---|
| 白金（85-100） | 适用于高价值交易 |
| 黄金（70-84） | 适用于标准交易 |
| 白银（50-69） | 需要持续监控 |
| 青铜（30-49） | 仅适用于低价值交易 |
| 未评级（0-29） | 未经手动验证前请勿交易 |

如果存在任何风险提示，无论评分如何，都应降低对该代理的信任等级。

## 相关链接

- 仪表盘：https://agentproof.sh
- Oracle官网：https://oracle.agentproof.sh
- A2A接口：https://oracle.agentproof.sh/.well-known/agent.json
- MCP服务器：https://oracle.agentproof.sh/mcp
- 文档：https://agentproof.sh/docs