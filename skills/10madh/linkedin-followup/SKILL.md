---
name: linkedin-followup
description: **从 Google Sheets 管理 LinkedIn 的潜在客户信息**  
- 可按名称搜索潜在客户；  
- 查看实时的对话记录；  
- 更新潜在客户的状态；  
- 发送恰当的跟进信息。  
该功能适用于在通过 LinkedIn 直接消息（LinkedIn DM）与潜在客户沟通后，用于跟踪他们的处理进度（状态变更：已发送 → 已回复 → 预约电话 → 演示完成 → 关闭）。
metadata:
  {
    "openclaw": {
      "emoji": "🔁",
      "requires": { "bins": ["gog"] },
      "skills": ["gog"],
      "tags": ["linkedin", "crm", "outreach", "sales", "follow-up"]
    }
  }
---

# linkedin-followup

该功能允许用户通过一个集中的 Google Sheets 客户关系管理（CRM）系统来管理与 LinkedIn 上的持续对话。用户可以阅读对话记录、草拟合适的回复内容、发送消息，并实时更新 CRM 表格——所有这些操作都通过同一个工具完成。

---

## 使用前的检查清单

在开始操作之前，请确保以下内容已准备齐全：

1. **CRM 表格 ID** — 请确认 CRM 表格的 ID（来自 `linkedin-dm` 的配置）。默认值为 `1eEZDGcr1dIbSC782mNkxvD7pVrF8rOFySWCVZ1RXkhM`，对应的标签页为 `Sheet1`（如果表格被重命名，则为 `Outreach`）。
2. **gog auth** — 运行 `gog auth list` 命令。如果没有 OAuth 令牌，请参阅下面的 [gog auth 设置](#gog-auth-setup) 部分。
3. **浏览器** — 打开 openclaw 的浏览器界面，并确保已登录 LinkedIn。首先导航到 `/feed/` 页面。
4. **操作模式** — 选择所需的操作模式（详见 [操作模式](#modes) 部分）。

---

## CRM 表格结构

该 CRM 表格使用以下列（A–P）来存储对话信息：

| 列 | 字段 | 说明 |
|---|---|---|
| A | 发送日期 | ISO 格式的日期 |
| B | 人员姓名 | 全名 |
| C | 职位/头衔 | |
| D | 公司名称 | |
| E | LinkedIn URL | 个人资料链接 |
| F | 开场白使用的链接 | 用于开启对话的链接 |
| G | 发送的开场白内容 | 第一条回复的文本 |
| H | 发送的推销内容 | 第二条回复的文本 |
| I | 活动标签 | 对话所属的批次标签 |
| J | 状态 | 对话的当前阶段 |
| K | 备注 | 对话的背景信息和历史记录 |
| L | 最后更新时间 | 最后一次更新的时间戳（ISO 格式） |
| M | 最后回复日期 | 对方最后一次回复的日期 |
| N | 最后回复内容预览 | 对方最后一次回复的前 200 个字符 |
| O | 对话记录 | 完整的对话记录（格式见下文） |
| P | 下一步行动 | 下一步应采取的措施（由机器人或人工完成） |

**状态值**：
`Sent` → `Replied` → `Call Scheduled` → `Demo Done` → `Follow Up Sent` → `No Response` → `Closed Won` → `Closed Lost`

**对话记录格式**（O 列）：
```
[2026-02-13 17:05 SENT] Hey Rishabh, we both had stints at CRED...
[2026-02-13 17:05 SENT] I'm building an AI calling agent...
[2026-02-15 09:30 RECEIVED] Hey! Sounds interesting, tell me more.
[2026-02-15 09:45 SENT] Happy to show you a live demo — are you free Thursday?
```

如果 M–P 列尚未存在，请先添加它们：
```bash
gog sheets update <SHEET_ID> "Sheet1!M1:P1" \
  --values-json '[["Last Reply Date","Last Reply (preview)","Conversation Log","Next Action"]]' \
  --input USER_ENTERED
```

---

## 操作模式

### 模式 1 — 快速状态更新

用户输入：“将 Rishabh 的状态标记为 ‘Replied’” 或 “Rishabh 回复我了，他表示有兴趣”

1. **查找对应记录** — 在表格中搜索该人员的记录：
   ```bash
   gog sheets get <SHEET_ID> "Sheet1!A:P" --json
   ```
   可以通过姓名（B 列）或 LinkedIn URL（E 列）进行查找，并获取记录的行号。
2. **更新状态（J 列）和最后更新时间（L 列）**：
   ```bash
   gog sheets update <SHEET_ID> "Sheet1!J<ROW>:L<ROW>" \
     --values-json '[["Replied","","<ISO_TIMESTAMP>"]]' \
     --input USER_ENTERED
   ```

3. 如果用户提供了回复内容，还需更新：
   - M 列：对方最后一次回复的日期
   - N 列：对方最后一次回复的前 200 个字符
   - O 列：将回复内容添加到对话记录中
   - P 列：下一步应采取的措施

4. 向用户确认更新结果。

---

### 模式 2 — 完整的跟进操作（阅读 + 草拟 + 发送）

用户输入：“跟进 Rishabh” 或 “给所有回复我的人发送跟进消息”

#### 第一步 — 从表格中加载该人员的详细信息

```bash
gog sheets get <SHEET_ID> "Sheet1!A:P" --json
```
查找该人员的记录，然后加载以下信息：姓名、公司名称、职位、LinkedIn URL、发送的开场白内容、推销内容、对话状态、备注以及下一步行动。

#### 第二步 — 导航到他们的 LinkedIn 个人资料页面

**务必先访问 `/feed/` 页面**（以防止被检测到）：
```
https://www.linkedin.com/feed/
```
等待 2–4 秒后，再导航到他们的 LinkedIn 个人资料链接（E 列）。

#### 第三步 — 打开对话记录并阅读对话内容

点击他们个人资料页面上的 **Message** 按钮，等待对话记录加载完成。

使用 JavaScript 抓取完整的对话记录：
```javascript
const events = Array.from(document.querySelectorAll('.msg-s-message-list__event'));
const messages = [];
events.forEach(el => {
  const groups = el.querySelectorAll('.msg-s-event-listitem');
  groups.forEach(g => {
    const nameEl = g.closest('.msg-s-message-group')?.querySelector('.msg-s-message-group__profile-link');
    const bodyEl = g.querySelector('.msg-s-event-listitem__body');
    const timeEl = g.closest('.msg-s-message-group')?.querySelector('.msg-s-message-group__timestamp');
    if (bodyEl?.textContent?.trim()) {
      messages.push({
        sender: nameEl?.textContent?.trim() || 'unknown',
        time: timeEl?.textContent?.trim() || '',
        text: bodyEl.textContent.trim()
      });
    }
  });
});
return JSON.stringify(messages);
```

如果对话记录为空或无法加载，请向上滚动以查看之前的消息。

#### 第四步 — 分析对话内容

根据加载的完整对话记录和他们的个人资料信息，确定：
- **他们上次说了什么？** — 找出他们最近的一条回复。
- **他们的意图是什么？** — 是表示感兴趣、希望了解更多信息、提出问题、表示反对意见，还是不感兴趣？
- **下一步应该发送什么消息？** — 可参考下面的 [回复策略](#response-playbook)。
- **语气** — 保持与对方相同的语气（随意或正式、简短或详细）。

#### 第五步 — 草拟跟进消息

撰写一条回复，内容应：
- **直接回应** 他们上次提到的内容
- **除非对方主动要求，否则不要再次推销产品**
- **明确指出下一步行动**（例如安排演示、安排电话会议、推荐给团队）
- **简洁明了** — 最多 2–4 句
- 保持自然，避免使用模板化的语言

在发送前向用户展示草稿并征求同意：

> **给 [姓名] 的回复草稿：**
> [回复内容]
>
> 要发送这条消息吗？（是 / 编辑 / 跳过）

#### 第六步 — 发送消息

使用与 `linkedin-dm` 相同的 JavaScript 代码发送消息：
```javascript
const active = document.querySelector('.msg-overlay-conversation-bubble--is-active .msg-form__contenteditable');
if (active) { active.focus(); document.execCommand('insertText', false, '<message>'); }
```

#### 第七步 — 更新表格

发送消息后：
```bash
gog sheets update <SHEET_ID> "Sheet1!J<ROW>:P<ROW>" \
  --values-json '[["<new_status>","<last_reply_date>","<last_reply_preview>","<updated_conversation_log>","<next_action>","<ISO_TIMESTAMP>"]]' \
  --input USER_ENTERED
```

---

### 模式 3 — 批量处理

用户输入：“哪些人需要跟进？” 或 “查看我的跟进任务”

1. 从表格中加载所有记录。
2. 根据状态和时间进行筛选：
   - 发送时间超过 3 天的记录 → 可视为 “No Response” 或需要温和的跟进
   - 状态为 “Replied” 的记录 → 需要回复
   - 状态为 “Follow Up Sent” 且发送时间超过 5 天的记录 → 也视为需要跟进
   - 状态为 “Call Scheduled” 的记录 → 检查是否已安排电话会议，并更新相应的状态

3. 显示需要跟进的人员列表：
```
   Name             Status    Last Updated    Suggested Action
   Rishabh Nayan    Replied   2026-02-14      Reply to their message
   Shorya Saini     Sent      2026-02-10      Follow-up nudge (4 days)
   Shantam Mohata   Sent      2026-02-13      Too soon (today)
   ```

4. 用户选择需要跟进的人员，然后对每个人分别执行模式 2 的操作。

---

## 回复策略

以下策略仅供参考，实际操作时请根据对话内容灵活调整：

| 对方的话 | 意图 | 你的应对方式 |
|---|---|---|
| “听起来很有趣，请详细说明” | 表示好奇 | 简要解释并提供一个具体的演示时间 |
| “这是如何工作的？” | 表示想要了解更多 | 提供 2 行的描述，并邀请对方进行 15 分钟的电话会议 |
| “我们已经在使用 [X] 了” | 表示反对 | 表示理解，解释差异，并提供演示机会 |
| “请发送更多详细信息” | 表示有初步兴趣 | 分享相关资料或链接，并在 2 天后再次跟进 |
| “现在不太合适” | 表示暂时不感兴趣 | 表示尊重对方的决定，并留有余地：“没关系，几个月后我会再联系您” |
| “还有谁在使用这个产品？” | 建立信任 | 分享一个相关的使用案例，并介绍相关人员 |
| **4 天内没有回复** | 表示对方没有回应 | 发送一条提醒消息：“嘿 [姓名]，最近怎么样？” |
| **8 天内没有回复** | 表示对方完全不感兴趣 | 发送最后一条消息，然后将其标记为 “No Response” |

---

## 防检测规则

遵循与 `linkedin-dm` 相同的规则：
- 在导航到个人资料页面之前，务必先访问 `/feed/` 页面。
- 加载对话记录后等待 2–4 秒。
- 每次操作最多发送 15–20 条消息（包括所有跟进消息）。
- 延迟发送消息的时间间隔要合理，避免连续快速发送给多人。
- 输入和发送消息之间要稍作间隔（1–2 秒）。

---

## gog Auth 设置

如果 `gog auth list` 的结果为空，用户需要设置 Google OAuth 凭据：

1. 访问 [console.cloud.google.com](https://console.cloud.google.com)
2. 创建一个新的项目（或选择现有项目）。
3. 启用 **Google Sheets API**（在 “APIs & Services” 中选择 “Library”）。
4. 创建 OAuth 凭据：在 “APIs & Services” → “Credentials” 中选择 “Create”，然后创建一个 OAuth 客户端 ID（类型为 “Desktop App”）。
5. 下载 `client_secret_<id>.json` 文件。
6. 运行以下命令：
   ```bash
   gog auth credentials set /path/to/client_secret.json
   gog auth add your@gmail.com --services sheets
   ```
7. 系统会打开一个浏览器窗口，用户需要登录并授权访问权限。
8. 验证授权是否成功：运行 `gog auth list` 命令。

**备用方案（无法使用 gog auth）**：所有表格的读写操作都可以通过浏览器手动完成——直接在 openclaw 浏览器中打开表格并直接更新单元格。虽然自动化程度较低，但功能依然可用。

---

## 操作限制

- 每次操作最多发送 15–20 条跟进消息。
- 每次发送消息后应立即更新到表格中（不要批量处理）。
- 如果无法使用 gog auth，可以将操作日志保存到本地的 `linkedin_followup_log.json` 文件中，并在下次会话时再同步到表格中。