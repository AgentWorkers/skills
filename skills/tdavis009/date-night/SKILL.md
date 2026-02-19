---
name: date-night
description: 您的AI约会之夜管家——通过浏览器自动化功能来规划、预订并协调整个晚上的活动。只需说“安排一场约会之夜”，它就能处理所有事务：餐厅预订（OpenTable、Resy）、电影票购买（Fandango、Megaplex、AMC）、活动门票查询（SeatGeek、Ticketmaster、StubHub）、天气查询、出行时间估算、预算统计、日历事件设置以及通知合作伙伴。系统支持自定义饮食偏好、育儿提醒、常用影院选择以及保姆费用预算功能。初次使用时会有详细的引导流程；之后只需告诉它您想要的约会类型即可。可触发操作包括：安排约会之夜、预订晚餐座位、使用OpenTable/Resy寻找餐厅、查询电影放映信息、购买音乐会门票、查找附近的体育赛事门票、同时安排晚餐和电影票、提供约会建议、取消预订或修改预订详情。
metadata:
  openclaw:
    emoji: "💑"
    requires:
      bins:
        - playwright-cli
      anyBins:
        - gog
        - gcal
        - ical
      optionalBins:
        - goplaces
        - imsg
        - jq
      optionalEnv:
        - GOOGLE_PLACES_API_KEY
      tools:
        - web_search
        - web_fetch
        - browser
        - message
    install:
      - id: playwright-cli
        kind: npm
        package: "@anthropic-ai/playwright-cli@latest"
        bins: ["playwright-cli"]
        label: "Install playwright-cli (npm)"
      - id: chromium
        kind: shell
        command: "npx playwright install chromium"
        label: "Install Chromium for playwright-cli"
    access:
      local_data:
        - path: "~/.openclaw/skills/date-night/config.json"
          purpose: "User preferences (name, email, phone, dietary, location)"
          sensitive: true
        - path: "~/.openclaw/skills/date-night/state/*.json"
          purpose: "Browser session cookies for Resy (opt-in, clearable)"
          sensitive: true
        - path: "~/.openclaw/skills/date-night/history.jsonl"
          purpose: "Date night log (restaurant, date, rating)"
          sensitive: false
      messaging:
        - channel: "configured notification channel"
          purpose: "Partner notifications — always drafted and shown for approval before sending"
          autonomous: false
      pii:
        - "Name, email, phone stored locally for auto-filling reservation forms"
        - "Never transmitted except to booking sites during form submission"
      sms_read:
        - purpose: "Retrieve booking verification codes from specific senders only"
          scope: "Last 1-2 messages from known booking service short codes (e.g. OpenTable 22395)"
          broad_scan: false
          always_on: false
          trigger: "Only during active reservation flow when site sends SMS verification"
      email_read:
        - purpose: "Find confirmation numbers for modify/cancel requests only"
          scope: "Targeted query (e.g. 'from:opentable reservation confirmed'), max 5 results"
          always_on: false
          trigger: "Only when user explicitly asks to modify/cancel and lacks confirmation number"
---
# 日期之夜技能（已发布）

提供从开始到结束的日期之夜规划服务：包括餐厅选择、电影预订、活动安排以及相关通知功能。该技能由 `playwright-cli` 浏览器自动化工具支持。

---

## 用户偏好设置

此技能会使用 `~/.openclaw/skills/date-night/config.json` 文件进行配置。**首次使用时会自动运行引导流程**（详见下方说明），之后每次会话开始时都会静默加载配置文件。

---

### 配置文件结构：
```json
{
  "name": "string",
  "first_name": "string",
  "last_name": "string",
  "user_email": "string",
  "user_phone": "string (digits only, e.g. 8015550155)",
  "partner": "string | null",
  "notify_channel": "iMessage | Telegram | Discord | Signal | SMS",
  "dietary": ["no alcohol", "vegetarian", "..."],
  "has_children": false,
  "children_count": 0,
  "children_ages": "string | null",
  "location": "City, ST",
  "zip": "00000",
  "preferred_theater": "string | null",
  "babysitter_rate": 18,
  "calendar_tool": "gog | gcal | ical",
  "onboarded_at": "ISO timestamp"
}
```

