---
name: signl4
description: 使用 SIGNL4 的入站 Webhook（URL 中包含团队密钥）来发送和关闭 SIGNL4 警报。
metadata: {"openclaw":{"emoji":"🚨","requires":{"bins":["curl"],"env":["SIGNL4_TEAM_SECRET"]},"primaryEnv":"SIGNL4_TEAM_SECRET"}}
---

## 概述  
使用此技能可通过 SIGNL4 的 **入站 webhook** 与其进行交互：  
- **向 SIGNL4 团队发送警报**  
- **使用外部关联 ID 关闭（解决）警报**  

身份验证通过 **嵌入在 webhook URL 中的团队密钥** 来完成。  

Webhook 文档：  
https://docs.signl4.com/integrations/webhook/webhook.html  

---

## 必需配置  
必须设置以下环境变量：  
- `SIGNL4_TEAM_SECRET` – 用于 webhook URL 的 SIGNL4 团队密钥  

（可选，高级配置）：  
- `SIGNL4_WEBHOOK_BASE` – 默认值为 `https://connect.signl4.com/webhook`  

---

## 从用户处收集的输入信息  

### 发送警报时  
- **必填项**：  
  - **标题** – 简短摘要  
  - **消息** – 详细描述  
  - **外部 ID** – 强烈推荐（后续关闭警报时需要）  

- **可选项**：  
  - **服务** (`X-S4-Service`)  
  - **警报场景** (`X-S4-AlertingScenario` – 例如 `single_ack`, `multi_ack`, `emergency`)  
  - **位置** (`X-S4-Location`，格式：`"lat,long"`)  

### 关闭警报时  
- **必填项**：  
  - **外部 ID** – 必须与创建警报时使用的 ID 相匹配  

---

## 如何发送警报  

- **规则**：  
  - 如果警报可能需要后续关闭，请务必包含 `X-S4-ExternalID`。  
  - 使用 `X-S4-Status: "new"` 来创建警报。  

### 命令模板  
设置 webhook URL：  
```sh
WEBHOOK_URL="${SIGNL4_WEBHOOK_BASE:-https://connect.signl4.com/webhook}/${SIGNL4_TEAM_SECRET}"
```  

发送警报：  
```sh
curl -sS -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "Title": "<TITLE>",
    "Message": "<MESSAGE>",
    "X-S4-ExternalID": "<EXTERNAL_ID>",
    "X-S4-Status": "new",
    "X-S4-Service": "<OPTIONAL_SERVICE>",
    "X-S4-AlertingScenario": "<OPTIONAL_SCENARIO>",
    "X-S4-Location": "<OPTIONAL_LAT_LONG>",
    "X-S4-SourceSystem": "OpenClaw"
  }'
```  

### 需要反馈的信息：  
- 确认警报已发送  
- 重复关键信息：  
  - 标题  
  - 外部 ID  
  - 可选的服务/场景  

如果请求失败：  
- 检查 `SIGNL4TEAM_SECRET` 是否已设置且正确  
- 确保 JSON 字段有效  

---

## 如何关闭（解决）警报  

- **规则**：  
  - 要关闭警报，必须使用与创建警报时相同的 **外部 ID**  
  - 将 `X-S4-Status` 设置为 `resolved`  

### 命令模板：  
```sh
curl -sS -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "X-S4-ExternalID": "<EXTERNAL_ID>",
    "X-S4-Status": "resolved"
  }'
```  

### 需要反馈的信息：  
- 确认已为给定的外部 ID 发送了关闭请求  
- 如果缺少外部 ID，请向用户询问该 ID  

---

## 安全注意事项  
- 将 `SIGNL4_TEAM_SECRET` 视为机密信息  
- 严禁在响应或日志中打印或显示团队密钥