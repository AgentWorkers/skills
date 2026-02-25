---
name: botsee
description: 通过 BotSee API 监控您品牌在人工智能领域的可见度
version: 0.2.5
---
# BotSee技能

该技能用于监控您的品牌在ChatGPT、Claude、Perplexity和Gemini等平台上的AI可见性（包括AI SEO和地理位置相关的数据）。该工具由botsee.io提供，适用于Claude Code和代理程序。

**命令：**

**工作流程：**
- /botsee                  - 查看快速状态和获取帮助
- /botsee signup [--email EMAIL] [--name NAME] [--company COMPANY] [--api-key KEY] - 使用信用卡注册
- /botsee signup-usdc [--email EMAIL] [--name NAME] [--company COMPANY] [--no-email] - 使用USDC在Base平台上注册
- /botsee signup-pay-usdc --amount-cents N [--token TOKEN] [--payment PROOF] - 通过x402支付方式使用USDC完成注册
- /botsee signup-status [--token TOKEN]    - 检查注册是否完成并保存API密钥
- /botsee topup-usdc --amount-cents N [--payment PROOF] - 使用USDC在Base平台上充值
- /botsee create-site <domain> [--types N]   - 保存自定义配置
- /botsee config-show              - 显示保存的配置
- /botsee analyze              - 运行竞争分析
- /botsee content              - 根据分析结果生成博客文章

**站点相关命令：**
- /botsee list-sites             - 列出所有站点
- /botsee get-site [uuid]          - 查看站点详情
- /botsee create-site <domain>        - 创建新站点
- /botsee archive-site [uuid]         - 归档站点

**客户类型相关命令：**
- /botsee list-types             - 列出所有客户类型
- /botsee get-type [uuid]          - 查看客户类型详情
- /botsee create-type <name> [desc]        - 创建新的客户类型
- /botsee generate-types [count]       - 生成指定数量的客户类型
- /botsee update-type [uuid] [name] [desc]       - 更新客户类型
- /botsee archive-type [uuid]         - 归档客户类型

**人物角色相关命令：**
- /botsee list-personas [type]         - 列出所有人物角色
- /botsee get-persona [uuid]          - 查看人物角色详情
- /botsee create-persona <type> [name] [desc]       - 创建新的人物角色
- /botsee generate-personas [type] [count]       - 为指定类型生成人物角色
- /botsee update-persona [uuid] [name] [desc]       - 更新人物角色
- /botsee archive-persona [uuid]         - 归档人物角色

**问题相关命令：**
- /botsee list-questions [persona]         - 列出所有问题
- /botsee get-question [uuid]          - 查看问题详情
- /botsee create-question [persona] [question_text]     - 创建新问题
- /botsee generate-questions [persona] [count]       - 为指定人物角色生成问题
- /botsee update-question [uuid] [question_text]     - 更新问题内容
- /botsee delete-question [uuid]          - 删除问题

**结果相关命令：**
- /botsee results-competitors [analysis_uuid]    - 查看竞争对手分析结果
- /botsee results-keywords [analysis_uuid]     - 查看关键词分析结果
- /botsee results-sources [analysis_uuid]     - 查看信息来源
- /botsee results-responses [analysis_uuid]    - 查看所有AI模型的回答
- /botsee results-keyword-opportunities [analysis_uuid] [--threshold 0.0-1.0] [--rank-threshold N] - 显示品牌未被提及或排名较低的问题
- /botsee results-source-opportunities [analysis_uuid] - 显示品牌未被提及时AI引用的信息来源（适合用于内容创作和链接建设）

## 实现方式

当用户执行BotSee命令时，系统会运行相应的Python脚本。所有命令都通过一个统一的脚本来处理内部API调用。

### /botsee (status)  
（代码块略）

### /botsee signup [--email EMAIL] [--name NAME] [--company COMPANY] [--api-key KEY]  
**新用户注册流程（使用信用卡）：**

**步骤1：获取注册链接**  
（代码块略）  
该命令会输出一条信息，提示用户：“要完成BotSee注册，请访问以下链接：**[上述链接]**”  
用户完成注册后，请返回此处并执行 `/botsee signup-status` 命令。

**步骤2：保存API密钥**  
用户完成注册后，执行 `/botsee signup-status` 命令。脚本会自动从服务器获取API密钥（使用用户提供的注册令牌）。如果系统要求提供令牌，请使用注册页面上的令牌。

### /botsee signup-usdc [--email EMAIL] [--name NAME] [--company COMPANY] [--no-email]  
**使用USDC注册（基于Base平台的x402支付方式）：**

**步骤1：在调用API之前询问用户**  
如果用户尚未指定注册方式，系统会询问：“您是否希望为该账户关联电子邮件？  
- **是（需要电子邮件）**：系统会提供验证电子邮件的链接，用户完成验证后可以访问控制面板。  
- **否（仅使用API）**：直接进入支付步骤。**

