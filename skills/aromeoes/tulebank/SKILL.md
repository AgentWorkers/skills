---
name: tulebank
description: **TuleBank** — 查看钱包余额、向任何CVU/ALIAS地址发送ARS（阿根廷比索）、兑换USDC/WARS（加密货币对）、管理受益人信息，以及将加密货币资金转入阿根廷银行账户。
user-invocable: true
metadata: {"clawdbot":{"requires":{"bins":["tulebank"]}}}
---
您可以使用 `tulebank` CLI 将阿根廷比索（ARS）通过 CVU 或 ALIAS 导入到任何银行账户中。`tulebank` 会与一个代理服务器通信，该代理服务器负责处理 Ripio Ramps API 的认证信息。

## CVU 与 ALIAS 的区别

- **ALIAS**：一个文本字符串（例如 `franv98`、`pilarcastilloz`、`tulezao`）。如果用户提供的是一个单词或简短文本，那么它就是一个别名。
- **CVU**：一个由 22 位数字组成的字符串（例如 `0000003100099123456789`）。如果用户提供的是一个长数字，那么它就是一个 CVU。
- 在 `beneficiaries add` 和 `send` 命令中，这两种格式都是有效的收款人地址。

## 重要规则

- 在执行 `tulebank send` 命令之前，**务必** 与用户确认收款人信息和转账金额。可以使用疑问句的形式进行确认（例如：“我应该将 3,000 阿根廷比索转给 Pilar Castillo (pilarcastilloz) 吗？”）。
- **仅通过 CLI 使用**：请通过 CLI 命令来操作 TuleBank，切勿导入 `lib/` 目录下的文件或使用自定义的 JavaScript 脚本来绕过 CLI。
- 所有命令都必须使用已安装的 `tulebank` 可执行文件。
- 如果 `tulebank` 未安装，请要求用户先安装它或设置正确的 PATH 环境变量后再继续操作。
- 当用户通过名称或描述来指定收款人时（例如 “la verdulería” 或 “mi hermano”），请先搜索收款人信息。
- 如果找到多个匹配项，请要求用户明确选择具体的收款人。
- 如果没有找到匹配项且用户提供了别名或 CVU，请运行 `beneficiaries add --to <alias_or_cvu>` 命令进行注册。Ripio 会返回收款人的姓名、CUIT（阿根廷税务识别号）和银行信息，请在转账前向用户展示这些信息并获取确认。`send` 命令需要已注册的收款人；系统不会自动创建新的收款人账户。
- CLI 的输出结果为 JSON 格式，请将其解析并以易于理解的方式呈现给用户。
- 在添加收款人或进行转账之前，用户必须先完成注册。如果尚未注册，请先运行 `tulebank signup` 命令。
- **OTP 验证**：对于现有的 Ripio 用户，`check-kyc` 会向他们的手机发送 OTP 码。请用户提供 6 位验证码，并使用 `otp --code <code>` 命令进行验证。
- `send` 命令会创建一个转账通道，用户需要将 USDC 或 wARS 存入指定的地址，Ripio 会将其转换为阿根廷比索并转账到银行。
- 如果用户配置了钱包（通过 `tulebank wallet setup` 命令），`send` 命令可以自动转账。在这种情况下，可以省略 `--token` 参数（系统会自动选择 wARS 或将 USDC 转换为 wARS）。
- `--to` 参数支持收款人姓名（例如 `--to Pili` 会匹配 “Pilar Castillo”）。系统支持名称前缀的匹配。
- 在自动转账前，系统会显示确认提示，包括收款人姓名、转账金额和收款人信息。用户必须确认后才能完成转账。只有在用户明确同意后，才能使用 `--yes` 参数跳过确认步骤。
- **法定货币账户激活**：Ripio 每位用户只能激活一个法定货币账户。`send` 命令会在转账前自动激活收款人的法定货币账户。如果账户被暂停，激活过程可能需要额外时间。
- 自动转账完成后，请显示交易哈希值，并运行 `tulebank history` 命令来确认交易记录。
- **货币兑换**：使用 `tulebank swap` 命令可以在 Base 平台上进行 USDC 和 wARS 之间的兑换。wARS 与阿根廷比索的兑换比例为 1:1，因此在转账前进行兑换可以锁定汇率。
- **转账金额**：当用户指定金额时，请使用 `--amount` 参数（单位为阿根廷比索），**切勿使用 `--token` 参数**。`--amount` 参数的值应为阿根廷比索金额。CLI 会自动处理转换（如果 wARS 可用则使用 wARS，否则会自动将 USDC 转换为 wARS）。**只有在用户明确要求转账 USDC 时才使用 `--token USDC` 参数**。
- **交易记录**：每次转账或兑换完成后，请运行 `tulebank history` 命令来确认交易记录。

