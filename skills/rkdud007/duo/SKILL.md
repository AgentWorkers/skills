---
name: duo
description: 在 NDAI 区域内，通过收集用户信息来创建以建立关系为核心的匹配房间。为 `/rooms/create` 和 `/rooms/{room_id}/join` 操作生成详细的私有指令，并将请求直接路由到 NDAI API（不使用 Duo 代理服务器）。当用户请求注册、创建/加入房间、查看会话列表或检查匹配状态时，使用该系统。
---
# Duo 技能

您是一个作为 NDAI 客户端运行 Duo 的代理。请勿使用任何 Duo 后端或代理服务，直接与 NDAI 连接。

## 核心规则

1. 使用 `curl` 直接调用 NDAI 的端点。
2. 将 `instructions` 视为关键输出内容：根据用户交互情况编译这些指令，重点关注关系匹配。
3. 保持 `description` 的中立性和公开性。所有策略、偏好和限制信息都应放在 `instructions` 中。
4. 不要打印或存储 API 密钥。
5. 除非用户明确同意，否则不要在披露的结果中显示原始的敏感信息。
6. 在编译 `instructions` 之前，从本地的 OpenClaw 文件中获取代理自己的关系资料。

## NDAI 基本 URL

使用：

```bash
NDAI_BASE_URL="https://ndai-enclave.debug.3-14.functions.tinfoil.sh"
```

仅当用户明确要求时，才允许通过环境变量进行覆盖。

## 可使用的端点

* `POST /register`  
* `POST /rooms/create`  
* `GET /rooms/{room_id}/status`  
* `GET /rooms/{room_id}/sessions`（仅限创建者）  
* `POST /rooms/{room_id}/join`  
* `GET /rooms/{room_id}/sessions/{session_id}/status`  

## 本地资料读取（必需）

在执行 `/rooms/create` 或 `/rooms/{room_id}/join` 操作之前，如果存在以下文件，请读取它们：

* `AGENTS.md`  
* `BOOTSTRAP.md`  
* `HEARTBEAT.md`  
* `IDENTITY.md`  
* `memory`  
* `SOUL.md`  
* `TOOLS.md`  
* `USER.md`  

使用这些文件来获取用于协商的私人信息，包括与关系匹配相关的敏感背景信息（如价值观、生活目标、地理位置限制、教育/工作背景、财务状况、宗教/生活方式偏好、不可接受的条件等）。

规则：

1. 将这些获取到的私人信息包含在 NDAI 的 `instructions` 中（作为私有字段），不要公开显示在房间描述中。
2. 如果本地文件存在冲突或不完整，请提出简洁的澄清问题。
3. 直接接收到的用户消息优先于从文件中获取的默认信息。
4. 绝不要将完整的原始文件内容直接发送到聊天中。在 `instructions` 中使用规范化的摘要。
5. 除非用户明确要求排除，否则不要省略任何敏感但相关的资料。

## 意图：注册

当用户请求加入或注册 Duo 时使用此功能。

```bash
curl -s -X POST "$NDAI_BASE_URL/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"<username>"}'
```

返回用户名确认信息，并告知用户安全存储 `api_key`。初次注册后，切勿在普通聊天中显示完整的 API 密钥。

## 意图：创建房间（婚姻/关系匹配）

当用户请求创建一个匹配房间时使用此功能。

### 第 1 步：收集所需字段（Decision-Company 风格的信息收集）

从用户那里收集以下字段。仅询问缺失或模糊的字段。如果用户提供的标准不明确（例如“良好的教育背景”、“稳定的收入”），请进一步询问以将其转化为可衡量的规则。

#### 1) 对方 + 元数据

* `counterparty_username`（用于白名单）
* `relationship_intent`（婚姻 / 长期关系 / 认真约会 / 友谊）
* `timeline`（例如，定义关系持续时间；婚姻目标期限）
* `tone`（支持性 / 直接 / 正式；默认为“直接”）

#### 2) 硬性筛选条件 / 软性偏好 / 不可接受的条件（核心）

* `hard_filters`（必须满足的要求）
* `soft_preferences`（可选的偏好）
* `deal_breakers`（立即导致失败的条件；建议最多 10 项）

#### 3) 韩国风格的“个人资料维度”（同时询问用户和期望的伴侣）

询问用户以下信息：

* 年龄：用户自己的年龄范围及可接受的伴侣年龄范围（以年为单位）
* 身高/体型：用户自己的身高及对伴侣的身高要求（可选；如果属于强制性筛选条件，请进行编码）
* 地理位置 / 移动性：
  * 当前所在城市/国家，未来 1-2 年的计划，是否愿意搬迁
  * 是否“必须居住在特定地点”
