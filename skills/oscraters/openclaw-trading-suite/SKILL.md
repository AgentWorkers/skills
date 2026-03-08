---
name: openclaw-trading-suite
description: Unified OpenClaw skill for autonomous algo and swing trading workflows: hypothesis generation, screening, technical/sentiment analysis, strategy-specific risk controls, execution gating, P&L and win-rate planning, and self-improvement loops backed by persistent trade data for ML/RL retraining.
---

# OpenClaw 交易套件

当用户需要端到端的交易代理功能时（涵盖分析、假设生成、风险管理、执行以及持续优化等环节），请使用此技能。

## 支持的范围

- **策略类型**：以“波段交易”为主，同时支持日内交易和事件驱动型策略。
- **资产类型**：默认支持股票和加密货币。
- **策略生命周期**：从研究开始，经过假设生成、验证、风险评估、执行、回顾，最终进入重新训练阶段。
- **数据保留**：所有决策、交易信号、成交结果以及模型版本都会被记录下来，以供后续分析使用。

## 核心工作流程

1. **数据采集**：整合市场数据、技术数据以及可选的轻度情绪/事件数据。
2. **策略筛选**：运行筛选器，生成可用于策略制定的候选股票/加密货币代码。
3. **策略构建**：明确设定入场、出场、策略失效的条件以及策略的置信度。
4. **应用特定策略的风险管理规则**（而非全局统一的静态策略）。
5. **执行控制**：根据回撤率、风险敞口和置信度阈值来决定是否执行交易。
6. **日志记录**：将每一步操作（包括研究过程、交易信号、订单执行结果及盈亏情况）持久化存储。
7. **定期评估**：定期检查策略的胜率、预期收益、回撤率等指标，并进行适应性调整。
8. **优化循环**：将交易结果反馈至优化/重新训练流程中，通过“冠军策略”与“挑战者策略”的对比进行评估。

## 策略目录

当用户需要具体策略或希望加入“4个机器人竞争”相关功能时，请参考 [references/strategy_profiles.md](references/strategy_profiles.md)。

## 数据模型与数据保留机制

在实现数据存储、分析或强化学习/机器学习训练功能时，请参考 [references/data_retention_schema.md](references/data_retention_schema.md)。

## 自主化设置

在配置用户自定义的自动化行为和审批流程时，请参考 [references/autonomymodes.md](references/autonomymodes.md)。

## 适配器扩展接口

在添加新的交易场所、数据源或研究工具时，请参考 [references/adapter_plugin_contract.md](references/adapter_plugin_contract.md)。

## 策略构建与执行控制

当用户需要自定义策略的触发条件或执行规则时，请参考 [references/strategy_builder_and_gates.md](references/strategy_builder_and_gates.md)。

## 保密性管理

在添加数据提供者、访问凭据或运行时配置时，请参考 [references/secrets_management.md](references/secrets_management.md)。

## 系统协调机制

在整合各个交易代理/工具、设定数据更新频率以及执行触发条件时，请参考 [references/system_orchestration.md](references/system_orchestration.md)。

## 执行策略的默认设置

- 除非用户明确要求，否则系统默认处于“模拟模式”（paper mode）。
- 新策略在首次实际执行前必须经过逐个假设的审批流程。
- 强制执行策略时需遵守策略内部的资金管理规则以及投资组合层面的风险控制机制。
- 如果策略在实时或模拟模式下的表现超出预设的回撤限制，系统将自动停止该策略的执行。

## 本仓库的代码复用指南

- 首先优先使用现有的模块，包括：`market-data-aggregator`、`technical-analysis-engine`、`risk-position-manager`、`strategy-optimizer`、`trade-signal-processor-executor`、`performance-reporter-learner`、`profit-forecaster` 和 `temp-rl-proto`。
- 请将较旧的 `SKILL.md` 文件视为组件级别的文档；本套件主要负责整个交易系统的协调与控制功能。
- 每晚的研究工作入口文件为 `scripts/nightly_research.py`。