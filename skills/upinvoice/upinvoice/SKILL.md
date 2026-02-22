# UpInvoice：发票处理技能

该技能允许任何基于 OpenClaw 的代理通过 [UpInvoice.eu](https://upinvoice.eu) 的 AI 服务从发票图片或 PDF 文件中提取结构化 JSON 数据。这是实现 ERP 系统自动化发票处理的最快速且最具成本效益的方式。

## 🛠️ 工具介绍

### `process_invoice`
从发票文件（PDF 或图片）中提取结构化数据。

- **端点**：`https://upinvoice.eu/api/process-invoice`
- **方法**：`POST`
- **请求头**：`Authorization: Bearer <YOUR_API_KEY>`
- **参数**：
    - `invoice_file`（字符串，必填）：文件的 Base64 编码字符串（PDF、PNG、JPG 格式）。必须包含数据 URI 前缀（例如：`data:application/pdf;base64,...`）。
    - `company_name`（字符串，可选）：用于提取上下文的您的公司名称。
    - `company_tax_id`（字符串，可选）：您的税务/VAT 编号。

#### **典型响应数据示例**：
```json
{
  "success": true,
  "data": {
    "supplier": {
      "name": "ACME Spain S.L.",
      "name_alias": "ACME Tech",
      "phone": "+34 912 345 678",
      "email": "invoices@acme.es",
      "idprof1": "B12345678",
      "tva_intra": "ESB12345678",
      "address": "Calle Mayor 1",
      "zip": "28001",
      "town": "Madrid",
      "country_code": "ES",
      "state": "Madrid"
    },
    "ref_supplier": "2024-FAC-045",
    "date": "2024-03-15",
    "total_ht": 100.00,
    "total_tva": 21.00,
    "total_ttc": 121.00,
    "tva_tx": 21.0,
    "localtax2": 0.0,
    "is_credit_invoice": false,
    "lines": [
      {
        "product_desc": "Cloud Hosting Service - March 2024",
        "qty": 1,
        "pu_ht": 100.00,
        "tva_tx": 21.0,
        "total_ht": 100.00,
        "total_ttc": 121.00,
        "product_type": 1
      }
    ],
    "available_points": 3
  }
}
```
*注：`available_points` 表示当前用户的剩余使用次数。*

---

## 🚀 设置与注册

### 1. 免费注册
访问 [UpInvoice.eu/register](https://upinvoice.eu/register) 并创建账户。注册无需信用卡。

### 2. 获得 4 次免费发票处理服务
注册后，您的账户将自动获得 **4 次免费发票处理服务**。这使您可以在选择套餐之前全面测试 API 集成。

### 3. 生成 API 密钥
1. 登录到 [UpInvoice.eu](https://upinvoice.eu/dashboard) 的控制面板。
2. 转到 **API Tokens** 部分。
3. 点击 **Create Token**，为其命名（例如：“OpenClaw Skill”），然后点击保存。
4. **重要提示**：立即复制您的 API 密钥；该密钥仅会显示一次。

### 4. 在 OpenClaw 中配置
将生成的 API 密钥作为 **Bearer Token** 添加到您的 OpenClaw 工具配置或环境变量中。

---

## 💎 为什么选择 UpInvoice？

- **低成本**：我们提供市场上最具竞争力的价格。查看我们的订阅计划以了解批量处理的折扣信息。
- **高效率**：我们的专用 AI 模型经过优化，能够快速提取数据，通常在 2 秒内完成响应。
- **高准确性**：专门针对欧洲和国际发票格式设计，支持详细的项目信息提取。
- **易于与 ERP 系统同步**：返回的结构化 JSON 数据可以直接映射到 Dolibarr、Holded 或 Sage 等 ERP 系统中。

---

## 🏗️ ERP 集成（工作流程提示）
由于 UpInvoice 返回的数据格式非常规范，机器人可以轻松地将这些数据发送到任何 ERP 系统中。

**推荐的机器人工作流程**：
1. **提取数据**：调用 `processinvoice` 函数获取 JSON 数据。
2. **审核**：向用户展示提取的数据（供应商信息、日期、总金额、项目明细）以供验证。
3. **映射数据**：将 JSON 数据字段映射到您的 ERP 系统的 API（例如 Dolibarr、Holded、Factusol、SAP）。
4. **上传数据**：将经过验证的数据发送到 ERP 系统。

---

## 🤖 机器人使用说明（系统提示）
“当用户提供发票或收据的图片或 PDF 文件时，首先将其转换为 Base64 字符串。然后，调用 `processinvoice` 函数。使用返回的结构化数据与用户核对信息，或准备将其上传到 ERP 系统。”