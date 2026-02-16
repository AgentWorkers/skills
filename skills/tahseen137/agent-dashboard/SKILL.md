---
name: agent-dashboard
description: >
  OpenClaw的实时代理仪表板：您可以随时随地监控正在进行的任务、cron作业的运行状态、存在的问题以及需要处理的事项。该仪表板提供三种设置级别：  
  1. **零配置版本**：直接在OpenClaw内部进行渲染，无需任何额外配置；  
  2. **GitHub Pages版本**：通过30秒一次的轮询机制获取数据，完全免费，设置过程仅需2分钟；  
  3. **Supabase Realtime + Vercel版本**：支持实时WebSocket更新，提供更快速的数据同步。  
  所有数据都存储在您的本地机器上，并采用PIN码进行保护，因此无需依赖任何外部服务。  
  **注意：**  
  - 第1级设置仅需要访问SUPABASE_URL和SUPABASE_ANON_KEY（无需service_role密钥）；  
  - 第3级设置会推送的数据仅包括任务名称、cron作业状态及时间戳等操作状态信息，绝不会包含任何凭据、API密钥或文件内容。
---
# 任务控制面板 🚀

这是一个实时仪表板，用于显示您的 OpenClaw 代理正在执行的任务、cron 作业的状态、需要关注的问题以及最近的活动。您可以从任何地方查看它——手机、笔记本电脑，无论在哪里。

## 快速入门

### 第一级 — Canvas（无需设置）⚡

不需要任何外部服务。代理会直接在您的 OpenClaw 会话中渲染仪表板。

**使用方法：**
```
Show me the mission control dashboard
```

代理将：
1. 收集当前状态（活动任务、cron 作业等）
2. 使用 Canvas 工具生成仪表板
3. 将其内联显示在您的会话中

就这样。无需部署，无需账户，无需任何配置。

---

### 第二级 — GitHub Pages + 轮询（推荐）🌐

免费托管，自动刷新间隔为 30 秒。设置只需 2 分钟。

**设置步骤：**

1. **创建仓库：**
   ```bash
   gh repo create mission-control --public --clone
   cd mission-control
   ```

2. **复制仪表板代码：**
   ```bash
   mkdir -p data
   # Copy tier2-github.html to index.html
   # Copy assets/templates/dashboard-data.json to data/
   ```

3. **编辑 `index.html`：**
   - 将 `YOUR_PIN_HERE` 更改为您选择的 PIN 码

4. **启用 GitHub Pages：**
   - 进入仓库设置 → Pages
   - 源代码：从 `main` 分支部署
   - 文件夹：`/ (root)`

5. **部署：**
   ```bash
   git add -A && git commit -m "Initial deploy" && git push
   ```

您的仪表板现在可以在 `https://YOUR_USERNAME.github.io/mission-control/` 查看。

---

### 第三级 — Supabase 实时 + Vercel（高级）⚡🔥

真正的 WebSocket 实时更新——数据更新会在 1 秒内显示。

**先决条件：**
- Supabase 账户（免费 tier 可用）
- Vercel 账户（免费 tier 可用）

**步骤 1：创建 Supabase 表**

在您的 Supabase SQL 编辑器中运行 `assets/templates/setup-supabase.sql`。

**步骤 2：获取密钥**

在 Supabase 仪表板 → 设置 → API：
- 复制 `SUPABASE_URL`（项目 URL）
- 复制 `SUPABASE_ANON_KEY`（匿名公共密钥）

就这样——无需 `service_role` 密钥。匿名密钥通过表特定的 RLS 来处理读取（仪表板）和写入（推送脚本）操作。

**步骤 3：编辑仪表板代码**

在 `tier3-realtime.html` 中：
1. 将 `YOUR_SUPABASE_URL` 替换为您的项目 URL
2. 将 `YOUR_supABASE_ANON_KEY` 替换为您的匿名密钥
3. 将 `YOUR_PIN_HERE` 替换为您选择的 PIN 码

