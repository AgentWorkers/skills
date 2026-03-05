---
name: riskofficer
description: 投资组合风险管理与分析功能：当用户需要计算风险价值（VaR）、执行蒙特卡洛模拟、进行压力测试、运用风险均衡（Risk Parity）、卡尔马（Calmar）或布莱克-利特曼（Black-Litterman）模型进行优化、进行交易前检查、监控行业集中度、管理投资组合或分析投资组合之间的相关性时，均可使用这些功能。此外，该系统还支持股票代码搜索、与经纪商的数据同步、批量创建投资组合以及投资组合之间的对比分析。
metadata: {"openclaw":{"requires":{"env":["RISK_OFFICER_TOKEN"]},"primaryEnv":"RISK_OFFICER_TOKEN","emoji":"📊","homepage":"https://riskofficer.tech"}}
---
## RiskOfficer投资组合管理

该技能通过连接RiskOfficer API来管理投资组合并计算财务风险指标。

**所需环境变量：** `RISK_OFFICER_TOKEN`（在RiskOfficer应用程序的设置 → API密钥中创建）。无需其他环境变量或二进制文件。

**来源：** 官方技能仓库：[github.com/mib424242/riskofficer-openclaw-skill](https://github.com/mib424242/riskofficer-openclaw-skill)；产品官网：[riskofficer.tech](https://riskofficer.tech)。该技能仅使用RiskOfficer应用程序生成的token，不会收集或存储任何凭证。

### 凭证和token处理

- **该技能不会存储或记录您的token。** Token仅通过HTTP `Authorization`头发送到`api.riskofficer.tech`；不会被写入磁盘、记录或发送到其他地方。您存储token的位置（环境变量或`~/.openclaw/openclaw.json`）完全由您控制。
- **建议** 将`RISK_OFFICER_TOKEN`设置为会话环境变量，而不是保存在`openclaw.json`中。如果使用`openclaw.json`，请限制文件权限，并注意哪些代理或用户可以读取该文件。
- **RiskOfficer目前仅发放账户级别的token**（不提供有范围的token）。为此技能创建一个token（例如“OpenClaw”），并在停止使用该技能时在RiskOfficer应用程序中撤销它。
- **Token权限：** Token允许该技能访问您的RiskOfficer数据（投资组合、风险计算、用于仅读分析的经纪商同步头寸）。如果需要撤销访问权限，请撤销或轮换token。
- **验证链接：** 在安装或提供token之前，请确认[github.com/mib424242/riskofficer-openclaw-skill](https://github.com/mib424242/riskofficer-openclaw-skill)和[riskofficer.tech](https://riskofficer.tech)与您信任的发布者匹配。

### 使用范围：** 仅用于分析和研究（虚拟投资组合）

**此技能中的所有投资组合数据和操作都在RiskOfficer自己的环境中进行。** 您在这里创建、编辑或优化的投资组合是**虚拟的**——仅用于分析和研究。该代理可以：
- **读取** 您的投资组合（包括从经纪商同步的头寸）、历史记录和风险指标
- **在RiskOfficer内部创建和更改** 虚拟/手动投资组合并运行优化
- **对这些投资组合运行计算**（VaR、蒙特卡洛、压力测试）

**此技能不会在您的经纪商账户中放置或执行任何实际订单。** 经纪商同步数据仅用于分析；任何重新平衡或交易都在您的经纪商应用程序或RiskOfficer自己的流程中完成，而不是由助手完成。Token仅用于访问RiskOfficer的API以进行这些分析和研究用途。

### 设置

1. 打开RiskOfficer应用程序 → 设置 → API密钥
2. 创建一个名为“OpenClaw”的新token
3. 设置环境变量：`RISK_OFFICER_TOKEN=ro_pat_...`

或者在`~/.openclaw/openclaw.json`中配置：
```json
{
  "skills": {
    "entries": {
      "riskofficer": {
        "enabled": true,
        "apiKey": "ro_pat_..."
      }
    }
  }
}
```

### API基础URL

```
https://api.riskofficer.tech/api/v1
```

所有请求都需要：`Authorization: Bearer ${RISK_OFFICER_TOKEN}`

### 货币政策

- **支持的货币：** 仅支持** RUB和USD。API合约和分析货币中不支持EUR/CNY/其他货币。
- **外汇来源：** 所有汇率均来自**俄罗斯中央银行（CBR）**通过数据服务（MOEX/CBR）。没有其他提供商可供选择。
- **每个投资组合只能包含一种货币：** 每个投资组合必须包含同一货币的资产（全部为MOEX或全部为USD）。不支持混合货币的投资组合；请创建单独的投资组合。
- **聚合视图：** 用户选择`base_currency`（RUB或USD）；其他货币的子投资组合将使用CBR汇率进行转换。