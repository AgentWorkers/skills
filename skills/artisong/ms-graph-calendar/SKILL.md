---
name: ms-graph-calendar
description: 使用 Microsoft Graph API 查找公司员工的可用会议时间以及他们的空闲/忙碌时段。该功能适用于用户需要安排会议、寻找空闲时间、查看员工的工作安排或查询某人的日历可用性时。
version: 1.0.0
metadata: {"openclaw": {"emoji": "📅", "requires": {"env": ["AZURE_TENANT_ID", "AZURE_CLIENT_ID", "AZURE_CLIENT_SECRET"], "bins": ["node", "curl"]}, "primaryEnv": "AZURE_CLIENT_SECRET"}}
---
# Microsoft Graph Calendar — 查找空闲时间

当用户需要以下操作时，可以使用此技能：
- 查找多名员工都空闲的时间
- 检查特定人员是否在指定时间有空
- 列出一个人或多个人的即将召开的会议/忙碌时间段
- 为公司内部人员推荐会议时间

## 设置（只需执行一次）

如果用户尚未进行设置，或者系统提示缺少凭据，请按照以下步骤操作：

1. 依次向用户询问以下三个值：
   - `AZURE_TENANT_ID`（在 Azure 门户 → Azure Active Directory → 概览中获取）
   - `AZURE_CLIENT_ID`（在应用注册 → 您的应用 → 应用（客户端）ID中获取）
   - `AZURE_CLIENT_SECRET`（在应用注册 → 您的应用 → 证书和密钥中获取）

2. 获取所有值后，运行以下命令：
```bash
node skills/ms-graph-calendar/scripts/setup.js \
  --tenant-id <AZURE_TENANT_ID> \
  --client-id <AZURE_CLIENT_ID> \
  --client-secret <AZURE_CLIENT_SECRET>
```

这些设置值将被保存在 `~/.openclaw/ms-graph-calendar.json` 文件中（权限设置为 600），并在每次使用该技能时自动加载。

3. 进行测试：
```bash
node skills/ms-graph-calendar/scripts/get-token.js
```
如果看到“✅ Token acquired”的提示，表示设置已完成，可以开始使用了。

**应用注册需要具备以下权限：**
- `Calendars.Read`：读取所有用户的日历
- `User.Read.All`：列出所有员工信息
- 需要管理员的授权许可

---

## 配置

首次登录后，认证信息会被缓存。设备代码流程不需要环境变量。

对于无界面/自动化操作，请设置以下环境变量：
- `AZURE_CLIENT_ID`：Azure AD 应用客户端 ID
- `AZURE_CLIENT_SECRET`：Azure AD 应用密钥
- `AZURE_TENANT_ID`：租户 ID（个人账户使用“consumers”）

---

## 工具

此技能通过 bash 运行 Node.js 脚本。相关文件如下：
- `scripts/`：Node.js 脚本
- `nicknames.md`：昵称与电子邮件地址的映射表（可随时修改）

---

## 操作步骤

### 第一步 — 获取访问令牌
在调用任何 Graph API 之前，先获取一个仅限应用使用的令牌：
```bash
node skills/ms-graph-calendar/scripts/get-token.js
```
将令牌存储在一个临时变量中，以便后续使用。

### 第二步 — 解析用户请求
从用户输入的信息中提取以下内容：
- **参与者**：参与者的姓名或电子邮件地址（例如：“Alice 和 Bob”或“市场团队”）
- **时间范围**：搜索的时间段（例如：“本周”、“下周一”或“3 月 5 日至 7 日”）
- **会议时长**：会议的默认时长为 60 分钟
- **时区**：如果未指定，则默认为 `Asia/Bangkok`

如果缺少任何信息，请在继续之前向用户询问。

### 第三步 — 解析员工电子邮件地址

