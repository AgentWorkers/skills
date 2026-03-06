---
name: katbot-trading
version: 0.2.9
description: 通过 Katbot.ai 在 Hyperliquid 平台上进行实时加密货币交易。该平台提供 BMI（市场分析工具）、代币选择功能以及基于人工智能的交易执行服务。
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

1. **市场分析**：查看BTC动量指数（BMI）以及24小时内的收益/亏损情况。
2. **代币选择**：根据当前市场趋势自动挑选最佳代币。
3. **交易建议**：获取基于AI的交易设置（入场价、止盈价、止损价、杠杆率）。
4. **交易执行**：在用户确认后，在Hyperliquid平台上执行并关闭交易。
5. **投资组合监控**：监控未平仓头寸、盈亏情况以及账户余额。

## 设置要求

- **Katbot API**：`https://api.katbot.ai`
- **工具**：该技能使用标准的Python包。运行安装命令来配置环境。
- **环境变量**：
  - `WALLET_PRIVATE_KEY`：您的MetaMask钱包私钥。**仅用于SIWE登录。**此密钥是临时性的，不应保存在shell历史记录或环境变量文件中。如果会话过期，请重新执行登录流程。
  - `KATBOT_HL_AGENT_PRIVATE_KEY`：用于Katbot投资组合的代理私钥。**这是日常交易操作的关键密钥**。
    - 登录脚本会将此密钥安全地保存到`~/.openclaw/workspace/katbot-identity/katbot_secrets.json`文件中（权限设置为600）。
    - 或者，您也可以将其设置为环境变量以用于临时执行。
- **配置文件**：
  - 身份文件存储在`~/.openclaw/workspace/katbot-identity/`目录下（可通过`KATBOT_IDENTITY_DIR`进行配置）。
  - `katbot_config.json`：包含`wallet_address`、`portfolio_id`和`chain_id`。
  - `katbot_token.json`：包含`access_token`和`refresh_token`（权限设置为600）。

## 认证流程

该技能通过`katbot_client.get_token()`自动管理代币：

1. **检查访问令牌有效期**：解码`katbot_token.json`中的JWT `exp`字段。如果有效（在60秒内未过期），则直接使用该令牌。
2. **令牌过期时刷新**：如果访问令牌已过期但`refresh_token`仍然有效，使用`{"refresh_token": "<token>"}`发起`POST /refresh`请求。成功后，新的`access_token`和`refresh_token`会自动保存回`katbot_token.json`文件中。
3. **刷新失败时重新认证**：如果`refresh_token`也过期或丢失，则通过`POST /login`进行完整的SIWE重新认证。这需要`WALLET_PRIVATE_KEY`。

**请务必在`/refresh`请求能够成功执行的情况下，****切勿直接调用`/login`。

## 使用规则

- **在建议任何新交易之前**，**必须**检查BMI。
- **未经用户明确确认**，**严禁**执行任何交易（例如：“确认执行AAVE多头交易吗？”）。
- **严禁**在聊天中记录或泄露私钥。
- **对于任何交易建议**，**必须**报告风险/回报比和杠杆率。
- **始终**让`get_token()`自动处理代币刷新——切勿手动管理代币。

## 工具

所有脚本位于`{baseDir}/tools/`目录下（依赖项在`requirements.txt`文件中）：

- `ensure_env.sh`：**在运行任何工具之前执行**。检查当前技能版本所需的依赖项是否已安装，如需则重新安装。每次运行都是安全的——如果依赖项已安装完毕，该脚本会立即退出。
- `katbot_onboard.py`：首次设置向导。使用您的钱包密钥通过SIWE进行认证，创建/选择投资组合，并将代理密钥保存到安全的身份目录中。
- `katbot_client.py`：用于认证和投资组合状态管理的核心API客户端。从身份目录中读取凭证。
- `katbot_workflow.py`：端到端的交易工作流程（从市场分析到交易建议）。
- `token_selector.py`：基于CoinGecko的数据选择最佳代币的脚本。

## 环境管理

该技能通过`{baseDir}/.installed_version`文件来跟踪已安装依赖项的版本。当技能升级时，文件中的版本号会与技能版本不匹配，`ensure_env.sh`会自动重新运行`pip install`命令来安装新的依赖项。

**代理在每次使用工具之前**，**必须**运行`ensure_env.sh`：

```bash
bash {baseDir}/tools/ensure_env.sh {baseDir}
```

- 如果文件中的版本号与当前版本匹配：立即退出（快速完成，无需执行`pip`命令）。
- 如果技能已升级或从未安装过：运行`pip install -r requirements.txt`并更新文件中的版本号。
- 如果系统缺少`python3`，会显示错误信息并退出（退出代码为1）。

### 检测升级

如果用户告知技能已更新，或者某个工具因`ImportError`或`ModuleNotFoundError`而失败，请务必先运行`ensure_env.sh`以同步依赖项。

## 首次设置

当用户首次安装此技能时，引导他们完成以下步骤：

```bash
# Ensure dependencies are installed
bash {baseDir}/tools/ensure_env.sh {baseDir}

# Run onboarding wizard
python3 {baseDir}/tools/katbot_onboard.py
```

向导将：
1. 如果环境变量中未设置`WALLET_PRIVATE_KEY`，会提示用户输入该密钥（输入方式为隐藏方式）。
2. 通过SIWE使用您的钱包密钥进行认证。
3. 列出现有的投资组合或创建一个新的投资组合。
4. 将`KATBOT_HL_AGENT_PRIVATE_KEY`和配置信息保存到`~/.openclaw/workspace/katbot-identity/`目录中。
5. 显示在Hyperliquid平台上授权代理的说明。

完成设置后，该技能将使用保存的凭证自动运行。

要运行这些工具，请使用`exec`命令，并指定`PYTHONPATH={baseDir}/tools`。