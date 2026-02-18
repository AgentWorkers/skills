---
name: sensorpro
description: "在 OpenClaw 中管理您的 Sensorpro 电子邮件营销账户。"
metadata:
  openclaw:
    emoji: "📨"
    homepage: "https://github.com/forcequit/openclaw-sensorpro"
    requires:
      env: ["SENSORPRO_API_KEY","SENSORPRO_ORG","SENSORPRO_USER","SENSORPRO_PASS"]
      bins: ["curl","python3"]
    primaryEnv: "SENSORPRO_API_KEY"
---
使用此技能来**管理您在 OpenClaw 中的 Sensorpro 电子邮件营销账户**。

**官方文档：**
- 主页：https://sensorpro.net/api/
- 联系人：https://sensorpro.net/api/contacts.html
- 活动 + 统计数据：https://sensorpro.net/api/campaigns.html
- 中继邮件：https://sensorpro.net/api/sendemail.html
- 导入数据：https://www.sensorpro.net/api/imports.html
- 账户：https://sensorpro.net/api/account.html

## 设置（必需）
在您的 OpenClaw `.env` 文件中（或在运行 `curl` 命令之前在 shell 中）设置以下环境变量：
- `SENSORPRO_API_KEY` — API 密钥（用于 `x-apikey` 标头）
- `SENSORPRO_ORG` — 组织代码/名称
- `SENSORPRO_USER` — API 用户名（**必须是 API 用户**）
- `SENSORPRO_PASS` — API 用户密码

### 如何获取 API 密钥
通过 Sensorpro 界面操作：
1) 进入 **API → API 密钥**
2) 选择 **“Sensorpro REST API 默认密钥”**
3) 将密钥值复制到 `SENSORPRO_API_KEY` 变量中
4) 如果您的 API 密钥受到 IP 地址限制，请将调用该密钥的 **IP 地址** 添加到白名单中（即运行 OpenClaw 的机器的 IP 地址）

API 密钥通过以下 HTTP 标头传递：
- `x-apikey: $SENSORPRO_API_KEY`

### 如何创建 API 用户
Sensorpro 区分普通用户和 API 用户：
- **API 用户** 没有界面访问权限，但**可以**使用 REST API。
- **普通用户** 有界面访问权限，但通常**不能**使用 REST API。
在 Sensorpro 中创建一个专用的 **API 用户**，并设置以下信息：
- `SENSORPRO_USER` 为该用户名
- `SENSORPRO_PASS` 为该密码

### 安全性注意事项（非常重要）
- 将敏感信息存储在 `~/.openclaw/.env` 文件中（或您的进程管理器中），**不要** 将其保存在 `SKILL.md` 文件中。
- **不要** 将 `.env` 文件提交到 Git 仓库中。
- 如果 API 密钥被公开使用，请定期更换它。

## 常见问题
- **IP 地址白名单**：Sensorpro 的 REST API 可以仅允许特定的 IP 地址访问。
- 每个响应都会包含 `Result.TotalErrors`；当该值为 `0` 时表示操作成功。
- 大多数 API 端点需要在 URL 路径中包含 **登录令牌**（`Token`）。
- **登出**：服务器可能要求发送请求体（否则会返回 HTTP 411 错误）。使用 `-d '{}'` 来发送空请求体以完成登出操作。

## 推荐的工作流程：
1) 登录一次 → 存储 `TOKEN`
2) 执行一个或多个 API 调用
3) 登出

**示例（bash 命令）：**
```bash
TOKEN=$(curl -sS -X POST "https://apinie.sensorpro.net/auth/sys/signin" \
  -H "Content-Type: application/json" \
  -H "x-apikey: ${SENSORPRO_API_KEY}" \
  -d "{\"Organization\":\"${SENSORPRO_ORG}\",\"User\":\"${SENSORPRO_USER}\",\"Password\":\"${SENSORPRO_PASS}\"}" \
| python3 -c 'import sys,json; print(json.load(sys.stdin).get("Token",""))')

# Call an endpoint (example)
curl -sS -X POST "https://apinie.sensorpro.net/api/Contact/UpdateAdd/${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"AddToList":[],"Contact":[{"PersonalEMail":"someone@example.com"}],"Options":{"Parameters":{},"Action":""},"ReturnFailedRequests":false,"UpdateByKey":"email","SendWelcomeEmail":false,"SignupFormId":"00000000-0000-0000-0000-000000000000"}'

# Log off (some servers require a body)
curl -sS -X POST "https://apinie.sensorpro.net/auth/sys/logoff/${TOKEN}" \
  -H "Content-Type: application/json" -d '{}'
```

---

# 核心 API 端点（快速参考）

## 认证
- `POST https://apinie.sensorpro.net/auth/sys/signin` （需要 `x-apikey` 标头）
- `POST https://apinie.sensorpro.net/auth/sys/logoff/[Token]`

## 联系人（需要登录令牌）
基础路径：`https://apinie.sensorpro.net/api/Contact/<Endpoint>/[Token]`
- `UpdateAdd`（推荐使用）
- `Add`, `Update`
- `GetContacts`, `GetContactsPaged`
- `UpdateAddAsync`, `GetUpdateAddAsyncStatus`
- `ChangeStatus`, `ChangeOptOutStatus`
- `DeleteContacts`, `ForgetMe`

## 活动 + 发送邮件
基础路径：`https://apinie.sensorpro.net/api/campaign/<Endpoint>/[Token]`（注意某些获取端点的大小写要求）
- `AddCampaign`, `AddDesign`, `AddSegment`, `AddBroadcast`

## 活动结果 / 统计数据
- `POST https://apinie.sensorpro.net/api/Campaign/GetBroadcastStatus/[Token]`
- `POST https://apinie.sensorpro.net/api/campaign/GetCampaignResults/[Token]`
- `POST https://apinie.sensorpro.net/api/campaign/GetCampaignResultsLinks/[Token]`

## 中继邮件
- `POST https://apinie.sensorpro.net/api/Email/SendEmail/[Token]`

## 导入数据
- `POST https://apinie.sensorpro.net/api/import/ExecuteFTPImport/[Token]`
- `POST https://apinie.sensorpro.net/api/import/GetImportStatus/[Token]`
- `POST https://apinie.sensorpro.net/api/import/ClearTagList/[Token]`

## 账户
- `POST https://apinie.sensorpro.net/api/Account/AddSubOrganization/[Token]`
- `POST https://apinie.sensorpro.net/api/Account/AddUpdateUser/[Token]`

---

# 示例代码
## 登录（手动使用 curl）
```bash
curl -sS -X POST "https://apinie.sensorpro.net/auth/sys/signin" \
  -H "Content-Type: application/json" \
  -H "x-apikey: ${SENSORPRO_API_KEY}" \
  -d '{"Organization":"'"${SENSORPRO_ORG}"'","User":"'"${SENSORPRO_USER}"'","Password":"'"${SENSORPRO_PASS}"'"}'
```

## 联系人：更新联系人信息（通过电子邮件添加/修改）
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

## 活动统计：获取活动结果
```bash
curl -sS -X POST "https://apinie.sensorpro.net/api/campaign/GetCampaignResults/${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"CampaignId": 53}'
```

## 中继邮件：发送邮件（一次性操作）
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