## 可用的命令

这些命令都可以通过 `tulebank` CLI 可执行文件来执行。

### 钱包设置
```
tulebank wallet setup
```
通过代理服务器在 Base 平台上创建一个 CDP 智能钱包（无需使用本地凭证）。

### 查看钱包信息
```
tulebank wallet info
```
显示钱包地址。

### 查看钱包余额
```
tulebank wallet balance
```
显示钱包中的 USDC、wARS 和 ETH 余额。

### 注册账户（必备步骤）
```
tulebank signup --email <email> --phone <phone>
```
创建一个 TuleBank 账户，生成每个用户的 API 密钥，并保存到配置文件中。此操作只需执行一次。可以使用 `tulebank setup --api-key <key>` 在其他设备上登录。

### 完成用户身份验证（现有 Ripio 用户）
```
tulebank check-kyc
tulebank otp --code <123456>
```
`check-kyc` 会向用户的手机发送 OTP 码。请用户提供验证码，然后使用 `otp --code <code>` 进行验证。

### 查看用户身份验证状态
```
tulebank kyc-status
```

### 搜索收款人
```
tulebank beneficiaries search "<query>"
```
根据姓名、描述或 CVU/ALIAS 来搜索收款人。当用户通过名称或描述来指定收款人时可以使用此命令。

### 列出所有收款人
```
tulebank beneficiaries list
```

### 添加收款人
```
tulebank beneficiaries add --to <CVU_OR_ALIAS> [--name "<name>"] [--description "<desc>"]
```
通过代理服务器创建一个法定货币账户（包括创建、确认和激活流程），然后保存到本地。如果省略 `--name` 参数，系统会自动从 Ripio 数据库中获取收款人信息（包括姓名、CUIT 和银行信息）。响应中会包含 `holder` 字段，用于向用户确认收款人信息。

### 转账（使用现有收款人）
```
tulebank send --to <name/CVU_OR_ALIAS>
```
向已注册的收款人转账。`--to` 参数会根据别名或 CVU 进行匹配；如果找不到收款人，系统会提示用户先使用 `tulebank beneficiaries add` 命令进行添加。

### 从钱包自动转账
```
tulebank send --to <CVU_OR_ALIAS> --amount <n> --token <USDC|wARS>
```
创建转账通道，并自动从配置好的钱包向 Ripio 的存款地址转账。转账前会显示确认提示。可以使用 `--yes` 参数跳过确认步骤（仅在用户确认后使用）。

### 在 Base 平台上兑换货币
```
tulebank swap --from USDC --to wARS --amount 10
```
在 Base 平台上通过 DEX 进行货币兑换。默认滑点为 100 bps（1%）。可以使用 `--slippage <bps>` 参数调整滑点。使用 `--yes` 参数可以跳过确认步骤（仅在用户确认后使用）。

### 查看转账通道状态
```
tulebank send-status --session <session-id>
```
显示转账通道的存款地址和交易记录。

### 获取报价
```
tulebank quote --from USDC --to ARS --amount 10 [--chain BASE]
```

### 查看交易限额
```
tulebank limits
```

### 查看法定货币账户状态
```
tulebank fiat-account --id <fiat-account-id>
```

### 查看交易历史
```
tulebank history
tulebank history --beneficiary "<name>"
tulebank history --type send
tulebank history --from 2026-01-01 --to-date 2026-01-31
```
显示本地交易记录。支持按收款人、交易类型（`send`/`swap`）和日期范围进行过滤。默认显示最近 30 天的交易记录。

## 智能转账规则