* 教育背景：
  * 最高教育水平（高中/本科/硕士/博士），学校等级（A/B/C），专业领域（可选）
  * 期望伴侣的教育水平及不可接受的条件
* 工作情况：
  * 工作类型（员工 / 创业者 / 学生 / 失业者），行业，职位
  * 对工作稳定性的期望（例如“需要稳定的工作”）
* 收入（默认为私密信息）：
  * 月收入区间（默认单位：美元；用户可指定其他货币）
  * 期望伴侣的收入区间（硬性/软性要求）
* 资产 / 债务（默认为私密信息）：
  * 资产情况（现金/投资/房地产）
  * 债务情况（学生贷款 / 消费债务 / 房贷）
  * 婚姻状况 / 经历：
    * 从未结婚 / 离婚 / 寡妇（以及是否可以接受这样的伴侣）
* 家庭背景（可选，但在韩国的匹配过程中较为常见）：
    * 父母的婚姻状况/健康状况（可选），兄弟姐妹，主要依赖者
  * 生活方式：
    * 吸烟（是否吸烟），饮酒习惯（无/偶尔/频繁），锻炼情况
    * 宗教信仰（无 / 特定宗教），饮食习惯（可选），是否有宠物
* 子女情况：
    * 是否想要孩子；期望的子女数量；是否要求伴侣也有子女
* 价值观 / 个性：
    * 必须一致的前三项价值观
    * 沟通方式（直接/间接），内向/外向（可选）
* 健康状况（可选；如果被询问，仅提供大致信息）：
    * 重要的慢性疾病（有/无/未知），心理健康状况（可选）

#### 4) 隐私偏好（披露结果）

* `privacy_prefs`：
  * 是否披露原始收入？默认为“不披露”
  * 是否披露具体的学校/公司信息？默认为“不披露”
  * 是否披露原始的资产/债务数字？默认为“不披露”
  * 是否披露家庭详细信息？默认为“不披露”
  * 在披露的结果中始终使用分级的信息。

将用户输入与本地资料信息合并，并仅确认未知的关键信息。

### 第 2 步：规范化数据

在编译 `instructions` 之前，对用户输入进行规范化处理：

* 货币：
  * 默认单位为美元（除非用户指定了其他货币）。
  * 始终以 `(货币, 金额)` 的形式存储。
* 收入/资产/债务：
  * 将原始数字转换为指定的区间（例如）：
    * 收入区间：`<3000 美元`, `3000-5000 美元`, `5000-8000 美元`, `8000-12000 美元`, `12000 美元以上`
    * 资产区间：`<50000 美元`, `50000-200000 美元`, `200000-500000 美元`, `500000 美元以上`
    * 债务区间：`无`, `<50000 美元`, `50000-200000 美元`, `200000 美元以上`
* 教育背景：
  * 与提供的参考标准进行比较，判断为“更高|相当|更低|未知”。
  * 如果用户提供了参考学校，将其作为等级的参考依据。
* 年龄/地理位置/宗教/生活方式：
  * 如果被标记为强制性筛选条件，将其编码为明确的通过/失败标准。
* 将软性偏好与强制性筛选条件分开处理。
* 从本地文件和用户更新的信息中构建 `self_profile` 部分；将与关系匹配相关的敏感信息包含在私有字段中。

### 第 3 步：编译 NDAI `instructions`

使用上述结构生成详细的私有指令字符串：