**3a. 先尝试根据昵称转换成电子邮件地址**（这样更快，无需调用 API）：
```bash
node skills/ms-graph-calendar/scripts/resolve-nicknames.js --names "แบงค์,มิ้ว,โบ้"
```
从 `nicknames.md` 文件中读取昵称对应的电子邮件地址（可以直接在该文件中进行修改）。

**3b. 如果在 `nicknames.md` 中找不到对应的电子邮件地址**，则通过 Graph API 进行查询：
```bash
node skills/ms-graph-calendar/scripts/list-users.js --search "ชื่อ"
```
如果有多个员工具有相同的昵称，请与用户确认。

### 第四步 — 查找空闲时间（选择一种方法）

**方法 A — findMeetingTimes**（适用于人数较少（≤10 人）的情况）：
```bash
node skills/ms-graph-calendar/scripts/find-meeting-times.js \
  --attendees "alice@company.com,bob@company.com" \
  --start "2025-03-01T08:00:00" \
  --end "2025-03-01T18:00:00" \
  --duration 60 \
  --timezone "Asia/Bangkok" \
  --max 5
```

**方法 B — getSchedule**（适用于人数较多或需要查看员工忙碌时间段的情况）：
```bash
node skills/ms-graph-calendar/scripts/get-schedule.js \
  --emails "alice@company.com,bob@company.com,carol@company.com" \
  --start "2025-03-01T00:00:00" \
  --end "2025-03-07T00:00:00" \
  --timezone "Asia/Bangkok" \
  --interval 30
```

### 第五步 — 显示结果

以清晰的方式展示可用的时间段：
```
📅 Available slots where everyone is free:

1. Monday 3 Mar · 10:00–11:00
2. Tuesday 4 Mar · 14:00–15:00
3. Wednesday 5 Mar · 09:00–10:00

Which slot works best?
```

如果没有找到合适的时间段，可以扩大搜索范围或重新尝试；如果在该时间段内没有所有参与者都空闲，可以报告这一情况。

---

## 示例对话

**用户：**“本周找一个 Alice、Bob 和 Carol 都有空的时间段，时长为 1 小时。”
**助手：**
1. 查找 Alice、Bob 和 Carol 的电子邮件地址
2. 运行 `find-meeting-times.js`，搜索时间范围为“本周一至周五”
3. 返回前三个可用的时间段

**用户：**“John 明天下午有空吗？”
**助手：**
1. 查找 John 的电子邮件地址
2. 运行 `get-schedule.js`，搜索时间范围为明天 12:00–18:00
3. 显示 John 的忙碌/空闲时间段

**用户：**“显示市场团队所有成员下周的可用时间。”
**助手：**
1. 通过 `list-users.js --group "Marketing"` 列出市场团队的成员
2. 运行 `get-schedule.js`，查询所有成员的日程安排
3. 以可视化方式展示他们的忙碌/空闲状态

---

## 错误处理

| 错误代码 | 原因 | 解决方法 |
|---|---|---|
| `401 Unauthorized` | 令牌过期或凭据错误 | 重新运行 `get-token.js`，检查环境变量 |
| `403 Forbidden` | 缺少管理员授权 | 请 IT 管理员在 Azure 门户中授权 |
| `404 Not Found` | 用户的电子邮件地址不存在 | 通过 `list-users.js` 验证电子邮件地址 |
| 未找到合适的时间段 | 所有人都忙碌 | 扩大搜索时间范围或减少参与人数 |

---

## 安全注意事项

- 凭据仅从环境变量中读取，切勿记录或显示它们
- 该技能仅具有**读取**日历数据的权限（`Calendars.Read`）
- 该技能无法创建、编辑或删除任何事件
- 如需限制应用程序可以访问的邮箱，请联系 IT 管理员在 Exchange Online 中设置**应用访问策略**：
  ```powershell
  New-ApplicationAccessPolicy -AppId <ClientId> -PolicyScopeGroupId <GroupId> -AccessRight RestrictAccess
  ```