**重要提示：** `user_email`、`user_phone`、`first_name` 和 `last_name` 用于自动填充预订和购票表单。这些信息仅存储在本地 `config.json` 文件中，不会在提交表单时被发送到任何第三方网站。

---

## 首次使用引导流程

**每次使用该技能时都会进行检查：**

如果系统提示 **需要引导流程**，请在执行任何操作之前先运行引导流程。

### 引导流程

以对话的方式逐一提问。这是一个关于日期之夜的辅助工具，请让整个过程显得温馨且有趣，而不是像填写车辆管理局（DMV）表格那样繁琐。

**开场语：**
> “嘿！看起来您是第一次使用这个日期之夜技能——非常棒！让我快速了解一下您的需求，这样就能为您量身定制服务。不会花太长时间。”

**提问顺序**（自然地提问，并等待每个问题的回答）：
1. **姓名：**
   > “首先，请告诉我您的名字？”
   — 收集用户的名字和姓氏（用于预订表单）。

2. **电子邮件和电话号码：**
   > “我应该使用哪个电子邮件和电话号码来预订？这些信息会直接填写到预订表单中，只会存储在本地，不会被发送到其他地方。”

3. **伴侣：**
   > “您是和伴侣一起计划这次活动，还是独自出行？（独自安排的日期之夜也是完全可行的。）”
   — 如果有伴侣： “伴侣的名字是什么？”

4. **通知伴侣的方式：**
   > “有什么最好的方式可以联系到您的伴侣呢？比如，如果我想提前通知他们预订信息，应该通过 iMessage、Telegram、Signal 还是 Discord 等方式？”
   — 如果是独自出行，则跳过此步骤。

5. **饮食/生活习惯：**
   > “您有什么饮食偏好或限制吗？例如是否不能喝酒、是否是素食者、是否对海鲜过敏，或者只是‘什么都不挑’？”

6. **是否有孩子：**
   > “您家里有孩子吗？（我会提醒您预订后需要安排看护服务。）”
   — 如果有孩子： “有几个孩子？大概多大年纪？”

7. **所在位置：**
   > “您所在的城市或邮政编码是什么？我会根据这些信息来查找附近的餐厅、电影院等场所。”

8. **电影院偏好（可选）：**
   > “您有没有喜欢的电影院连锁店，或者附近常去的电影院？我可以在搜索放映时间时使用这些信息作为默认选项。（如果没有特别偏好，可以跳过此步骤。）”

9. **保姆费用（仅适用于有孩子的用户）：**
   > “您大概愿意支付多少保姆费用？我会根据这个费用来估算预算。如果没有具体费用，默认为每小时 18 美元。”

10. **日历工具：**
    > “最后一个问题，您是如何管理日历的？我可以自动为您添加活动安排的。可选的日历工具包括：`gog`（Google）、`gcal`、`ical`，或者直接告诉我您使用的是哪个工具。”

**结束语：**
> “太好了！您已经设置好了！🎉 以后您只需要说‘安排一次日期之夜’、‘帮我们找一家餐厅’或者‘帮我们买票’就可以了。其余的我都已经准备好了。”

---

### 保存配置

收集完所有信息后，将配置内容写入 `config.json` 文件：
```bash
mkdir -p ~/.openclaw/skills/date-night
cat > ~/.openclaw/skills/date-night/config.json << 'EOF'
{
  "name": "{name}",
  "first_name": "{first_name}",
  "last_name": "{last_name}",
  "user_email": "{email}",
  "user_phone": "{phone_digits}",
  "partner": "{partner_or_null}",
  "notify_channel": "{channel}",
  "dietary": ["{pref1}", "{pref2}"],
  "has_children": {true|false},
  "children_count": {N},
  "children_ages": "{ages_or_null}",
  "location": "{City, ST}",
  "zip": "{zip}",
  "preferred_theater": "{theater_or_null}",
  "babysitter_rate": {rate},
  "calendar_tool": "{tool}",
  "onboarded_at": "{ISO_TIMESTAMP}"
}
EOF
```