**步骤 4：部署到 Vercel**

```bash
mkdir mission-control && cd mission-control
# Copy tier3-realtime.html as index.html
vercel deploy --prod
```

**步骤 5：配置推送脚本**

```bash
export SUPABASE_URL="https://YOUR_PROJECT.supabase.co"
export SUPABASE_ANON_KEY="eyJ..."  # Same anon key used by the dashboard
```

---

## 🔄 自动更新机制

**仪表板会自动更新。**具体方式如下：

### 1. Cron 自动更新（每 30 分钟）

设置一个 cron 作业，从 OpenClaw API 收集数据并推送：

```
Create a cron job called "Dashboard Update" that runs every 30 minutes.
It should:
1. Run `cron list` to get all cron job statuses, error counts, last run times
2. Run `sessions_list` to find any active sub-agents and their current tasks
3. Build the dashboard JSON from this API data
4. Push to Supabase (or git push for Tier 2)
```

**数据来源：** 仅限 OpenClaw 内置 API（`cron list`、`sessions_list`）。不读取本地文件。操作项和最近的活动需要通过下面的“手动更新”命令手动添加。

**示例 cron 配置：**
```yaml
name: Dashboard Update
schedule: "*/30 * * * *"  # Every 30 minutes
model: sonnet             # Fast model for quick updates
prompt: |
  Update the Mission Control dashboard:
  
  1. Run `cron list` to get job names, statuses, error counts, last run times
  2. Run `sessions_list` to find active sub-agents and their tasks
  3. Build JSON matching the dashboard schema from API data only
  4. Push to Supabase or GitHub
  
  Do not read local files. Only use cron list and sessions_list data.
```

### 2. 实时事件推送**

除了定期的 cron 更新外，当发生重要事件时，代理会立即推送更新：

- ✅ 任务开始或完成
- ❌ 出现错误或失败
- 🚀 部署完成
- 📧 收到重要通知

这意味着仪表板可以在几秒钟内反映变化，而不仅仅是每 30 分钟更新一次。

**启用方法：** 当您启动一个重要任务时，告诉代理：
```
After this deploy finishes, push an update to Mission Control.
```

### 3. 强制更新按钮

每个级别的仪表板都包含一个 **🔄 更新** 按钮：
- **第二级：** 立即重新获取 `dashboard-data.json`
- **第三级：** 立即从 Supabase 重新获取数据
- 重置“X 分钟前更新”计时器
- 在获取数据时显示加载指示器

当您想立即查看最新状态时，请使用此按钮。

### 结果

**定期 cron 更新 + 实时推送 + 手动刷新** 的组合确保了仪表板的准确性。您将始终能够看到代理的实际操作情况。

---

## 仪表板功能

### 🚨 需要操作的事项
需要您关注的紧急事项。在顶部用优先级徽标（高/中/低）标出。

### ⚡ 当前活动
代理当前正在处理的任务，包括模型名称和持续时间。

### 📊 产品
产品卡片，带有实时/测试/关闭状态徽标。

### ⏰ Cron 作业
显示所有计划任务的列表，包括状态、上次运行时间和错误计数。点击可展开错误详情。

### 📋 最近活动
最近事件和成就的时间线。

### 🔴 实时指示器（仅第三级）
绿色闪烁点表示 WebSocket 已连接。数据更新时会显示动画。

---

## 各级别的要求

| 级别 | 所需工具 | 外部账户 | 环境变量 |
|------|-------------|-------------------|----------|
| **第一级** | 无 | 无 | 无 |
| **第二级** | `git`、`gh` CLI | GitHub（免费） | `DASHBOARD_PIN` |
| **第三级** | `curl` | Supabase（免费）、Vercel（免费） | 详见下文 |

### 环境变量

