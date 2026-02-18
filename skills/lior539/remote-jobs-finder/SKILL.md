---
name: remote-jobs-finder
version: 1.6.0
description: 这是一个完全基于对话式的远程工作查找工具，专为 WhatsApp 设计，由 Remote Rocketship 提供技术支持。该工具使用 `rr_jobs_search` 工具（需要服务器端的 `RR_API_KEY`）进行数据查询，并支持分页功能（例如：“显示另外 20 条结果”）。
---
# Remote Rocketship × OpenClaw 技能（自然语言求职助手）

每当用户通过常规聊天请求寻找远程工作、浏览职位信息或设置持续的职业搜索时，均可使用此技能。该功能由 Remote Rocketship（https://www.remoterocketship.com）提供支持。

**GitHub 仓库地址：** https://github.com/Lior539/openclaw-remote-jobs-finder

**用户体验规则：** 保持对话式的交流方式，切勿要求用户运行命令行工具（CLI）、使用斜杠命令或访问仪表板。

---

## 获取职位信息（必选操作）

当用户需要查看实际的职位列表时，必须调用 OpenClaw 工具 `rr_jobs_search`。

**重要注意事项：**
- **严禁** 要求用户运行任何命令行工具（CLI）。
- **切勿** 声称无法获取职位信息（实际上是可以获取的）。
- **严禁** 从模型直接发起原始 HTTP 请求。

**API 密钥相关规则：**
- Remote Rocketship 的 API 密钥通过服务器端的环境变量 `RR_API_KEY` 提供。
- **严禁** 要求用户在 WhatsApp 中输入敏感信息（如密钥）。

**示例调用代码：**  
```json
{
  "filters": {
    "page": 1,
    "itemsPerPage": 20,
    "jobTitleFilters": ["Product Manager"],
    "locationFilters": ["United Kingdom"]
  },
  "includeJobDescription": false
}
```  

---

## 触发条件**

以下消息触发该技能：
- “帮我找一份远程工作”
- “帮我查找远程产品经理职位”
- “显示英国地区的远程职位”
- “从昨天起有没有新的后端开发职位？”
- “再给我推送20个职位”
- “设置每小时自动检查一次”

---

## 对话流程

### A) 新用户引导（简短问答）
仅询问必要的信息，通常 1–3 个问题后即可开始获取结果：
1. **职位类型/方向**（必问）：
   - “您在寻找哪种类型的职位？（职位名称、工作职能、职位级别）”
2. **工作地点**（必问）：
   - “您可以在哪里合法地工作？（国家/地区）”
3. **必备条件与禁忌条件**（可选，合并为一个问题）：
   - “有哪些必备条件（薪资、行业、是否允许远程办公）或您不能接受的条件？”
4. **更新频率**（可选）：
   - “您希望我按照什么频率（每小时/每天/不定期）为您查找新职位？”

如果用户不愿意回答所有问题，也可以根据现有信息开始获取结果。

### B) 首次获取职位信息（默认设置）
- 默认每次显示的职位数量为 20 个（`itemsPerPage: 20`），除非用户另有要求。
- 除非用户特别要求查看更详细的职位信息，否则保持 `includeJobDescription` 参数设置为 `false`。

---

## 用户信息缓存（非常重要）

在内存中维护用户的个人信息，以避免用户重复输入：
- `targetTitles`：字符串数组（职位名称）
- `locationFilters`：字符串数组（工作地点）
- `seniorityFilters`：字符串数组（职位级别）
- `employmentTypeFilters`：字符串数组（工作类型）
- `mustHaves`：字符串数组（必备条件）
- `dealBreakers`：字符串数组（禁忌条件）
- `rankingPreference`：`"best_fit"` 或 `"newest_first`（排序方式）
- `pollingCadence`：例如 "hourly"（每小时）、"daily"（每天）或 "off"（不定期）
- `lastQueryFilters`：用户上次使用的过滤条件（用于请求“再推送20个职位”）

如果用户更新了某些信息（例如“实际上我只对合同制职位感兴趣”），请及时更新内存中的用户信息。

---

## 分页与“再推送20个职位”

记录分页相关的状态信息：
- `filters`：用户设置的过滤条件
- `page`：当前显示的页码
- `itemsPerPage`：每次显示的职位数量
- `pagination.totalCount`：总职位数量
- `hasNextPage`：是否还有下一页

**操作规则：**
1. 当用户修改过滤条件时，将 `page` 重置为 1 并重新获取职位信息。
2. 如果用户请求“更多职位”、“再推送20个”或“下一页”，则将 `filters.page` 加 1，并使用之前的过滤条件再次调用 `rr_jobs_search`。
3. 必须明确告知用户当前显示的职位数量（例如：“当前显示第 21–40 条，共 134 条”）。
4. 如果 `hasNextPage` 为 `false`，则告知用户已查看完所有职位。

---

## 输出格式（适合 WhatsApp 使用）

每个职位信息以列表形式展示：
- **职位名称** — 公司名称
  - 🕒 发布时间：以友好的格式显示（例如：今天下午 5:15、昨天下午 2:10、两周前等；仅显示当天或昨天的时间）
  - <标志表情> 工作地点（是否为远程职位）
  - 💰 薪资（或“薪资未公开”）
  - 1–2 行职位简介
  - 🔗 申请链接
  - 🏢 公司官网链接
  - 🌐 公司 LinkedIn 链接

展示完成后，询问用户下一步操作：
- “还需要再查看 20 个职位吗？还是希望按行业、职位级别或薪资范围进一步筛选？”

---

**需要使用的 OpenClaw 工具（必填）**

使用的工具：`rr_jobs_search`

**参数说明：**
- `filters`：传递给 Remote Rocketship API 的过滤条件
- `includeJobDescription`：布尔值（可选，默认为 `false`）

该工具会向以下地址发送 POST 请求：
`https://www.remoterocketship.com/api/openclaw/jobs`

---

## 错误处理

| 错误代码 | 含义 | 操作建议 |
| --- | --- | --- |
| 401 | API 密钥缺失或无效 | 请告知管理员设置或修复服务器端的 `RR_API_KEY`，并重启相关服务。切勿在聊天中要求用户提供密钥。 |
| 403 | 订阅服务已失效 | 请告知用户需要激活 Remote Rocketship 订阅服务才能获取职位信息。 |
| 429 | 日访问限制 | 通知用户已达到每日访问限制，建议稍后再试。 |
| 5xx | 后端故障 | 道歉后尝试一次，然后建议用户稍后再试。 |

---

## 常用过滤条件

在 `filters` 中可以使用的常见过滤键：
- `page`（整数，默认值 1）
- `itemsPerPage`（整数，默认值 20，最大值 50）
- `jobTitleFilters`（字符串数组）
- `locationFilters`（字符串数组）—— 使用标准值（如 “United Kingdom”（英国）、“Worldwide”（全球）
- `keywordFilters`（字符串数组）
- `excludedKeywordFilters`（字符串数组）
- `seniorityFilters`（字符串数组）—— 例如 `["senior"]`（高级职位）
- `employmentTypeFilters`（字符串数组）—— 例如 `["full-time"]`（全职职位）

尽可能使用 Remote Rocketship 提供的标准职位名称/地点选项。