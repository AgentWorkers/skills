---
name: esign-automation
description: 通过调用 eSignGlobal CLI 工具，可以自动化合同签署、电子签名（esign）以及相关的签名工作流程。eSignGlobal CLI 对代理程序（agents）非常友好，其默认输出格式为 JSON，这使得签名操作易于解析和后续处理（即可以轻松地与其他系统或流程进行集成）。
metadata: {"openclaw":{"primaryEnv":"ESIGNGLOBAL_APIKEY"}}
version: 1.5.5
homepage: https://github.com/esign-cn-open-source/skills
---
# eSign Automation

该技能为 eSignGlobal 电子签名平台提供了自动化功能，允许 AI 代理自动执行文档签名流程，并与 eSignGlobal 的 API 进行集成。该技能由 eSignGlobal 团队维护，旨在确保合同签名流程的安全性。

## 适用场景

当用户需要执行以下操作时，可以使用该技能：
- 发送合同、协议或审批表单以供签名
- 从本地文件启动新的电子签名流程
- 将一份文档发送给一个或多个接收者进行签名

**示例请求：**
- “将这份合同发送给 John 进行签名”
- “为这份 PDF 文件启动签名流程”
- “将这份协议发送给 Alice 和 Bob”

## 安装

通过 `npx` 命令行工具来安装外部 CLI：

```bash
npx @esignglobal/envelope-cli <command>
```

## 设置

在调用任何发送操作之前，请在 shell 环境中设置 `ESIGNGLOBAL_APIKEY`。如果用户尚未拥有 API 密钥，请引导他们按照以下步骤操作：
1. 登录到 `https://www.esignglobal.com`
2. 进入“设置 -> 集成 -> 应用程序”
3. 创建一个新的应用程序并复制生成的 API 密钥

```bash
# Windows PowerShell
$env:ESIGNGLOBAL_APIKEY="your_api_key"

# macOS / Linux
export ESIGNGLOBAL_APIKEY="your_api_key"

# Verify connectivity
npx @esignglobal/envelope-cli config health
```

**凭证处理规则：**
- CLI 仅从 `ESIGNGLOBAL_APIKEY` 中读取凭证信息
- 严禁在该技能内部实现本地凭证存储
- 禁止打印或保存任何敏感信息

## 工作流程：
1. 收集文件的绝对路径 (`filePath`)、签名者列表以及可选的邮件主题 (`subject`)
2. 确认文件为 `.pdf` 格式，并且签名者信息完整
3. 在当前 shell 会话中设置 `ESIGNGLOBAL_APIKEY`
4. 运行外部 CLI 命令以发送签名请求
5. 将 CLI 的执行结果返回给用户

## 安全规则：
- 仅使用用户明确提供的文件路径
- 每次运行时仅处理一个本地 PDF 文件
- 不支持相对路径，必须提供 `.pdf` 文件的绝对路径
- 在调用 CLI 之前，拒绝处理非 PDF 格式的文件
- 绝不允许打印或保存任何敏感信息
- 严禁代表用户扫描目录、扩展通配符或自动查找文件
- 仅使用为当前环境配置的受信任的 eSignGlobal CLI 工具

## 必需输入参数：
- `filePath`：本地 PDF 文件的绝对路径
- `signers`：签名者的 JSON 数组
- `subject`：可选的邮件主题

每个签名者对象必须包含以下信息：
- `userName`
- `userEmail`

**可选字段：**
- `signOrder`（整数，最小值为 1）

## 输入格式：
### filePath**
`filePath` 必须是本地 PDF 文件的绝对路径。

**示例：**
```text
/tmp/contract.pdf
```

### signers**
每个签名者对象必须包含以下信息：
- `userName`
- `userEmail`

**可选字段：**
- `signOrder`（整数，最小值为 1）

**单个签名者的示例：**
```json
[
  {
    "userName": "Bob Smith",
    "userEmail": "bob@example.com"
  }
]
```

**顺序签名示例：**
```json
[
  {
    "userName": "Bob Smith",
    "userEmail": "bob@example.com",
    "signOrder": 1
  },
  {
    "userName": "Alice Jones",
    "userEmail": "alice@example.com",
    "signOrder": 2
  }
]
```

**并行签名示例：**
```json
[
  {
    "userName": "Bob Smith",
    "userEmail": "bob@example.com",
    "signOrder": 1
  },
  {
    "userName": "Alice Jones",
    "userEmail": "alice@example.com",
    "signOrder": 1
  }
]
```

## 外部 CLI 使用说明**

建议使用外部命令行工具，而非内置的脚本：

```bash
npx @esignglobal/envelope-cli send-envelope --file <filePath> --signers '<signersJson>' [--subject <subject>] --confirm
```

如需查看可用命令，请参考相关文档：

```bash
npx @esignglobal/envelope-cli help
```

**示例：**
```bash
npx @esignglobal/envelope-cli send-envelope --file "C:\\docs\\contract.pdf" --signers '[{"userName":"Bob Smith","userEmail":"bob@example.com"}]' --subject "Please sign this contract" --confirm
```

## 系统要求：**
- 确保系统安装了 Node.js 18 或更高版本
- 必须能够访问受信任的外部 CLI 工具（已预安装或可通过 `npx` 命令访问）
- `ESIGNGLOBAL_APIKEY` 必须已在 shell 环境中配置完毕

## 输出结果：
仅返回外部 CLI 的执行结果。严禁在该技能内部实现文件上传逻辑。