### 在整个技能中使用配置信息

加载配置后，将配置中的各项信息应用到以下所有地方：
| 配置字段 | 使用场景 |
|-------------|---------|
| `first_name` / `last_name` | 自动填充预订和购票表单 |
| `user_email` | 自动填充预订表单、账户查询 |
| `user_phone` | 自动填充预订表单、短信验证 |
| `dietary` | 根据用户偏好推荐餐厅 |
| `location` / `zip` | 用于搜索附近的餐厅、电影院等场所 |
| `partner` | 生成伴侣通知的草稿 |
| `notify_channel` | 确定发送伴侣通知的方式 |
| `has_children` | 在每次预订后提醒用户是否需要安排看护服务 |
| `babysitter_rate` | 用于预算估算 |
| `preferred_theater` | 用于电影搜索的默认电影院 |
| `calendar_tool` | 用于创建日历事件的命令 |

**执行饮食偏好设置：**
如果用户的饮食偏好中包含 “不喝酒”，在推荐餐厅或活动时，将不会显示任何与酒精相关的信息（如酒单、鸡尾酒菜单或酒吧相关的内容）。推荐时主要考虑餐厅的食物、氛围和服务。

---

## 重新配置

如果用户输入 **“更新我的日期之夜偏好设置”**、**“重新配置日期之夜安排”** 或 **“更改我的日期之夜设置”**，则重新运行引导流程，并使用当前的用户信息作为默认值：
> “好的，让我们来更新您的偏好设置。我会先展示您目前的设置，您可以随时修改。按 Enter 键确认。”

重新配置完成后，系统会覆盖 `config.json` 文件。确认后：  
> “设置已更新！下次日期之夜的安排将使用新的设置。”

---

## 所需软件和工具

### 需要单独安装的外部二进制文件

| 软件/工具 | 安装方法 | 是否必需？ |
|--------|---------|-----------|
| `playwright-cli` | `npm install -g @playwright/cli@latest` | **是** |
| Chromium | `npx playwright install chromium` | **是**（`playwright-cli` 需要 Chromium 浏览器） |
| `goplaces` | `brew install steipete/tap/goplaces` | 可选——用于增强餐厅搜索功能 |

**路径设置：**  
`export PATH="$HOME/.npm-global/bin:$PATH"`  

### 环境变量

| 变量 | 用途 | 是否必需？ |
|----------|---------|-----------|
| `GOOGLE_PLACES_API_KEY` | `goplaces` 工具所需的 Google Places API 密钥 | 仅在使用 `goplaces` 时需要 |

### OpenClaw 内置功能

这些是 OpenClaw 的标准代理工具，无需额外安装。只要启用了相应的工具策略，任何 OpenClaw 代理都可以使用这些功能：

| OpenClaw 工具 | 在此技能中的用途 |
|---------------|----------------------|
| `web_search` | 查找餐厅、活动、电影及评论（公开网站） |
| `web_fetch` | 从网站获取菜单、评论和放映时间（公开网站） |
| `message`（发送通知） | 生成伴侣通知的草稿——发送前会显示给用户审核 |
| 日历功能（`gog`/`ical`） | 预订后创建日历事件 |
| SMS/iMessage 功能（`imsg`） | 获取预订验证码（详见敏感数据访问部分） |

**这些内置工具不需要额外的凭据或 API 密钥**，它们会使用用户已在 OpenClaw 中配置的通信渠道和连接方式。

### 敏感数据访问说明

**短信验证码：** 在预订过程中，OpenTable 和 Resy 会通过短信发送 6 位的验证码。该技能会从用户的短信收件箱中读取最近的一条或两条来自特定发送方的消息来获取验证码（例如，OpenTable 的短信代码是 `22395`）。该技能不会进行大规模的收件箱扫描。

**Gmail（仅用于修改/取消预订）：** 当用户明确要求修改或取消预订且没有确认码时，该技能会使用特定的查询在 Gmail 中搜索（例如：`from:opentable reservation confirmed`），搜索结果最多显示 5 条记录。在正常的预订流程中，此功能不会被触发。

