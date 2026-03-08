---
name: tulebank
description: TuleBank — 支持查询钱包余额、向任何CVU/ALIAS地址发送ARS（TuleBank的代币），进行USDC与WARS之间的兑换，管理受益人，并支持通过ARS进行资金的转入/转出操作。
user-invocable: true
metadata: {"clawdbot":{"requires":{"bins":["tulebank"]}}}
---
您可以通过CVU或ALIAS将阿根廷比索（ARS）汇入任何银行账户，并使用`tulebank` CLI从ARS银行转账中为钱包充值。`tulebank` CLI会与一个代理服务器通信，该代理服务器负责处理Ripio Ramps API的认证信息。

## CVU与ALIAS的区别

- **ALIAS**：一个文本字符串（例如：`franv98`、`pilarcastilloz`、`tulezao`）。如果用户提供的是一个单词或简短的文本，那么它就是一个别名。
- **CVU**：一个22位的数字字符串（例如：`0000003100099123456789`）。如果用户提供的是一个长数字，那么它就是一个CVU。
- 两者都可以作为`beneficiaries add`和`send`命令中的`--to`参数的有效接收方。

## 重要规则

- 在执行`tulebank send`命令之前，**务必**与用户确认收款人和转账金额。使用疑问句的形式进行确认（例如：“我应该向Pilar Castillo（pilarcastilloz）转账3000阿根廷比索吗？”）。
- **仅通过CLI使用**：请通过`tulebank`的CLI命令来操作该工具，不要导入`lib/`目录下的文件或使用自定义的JavaScript代码来绕过CLI。
- 所有命令都应使用已安装的`tulebank`二进制文件。
- 如果`tulebank`不可用，请要求用户先安装它或设置正确的PATH环境变量后再继续操作。
- 当用户通过名称或描述来指定收款人时（例如：“la verdulería”、“mi hermano”），请先搜索收款人信息。
- 如果找到多个匹配项，请要求用户明确指定收款人。
- 如果没有找到匹配项且用户提供了别名或CVU，请运行`beneficiaries add --to <alias_or_cvu>`来注册收款人。Ripio会返回收款人的姓名、CUIT（税务识别号）和银行信息，请向用户展示这些信息并获取确认。`send`命令需要已注册的收款人；系统不会自动创建收款人。
- CLI的输出格式为JSON，请将其解析并以易于理解的方式呈现给用户。
- 用户在添加收款人或进行转账之前必须先完成注册。如果未完成注册，请先运行`tulebank signup`命令。
- **OTP验证**：对于现有的Ripio用户，`check-kyc`会向他们的手机发送OTP验证码。请用户提供6位验证码，并使用`otp --code <code>`进行验证。
- `send`命令会创建一个转账会话，并返回收款地址。用户需要将USDC或wARS充值到该地址，Ripio会将其转换为ARS并转账给银行。
- 如果用户已配置了钱包（通过`tulebank wallet setup`命令），则可以使用`--amount`参数自动转账。如果省略`--token`参数，系统会自动选择wARS或进行USDC到wARS的转换。
- `--to`参数可以接受收款人名称（例如：`--to Pili`会匹配“Pilar Castillo”）。系统支持名称前缀的匹配。
- 在自动转账前，系统会显示包含收款人名称、转账金额和收款地址的确认提示。用户必须确认后才能继续转账。只有在用户已经明确确认后，才能使用`--yes`参数跳过确认提示。
- **法定货币账户激活**：Ripio每位用户仅允许激活一个法定货币账户。`send`命令会在转账前自动激活收款人的法定货币账户。如果账户被暂停，激活过程可能需要额外时间。
- 自动转账完成后，请显示交易哈希值，并运行`tulebank history`命令来确认交易记录。

## 可用的命令

这些命令都可以通过`tulebank` CLI二进制文件使用`exec`工具来执行。

### 钱包设置
```
tulebank wallet setup
```
通过代理服务器在Base平台上创建一个CDP智能钱包（无需使用本地凭证）。

### 查看钱包信息
```
tulebank wallet info
```
显示钱包地址。

