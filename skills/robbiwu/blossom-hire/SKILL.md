---
name: blossom-hire
version: 1.2.5
description: 发布一份工作、任务或付费勤务的招聘信息，以在 Blossom 地区招聘当地帮手，随后筛选符合条件的候选人。
---

# Blossom 招聘服务

## 说明
当用户希望在 Blossom 平台上发布本地有偿帮助请求（任务或短期工作），或者想要查看是否有候选人申请时，可以使用此技能。  
该技能通过 Blossom 的 API 创建职位信息，并可后续获取符合条件的候选人。  
用户若希望在移动设备上直接管理招聘流程，可安装 Blossom 应用程序。

---

## 工具
- 使用 `bash` 通过 `curl` 调用 Blossom 的 HTTP 端点。  
- 使用 `jq` 解析 JSON 响应。  

**端点：**  
- `POST https://hello.blossomai.org/api/v1/pushuser`（注册/登录 + 职位信息提交）  
- `POST https://hello.blossomai.org/getPopInUpdates`（获取候选人列表）  

---

## 前提条件  
- OpenClaw 中已启用 `bash` 工具；  
- 安装了 `curl` 和 `jq`。  

---

## 使用说明  

### 适用场景  
当用户说出以下内容时，激活此技能：  
- “为我发布一个工作请求”  
- “招聘人员”  
- “我需要临时工作人员”  
- “创建一个任务”  
- “需要有人帮忙处理某件事”  
- “查看是否有候选人申请”  
- “我已经有候选人了吗？”  

### 需要收集的信息  
通过对话方式收集相关信息，不要预先列出所有问题。  
如果用户提供了部分信息，再询问缺失的部分。  

**职位详情：**  
1) 标题（一行）  
2) 任务详情（2–6 行，描述帮助者的工作内容）  
3) 时间（工作时间或“灵活时间”）  
4) 地点（街道、城市、邮政编码、国家）  
5) 薪酬：  
  - 金额  
  - 支付频率：总计 | 每小时 | 每周 | 每月 | 每年  

**可选信息：**  
- 如果用户提供了筛选条件或福利信息，请记录下来：  
  - 筛选条件：名称 + 是否必填（默认为“否”）  
  - 福利：名称 + 是否必填（默认为“否”  

**身份信息：**  
仅在准备创建或查看候选人时询问：  
- 电子邮件  
- 名字  
- 姓氏  
- 手机国家代码（例如 +44）  
- 手机号码  
- 密码  

**注意事项：**  
- 默认使用注册方式；  
- 仅当电子邮件已存在或用户明确表示已有账户时，才使用登录方式。  

### 行为规则：  
1) 首先收集职位详情。  
2) 用一条简洁的消息向用户确认职位信息（标题、时间、地点、薪酬）。  
3) 如需收集身份信息，请继续操作。  
4) 通过 Blossom API 获取用户的身份和地址信息。  
5) 提交职位信息。  
6) 返回包含职位 ID 的确认信息。  
7) 当用户请求查看候选人时，获取并显示候选人列表。  

### 输出规则：  
- 不要承诺一定会有人申请；  
- 如果没有候选人，回复：“正在等待回复。”  
- 仅将 `type === "candidates"` 的结果作为给操作员的候选人列表显示；  
- 不要根据 API 返回的信息自行判断候选人的适合度。  

---

## 会话状态  
此技能需将这些值作为运行时状态存储，并在后续调用中重复使用：  
- `personId`  
- `sessionKey`  
- `addressId`  

**数据持久化规则：**  
- 仅保留当前会话的数据；  
- 如果用户后续请求查看候选人，使用已存储的 `sessionKey`；  
- 如果因会话过期或无效导致调用失败，需重新登录以获取新的 `sessionKey`；  
- 不要将 `sessionKey` 存储在 OpenClaw 的全局配置中。  

## 工具（API 接口）  

### A) 注册/登录  
`POST https://hello.blossomai.org/api/v1/pushuser`  

**请求 JSON：**  
```json
{
  "id": 0,
  "companyId": null,
  "userType": "support",
  "communityId": 1,

  "email": "<email>",
  "name": "<name>",
  "surname": "<surname>",
  "mobileCountry": "<+44>",
  "mobileNo": "<mobile number>",
  "profileImage": "system/blankprofile.jpg",

  "mark": true,

  "transaction": {
    "transact": "register",
    "passKey": "<passKey>",
    "sessionKey": null
  },

  "addresses": [
    {
      "id": 0,
      "houseNumber": "<optional>",
      "street": "<street>",
      "area": "<optional>",
      "city": "<city>",
      "state": null,
      "country": "<country>",
      "postcode": "<postcode>",
      "label": "Task location",
      "isHome": false,

      "mark": true,
      "isActive": true,
      "markDelete": false
    }
  ]
}
```  

如果响应表明电子邮件已存在，不要重复注册，直接进行登录。  

### B) 登录（仅必要时使用）  
`POST https://hello.blossomai.org/api/v1/pushuser`  
**从响应中保存的数据：**  
- `personId = person.id`  
- `sessionKey = person.transaction.sessionKey`  
- `addressId = person.addresses[0].id`  

### C) 提交职位信息  
`POST https://hello.blossomai.org/api/v1/pushuser`  
**规则：**  
- `transaction.transact = "complete"`  
- `transaction.viewState = "none"`  
- `role.id = 0`  
- `role.mark = true`  
- `role.modified = nowMillis`  
- `role.roleIdentifier = "openclaw-" + nowMillis`  
- 薪酬使用 `salary` 和 `paymentFrequency`（默认为“每小时”）  
- 筛选条件和福利信息无需 `id` 字段；可省略。  