**伴侣通知：** 通知内容会先生成草稿并显示给用户审核，然后再发送。该技能不会自动发送消息。消息发送渠道（iMessage/Telegram/Discord/Signal）由用户在 OpenClaw 中配置，该技能不会存储用户的任何额外凭据。

**认证状态持久化：** Resy 功能可以选择将浏览器会话状态保存在 `~/.openclaw/skills/date-night/state/resy-auth.json` 文件中，以避免用户重新登录。该文件包含会话 cookie。如需清除会话状态：`rm -rf ~/.openclaw/skills/date-night/state/`。该技能 **不会请求或存储用户的网站密码**，它使用浏览器的交互式登录方式，并仅在用户同意的情况下保存会话 cookie。

### 数据存储

| 文件路径 | 存储内容 | 是否包含敏感信息？ |
|------|----------|------------|
| `~/.openclaw/skills/date-night/config.json` | 偏好设置、姓名、电子邮件、电话号码 | **是**（包含个人身份信息） |
| `~/.openclaw/skills/date-night/history.jsonl` | 日期之夜活动记录（餐厅名称、日期、评分） | 低风险 |
| `~/.openclaw/skills/date-night/state/*.json` | 浏览器会话 cookie（仅 Resy 功能需要，用户可选择是否保存） | **是**（包含认证 token） |

**清除所有数据：** `rm -rf ~/.openclaw/skills/date-night/`

---

## 预订前的检查事项
```bash
# Verify playwright-cli is available
export PATH="$HOME/.npm-global/bin:$PATH"
playwright-cli --version || echo "INSTALL: npm install -g @playwright/cli@latest"
```

---

## 参考资料

| 相关文档 | 链接 |
|-------|------|
| Playwright CLI | [references/playwright-cli.md](references/playwright-cli.md) |
| OpenTable 预订流程 | [references/opentable-flow.md](references/opentable-flow.md) |
| Resy 预订流程 | [references/resy-flow.md](references/resy-flow.md) |
| 餐厅搜索 | [references/search-restaurants.md](references/search-restaurants.md) |
| 电影预订 | [references/movie-booking.md](references/movie-booking.md) |
| 活动门票 | [references/event-tickets.md](references/event-tickets.md) |
| 电影搜索 | [references/search-movies.md](references/search-movies.md) |
| 活动搜索 | [references/search-events.md](references/search-events.md) |
| 修改/取消预订 | [references/modify-cancel.md](references/modify-cancel.md) |
| SMS 验证码 | [references/sms-codes.md](references/sms-codes.md) |
| 晚餐前的准备工作 | [references/pre-evening.md](references/pre-evening.md) |
| 智能功能 | [references/smart-features.md](references/smart-features.md) |

---

## 快速预订流程：晚餐预订

1. **查找餐厅** — 参见 [references/search-restaurants.md](references/search-restaurants.md)
2. **打开餐厅页面**：
   ```bash
   playwright-cli open "https://www.opentable.com/r/{slug}?covers={N}&dateTime={YYYY-MM-DDTHH:MM}" --headed
   ```
3. **选择日期和时间**
4. **填写客人信息**（姓名、电话号码、电子邮件地址可以从用户的 `MEMORY.md` 或 `config.json` 中获取）
5. **提交 → 处理短信验证**（详见 [references/sms-codes.md](references/sms-codes.md)
6. **确认 → 预订后的操作**（详见下方）

完整流程详情：[opentable-flow.md](references/opentable-flow.md) | [resy-flow.md](references/resy-flow.md)

---

## 快速购票流程：

1. 从用户配置中选择首选的电影院开始，或者通过 Fandango 网站搜索电影；
2. 选择电影、放映时间和座位；
3. ⚠️ **在支付步骤前务必确认总价**；
4. 完成购买后的操作（详见下方）。

完整流程详情：[movie-booking.md](references/movie-booking.md) | [search-movies.md](references/search-movies.md)

