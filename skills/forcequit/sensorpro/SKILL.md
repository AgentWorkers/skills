---
name: sensorpro
description: "通过 `curl` 使用 Sensorpro 的 REST API（包括身份验证/登录、联系人管理（CRUD 操作）、活动管理、指标/结果查询、数据导入以及中继邮件发送等功能）。当您需要将 Sensorpro 与 OpenClaw 集成时，可以使用这些 API 来执行以下操作：添加/更新联系人信息、创建/发送营销活动、查询邮件打开率/点击率/退信率、执行数据导入操作，或发送一次性中继邮件。"
metadata:
  openclaw:
    emoji: "📨"
    homepage: "https://github.com/forcequit/openclaw-sensorpro"
    requires:
      env: ["SENSORPRO_API_KEY","SENSORPRO_ORG","SENSORPRO_USER","SENSORPRO_PASS"]
      bins: ["curl","python3"]
    primaryEnv: "SENSORPRO_API_KEY"
---
将此技能手册作为调用 Sensorpro REST API 的**实用操作指南**来使用。

**官方文档：**  
- 主页：https://sensorpro.net/api/  
- 联系方式：https://sensorpro.net/api/contacts.html  
- 活动与指标：https://sensorpro.net/api/campaigns.html  
- 中继邮件：https://sensorpro.net/api/sendemail.html  
- 导入功能：https://www.sensorpro.net/api/imports.html  
- 账户信息：https://sensorpro.net/api/account.html  

## **设置（必需）**  
在 OpenClaw 的 `.env` 文件中（或在运行 `curl` 命令前在 shell 中）设置以下环境变量：  
- `SENSORPRO_API_KEY` — API 密钥（用于 `x-apikey` 请求头）  
- `SENSORPRO_ORG` — 组织代码/名称  
- `SENSORPRO_USER` — API 用户名（**必须是 API 用户**）  
- `SENSORPRO_PASS` — API 用户密码  

### **如何获取 API 密钥**  
1. 登录 Sensorpro 界面：  
   - 进入 **API → API 密钥**  
   - 选择 “Sensorpro REST API 默认密钥”  
   - 将密钥值复制到 `SENSORPRO_API_KEY` 变量中  
2. 如果您的 API 密钥受到 IP 地址限制，请将运行 OpenClaw 的机器添加到允许访问的 IP 列表中。  

密钥通过以下 HTTP 请求头传递：  
`x-apikey: $SENSORPRO_API_KEY`  

### **如何创建 API 用户**  
Sensorpro 区分普通用户和 API 用户：  
- **API 用户** 无法访问用户界面，但可以使用 REST API。  
- **普通用户** 可以访问用户界面，但通常无法使用 REST API。  
在 Sensorpro 中创建一个专用的 **API 用户**，并设置相应的用户名和密码：  
- `SENSORPRO_USER`：API 用户名  
- `SENSORPRO_PASS`：API 用户密码  

### **安全注意事项**  
- 将敏感信息（如 API 密钥）存储在 `~/.openclaw/.env` 文件中（或您的进程管理器配置文件中），**切勿** 将其保存在 `SKILL.md` 文件中。  
- **不要将 `.env` 文件提交到 Git 仓库中**。  
- 如果 API 密钥被公开使用，请定期更换它。  

## **常见注意事项**  
- **IP 地址限制**：Sensorpro REST API 可以仅允许特定的 IP 地址访问。  
- 每个响应都会包含 `Result.TotalErrors`；其中 `0` 表示操作成功。  
- 大多数 API 端点在 URL 路径中都需要使用 **登录令牌（Token）**。  
- **登出** 时，服务器可能要求发送请求体（HTTP 411 错误代码）；请使用 `-d '{}'` 参数进行登出操作。  

## **推荐的工作流程**  
1. 登录一次 → 存储登录令牌（`TOKEN`）  
2. 发起一个或多个 API 请求  
3. 登出  

`scripts/` 目录下的脚本实现了上述工作流程。  

---

# **推荐脚本**  
## `scripts/sensorpro_signin.sh`  
- 登录并仅输出登录令牌（便于脚本编写）  