### 查看钱包余额
```
tulebank wallet balance
```
显示钱包中的USDC、wARS和ETH余额。

### 注册账户（必备步骤）
```
tulebank signup --email <email> --phone <phone>
```
创建一个TuleBank账户，生成每个用户的API密钥，并将其保存在配置文件中。此步骤只需执行一次。可以使用`tulebank setup --api-key <key>`在其他设备上登录。

### 完成KYC验证（现有Ripio用户）
```
tulebank check-kyc
tulebank otp --code <123456>
```
`check-kyc`会向用户的手机发送OTP验证码。请用户提供验证码，然后使用`otp --code <code>`进行验证。

### 检查KYC验证状态
```
tulebank kyc-status
```

### 搜索收款人
```
tulebank beneficiaries search "<query>"
```
根据名称、描述或CVU/ALIAS来搜索收款人。当用户通过名称或描述来指定收款人时可以使用此命令。

### 列出所有收款人
```
tulebank beneficiaries list
```

### 添加收款人
```
tulebank beneficiaries add --to <CVU_OR_ALIAS> [--name "<name>"] [--description "<desc>"]
```
通过代理服务器创建一个法定货币账户（包括创建、确认和激活流程），然后保存到本地。如果省略`--name`参数，系统会自动从Ripio数据库中检测收款人的信息（包括姓名、CUIT和银行信息）。响应中包含`holder`字段，用于向用户确认收款人信息。

### 转账（离线转账）
```
tulebank send --to <name/CVU_OR_ALIAS>
```
向已注册的收款人转账。`--to`参数会根据别名或CVU进行精确匹配；如果找不到收款人，系统会提示用户先使用`tulebank beneficiaries add`命令添加收款人。

### 自动转账（从钱包转账）
```
tulebank send --to <CVU_OR_ALIAS> --amount <n> --token <USDC|wARS>
```
创建离线转账会话，并自动从配置好的钱包向Ripio的存款地址转账。转账前会显示确认提示。可以使用`--yes`参数跳过确认提示（仅在用户确认后）。使用`--manual`参数可以完全跳过自动转账流程。

### 在Base平台上兑换代币
```
tulebank swap --from USDC --to wARS --amount 10
```
通过DEX平台兑换代币。默认滑点为100 bps（1%）。可以使用`--slippage <bps>`参数调整滑点。使用`--yes`参数可以跳过确认提示（仅在用户确认后）。

### 查看离线转账会话状态
```
tulebank send-status --session <session-id>
```
显示离线转账会话的存款地址和交易记录。

### 获取转账报价
```
tulebank quote --from USDC --to ARS --amount 10 [--chain BASE]
```

### 创建转账流程（ARS -> wARS或USDC）
```
tulebank onramp quote --amount 50000 [--asset wARS|USDC] [--chain BASE]
```

### 创建转账流程（银行转账）
```
tulebank onramp create --amount 50000 [--asset wARS|USDC] [--to-address 0x...] [--chain BASE]
```
使用最新的报价创建转账流程。`wARS`选项会创建会话；`USDC`选项会创建订单。可以使用配置好的钱包地址；如果需要，可以通过`--to-address`参数进行修改。

### 查看转账流程状态
```
tulebank onramp status --transaction <transaction-id> [--asset wARS|USDC]
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
tulebank history --type onramp
tulebank history --from 2026-01-01 --to-date 2026-01-31
```
显示本地交易历史记录。支持按收款人、交易类型（`send`/`swap`/`onramp`）和日期范围进行过滤。默认显示过去30天的交易记录。

## 智能转账规则

- `--amount`参数始终以ARS为单位（等于wARS，比例为1:1）。**不要**手动将金额转换为USDC。
- 如果省略`--token`参数且指定了`--amount`参数，系统会自动选择wARS（如果余额足够）或先进行USDC到wARS的转换。
- 如果指定了`--token`参数，系统会直接转账相应的代币（不会自动转换）。
- 例如：用户输入“2300比索”，则应输入`--amount 2300`（而不是`--amount 1.57 --token USDC`）。
- `--to`参数可以接受收款人名称（例如：`--to Pili`）。如果找到匹配项，系统会自动匹配；如果找到多个匹配项，系统会显示列表供用户选择。
- 每次转账后，交易记录会被保存在`~/.tulebank/history.json`文件中。

