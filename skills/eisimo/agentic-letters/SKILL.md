---
name: agentic-letters
description: "只需一个命令，即可将实体信件寄送到德国的任何地方。适用场景：用户需要寄送实体信件。使用该功能前，需要获取来自 agentic-letters.com 的 API 密钥。"
homepage: https://agentic-letters.com
metadata:
  {
    "openclaw":
      {
        "emoji": "✉️",
        "requires": { "bins": ["python3"] },
        "primaryEnv": "AGENTIC_LETTERS_API_KEY",
      },
  }
---
# AgenticLetters

您可以通过 [agentic-letters.com](https://agentic-letters.com) 的 API 将纸质信件寄送到德国的任何地方。您的 PDF 文件会被打印出来、装入信封并寄出——一次 API 调用，就完成了一封真实的信件发送。

## 使用场景

- 用户需要发送纸质信件、取消通知或法律声明
- 用户需要将文档（PDF 格式）寄送到德国的地址
- 用户请求“发送信件”、“发送解约通知”等类似操作
- 用户需要发送 DSGVO 数据请求、投诉信或贺卡

## 设置

```bash
mkdir -p ~/.openclaw/secrets
echo 'AGENTIC_LETTERS_API_KEY=al_your_api_key' > ~/.openclaw/secrets/agentic_letters.env
```

## 获取 API 密钥

AgenticLetters 没有账户系统，也不需要登录。获取密钥的步骤如下：

1. 访问 https://agentic-letters.com/buy
2. 输入电子邮件地址并选择相应的信用套餐
3. 通过 Stripe（信用卡）完成支付
4. API 密钥（以 `al_` 开头）会立即发送到该电子邮件地址

该密钥是一个用于所有请求的令牌。如果用户后来使用相同的电子邮件购买更多信用额度，现有密钥会被自动补充，而不会重新生成新的密钥。如果用户尚未拥有密钥，请引导他们访问 https://agentic-letters.com/buy。

## 工具

`{baseDir}/agentic_letters.py` 是一个不依赖任何外部库的 Python 命令行工具（仅使用标准库）。

## 发送信件

1. 生成 A4 格式的 PDF 文件（最多 3 页，大小不超过 10 MB，黑白打印）
2. 运行以下命令：

```bash
python3 {baseDir}/agentic_letters.py send \
  --pdf letter.pdf \
  --name "Max Mustermann" \
  --street "Musterstraße 1" \
  --zip 10115 \
  --city Berlin \
  --label "Kündigung Fitnessstudio"
```

可选参数：
- `--type <type>` — 信件类型（默认为 `standard`）；未来会添加新的类型，API 会拒绝未知类型的请求。
- `--country <code>` — 国家代码（默认为 `DE`）；目前仅支持德国。

**输出结果（JSON 格式，输出到标准输出）：**

```json
{
  "id": "550e8400-e29b-41d4-a716",
  "status": "queued",
  "type": "standard",
  "label": "Kündigung Fitnessstudio",
  "created_at": "2026-02-24T19:00:00Z",
  "credits_remaining": 4
}
```

## 查看信件状态

```bash
python3 {baseDir}/agentic_letters.py status <letter-id>
```

状态值：`queued` → `printed` → `sent` → `returned`

## 查看剩余信用额度

```bash
python3 {baseDir}/agentic_letters.py credits
```

## 列出所有已发送的信件

```bash
python3 {baseDir}/agentic_letters.py list
```

## 本地记录

每封已发送的信件都会被保存在 `{baseDir}/records/` 目录中。每个文件的名称格式为 `YYYY-MM-DD_<id-prefix>.json`，内容包含以下信息：

```json
{
  "id": "550e8400-...",
  "status": "queued",
  "type": "standard",
  "label": "Kündigung Fitnessstudio",
  "recipient": {
    "name": "Max Mustermann",
    "street": "Musterstraße 1",
    "zip": "10115",
    "city": "Berlin",
    "country": "DE"
  },
  "created_at": "2026-02-24T19:00:00Z",
  "credits_remaining": 4,
  "last_checked": null
}
```

记录会在发送信件时自动创建，并在状态更新时进行更新。通过日期前缀，管理员可以快速找到最近的信件，而无需浏览旧文件。要查看待处理的信件，请查看最近的记录文件，并对状态为 `queued` 的信件执行 `status` 操作。

## 生成 PDF 文件

如果用户没有准备好 PDF 文件，可以按照以下方法生成：

- 使用 `pandoc` 将 Markdown 文件转换为 PDF：`echo "Dear Sir..." | pandoc -o letter.pdf`
- 使用 `wkhtmltopdf` 将 HTML 文件转换为 PDF：`wkhtmltopdf letter.html letter.pdf`
- 使用 `fpdf2` 或 `reportlab` 等库进行程序化生成

请确保 PDF 文件为 A4 格式（210 × 297 毫米），并保留至少 15 毫米的页边距。

## 错误处理

错误信息会带有明确的来源标签输出到标准错误输出（stderr）。请求失败时，程序的退出代码非零。

**错误来源：**
- `[local]` — 请求前出现的问题（例如文件缺失、API 密钥未设置）
- `[server]` — API 拒绝了请求（包含错误代码、HTTP 状态码、详细信息及相关字段）
- `[network]` — 无法连接到 API（DNS 错误、超时、连接被拒绝）

**服务器错误示例：**

```plaintext
[server] 无效的德国邮政编码
  code: recipient_zip_invalid
  http_status: 400
  detail: 需要 5 位数的德国邮政编码（例如 "10115"），但收到的是 "123"。
  field: recipient.zip
```

请求成功时，结果会以 JSON 格式输出到标准输出；失败时，没有任何输出。

## 重要限制

- **仅限德国** — 收件人必须拥有德国地址
- **最多 3 页** — 超过 3 页的 PDF 文件会被服务器拒绝
- **最大文件大小 10 MB** — 如有需要，请压缩图片
- **黑白打印** — 图片将以灰度显示
- **1 信用额度对应 1 封信件** — 发送前请检查剩余信用额度
- **必须使用 A4 格式** — 请确保文件符合尺寸要求
- **不要在本地验证 PDF 文件** — 所有 PDF 验证工作由服务器完成

## 常见使用场景

- **解约通知（Kündigung）**：提供服务名称、客户编号和收件人地址，生成正式的解约通知信并发送。
- **DSGVO 数据请求（DSGVO Auskunftsersuchen）**：提供公司名称和地址以及用户的全名，生成符合 DSGVO 第 15 条规定的请求信并发送。
- **异议/申诉（Widerspruch）**：提供相关机构/公司信息、参考编号和理由，生成正式的异议信并发送。