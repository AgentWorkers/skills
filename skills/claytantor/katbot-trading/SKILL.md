---
name: katbot-trading
version: 0.1.6
description: 通过 Katbot.ai 在 Hyperliquid 平台上进行实时加密货币交易。该平台提供 BMI（市场分析工具）、代币选择功能以及基于 AI 的交易执行服务。
# Note: Homepage URL removed to avoid GitHub API rate limit errors during publish
metadata:
  {
    "openclaw":
      {
        "emoji": "📈",
        "requires": { "bins": ["python3"], "env": ["WALLET_PRIVATE_KEY", "KATBOT_HL_AGENT_PRIVATE_KEY"] },
        "primaryEnv": "KATBOT_HL_AGENT_PRIVATE_KEY",
        "install": "pip install -r requirements.txt"
      }
  }
---
# Katbot交易技能

该技能教会代理如何使用Katbot.ai API来管理Hyperliquid交易投资组合。

## 功能

1. **市场分析**：查看BTC动量指数（BMI）以及24小时内的涨跌情况。
2. **代币选择**：根据当前市场趋势自动挑选最佳代币。
3. **交易建议**：获取基于AI的交易策略（包括入场价、止盈价、止损价和杠杆率）。
4. **交易执行**：在用户确认后，在Hyperliquid平台上执行并关闭交易。
5. **投资组合监控**：实时跟踪未平仓头寸、盈亏情况以及账户余额。

## 设置要求

- **Katbot API**：`https://api.katbot.ai`
- **工具**：该技能依赖于标准的Python包。请运行安装命令来配置开发环境。
- **环境变量**：
  - `WALLET_PRIVATE_KEY`：您的MetaMask钱包私钥。**仅用于初次设置（SIWE登录）。**此密钥为临时密钥，不应保存在shell历史记录或环境变量文件中。如果会话过期，请重新执行初始化流程。
  - `KATBOT_HL_AGENT_PRIVATE_KEY`：用于Katbot投资组合的代理私钥。**这是日常交易操作的关键密钥**。初始化脚本会将此密钥安全地保存到`~/.openclaw/workspace/katbot-identity/katbot_secrets.json`文件中（权限设置为600）。
  - 或者，您也可以将其设置为环境变量以用于临时执行。
- **配置文件**：
  - 身份文件存储在`~/.openclaw/workspace/katbot-identity/`目录下（可通过`KATBOT_IDENTITY_DIR`进行配置）。
  - `katbot_config.json`：包含`wallet_address`、`portfolio_id`和`chain_id`信息。
  - `katbot_token.json`：包含用于身份验证的JWT令牌。

## 使用规则

- 在提出新的交易建议之前，**务必**先查看BMI。
- **未经用户明确确认**，**切勿**执行任何交易（例如：“确认执行AAVE的多头交易吗？”）。
- **切勿**在聊天中记录或泄露私钥。
- **对于任何交易建议**，**务必**报告风险/收益比率和杠杆率。

## 所需工具

该技能包含以下脚本（位于`{baseDir}/tools/`目录中，具体依赖项在`requirements.txt`中列出）：

- `katbot_onboard.py`：初次设置向导。通过SIWE使用您的钱包密钥进行身份验证，创建/选择投资组合，并将代理密钥保存到安全的身份目录中。
- `katbot_client.py`：用于身份验证和投资组合状态管理的核心API客户端。从身份目录中读取凭据。
- `katbot_workflow.py**：完整的交易流程脚本（从市场分析到交易建议）。
- `token_selector.py`：基于CoinGecko数据的代币选择工具。

## 初次设置流程

当用户首次安装此技能时，请指导他们完成以下初始化步骤：

```bash
# Install dependencies
pip install -r requirements.txt

# Run onboarding wizard
python3 {baseDir}/tools/katbot_onboard.py
```

向导将：
1. 如果环境变量中未设置`WALLET_PRIVATE_KEY`，则会提示用户输入该密钥（该密钥将以隐藏形式输入）。
2. 通过SIWE使用api.katbot.ai进行身份验证。
3. 列出现有的投资组合或创建一个新的投资组合。
4. 将`KATBOT_HL_AGENT_PRIVATE_KEY`和配置信息保存到`~/.openclaw/workspace/katbot-identity/`目录中。
5. 显示在Hyperliquid平台上授权代理的说明。

初始化完成后，该技能将使用保存的凭据自动运行。

要运行这些工具，请使用`exec`命令，并指定`PYTHONPATH={baseDir}/tools`。