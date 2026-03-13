---
name: ai-dating
description: "该技能支持约会和配对工作流程。当用户请求交友、寻找伴侣、进行配对服务或更新个人资料/偏好设置时，可以使用该技能。该技能会执行 `dating-cli` 命令来完成个人资料的设置、任务创建/更新、匹配结果检查以及联系信息的展示等操作。"
---
# 人工智能辅助约会

该功能通过 `dating-cli` 支持约会和匹配工作流程。  
它帮助用户创建个人资料、定义伴侣偏好、查看匹配结果、显示联系方式，并提交聊天后的评价。

## 触发条件  
当出现以下任意意图时，触发此功能：  
1. 用户明确表示希望交友、寻找伴侣、约会或进行匹配。  
2. 用户提供个人信息并请求系统帮助寻找合适的对象。  
3. 用户描述伴侣偏好（如性别、身高、收入、城市、性格、爱好）并请求匹配服务。  

## 语言对齐规则  
在构建 `dating-cli` 命令参数时，所有自由文本字段和标签应使用与用户相同的语言（例如 `--task-name`、`--character-text`、`--hobby-text`、`--ability-text`、`--intention`、`--preferred-*` 等字段以及 `--comment`）。  
- 除非用户明确要求翻译，否则不要翻译用户提供的内容。  
- 确保整个命令中的语言风格保持一致（例如，如果用户使用中文，则字符串参数中也应使用中文）。  

## 标准执行流程（AI 代理）  
1. 检查命令行工具（CLI）是否可用。  
   ```bash
command -v dating-cli
dating-cli --help
```  
   如果缺失，请安装：  
   ```bash
npm install -g dating-cli
# or
bun install -g dating-cli
```  
2. 检查本地 CLI 的状态（包含完整示例）。  
   ```bash
dating-cli config show
dating-cli config path
```  
3. 注册或登录（包含完整参数示例）。  
   ```bash
dating-cli register --username "amy_2026"
dating-cli login --username "amy_2026" --password "123456"
```  
   
> **注意：** `profile update`、`task create` 和 `task update` 的参数是可选的。  
> 对于个人资料图片，首先使用 `POST /minio/upload` 上传图片文件，然后通过 `--photo-url` 参数传递返回的图片 URL（该参数对应于 `/member-profile` 中的 `photoUrls` 字段）。  

4. 解析用户的自我描述并更新个人资料（包含完整参数示例）。用户无需填写所有字段，只需提供他们已有的信息即可。  
   ```bash
dating-cli profile update \
  --gender male \
  --birthday 1998-08-08 \
  --height-cm 180 \
  --weight-kg 72 \
  --annual-income-cny 300000 \
  --character-text "sincere, steady, humorous" \
  --hobby-text "badminton, travel, photography" \
  --ability-text "cooking, communication, English" \
  --major "Computer Science" \
  --nationality "China" \
  --country "China" \
  --province "Zhejiang" \
  --city "Hangzhou" \
  --address-detail "Xihu District" \
  --current-latitude 30.27415 \
  --current-longitude 120.15515 \
  --current-location-text "Hangzhou West Lake" \
  --photo-url "https://cdn.example.com/photos/amy-1.jpg" \
  --photo-url "https://cdn.example.com/photos/amy-2.jpg" \
  --email "amy@example.com" \
  --phone "13800000000" \
  --telegram "amy_tg" \
  --wechat "amy_wechat" \
  --whatsapp "amy_wa" \
  --signal-chat "amy_signal" \
  --line "amy_line" \
  --snapchat "amy_snap" \
  --instagram "amy_ins" \
  --facebook "amy_fb" \
  --other-contact "x=amy_xhs" \
  --other-contact "discord=amy#1234"
```  
5. 解析用户的伴侣偏好并创建匹配任务（包含完整参数示例）。用户无需填写所有字段，只需提供他们已有的信息即可。  
   ```bash
dating-cli task create \
  --task-name "Find partner in Hangzhou" \
  --preferred-gender-filter '{"eq":"female"}' \
  --preferred-height-filter '{"gte":165,"lte":178}' \
  --preferred-income-filter '{"gte":200000}' \
  --preferred-city-filter '{"eq":"Hangzhou"}' \
  --preferred-nationality-filter '{"eq":"China"}' \
  --preferred-education-filter '{"contains":"Bachelor"}' \
  --preferred-occupation-filter '{"contains":"Product"}' \
  --preferred-education-stage "Bachelor or above" \
  --preferred-occupation-keyword "Product Manager" \
  --preferred-hobby-text "reading, travel" \
  --preferred-character-text "kind, positive" \
  --preferred-ability-text "strong communication" \
  --intention "long-term relationship" \
  --hobby-embedding-min-score 0.72 \
  --character-embedding-min-score 0.70 \
  --ability-embedding-min-score 0.68 \
  --intention-embedding-min-score 0.70 \
  --preferred-contact-channel telegram
```  
6. 如果存在未完成的 `taskId` 且用户未明确请求新任务，则更新现有任务（包含完整参数示例）。  
   ```bash
dating-cli task update 12345 \
  --task-name "Update criteria - Hangzhou/Shanghai" \
  --preferred-gender-filter '{"eq":"female"}' \
  --preferred-height-filter '{"gte":163,"lte":180}' \
  --preferred-income-filter '{"gte":250000}' \
  --preferred-city-filter '{"in":["Hangzhou","Shanghai"]}' \
  --preferred-hobby-text "reading, travel, sports" \
  --preferred-character-text "independent, optimistic" \
  --preferred-ability-text "communication and collaboration" \
  --intention "serious relationship with marriage plan" \
  --hobby-embedding-min-score 0.70 \
  --character-embedding-min-score 0.70 \
  --ability-embedding-min-score 0.65 \
  --intention-embedding-min-score 0.68 \
  --preferred-contact-channel wechat
```  
7. 查询任务状态（包含完整参数示例）。  
   ```bash
dating-cli task get 12345
```  
8. 执行 `check` 命令以查看匹配结果（包含分页示例）。每页返回 10 位候选人。如需查看后续页面，请使用 `--page` 参数。  
   如果返回结果为 `NO_RESULT_RETRY_now`，则根据需要再次调用 `check` 命令。  
   如果返回结果为 `MATCH_FOUND`，则继续进行联系方式的展示。  
   建议用户通过 `dating-cli profile update --email ...` 注册电子邮件地址，以便接收定期的匹配推荐通知。  

9. 从匹配结果中选择最合适的候选人并显示其联系方式（包含完整参数示例）。  
   ```bash
dating-cli reveal-contact 67890
```  
10. 如有需要，提交评价（包含完整参数示例）。  
   ```bash
dating-cli review 67890 --rating 5 --comment "Good communication and aligned values"
```  
11. 可选命令（包含完整参数示例）。  
   ```bash
dating-cli task stop 12345
dating-cli logout
```  

## 参考文档  
有关详细字段行为、验证规则和响应结构的更多信息，请参阅：  
- `references/dating-cli-operations.md`