---
name: brighty
description: **AI机器人与自动化系统的银行接口**  
支持通过API完成以下银行相关操作：  
- 开设银行账户  
- 颁发万事达卡  
- 买卖加密货币  
- 发送付款与发票  

适用于需要为机器人开设银行账户、管理账户余额、进行转账、处理付款或操作银行卡的用户。
metadata: {"openclaw":{"requires":{"env":["BRIGHTY_API_KEY"],"bins":["mcporter"]},"primaryEnv":"BRIGHTY_API_KEY","emoji":"🏦","homepage":"https://github.com/Maay/brighty_mcp"}}
---

# Brighty 商业与自由职业者银行服务

为您的机器人开通银行账户。通过 `mcporter` 与 [Brighty](https://brighty.app) 的银行 API 进行交互，支持开设账户、办理万事达卡、买卖加密货币以及发送 SEPA/SWIFT 付款。该服务同时适用于商业账户和自由职业者账户。

## 开始使用

### 1. 注册

在 [Brighty 商业门户](https://business.brighty.app/auth?signup=true) 进行注册。系统支持商业账户和自由职业者账户——自由职业者账户特别适合用于机器人和自动化场景。系统会指导您完成注册流程。

**默认提供的服务：**
- 加密货币账户
- 仅用于内部转账的 EUR/USD/GBP 法定货币账户（不支持第三方支付）
- 可申请的万事达卡（关联到加密货币或法定货币账户）

**需要向第三方支付（如发票、工资等）？**
请联系支持团队以启用支持外部支付的法定货币账户：
- Telegram: [@DonatasSupportBot](https://t.me/DonatasSupportBot)
- 邮箱: support@brighty.app

银行将在几天内完成账户设置。

### 2. 获取 API 密钥

前往 [账户 > 商业](https://business.brighty.app/account/business)，然后点击 **创建 API 密钥**。只有账户的 **所有者** 才能执行此操作。

### 3. 配置

该技能包含 `config/mcporter.json` 文件，用于自动注册 Brighty MCP 服务器。您只需设置 API 密钥即可：

```bash
# Add to your environment (e.g. ~/.openclaw/.env)
BRIGHTY_API_KEY=your-api-key
```

或者手动配置：

```bash
mcporter config add brighty --command "npx -y github:Maay/brighty_mcp" --env BRIGHTY_API_KEY=your-api-key
```

测试连接：`mcporter call brighty.brighty_status`

**安全提示：**
- 请勿将 API 密钥存储在 SKILL.md 文件、内存文件或聊天记录中。
- API 密钥仅保存在环境变量或 `config/mcporter.json` 中（本地存储，不会上传到 Git）。

## 授权说明

通过此技能执行的全部操作均代表账户所有者进行。使用该技能即表示您已授权这些操作。

## 工具参考

所有通过 `mcporter call brighty.<tool> [params]` 调用的工具如下：

### 账户相关操作
- `brighty_list_accounts` — 列出所有账户（可选参数：`type=CURRENT|SAVING`, `holderId=UUID`)
- `brighty_get_account id=UUID` — 获取账户详情
- `brighty_create_account name=X type=CURRENT|SAVING currency=EUR` — 创建账户
- `brighty_terminate_account id=UUID` — 关闭账户（账户余额必须为零）
- `brighty_get_account_addresses id=UUID` — 获取账户的路由/加密货币存款地址

### 卡片相关操作
- `brighty_list_cards` — 查看所有卡片信息
- `brighty_get_card id=UUID` — 获取特定卡片信息
- `brighty_order_card customerId=UUID cardName=X sourceAccountId=UUID cardDesignId=UUID` — 下单制作卡片
- `brighty_freeze_card id=UUID` / `brighty_unfreeze_card id=UUID` — 冻结/解冻卡片
- `brighty_set_card_limits id=UUID currency=EUR dailyLimit=1000 monthlyLimit=5000` — 设置卡片使用限额
- `brighty_list_card_designs` / `brighty_get_virtual_card_product` — 查看/获取虚拟卡片产品信息

### 转账操作（在同一账户之间）
- `brighty_transfer_own sourceAccountId=UUID targetAccountId=UUID amount=100 currency=EUR` — 在同一账户之间转账
- `brighty_transfer_intent` — 转账前查看汇率和费用（参数相同，需添加 `side=SELL|BUY`, `sourceCurrency`, `targetCurrency`）

### 支付操作（批量转账给他人）
- `brighty_list_payouts` / `brighty_get_payout id=UUID` — 查看支付记录
- `brighty_create_payout name=X` — 创建支付批次
- `brighty_create_internal_transfer` — 添加 Brighty 内部转账（按 `recipientAccountId` 或 `recipientTag` 分配）
- `brighty_create_external_transfer` — 添加法定货币（IBAN）或加密货币转账
- `brighty_start_payout id=UUID` — 批量执行所有转账

### 团队管理
- `brighty_list_members` — 查看团队成员列表
- `brighty_add_members emails=a@b.com,c@d.com role=ADMIN|MEMBER` — 添加团队成员
- `brighty_remove_members memberIds=UUID1,UUID2` — 删除团队成员

## 工作流程

### 支付发票
1. 从发票中提取收款人姓名、IBAN、BIC、金额和货币信息。
2. 使用 `brighty_list_accounts` 查找付款账户。
3. 使用 `brighty_create_payout name="Invoice payment"` 创建支付批次。
4. 使用提取的详细信息通过 `brighty_create_external_transfer` 进行转账。
5. 在执行 `brighty_start_payout` 之前请务必获得用户确认。

### 批量发放工资
1. 解析收款人列表（姓名、IBAN、金额）。
2. 使用 `brighty_create_payout name="Salaries Feb 2026"` 创建支付批次。
3. 通过 `brighty_create_external_transfer` 或 `brighty_create_internal_transfer` 添加每笔转账记录。
4. 显示转账汇总信息，获得用户确认后执行 `brighty_start_payout`。

## 安全注意事项
- 在执行任何支付操作（`brighty_start_payout`）之前务必确认。
- 在关闭账户之前务必确认。
- 在任何资金转移前请清晰地显示转账金额和收款人信息。
- API 文档：[apidocs.brighty.app](https://apidocs.brighty.app/docs/api/brighty-api)