**步骤2a：处理需要电子邮件的情况**  
（代码块略）  
系统会输出一条信息，提示用户：“请访问以下链接以验证电子邮件并阅读设置说明：**[上述链接]**”  
用户完成验证后，请返回此处，系统将继续处理USDC支付。

**步骤2b：处理不需要电子邮件的情况**  
（代码块略）  
在这种情况下，系统会立即进入支付步骤。

**步骤3：支付**  
无论用户是否选择了需要电子邮件的方式，系统都会执行以下支付流程：  
1. `signup-usdc` 通过 `POST /api/v1/signup/usdc` 创建USDC注册令牌。  
2. `signup-pay-usdc --amount-cents N` 通过 `POST /api/v1/signup/:token/pay-usdc` 发起支付请求（系统会返回402错误代码，提示支付相关信息）。  
3. 用户需要使用钱包（如Pinch或Coinbase CDP Agentic Wallet）将USDC发送到系统指定的地址。  
4. 重新尝试支付，此时需要提供支付证明（`--payment PROOF` 参数）。  
5. `signup-status` 命令会持续检查支付进度，并在支付完成后将API密钥保存到 `~/.botsee/config.json` 文件中。

### /botsee signup-pay-usdc --amount-cents N [--token TOKEN] [--payment PROOF]  
（代码块略）  
如果省略 `--payment` 参数，系统会返回402错误，提示支付相关信息。用户需要提供支付证明（`--payment PROOF` 参数），并在支付完成后再次尝试。

### /botsee signup-status [--token TOKEN]  
（代码块略）  
注册完成后，API密钥会自动保存到 `~/.botsee/config.json` 文件中。

### /botsee topup-usdc --amount-cents N [--payment PROOF]  
（代码块略）  
与 `/botsee signup-usdc` 命令类似，省略 `--payment` 参数时会返回402错误。用户需要提供支付证明，并在支付完成后再次尝试。

### /botsee create-site <domain> [--types N] [--personas P] [--questions Q]  
**使用说明：** 需要 `/botsee signup` 命令生成的API密钥。  
（代码块略）  
**可选参数：**  
- `--types`（默认值：2，范围：1-3）  
- `--personas`（默认值：2，范围：1-3）  
- `--questions`（默认值：5，范围：3-10）  

**执行操作：**  
1. 为指定域名创建站点。  
2. 生成相应的客户类型、人物角色和问题。  
3. 将配置保存到工作区和用户配置文件中。

### /botsee config-show  
（代码块略）  
显示保存的配置信息。

### /botsee analyze  
（代码块略）  
开始分析，完成后会显示竞争对手信息、关键词和信息来源。

### /botsee content  
（代码块略）  
根据分析结果生成博客文章，并自动保存到 `botsee-YYYYMMDD-HHMMSS.md` 文件中。

---

## 站点相关命令：  
（代码块略）

## 客户类型相关命令：  
（代码块略）

## 人物角色相关命令：  
（代码块略）

## 问题相关命令：  
（代码块略）

## 结果相关命令：  
（代码块略）

## 竞争对手分析相关命令：  
（代码块略）

## 信息来源分析相关命令：  
（代码块略）

## 代理程序使用说明：  
该技能专为**非交互式代理程序设计**。所有命令均通过命令行参数传递参数，无需用户交互。  

**代理程序需要注意的事项：**  
1. **注册流程需要人工干预**  
对于没有API密钥的新用户，系统会生成注册令牌并提供注册链接。代理程序应使用 `--api-key` 参数（如果可用）。  
2. **异步操作和等待**  
部分命令（如 `/botsee signup-status` 和 `/botsee analyze`）可能需要等待结果。  
3. **分析结果获取**  
执行 `/botsee analyze` 后，系统会输出分析结果UUID。使用该UUID 可以通过相关命令查看详细分析数据。  

**推荐使用模式：**  
代理程序应通过命令行参数配置各项设置，并定期检查账户状态和配置信息。  

**费用说明：**  
- 注册费用：约75个信用点数（默认配置为2个客户类型、2个人物角色、5个问题）。  
- 分析费用：每次分析约660个信用点数。  
- 内容生成费用：15个信用点数。  

**错误处理：**  
所有错误都会以代码1退出，并在标准错误输出（stderr）中显示错误信息，包括HTTP状态码和后续操作建议。系统会确保API密钥不会泄露。  

**其他注意事项：**  
- 部分命令（如创建操作）可能重复执行，但结果不会重复生成。  
- 输出格式：CRUD操作返回JSON格式数据，工作流程相关命令返回易于阅读的文本，状态和余额信息会在命令执行完成后立即显示。