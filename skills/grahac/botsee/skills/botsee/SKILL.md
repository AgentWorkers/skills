---
name: botsee
description: 通过 BotSee API 监控您品牌在人工智能领域的可见度
version: 0.2.5
---
# BotSee技能

该技能用于监控您的品牌在ChatGPT、Claude、Perplexity和Gemini等平台上的AI可见性（包括AI SEO和地理位置相关数据）。该工具由botsee.io提供，适用于Claude Code及相关代理程序。

**命令：**

**工作流程：**
- /botsee                  - 获取快速状态和帮助信息
- /botsee signup [--email EMAIL] [--name NAME] [--company COMPANY] [--api-key KEY] - 使用信用卡注册
- /botsee signup-usdc [--email EMAIL] [--name NAME] [--company COMPANY] [--no-email] - 使用USDC在Base平台上注册
- /botsee signup-pay-usdc --amount-cents N [--token TOKEN] [--payment PROOF] - 通过x402支付方式完成USDC注册
- /botsee signup-status [--token TOKEN]    - 检查注册进度并保存API密钥
- /botsee topup-usdc --amount-cents N [--payment PROOF] - 通过x402在Base平台上使用USDC充值
- /botsee create-site <domain> [--types N]   - 保存自定义配置
- /botsee config-show              - 显示已保存的配置
- /botsee analyze              - 运行竞争分析
- /botsee content              - 根据分析结果生成博客文章

**站点相关命令：**
- /botsee list-sites             - 列出所有站点
- /botsee get-site [uuid]            - 查看站点详情
- /botsee create-site <domain>           - 创建新站点
- /botsee archive-site [uuid]          - 归档站点

**客户类型相关命令：**
- /botsee list-types             - 列出所有客户类型
- /botsee get-type <uuid>            - 查看类型详情
- /botsee create-type <name> [desc]         - 创建新的客户类型
- /botsee generate-types [count]         - 生成指定数量的客户类型
- /botsee update-type <uuid> [name] [desc]        - 更新客户类型
- /botsee archive-type <uuid>          - 归档客户类型

**人物角色相关命令：**
- /botsee list-personas [type]           - 列出所有人物角色（或按类型筛选）
- /botsee get-persona <uuid>            - 查看人物角色详情
- /botsee create-persona <type> [name] [desc]         - 创建新的人物角色
- /botsee generate-personas <type> [count]         - 为指定类型生成人物角色
- /botsee update-persona <uuid> [name] [desc]         - 更新人物角色信息
- /botsee archive-persona <uuid>          - 归档人物角色

**问题相关命令：**
- /botsee list-questions [persona]           - 列出所有问题（或按人物角色筛选）
- /botsee get-question <uuid>            - 查看问题详情
- /botsee create-question <persona> [question_text]       - 创建新问题
- /botsee generate-questions <persona> [count]         - 为指定人物角色生成问题
- /botsee update-question <uuid> [question_text]       - 更新问题内容
- /botsee delete-question <uuid>            - 删除问题

**结果相关命令：**
- /botsee results-competitors <analysis_uuid>     - 查看竞争对手分析结果
- /botsee results-keywords <analysis_uuid>     - 查看关键词分析结果
- /botsee results-sources <analysis_uuid>     - 查看数据来源信息
- /botsee results-responses <analysis_uuid>     - 查看所有AI生成的回答

## 实现方式

当用户执行BotSee命令时，系统会运行相应的Python脚本。所有命令都通过一个统一的脚本来处理内部的API调用。

### /botsee (status)  
（代码块省略）

### /botsee signup [--email EMAIL] [--name NAME] [--company COMPANY] [--api-key KEY]  
**新用户注册流程（使用信用卡）：**

**步骤1：获取注册链接**  
（代码块省略）  
该命令会输出如下内容：  
“要完成BotSee注册，请访问以下链接：**[上述链接]**”  
用户完成该页面的注册后，请返回此处并执行 `/botsee signup-status` 命令。

**步骤2：保存API密钥**  
用户完成注册后，执行 `/botsee signup-status` 命令。  
脚本会自动从服务器获取您的API密钥（使用注册时提供的令牌）。  
如果系统要求输入令牌，请使用注册页面上的令牌。

### /botsee signup-usdc [--email EMAIL] [--name NAME] [--company COMPANY] [--no-email]  
**使用USDC注册（基于Base平台的x402支付方式）：**

**步骤1：在调用API前询问用户**  
如果用户在注册时未指定偏好设置，系统会询问：  
“您是否希望将此账户与电子邮件关联？  
- **是（需要电子邮件）**：您将收到一个验证电子邮件的链接，并可稍后访问控制面板  
- **否（仅使用API）**：直接跳过电子邮件步骤，进入支付流程**

**步骤2a：处理需要电子邮件的情况**  
执行以下命令：  
（代码块省略）  
系统会输出如下内容：  
“请访问以下链接以验证您的电子邮件并阅读设置说明：**[上述链接]**”  
用户完成验证后，请返回此处，系统将继续完成USDC支付流程。  
**注意：** 在此之前不要执行 `/botsee signup-pay-usdc` 命令。  

**步骤2b：处理不需要电子邮件的情况**  
系统将直接进入支付流程，无需执行额外的步骤。

