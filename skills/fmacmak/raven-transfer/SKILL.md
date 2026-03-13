---
name: raven-transfer
description: 适用于NGN支付的、支持钱包管理的Raven Atlas转账操作：当代理需要检查钱包余额、处理尼日利亚银行账户相关事宜、强制使用确认令牌（confirmation tokens），以及向银行收款人或商户结算账户执行可重复执行的确认转账（idempotent confirmed transfers）时，应使用此功能。
---
# Raven Transfer Skill

通过Raven Atlas执行安全的NGN（Nigeria Naira）支付操作。

## 所包含的文件

- `scripts/raven-transfer.mjs`：转移操作的命令行界面（CLI）实现
- `agents/openai.yaml`：运行时所需的元数据和环境配置
- `references/*.md`：包含工作流程、命令契约、安全策略以及安装指南
- `tests/*.test.mjs`：用于单元测试和实时契约验证的脚本

## 使用该技能的步骤

1. 确定支付目标类型：`bank`（银行）或`merchant`（商户）。
2. 在进行任何转移之前，检查NGN钱包的余额以确保有足够的资金。
3. 根据账户号码和银行信息解析出账户名称。
4. 从转移预览界面获取明确的确认令牌。
5. 使用`--confirm="CONFIRM TXN_..."`选项仅执行一次转移操作。
6. 报告标准化后的结果字段（`available_balance`、`fee`、`total_debit`、`status`、`raw_status`）。

**注意：** 请务必执行确认令牌的检查，切勿自动重试转移操作。如果转移失败，通常会在几分钟后自动撤销/退款；请等待一段时间后，再次检查`transfer-status`和钱包余额后再尝试。

## 所需的环境配置

- 运行时环境中必须至少有一个认证源：
  - `RAVEN_API_KEY_FILE`（推荐使用，该文件应具有`chmod 600`或`chmod 400`权限）
  - `RAVEN_API_KEY`
- 可选的运行时配置参数：
  - `RAVEN_API_BASE`（默认值：`https://integrations.getravenbank.com/v1`）
  - `RAVEN_TIMEOUT_MS`（默认值：`30000`）
  - `RAVEN_READ_RETRIES`（默认值：`2`）
  - `RAVEN_RETRY_DELAY_MS`（默认值：`300`）
- 可选的安全增强设置：
  - `RAVEN_DISABLE_LOCAL_STATE=1`：禁用本地状态记录功能

## 调用规则

- 该技能不允许隐式调用模型；需要时请使用`$raven-transfer`命令显式调用。

## 运行命令

请从该技能文件夹中运行所有命令：

```bash
node ./scripts/raven-transfer.mjs --cmd=<command> [flags]
```

**可用命令：**

- `balance`：检查钱包余额并确认NGN是否可用。
- `banks`：列出所有银行（可选参数`--search`）。
- `lookup`：根据账户号码或银行代码解析账户名称。
- `transfer-status`：根据`trx_ref`/`merchant_ref`获取最新的转移状态，并检测转移是否被撤销。
- `transfer`：预览或执行带有确认令牌的银行转账操作。
- `transfer-merchant`：预览或执行针对商户的结算转账操作。

## 商户支付流程

将商户支付视为对商户结算账户的普通银行转账。

**所需的商户转账信息：**

- 商户名称
- 商户的结算银行名称及银行代码
- 商户的结算账户号码
- 通过`lookup`功能解析出的账户名称
- 转账金额
- 预计的费用估算
- 转账说明（备注）

## 参考文件

在执行前，请查阅以下文件：

- [references/workflow.md](references/workflow.md)：确定性的执行流程
- [references/commands.md](references/commands.md)：命令参数及标准化输出格式
- [references/safety.md](references/safety.md)：重试机制、幂等性及防止重复处理的规则
- [references/install.md](references/install.md)：相关规范及通用安装指南