---

## 快速购买活动门票：

1. 首先通过 SeatGeek 网站查找最优惠的电影票（包含价格和折扣信息）；
2. 然后通过 Ticketmaster 或 StubHub 网站确认购票信息；
3. ⚠️ **在支付步骤前务必确认总价**。

---

## 完整的日期之夜流程

当用户输入 “围绕某个活动/电影/想法安排一次日期之夜” 时，执行以下步骤：

```
1. LOAD config.json silently
2. FIND the event/movie → SeatGeek + Ticketmaster + StubHub price comparison
3. PRESENT options + prices to user → get approval to proceed
4. BOOK tickets (with explicit user confirmation at payment)
5. NOTE venue and show time
6. SEARCH restaurants within 1 mile of venue, open before the show
7. SUGGEST 2-3 dinner options with ratings and OpenTable availability
8. BOOK dinner (with approval) at time that ends ~1 hr before show
9. CHECK weather for that evening → include in summary
10. CALCULATE timeline: leave home → dinner → venue → showtime
11. ADD both events to calendar ({config.calendar_tool})
12. DRAFT partner notification → show draft → send with approval
13. IF has_children: PROMPT about childcare — every time, no exceptions
14. OFFER dessert spot near venue (optional extension)
15. PRESENT budget estimate: dinner + tickets + babysitter total
```

**以晚上 7:30 的电影为例的流程示例：**
```
6:00 PM  Leave home
6:30 PM  Dinner (2-block walk from venue)
8:00 PM  Walk to venue
7:30 PM  Show
10:30 PM Done — dessert optional
```

---

## 预订后的操作

在每次完成预订或购票后，需要执行以下操作：

### 1. 将预订信息添加到日历中
```bash
{config.calendar_tool} calendar create primary \
  --summary "{Event/Dinner} @ {Venue/Restaurant}" \
  --from "{datetime}" \
  --to "{datetime+duration}" \
  --location "{address}" \
  --description "{details + confirmation number}" \
  --reminder "popup:2h" --reminder "popup:1d"
```

### 2. 通知伴侣（如果已配置）
以用户自然的语气生成通知草稿 → 显示给用户审核 → **发送前需要用户确认**。
```
"Hey {partner}, got us a reservation at {Restaurant} on {date} at {time} 🍽️"
```

### 3. 询问是否需要安排看护服务
如果用户有孩子，**必须询问**：
> “您已经安排好当晚的看护服务了吗？需要照顾 {N} 个孩子。”

### 4. 记录预订信息到历史记录中
```bash
mkdir -p ~/.openclaw/skills/date-night
cat >> ~/.openclaw/skills/date-night/history.jsonl << 'EOF'
{"date":"{YYYY-MM-DD}","restaurant":"{name}","event":"{event_or_null}","total_cost":null,"rating":null,"would_return":null,"weather":null,"notes":""}
EOF
```

---

## 错误处理

| 错误类型 | 处理方法 |
|-------|----------|
| 配置文件未找到 | 在继续之前运行引导流程 |
| 超时： | 从餐厅页面重新开始预订流程 |
| 未收到验证码： | 等待 30 秒后重新发送请求，或检查短信 |
| 电话号码字段为空： | 这是一个已知的系统错误——请重新填写后再提交 |
| Ticketmaster 队列或 CAPTCHA 问题： | 为用户提供帮助；或提供手动协助 |
| 座位地图无法加载： | 使用 `playwright-cli` 的截图功能进行诊断 |
| StubHub 的价格发生变化： | 在提交前重新核对价格 |

---

## 检查清单

### 预订前的准备事项：
- 配置文件已加载
- 已与用户确认餐厅/电影/活动的信息、日期、时间以及参加人数
- 在任何购买操作前已向用户显示总价

### 预订后的操作：
- 日历事件已创建
- 通知伴侣（如果已配置）
- 询问用户是否需要看护服务（如果有孩子）
- 将预订信息记录到历史记录中
- 提供晚餐前的相关信息（天气、停车信息、预计行驶时间）
- 向用户展示预算估算