**步骤3：支付**  
无论用户是否选择了需要电子邮件的选项，系统都会执行以下支付流程：  
（代码块省略）  
1. `signup-usdc` 通过 `POST /api/v1/signup/usdc` 创建USDC注册令牌。  
2. `signup-pay-usdc --amount-cents N` 通过 `POST /api/v1/signup/:token/pay-usdc` 发起支付请求（无需提供支付相关信息）。  
3. 使用钱包（如Pinch或Coinbase CDP Agentic Wallet）将USDC发送到系统指定的地址。  
4. 重新尝试支付，需提供支付凭证（`--payment PROOF` 参数）。  
5. `signup-status` 命令会持续检查支付进度并保存API密钥。

### /botsee signup-pay-usdc --amount-cents N [--token TOKEN] [--payment PROOF]  
（代码块省略）  
省略 `--payment` 参数时，系统会提示用户提供支付相关信息（网络信息、金额和收款地址）。  
在钱包完成支付后，再次执行 `/botsee signup-pay-usdc` 命令，并提供 `--payment <base64-proof>` 参数。

### /botsee signup-status [--token TOKEN]  
（代码块省略）  
注册完成后，API密钥会自动保存到 `~/.botsee/config.json` 文件中。

### /botsee topup-usdc --amount-cents N [--payment PROOF]  
（代码块省略）  
省略 `--payment` 参数时，系统会提示用户提供支付相关信息（网络信息、金额和收款地址）。  
在钱包完成支付后，再次执行 `/botsee topup-usdc` 命令，并提供 `--payment <base64-proof>` 参数。

### /botsee create-site <domain> [--types N] [--personas P] [--questions Q]  
**使用说明：** 需要 `/botsee signup` 命令生成的API密钥。  
（代码块省略）  
**可选参数：**  
- `--types`（默认值：2，范围：1-3）  
- `--personas`（默认值：2，范围：1-3）  
- `--questions`（默认值：5，范围：3-10）  

**操作流程：**  
1. 为指定域名创建站点。  
2. 生成相应的客户类型、人物角色和问题。  
3. 将配置信息保存到工作区和用户配置文件中。

### /botsee config-show  
（代码块省略）  

### /botsee analyze  
（代码块省略）  
系统开始分析，完成后会显示竞争对手信息、关键词和数据来源。

### /botsee content  
（代码块省略）  
根据分析结果生成博客文章，并自动保存到 `botsee-YYYYMMDD-HHMMSS.md` 文件中。

---

## 站点相关命令：  
（代码块省略）

## 客户类型相关命令：  
（代码块省略）

## 人物角色相关命令：  
（代码块省略）

## 问题相关命令：  
（代码块省略）

## 结果相关命令：  
（代码块省略）

## 代理程序使用说明：  
该技能专为**非交互式代理程序**设计。所有命令均通过命令行参数传递参数，无需用户交互。  

**代理程序使用时的关键注意事项：**  
1. **注册流程需要人工干预**  
对于没有API密钥的新用户，系统会生成一个注册令牌并提供注册链接。  
   - 如果代理程序拥有API密钥，请使用 `--api-key` 参数。  
   - 若需要用户注册，请告知用户（代理程序无法完成注册操作）。  
   - 确保API密钥是代理程序自主运行的前提条件。  

2. **异步操作与等待**  
部分命令需要等待结果（如 `/botsee signup-status` 和 `/botsee analyze`），这些操作可能会阻塞一段时间。  

3. **分析结果的处理**  
分析完成后，需要获取分析结果的UUID（通过 `/botsee analyze` 命令获取），并使用该UUID执行后续的结果查询命令。  

**推荐使用模式：**  
（代码块省略）

**配置文件说明：**  
系统使用两个配置文件：  
- **用户配置文件：`~/.botsee/config.json`（包含API密钥和站点UUID）  
- **工作区配置文件：`.context/botsee-config.json`（包含生成配置的默认值，可选）  
代理程序可以通过以下命令查看状态：  
  - `/botsee`：显示账户信息  
  - `/botsee config-show`：显示工作区配置  

4. **费用说明**  
部分操作会消耗信用点数。代理程序应：  
  - 在执行高成本操作前检查剩余信用点数（例如 `/botsee` 命令）。  
  - 正确处理“信用点数不足”的错误情况。  
  - 监控信用点数的使用情况（每次操作后都会显示剩余信用点数）。  

5. **错误处理**  
所有错误都会以代码1退出，并将错误信息输出到标准错误流（stderr）。错误信息包括：  
  - 相关的HTTP状态码  
  - 下一步的操作建议  
  - 确保API密钥不会泄露。  

6. **幂等性说明：**  
- 一些命令（如状态查询、列表展示和信息获取）是安全的，可以重复执行。  
- 创建操作可能会导致数据重复。  
- 更新操作需要特定的UUID，可以安全地重复执行。  

7. **输出格式**：  
  - 数据创建/更新操作的输出为JSON格式，便于解析。  
  - 工作流程相关的命令输出为人类可读的文本。  
  - 状态和剩余信用点数会在命令执行完成后立即显示。  

**代理程序示例工作流程：**  
（代码块省略）