| 变量 | 是否必需 | 级别 | 用途 |
|----------|----------|------|---------|
| `DASHBOARD_PIN` | 否 | 所有级别 | 用于仪表板访问的 PIN 码（直接在 HTML 配置中设置） |
| `SUPABASE_URL` | 是 | 仅第三级 | 您的 Supabase 项目 URL |
| `SUPABASE_ANON_KEY` | 是 | 仅第三级 | Supabase 匿名密钥——用于仪表板的读取和推送脚本的写入 |

**第一级不需要任何环境变量。** 第二级只需要一个 GitHub 仓库。第三级只需要 `SUPABASE_URL` 和 `SUPABASE_ANON_KEY`——不需要 `service_role` 密钥。**

### OpenClaw 使用的权限

| 级别 | 权限 | 原因 |
|------|-------------|-----|
| 第一级 | 无 | Canvas 内置在 OpenClaw 中 |
| 第二级 | `exec` | 用于向您的 GitHub 仓库执行 `git push` |
| 第三级 | `exec` | 用于向您的 Supabase 项目执行 `curl` |

不需要其他权限。不需要 `read` 权限——此技能不访问本地文件。

---

## 数据架构

仪表板期望接收以下格式的 JSON 数据：

```json
{
  "lastUpdated": "2024-01-15T12:00:00Z",
  "actionRequired": [
    {
      "title": "Review PR #42",
      "url": "https://github.com/you/repo/pull/42",
      "priority": "high"
    }
  ],
  "activeNow": [
    {
      "task": "Deploying new feature",
      "model": "opus",
      "startedAt": "2024-01-15T11:45:00Z"
    }
  ],
  "products": [
    {
      "name": "My App",
      "url": "https://myapp.example.com",
      "status": "live",
      "lastChecked": "2024-01-15T12:00:00Z"
    }
  ],
  "crons": [
    {
      "name": "Daily Report",
      "schedule": "9:00 AM daily",
      "lastRun": "2024-01-15T09:00:00Z",
      "status": "ok",
      "errors": 0,
      "lastError": null
    }
  ],
  "recentActivity": [
    {
      "time": "2024-01-15T11:30:00Z",
      "event": "✅ Deployed v2.1.0 to production"
    }
  ]
}
```

### 字段参考

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `lastUpdated` | ISO-8601 | 数据最后一次更新的时间 |
| `actionRequired[].priority` | `high\|medium\|low` | 紧急程度 |
| `products[].status` | `live\|testing\|down` | 产品状态 |
| `crons[].status` | `ok\|error\|paused` | 作业状态 |

---

## 安全性与隐私

**这是一个仅提供指令的技能——没有可执行代码，没有安装脚本，也没有第三方依赖。**

### 该技能的功能和限制

| ✅ 可以做什么 | ❌ 不能做什么 |
|---------|-----------|
| 渲染 HTML 仪表板 | 读取本地文件（不读取 HEARTBEAT.md、内存文件或源代码） |
| 将操作状态推送到您的服务 | 将数据发送到第三方服务 |
| 仅读取 OpenClaw API（`cron list`、`sessions_list`） | 不存储、记录或传输凭据 |
| 使用您的 Supabase/GitHub 账户 | 需要 `service_role` 或管理员密钥 |

### 确切推送的数据（第二级和第三级）

仪表板仅推送以下字段——没有其他数据：

| 字段 | 示例 | 是否包含敏感信息？ |
|-------|---------|-------------------|
| `actionRequired[].title` | “审查 PR #42” | ❌ 不包含 |
| `activeNow[].task` | “正在部署 v2.0” | ❌ 不包含 |
| `products[].name` | “我的应用” | ❌ 不包含 |
| `products[].url` | “https://myapp.com” | ❌ 不包含（仅包含公共 URL） |
| `products[].status` | “实时” | ❌ 不包含 |
| `crons[].name` | “每日报告” | ❌ 不包含 |
| `crons[].status` | “ok” / “error” | ❌ 不包含 |
| `crons[].lastError` | “30 秒后超时” | ❌ 不包含（仅包含错误信息） |
| `recentActivity[].event` | “✅ 部署了 v2.1” | ❌ 不包含 |

