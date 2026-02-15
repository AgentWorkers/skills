---
name: invoice-generator
description: 根据 JSON 数据生成专业的 PDF 发票。适用于用户需要创建包含公司/客户详细信息及商品明细的发票、账单或付款请求的情况。
metadata: {"clawdbot":{"emoji":"🧾","requires":{"bins":["node","jq","weasyprint"],"env":["INVOICE_DIR"]},"primaryEnv":"INVOICE_DIR"}}
---

# 发票生成器

该工具能够根据结构化的 JSON 数据生成 PDF 发票。

## 设置

1. 安装 Node.js 所需的依赖项：

```bash
cd invoice-generator && npm install
```

2. 设置 `INVOICE_DIR` 环境变量（或在 `skills.entriesinvoice-generator.env` 文件中配置）：

```bash
export INVOICE_DIR="/path/to/your/invoices"
```

这将创建以下目录结构：

```
$INVOICE_DIR/
├── configs/    # Optional: saved invoice configs
└── invoices/   # Generated PDF output
```

## 使用方法

```bash
# From stdin (on-the-fly)
cat invoice-data.json | {baseDir}/scripts/generate.sh

# From a full file path
{baseDir}/scripts/generate.sh /path/to/invoice-data.json

# From a saved config (looks in $INVOICE_DIR/configs/)
{baseDir}/scripts/generate.sh client-template
# Loads: $INVOICE_DIR/configs/client-template.json

# Output goes to: $INVOICE_DIR/invoices/invoice-{number}.pdf (auto-versions if exists)
```

## 输入数据格式

JSON 输入数据必须包含以下字段：

```json
{
  "company": {
    "name": "Your Company",
    "address": "123 Main St",
    "cityStateZip": "City, State, 12345",
    "country": "Country"
  },
  "client": {
    "name": "Client Name",
    "address": "456 Client Ave",
    "cityStateZip": "City, State, 67890",
    "country": "Country",
    "taxId": "TAX123"
  },
  "invoice": {
    "number": "INV-2025.01",
    "date": "Jan 15 2025",
    "dueDate": "Jan 30 2025"
  },
  "items": [
    {
      "description": "Service description",
      "rate": "1000.00",
      "currency": "USD"
    }
  ],
  "totals": {
    "currency": "USD",
    "total": "1,000.00"
  }
}
```

有关字段的详细信息，请参阅 [references/data-schema.md](references/data-schema.md)。

## 输出结果

脚本在成功生成 PDF 文件后，会输出该文件的路径：

```
$INVOICE_DIR/invoices/invoice-INV-2025.01.pdf
# If that filename already exists, the script will write:
# $INVOICE_DIR/invoices/invoice-INV-2025.01-2.pdf (then -3, etc.)
```

## 错误处理

- 如果 JSON 数据无效或缺少必要字段，程序将以代码 1 退出；
- 如果 weasyprint 无法生成 PDF 文件，程序将以代码 2 退出；
- 错误信息会被写入标准错误输出（stderr）。