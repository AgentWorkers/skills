---
name: polymarket-bot
description: 自动化 Polymarket 机器人操作，包括获取市场数据、执行交易以及实施套利策略。适用于用户需要构建或运行用于预测市场的机器人、监控价格或在 Polygon 区块链上执行交易的情况。
---
# Polymarket Bot 技能

## 概述  
该技能用于创建和操作 Polymarket 机器人，可执行获取活跃市场信息、监控价格、下达订单以及运行交易策略等任务。它专为参与加密货币预测市场的用户设计，旨在通过 Polymarket API 自动化交互流程，同时降低风险。

## 快速入门  
要开始使用，请使用该技能中的脚本来初始化并运行一个基本机器人。例如，执行 `scripts/fetch_markets.py` 以获取活跃市场信息，然后使用 `scripts/bot_strategy.py` 进行套利检测。

## 基于任务的架构  
该技能按照标准操作流程（SOP）中的任务进行组织，为机器人开发提供了模块化的组件。

### 第 1 步：研究并准备前提条件  
- 阅读 SOP 中概述的 Polymarket API（Gamma、CLOB、Data）。  
- 确保已安装 Python 和 Web3.py 等工具。  
- 参考 `references/api_guide.md` 以了解详细的 API 使用方法。

### 第 2 步：定义机器人功能与策略  
- 实现数据获取和交易执行等核心功能。  
- 使用 `references/prompts.md` 中提供的提示生成策略相关代码。  
- 示例：运行 `scripts/strategy_logic.py` 进行套利检测。

### 第 3 步：开发阶段  
- **数据获取模块**：使用 `scripts/fetch_markets.py` 查询市场信息。  
- **身份验证与交易设置**：在 `scripts/auth_setup.py` 中处理。  
- **测试与部署**：使用 `scripts/test_bot.py` 进行测试，并通过指定方式部署机器人。

### 第 4 步：潜在挑战及应对措施  
- 参考 `references/challenges.md` 了解速率限制、费用及安全相关注意事项。

### 第 5 步：资源  
- 请参阅以下基于 SOP 的脚本和参考资料。

## 资源  

### scripts/  
- `fetch_markets.py`：从 Polymarket API 获取并解析市场数据的脚本。  
- `auth_setup.py`：处理身份验证并生成 API 密钥。  
- `strategy_logic.py`：实现套利等交易策略。  
- `bot_integration.py`：将各阶段整合为完整的机器人脚本。

### references/  
- `api_guide.md`：关于 Polymarket API 及设置的文档。  
- `strategy_examples.md`：用于生成策略代码的提示示例。  
- `challenges.md`：机器人开发中常见的问题及应对方法。

### assets/  
- （目前该技能无需使用任何资产。）