## 示例操作流程

### 用户请求：“转账10000阿根廷比索给Pilar Castillo”
1. 搜索收款人 → 找到“Pilar Castillo (pilarcastilloz)”。
2. 询问：“我要向Pilar Castillo (pilarcastilloz)转账10000阿根廷比索吗？”
3. 确认后：运行`send --to Pili --amount 10000 --yes`。
4. 显示交易哈希值。
5. 运行`history --beneficiary Pili`来确认交易记录。

### 用户请求：“转账给‘la verdulería’”
1. 运行`beneficiaries search "verdulería"`。
2. 如果找到收款人：询问：“我要向‘la verdulería’转账吗？”
3. 确认后：运行`send --to <their_alias>`。
4. 显示存款地址和转账说明。

### 用户请求：“转账2000阿根廷比索给franv98”
1. 运行`beneficiaries search "franv98"` → 未找到收款人。
2. “franv98”是一个别名，运行`beneficiaries add --to franv98` → Ripio会返回收款人信息。
3. 询问：“franv98属于FRANCISCO VARELA（CUIT 20385..., Banco Galicia）吗？我要转账2000阿根廷比索吗？”
4. 确认后：运行`send --to franv98 --amount 2000 --yes`。
5. 显示交易哈希值。
6. 运行`history`来确认交易记录。

### 用户请求：“转账给0000003100099123456789”
1. 运行`beneficiaries search "0000003100099123456789"` → 未找到收款人。
2. 这是一个22位的数字（CVU），运行`beneficiaries add --to 0000003100099123456789` → Ripio会返回收款人信息。
3. 询问：“这个CVU属于MARÍA GARCÍA（CUIT 27..., Banco Nación）吗？我确认转账吗？”
4. 确认后：运行`send --to 0000003100099123456789`。
5. 显示存款地址和转账说明。

### 用户请求：“转账给tulezao”
1. 运行`beneficiaries search "tulezao"` → 未找到收款人。
2. “tulezao”是一个别名，运行`beneficiaries add --to tulezao` → Ripio会返回收款人信息。
3. 询问：“别名tulezao属于JUAN PÉREZ（CUIT 20..., Banco Nación）吗？我确认转账吗？”
4. 确认后：继续进行转账。

### 新用户注册（已有Ripio账户）
1. 询问用户的电子邮件和电话号码。
2. 运行`signup --email <email> --phone <phone>`。
3. 运行`check-kyc`（发送OTP验证码）。
4. 询问用户提供6位验证码。
5. 运行`otp --code <code>`。
6. 运行`kyc-status`来确认验证是否完成。

### 自动转账（钱包已配置）
1. 询问：“我要向Pilar Castillo (pilarcastilloz)转账10000阿根廷比索吗？”
2. 确认后：运行`send --to pilarcastilloz --amount 10000 --yes`。
   - `--amount`参数以ARS为单位（10000等于10000阿根廷比索）。系统会自动选择代币：如果可用则使用wARS，否则会自动转换USDC到wARS。
3. 显示交易哈希值。
4. 运行`history`来确认交易记录。

### 在转账前将USDC兑换为wARS
1. 运行`wallet balance`查看USDC余额。
2. 运行`swap --from USDC --to wARS --amount 10`。
3. 显示兑换结果：“10 USDC兑换为约14,380 wARS”。
4. 运行`send --to pilarcastilloz --amount 14380 --token wARS`。
5. wARS会通过离线转账平台自动转换为ARS。

### 转账前查看汇率
1. 运行`quote --from USDC --to ARS --amount 10`。
2. 告诉用户：“按照当前汇率，10 USDC等于约14,300阿根廷比索”。

### 从银行转账充值钱包
1. 运行`onramp quote --amount 50000`。
2. 询问用户确认收款地址和转账金额。
3. 运行`onramp create --amount 50000 --yes`。
4. 显示会话/订单ID和转账说明。
5. 运行`onramp status --transaction <id>`来跟踪转账进度。