**永远不会推送：** 密码、API 密钥、令牌、文件内容、数据库凭据或个人身份信息（PII）。代理仅根据操作状态构建 JSON 数据。**

### 代理读取的数据

自动更新 cron 仅使用 OpenClaw 内置 API：

| 数据来源 | 读取的内容 | 是否敏感？ |
|--------|-----------------|------------|
| `cron list`（OpenClaw API） | 作业名称、状态、错误计数 | ❌ 不包含 |
| `sessions_list`（OpenClaw API） | 活动任务标签、模型 | ❌ 不包含 |

**不读取任何本地文件。** Cron 不会访问 HEARTBEAT.md、内存文件、源代码或磁盘上的任何其他文件。操作项和最近的活动需要通过用户点击“手动更新”命令手动添加。

### 不需要 `service_role` 密钥

**此技能不需要 Supabase 的 `service_role` 密钥。** 匿名密钥通过表特定的 RLS 来处理读取和写入操作：
- `dashboard_state` 表允许匿名用户执行 `SELECT` 和 `UPDATE` 操作（通过 RLS 策略）
- 匿名密钥只能读取/写入这个表——无法访问其他表
- 最坏情况下，即使有人获得了您的匿名密钥，他们也只能覆盖仪表板的状态数据（这些数据并不敏感）
- 匿名密钥与您客户端 Supabase 应用中已嵌入的密钥相同

### 行级安全（第三级）

提供的 SQL（`setup-supabase.sql`）配置了表特定的 RLS：
- **`SELECT`：** 匿名用户可以执行操作——仪表板可以读取状态 |
- **`UPDATE`：** 匿名用户只能在 `dashboard_state` 表上执行更新操作——推送脚本可以更新状态 |
- **其他表：** 不受影响——匿名用户对其他表的 RLS 策略保持不变 |
- **`DELETE`：** 匿名用户无法删除仪表板行

### PIN 保护——限制

客户端侧的 PIN 码可以防止随意访问，但不能防止有针对性的攻击。

**为了更强的保护：**
- **第二级：** 将您的 GitHub Pages 仓库设置为 **私有**（GitHub Pro 订阅）
- **第三级：** 使用 Vercel 的 **密码保护**（Pro 计划）或添加 Supabase 认证 |
- **所有级别：** 仪表板仅包含操作状态——即使被访问，也不会泄露任何敏感信息**

---

## 包含的文件

```
agent-dashboard/
├── SKILL.md                      # This file
├── assets/
│   ├── tier1-canvas.html         # Lightweight canvas version
│   ├── tier2-github.html         # GitHub Pages + polling
│   ├── tier3-realtime.html       # Supabase Realtime version
│   └── push-dashboard.sh         # Push script for Tier 3
├── assets/templates/
│   ├── dashboard-data.json       # Sample data structure
│   └── setup-supabase.sql        # Supabase table setup
└── references/
    └── customization.md          # Theme and layout customization
```

---

## 故障排除

### 仪表板显示“断开连接”（第三级）
- 检查 Supabase 项目是否正在运行
- 确认匿名密钥是否正确
- 确保表上的实时更新功能已启用

### 数据未更新（第二级）
- 检查 GitHub Pages 是否已启用
- 确认 `data/dashboard-data.json` 是否已成功推送
- 强制刷新页面（Ctrl+Shift+R）
- 点击强制更新按钮以确认数据是否过时

### PIN 无效
- PIN 码区分大小写
- 确认您在 HTML 配置中使用的 PIN 码是否正确

### Cron 状态不准确
- 确保您的仪表板更新 cron 作业正在运行（`cron list`）
- 检查 cron 输出中的错误
- 手动运行更新命令：“立即更新我的任务控制面板”

---

## 致谢

此技能专为 OpenClaw 社区开发。采用 MIT 许可证。