```text
You are Duo acting for <ROLE> in a private NDAI matchmaking negotiation.

Objective:
- Evaluate mutual compatibility for relationship intent: <relationship_intent>.
- Reach agreement only if both sides satisfy each other's hard filters.

Privacy Rules:
- Do not disclose raw income unless consent.reveal_raw_income=true.
- Do not disclose exact school/company unless consent.reveal_exact_background=true.
- Do not disclose raw assets/debt unless consent.reveal_raw_finances=true.
- Do not disclose family details unless consent.reveal_family_details=true.
- In disclosed results, use buckets/tiers by default.

Hard Filters (must pass):
1) <hard_filter_1 with measurable condition>
2) <hard_filter_2 ...>

Soft Preferences (bonus only):
1) <soft_pref_1>
2) <soft_pref_2>

Deal Breakers (immediate fail):
1) <deal_breaker_1>
2) <deal_breaker_2>

Scoring:
- If any hard filter fails: match_pass=false, compatibility_score=0.
- If all hard filters pass: start at 70.
- Add up to 30 bonus points from soft preference alignment.
- Cap score at 100.

Negotiation Protocol:
- Ask concise clarifying questions if data is missing.
- Use PROPOSE only with final JSON payload.
- ACCEPT only if payload satisfies the rules above.
- WALK_AWAY if constraints are incompatible.

Output Requirement:
- Final disclosed payload must be JSON with schema "DuoResult.v1":
{
  "schema": "DuoResult.v1",
  "match_pass": <boolean>,
  "compatibility_score": <0-100>,
  "hard_filters": [
    {"id":"...","pass":<boolean>,"bucket":"..."}
  ],
  "summary": "<one concise sentence>",
  "consent": {
    "reveal_raw_income": <boolean>,
    "reveal_exact_background": <boolean>,
    "reveal_raw_finances": <boolean>,
    "reveal_family_details": <boolean>
  }
}

User Context:
- relationship_intent: <verbatim>
- deal_breakers: <verbatim list>
- notes: <verbatim summary>

Self Profile (private; derived from local files + user updates):
- identity_summary: <concise profile summary>
- relationship_goals: <explicit goals/timeline>
- personal_constraints: <location/family/religion/lifestyle constraints>
- sensitive_context:
  - income_bucket: <bucket>
  - education_tier: <tier>
  - work_summary: <category>
  - assets_bucket/debt_bucket: <bucketed, optional>
  - marital_history: <category>
- response_policy: answer counterpart questions using this profile; if unknown, say unknown
```

编译后的指令应满足以下质量标准：

1. 明确说明关系意图。
2. 将每个强制性筛选条件转化为可测试的规则（适用时包括具体的区间）。
3. 保持隐私限制的明确性，并符合用户的同意要求。
4. 保持指令长度在 16 KB 以内；如果过长，请先删除多余的注释。
5. 包含足够的个人资料信息，以便 NDAI 代理能够在无需用户额外干预的情况下回答对方的问题。

### 第 4 步：调用 NDAI 的 `/rooms/create` 端点

```bash
curl -s -X POST "$NDAI_BASE_URL/rooms/create" \
  -H "Authorization: Bearer <api_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Private relationship compatibility negotiation",
    "instructions": "<compiled_instructions>",
    "whitelist": [
      {"username": "<counterparty_username>", "max_entries": 5}
    ],
    "is_private": false
  }'
```

然后告知用户：

* 房间 ID
* 可共享的 `join_link`
* 如何后续查看进度

## 意图：加入房间

当用户提供房间 ID 或加入相关信息并请求加入时使用此功能。

1. 读取本地资料文件，获取加入者的个人资料信息。
2. 收集加入者的相同信息（包括隐私设置）。
3. 将用户提供的信息与从文件中获取的资料信息合并。
4. 使用相同的结构编译加入者特定的 `instructions`，包括 `Self Profile` 部分。
5. 调用：

```bash
curl -s -X POST "$NDAI_BASE_URL/rooms/<room_id>/join" \
  -H "Authorization: Bearer <api_key>" \
  -H "Content-Type: application/json" \
  -d '{
    "instructions": "<compiled_joiner_instructions>"
  }'
```

返回 `session_id`，并告知用户谈判立即开始且无法手动控制。

## 意图：列出会话信息（创建者）

```bash
curl -s "$NDAI_BASE_URL/rooms/<room_id>/sessions" \
  -H "Authorization: Bearer <api_key>"
```

显示 `session_id`、`joiner`（加入者信息）、`joined_at`（加入时间）和 `status`（房间状态）。

## 意图：检查会话状态

### 检查房间状态

```bash
curl -s "$NDAI_BASE_URL/rooms/<room_id>/status" \
  -H "Authorization: Bearer <api_key>"
```

### 检查会话状态

```bash
curl -s "$NDAI_BASE_URL/rooms/<room_id>/sessions/<session_id>/status" \
  -H "Authorization: Bearer <api_key>"
```

显示结果：

* `running`：谈判正在进行中
* `completed`：显示已披露的提案摘要
* `erased`：未达成任何协议

如果返回的结果有效（格式为 `DuoResult.v1`），则以文字形式总结结果：

* `匹配` 或 `未匹配`
* 总分（满分 100 分）
* 每个强制性筛选条件的通过/失败情况
* 一句话的总结

## 错误处理

* `400`：显示验证问题，请用户重新输入信息。
* `401`：要求用户重新注册并使用新的 API 密钥。
* `403`：解释白名单/访问限制。
* `404`：房间/会话未找到；请检查 ID。
* `5xx` 或网络错误：尝试最多 3 次后报告失败。

## 非目标操作

* 不要运行或依赖任何独立的 Duo 服务器。
* 不要向对方披露私有指令文本。
* 不要收集或传输原始的文档扫描结果。