## `scripts/sensorpro_call.sh`  
- 使用 JSON 格式的数据发送 API 请求，并自动处理登录和登出操作。  

---

# **核心 API 端点概览**  

## **身份验证**  
- `POST https://apinie.sensorpro.net/auth/sys/signin`（需要 `x-apikey` 请求头）  
- `POST https://apinie.sensorpro.net/auth/sys/logoff/[Token]`  

## **联系人管理（需要登录令牌）**  
基础路径：`https://apinie.sensorpro.net/api/Contact/<Endpoint>/[Token]`  
- `UpdateAdd`（推荐）  
- `Add`、`Update`  
- `GetContacts`、`GetContactsPaged`  
- `UpdateAddAsync`、`GetUpdateAddAsyncStatus`  
- `ChangeStatus`、`ChangeOptOutStatus`  
- `DeleteContacts`、`ForgetMe`  

## **活动与发送功能**  
基础路径：`https://apinie.sensorpro.net/api/campaign/<Endpoint>/[Token>`（部分 Get 端点的大小写需要注意）  
- `AddCampaign`、`AddDesign`、`AddSegment`、`AddBroadcast`  

## **活动结果与指标**  
- `POST https://apinie.sensorpro.net/api/Campaign/GetBroadcastStatus/[Token]`  
- `POST https://apinie.sensorpro.net/api/campaign/GetCampaignResults/[Token]`  
- `POST https://apinie.sensorpro.net/api/campaign/GetCampaignResultsLinks/[Token]`  

## **中继邮件**  
- `POST https://apinie.sensorpro.net/api/Email/SendEmail/[Token]`  

## **导入功能**  
- `POST https://apinie.sensorpro.net/api/import/ExecuteFTPImport/[Token]`  
- `POST https://apinie.sensorpro.net/api/import/GetImportStatus/[Token]`  
- `POST https://apinie.sensorpro.net/api/import/ClearTagList/[Token]`  

## **账户管理**  
- `POST https://apinie.sensorpro.net/api/Account/AddSubOrganization/[Token]`  
- `POST https://apinie.sensorpro.net/api/Account/AddUpdateUser/[Token]`  

---

**示例**  
- **手动登录（使用 curl 命令）**  
```bash
curl -sS -X POST "https://apinie.sensorpro.net/auth/sys/signin" \
  -H "Content-Type: application/json" \
  -H "x-apikey: ${SENSORPRO_API_KEY}" \
  -d '{"Organization":"'"${SENSORPRO_ORG}"'","User":"'"${SENSORPRO_USER}"'","Password":"'"${SENSORPRO_PASS}"'"}'
```  

- **联系人管理：添加/更新联系人（通过电子邮件）**  
```bash
curl -sS -X POST "https://apinie.sensorpro.net/api/Contact/UpdateAdd/${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "AddToList": [],
    "Contact": [{"PersonalEMail":"someone@example.com","FirstName":"","LastName":""}],
    "Options":{"Parameters":{},"Action":""},
    "ReturnFailedRequests": true,
    "UpdateByKey": "email",
    "SendWelcomeEmail": false,
    "SignupFormId": "00000000-0000-0000-0000-000000000000"
  }'
```  

- **活动指标：获取活动结果**  
```bash
curl -sS -X POST "https://apinie.sensorpro.net/api/campaign/GetCampaignResults/${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"CampaignId": 53}'
```  

- **中继邮件：发送邮件（一次性操作）**  
```bash
curl -sS -X POST "https://apinie.sensorpro.net/api/Email/SendEmail/${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "From": {"DisplayName":"Marketing","Email":"marketing@myco.net"},
    "To": [{"DisplayName":"","Email":"recipient@example.com"}],
    "Cc": [],
    "Bcc": [],
    "Headers": {},
    "ReplyTo": null,
    "ReturnPath": null,
    "Subject": "Hello",
    "HTMLMessageStyle": "",
    "HTMLMessageEncoded": "<html><body><p>Hello</p></body></html>",
    "PlainTextMessage": "Hello",
    "MsgType": 0,
    "MailEncoding": "UTF8",
    "Schedule": {"DelayByMinutes": 0, "DelayUntilUTC": ""}
  }'
```