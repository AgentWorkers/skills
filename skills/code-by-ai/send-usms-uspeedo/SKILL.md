---
name: send-usms-uspeedo
description: 通过 uspeedo 平台的 HTTP API 发送国际短信（USMS）。适用于用户需要发送国际短信、批量短信、验证/通知/营销消息，或者与 uspeedo 的 SendBatchUSMSMessage API 集成的场景。
---
# 通过 uspeedo 发送国际短信

## 技能概述

该技能通过 **uspeedo HTTP API** 发送 **国际短信（USMS）**，支持验证码、通知和营销短信的发送。配置好环境变量后，可以批量发送短信，并根据模板填充内容。有关 API 文档和账户管理信息，请访问 [uspeedo 控制台](https://console.uspeedo.com/)。

## 环境变量

在使用前请进行配置（可以从环境变量或 `.env` 文件中读取）：

| 变量          | 是否必填 | 说明                                      |
|-----------------|---------|-----------------------------------------|
| `USPEEDO_ACCESSKEY_ID`    | 是       | 访问密钥 ID（在控制台创建）                         |
| `USPEEDO_ACCESSKEY_SECRET` | 是       | 访问密钥密钥（在控制台创建）                         |
| `USPEEDO_ACCOUNT_ID`    | 否       | 账户 ID（可选），详见 [文档](https://docs.uspeedo.com/docs/sms/api/)         |
| `USPEEDO TEMPLATE_ID_VERIFICATION` | 根据需要 | 验证码模板 ID                              |
| `USPEEDO TEMPLATE_ID_NOTIFICATION` | 根据需要 | 通知模板 ID                              |
| `USPEEDO TEMPLATE_IDMARKETING` | 根据需要 | 营销模板 ID                              |
| `USPEEDO_SENDER_ID`    | 否       | 发件人 ID；如无则使用空字符串                         |

请为每种要发送的短信类型配置相应的模板 ID。**本技能中使用的所有模板 ID 都是全变量模板**；`TemplateParams` 表示 **实际的短信内容**（通常是一个元素数组，例如 `["您的验证码是 123456，有效期为 5 分钟."]`）。

## 预检和用户指导

在发送短信之前，请检查环境变量是否配置正确。如果未配置，请按照以下步骤指导用户：

**1. 当 `USPEEDO_ACCESSKEY_ID` 或 `USPEEDO_ACCESSKEY_SECRET` 未设置，或者没有 `.env` 文件/环境变量时**

告诉用户直接按照以下步骤操作：  
- 打开 [uspeedo 控制台](https://console.uspeedo.com/?SaleCode=UI2346) 进行注册和登录。  
- 在控制台中创建一个 **访问密钥**，并保存 `ACCESSKEY_ID` 和 `ACCESSKEY_SECRET`。  
- 进入 [短信模板管理](https://console.uspeedo.com/sms/template)，创建一个 **全变量模板**（选择“验证码”或“通知/营销”类型），设置模板内容为 `{1}`，然后提交并等待审核。  
- 审核通过后，从模板列表中复制模板 ID。建议为每种类型（验证码、通知、营销）创建一个模板，并分别设置 `USPEEDO TEMPLATE_ID_VERIFICATION`、`USPEEDO TEMPLATE_ID_NOTIFICATION`、`USPEEDO TEMPLATE_IDMARKETING`。  
- 将 `ACCESSKEY_ID`、`ACCESSKEY_SECRET` 和模板 ID 写入 `.env` 文件或环境变量中，然后重新尝试发送短信。

**2. 当访问密钥已设置，但要发送的短信类型的模板 ID 未配置时**

（例如，要发送验证码短信但 `USPEEDO TEMPLATE_ID_VERIFICATION` 未设置）  
告诉用户：**您要发送验证码/通知/营销短信，但相应的模板 ID 未配置。请前往 [短信模板管理](https://console.uspeedo.com/sms/template)，为该类型创建一个全变量模板（模板内容为 `{1}`），审核通过后设置 `USPEEDO TEMPLATE_ID_VERIFICATION`、`USPEEDO TEMPLATE_ID_NOTIFICATION`、`USPEEDO TEMPLATE_IDMARKETING`。**

## 请求方式

- **URL**：`POST https://api.uspeedo.com/api/v1/usms/SendBatchUSMSMessage`  
- **Content-Type**：`application/json`  
- **认证**：在请求头中添加 `Authorization: Basic base64(ACCESSKEY_ID:ACCESSKEY_SECRET)`。将 `USPEEDO_ACCESSKEY_ID:USPEEDO_ACCESSKEY_SECRET` 进行 Base64 编码，并设置请求头为 `Basic <encoded_result>`。

## 请求体

仅发送 **TaskContent** 数组。每个元素包含以下内容：  
- **TemplateId**：对应类型的模板 ID  
- **SenderId**：如果有发件人 ID 请设置，否则使用空字符串 `""`  
- **Target**：包含以下内容的数组：  
  - **Phone**：电话号码，例如 `13800138000` 或国际格式 `(852)55311111`  
  - **TemplateParams**：字符串数组。对于全变量模板，这表示要发送的短信内容，通常是一个元素（例如 `["您的验证码是 123456，有效期为 5 分钟."]`）

## 示例

**请求体（单条验证码短信）：**

```json
{
  "TaskContent": [
    {
      "TemplateId": "template_id_1",
      "SenderId": "USpeedo",
      "Target": [
        {
          "Phone": "13800138000",
          "TemplateParams": ["Your verification code is 123456"]
        }
      ]
    }
  ]
}
```

**curl 命令示例：**

```bash
curl -X POST "https://api.uspeedo.com/api/v1/usms/SendBatchUSMSMessage" \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic $(echo -n 'YOUR_ACCESSKEY_ID:YOUR_ACCESSKEY_SECRET' | base64)" \
  -d '{
    "TaskContent": [
      {
        "TemplateId": "template_id_1",
        "SenderId": "USpeedo",
        "Target": [
          {
            "Phone": "13800138000",
            "TemplateParams": ["Your verification code is 123456"]
          }
        ]
      }
    ]
  }'
```

## 工作流程：  
1. **预检**：如果 `USPEEDO_ACCESSKEY_ID` 或 `USPEEDO_ACCESSKEY_SECRET` 未设置，或者没有 `.env` 文件/环境变量，请按照第 1 点进行操作。如果用户要发送的短信类型没有配置模板 ID（例如，验证码短信的 `USPEEDO TEMPLATE_ID_VERIFICATION` 未设置），请按照第 2 点操作。  
2. 确认短信类型（验证码/通知/营销），并选择相应的模板 ID。  
3. 从环境变量中读取 `USPEEDO_ACCESSKEY_ID`、`USPEEDO_ACCESSKEY_SECRET`、选定的模板 ID 以及可选的 `USPEEDO_SENDER_ID`。在请求头中设置 `Authorization: Basic base64(ACCESSKEY_ID:ACCESSKEY_SECRET)`，然后向 `https://api.uspeedo.com/api/v1/usms/SendBatchUSMSMessage` 发送 POST 请求。  
4. 构建 `TemplateParams`（对于全变量模板，即为要发送的短信内容）。如有需要，请将电话号码格式化为国际格式（包含国家/地区代码）。  
5. 发送请求，解析返回的 `RetCode` 和 `Message`，并报告发送结果（成功或失败）。如遇到错误代码，请参考下方的 “常见错误” 部分。

## 常见错误  

- **`{"Message":"Failed to parse token","RetCode":215398}`**  
  表示访问密钥（`ACCESSKEY_ID` 或 `ACCESSKEY_SECRET`）无效或已过期。请告知用户：**访问密钥无效。请在 [uspeedo 控制台](https://console.uspeedo.com/) 登录并更新 `ACCESSKEY_ID` 和 `ACCESSKEY_SECRET`。**

## 注意事项：  
- **请勿自行编写发送短信的脚本**；请使用本文档中的 curl 命令示例。  
- 请勿在代码或配置文件中硬编码 `ACCESSKEY_ID` 或 `ACCESSKEY_SECRET`；请从环境变量中读取这些信息。  
- 电话号码应采用国际格式（包含国家/地区代码），例如 `(852)55311111`。  
- 如果没有发件人 ID，请使用空字符串 `""`；否则可能会导致 API 错误。