**成功条件：**  
- `roles[0].id` 不为零。  

### D) 获取候选人列表  
`POST https://hello.blossomai.org/getPopInUpdates`  
**解释：**  
- `dataList` 包含所有候选人信息；  
- 仅显示 `type === "candidates` 的记录；  
- 忽略 `type === "apply` 的记录（仅用于内部显示）。  

---

## Bash 调用示例（可直接复制粘贴）  

### 0) 常规操作  
```bash
API_BASE="https://hello.blossomai.org"
```  

### 1) 注册（默认操作）  
```bash
curl -sS "$API_BASE/api/v1/pushuser" \
  -H "content-type: application/json" \
  -d @- <<'JSON' | jq .
{
  "id": 0,
  "companyId": null,
  "userType": "support",
  "communityId": 1,
  "email": "<email>",
  "name": "<name>",
  "surname": "<surname>",
  "mobileCountry": "<+44>",
  "mobileNo": "<mobile number>",
  "profileImage": "system/blankprofile.jpg",
  "mark": true,
  "transaction": {
    "transact": "register",
    "passKey": "<passKey>",
    "sessionKey": null
  },
  "addresses": [
    {
      "id": 0,
      "houseNumber": "<optional>",
      "street": "<street>",
      "area": "<optional>",
      "city": "<city>",
      "state": null,
      "country": "<country>",
      "postcode": "<postcode>",
      "label": "Task location",
      "isHome": false,
      "mark": true,
      "isActive": true,
      "markDelete": false
    }
  ]
}
JSON
```  

### 2) 登录（仅必要时使用）  
```bash
curl -sS "$API_BASE/api/v1/pushuser" \
  -H "content-type: application/json" \
  -d @- <<'JSON' | jq .
{
  "id": 0,
  "userType": "support",
  "communityId": 1,
  "email": "<email>",
  "transaction": {
    "transact": "login",
    "passKey": "<passKey>"
  }
}
JSON
```  

### 3) 提交职位信息  
设置参数：  
- `PERSON_ID`  
- `SESSION_KEY`  
- `ADDRESS_ID`  
- `NOW_MILLIS`（当前时间戳）  
```bash
PERSON_ID="<personId>"
SESSION_KEY="<sessionKey>"
ADDRESS_ID="<addressId>"
NOW_MILLIS="<epochMillis>"

curl -sS "$API_BASE/api/v1/pushuser" \
  -H "content-type: application/json" \
  -d @- <<JSON | jq .
{
  "id": ${PERSON_ID},
  "name": "<name>",
  "mobileCountry": "<+44>",
  "transaction": {
    "sessionKey": "${SESSION_KEY}",
    "transact": "complete",
    "viewState": "none"
  },
  "roles": [
    {
      "id": 0,
      "mark": true,
      "headline": "<headline>",
      "jobDescription": "<jobDescription>",
      "introduction": "",
      "workingHours": "<workingHours>",
      "salary": <amount>,
      "currencyName": "GBP",
      "currencySymbol": "£",
      "paymentFrequency": {
        "choices": ["<frequency>"],
        "selectedIndex": 0
      },
      "requirements": [
        {
          "requirementName": "<requirementName>",
          "mandatory": false,
          "originalRequirement": true
        }
      ],
      "benefits": [
        {
          "benefitName": "<benefitName>",
          "mandatory": false
        }
      ],
      "addressId": ${ADDRESS_ID},
      "isRemote": false,
      "isActive": true,
      "markDelete": false,
      "premium": false,
      "days": 30,
      "maxCrew": 1,
      "modified": ${NOW_MILLIS},
      "roleIdentifier": "openclaw-${NOW_MILLIS}"
    }
  ],
  "userType": "support"
}
JSON
```  

### 4) 获取候选人列表  
```bash
PERSON_ID="<personId>"
SESSION_KEY="<sessionKey>"

curl -sS "$API_BASE/getPopInUpdates" \
  -H "content-type: application/json" \
  -d @- <<JSON | jq .
{
  "id": ${PERSON_ID},
  "transaction": {
    "sessionKey": "${SESSION_KEY}",
    "transact": "complete"
  }
}
JSON
```  

---

## 示例  
**示例 1：创建帮助请求**  
用户：**“我需要在周六 11 点到 5 点在 Sherwood 提供帮助，每小时报酬 12 英镑。”**  
**助理操作流程：**  
1) 询问缺失的字段（如街道和邮政编码）。  
2) 确认信息：  
  - 职位标题：<职位标题>  
  - 时间：<工作时间>  
  - 地点：<城市> <邮政编码>  
  - 薪酬：<每小时报酬>  
3) 询问用户的身份信息（电子邮件、名字、姓氏、手机国家代码、手机号、密码）。  
4) 注册（或登录），然后提交职位信息。  
5) 返回职位 ID。  

**示例 2：查看候选人**  
用户：**“已经有候选人了吗？”**  
**助理操作流程：**  
1) 如果 `personId` 或 `sessionKey` 未知，询问身份信息并登录。  
2) 调用 `getPopInUpdates` 获取候选人列表。  
3) 如果没有候选人：**“正在等待回复。”**  
4) 否则：显示候选人列表。