- `--amount` 参数始终以阿根廷比索为单位（wARS 与阿根廷比索的兑换比例为 1:1）。**切勿手动将金额转换为 USDC**。
- 如果省略了 `--token` 参数且指定了转账金额，CLI 会自动选择 wARS（如果钱包中有足够的 wARS）或先将 USDC 转换为 wARS。
- 如果指定了 `--token` 参数，则会直接转账相应的代币（不会自动转换）。
- 例如：用户输入 “2300 比索” → 应输入 `--amount 2300`（而不是 `--amount 1.57 --token USDC`）。
- `--to` 参数支持收款人姓名。如果找到匹配项，系统会自动匹配；如果找到多个匹配项，则会显示匹配项列表。
- 每次转账后，交易记录会保存在 `~/.tulebank/history.json` 文件中。

## 示例操作流程

### 用户操作示例：
1. 用户说：“给 Pilar Castillo 转 10,000 阿根廷比索”
   - 搜索收款人 → 找到 “Pilar Castillo (pilarcastilloz)”。
   - 询问用户：“要给 Pilar Castillo 转 10,000 阿根廷比索吗？”
   - 确认后：运行 `send --to Pili --amount 10000 --yes`。
   - 显示交易哈希值。
   - 运行 `history --beneficiary Pili` 来确认交易记录。

2. 用户说：“给 ‘la verdulería’ 转钱”
   - 运行 `beneficiaries search "verdulería"`。
   - 如果找到收款人：询问用户：“要给 ‘la verdulería’ 转钱吗？”
   - 确认后：运行 `send --to <their_alias>`。
   - 显示存款地址和转账说明。

3. 用户说：“给 franv98 转 2,000 阿根廷比索”
   - 运行 `beneficiaries search "franv98"` → 未找到收款人。
   - “franv98” 是一个别名，运行 `beneficiaries add --to franv98` → Ripio 会返回收款人信息。
   - 询问用户：“franv98 属于 FRANCISCO VARELA（CUIT 20385..., Banco Galicia），要转 2,000 阿根廷比索吗？”
   - 确认后：运行 `send --to franv98 --amount 2000 --yes`。
   - 显示交易哈希值。
   - 运行 `history` 来确认交易记录。

4. 用户说：“转 0000003100099123456789”
   - 运行 `beneficiaries search "0000003100099123456789"` → 未找到收款人。
   - 这是一个 22 位的数字（CVU），运行 `beneficiaries add --to 0000003100099123456789` → Ripio 会返回收款人信息。
   - 询问用户：“这个 CVU 属于 MARÍA GARCÍA（CUIT 27..., Banco Nación），要确认转账吗？”
   - 确认后：运行 `send --to 0000003100099123456789`。
   - 显示存款地址和转账说明。

5. 用户说：“转给 tulezao”
   - 运行 `beneficiaries search "tulezao"` → 未找到收款人。
   - “tulezao” 是一个别名，运行 `beneficiaries add --to tulezao` → Ripio 会返回收款人信息。
   - 询问用户：“别名 tulezao 属于 JUAN PÉREZ（CUIT 20..., Banco Nación），要转账吗？”
   - 确认后：继续执行转账。

### 新用户注册流程（已有 Ripio 账户）
   - 询问用户的电子邮件和电话号码。
   - 运行 `signup --email <email> --phone <phone>`。
   - 运行 `check-kyc`（发送 OTP 码）。
   - 询问用户并提供 6 位验证码。
   - 运行 `otp --code <code>`。
   - 运行 `kyc-status` 以确认注册完成。

### 自动转账（钱包已配置）
   - 询问用户：“要给 Pilar Castillo 转 10,000 阿根廷比索吗？”
   - 确认后：运行 `send --to pilarcastilloz --amount 10000 --yes`。
   - `--amount` 参数以阿根廷比索为单位（10,000 表示 10,000 阿根廷比索）。CLI 会自动选择转账货币（如果钱包中有 wARS 则使用 wARS，否则会自动将 USDC 转换为 wARS）。
   - 显示交易哈希值。
   - 运行 `history` 来确认交易记录。

### 转账前兑换 USDC 为 wARS
   - 运行 `wallet balance` 查看钱包中的 USDC 余额。
   - 运行 `swap --from USDC --to wARS --amount 10`。
   - 显示兑换结果：“已将 10 USDC 兑换为 ~14,380 wARS”。
   - 运行 `send --to pilarcastilloz --amount 14380 --token wARS`。
   - wARS 会自动转换为阿根廷比索。

### 转账前查看汇率
   - 运行 `quote --from USDC --to ARS --amount 10`。
   - 告诉用户：“当前汇率下 10 USDC 等于 ~14,300 阿根廷比索”。