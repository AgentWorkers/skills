---
name: raven-transfer
description: 支持钱包功能的Raven Atlas转账操作，适用于NGN（尼日利亚奈拉）的支付场景。当代理需要检查钱包余额、处理尼日利亚银行账户相关事务、强制使用确认令牌（confirmation tokens），以及向银行收款人或商户结算账户执行可重复执行的转账（idempotent transfers）时，应使用此功能。
---
# Raven Transfer Skill

通过Raven Atlas执行安全的NGN（Nigerian Naira）支付操作。

## 使用该技能的步骤：

1. 确定支付目标类型：`bank`（银行）或`merchant`（商户）。
2. 在进行任何转账之前，通过检查NGN钱包余额来验证资金是否充足。
3. 根据账户号码和银行信息查询对应的账户名称。
4. 从转账预览界面中获取明确的确认令牌（confirmation token）。
5. 使用`--confirm="CONFIRM TXN_..."`参数仅执行一次转账操作。
6. 报告标准化后的结果字段（`available_balance`、`fee`、`total_debit`、`status`、`raw_status`）。

**注意：**请务必进行确认令牌的检查，切勿自动重试转账操作。

## 所需环境：

- 运行时环境中必须包含`RAVEN_API_KEY`。
- 确保主机代理在运行命令时能够正确暴露该变量。

## 运行命令：

请使用以下命令来执行该技能中的所有操作：

```bash
node ./scripts/raven-transfer.mjs --cmd=<command> [flags]
```

**可用命令：**

- `balance`：检查钱包余额并确认NGN资金是否可用。
- `banks`：列出所有银行（可选参数`--search`）。
- `lookup`：根据账户号码或银行代码查询账户名称。
- `transfer-status`：通过`trx_ref`/`merchant_ref`获取最新的转账状态，并检测转账是否被撤销。
- `transfer`：预览或执行带有确认令牌的银行转账操作。
- `transfer-merchant`：预览或执行针对商户的结算转账操作。

## 商户付款流程：

将商户付款视为对商户结算账户的普通银行转账。

**所需的商户转账信息：**

- 商户名称
- 商户的结算银行名称及银行代码
- 商户的结算账户号码
- 通过查询得到的账户名称
- 转账金额
- 预计的转账费用（用于预检查）
- 付款说明（narration）

## 参考文件：

在执行前，请查阅以下文件：

- [references/workflow.md](references/workflow.md)：确定的执行流程。
- [references/commands.md](references/commands.md)：命令参数及标准化输出格式。
- [references/safety.md](references/safety.md)：重试机制、幂等性以及防止重复操作的规则。
- [references/install.md](references/install.md)：相关规范及通用安装指南。