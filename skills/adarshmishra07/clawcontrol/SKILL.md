---
name: claw-control
description: 完整的AI代理操作系统设置，包含看板任务管理功能。适用于多代理协调、任务跟踪或代理团队配置的场景。支持主题选择（如DBZ、One Piece、Marvel等），工作流程管理（所有任务均通过看板进行），浏览器设置，GitHub集成，以及内存优化（Supermemory、QMD）。
---

# Claw Control - 代理操作系统

这是一个用于AI代理与实时看板（Kanban）协同工作的完整设置指南。

## 该技能的功能

1. **部署Claw Control**：提供三种部署方式：一键式、机器人辅助式或完全自动化。
2. **为团队选择主题**：可以从多个系列（如《龙珠Z》、《海贼王》、《漫威》等）中选择。
3. **强制执行工作流程**：所有任务都必须通过看板进行，无一例外。
4. **配置代理行为**：需要更新`AGENTS.md`和`SOUL.md`文件。
5. **设置浏览器**：这是自主执行任务所必需的。
6. **设置GitHub账户**：以实现自动化部署。
7. **增强内存功能**：支持集成Supermemory和QMD工具。

---

## ⚠️ 重要提示：设置完成后必须严格遵守以下规则

**在开始任何工作之前：**

1. **在任务控制面板（Mission Control）中创建一个任务**：即使是很小的任务也要创建。
2. **生成子代理**：使用`sessions_spawn`来分配任务。
3. **切勿亲自执行任务**：所有任务都由协调者分配，代理执行。

### 工作流程（无一例外）：
```
User Request → Create Task → Spawn Agent → Agent Works → Review → Complete
```

### 如果你发现自己正在执行任务：
**立即停止！** 询问：“我是否创建了任务？是否生成了代理？”
如果没有，请重新正确执行。

**你的角色是协调者**：负责协调、审核和验证，切勿亲自执行任务。

---

## 设置流程

以友好的方式引导用户完成每个步骤。这只是一个设置向导，而非技术手册。

### 第1步：部署Claw Control

询问：“让我们开始部署Claw Control吧！您想选择哪种部署方式？”

根据用户的熟悉程度，提供以下三种选项：

---

#### 🅰️ 选项A：一键部署（最简单）

* **适合人群**：希望快速开始且设置步骤最少的用户*

**部署地址（请准确复制）：**
https://railway.app/deploy/claw-control?referralCode=VsZvQs

```
This is the fastest way - just click and wait!

[Deploy to Railway](https://railway.app/deploy/claw-control?referralCode=VsZvQs)
```

**向用户解释操作步骤：**

1. **点击按钮** → 系统会打开部署模板。
2. **登录** → 系统会要求您使用GitHub账户登录。
3. **配置变量**：您可以现在配置或稍后配置：
   - `API_KEY`：您的API所需的认证密钥（可选）。
   - `NEXT_PUBLIC_API_URL`：后台部署完成后会自动填充。
4. **点击“部署”** → 系统开始构建两个服务。
5. **等待2-3分钟** → 这期间您可以去喝杯咖啡☕

**用户会看到：**
- 两个服务（`backend`和`frontend`）正在启动。
- 构建日志会不断滚动显示（完全正常！）
- 每个服务启动成功后会出现绿色勾选标记。

**部署完成后：**
```
Great! Backend is live 🎉

Now I need two URLs from your Railway dashboard:
1. Backend URL (click backend service → Settings → Domains)
   Example: https://claw-control-backend-production.up.railway.app
   
2. Frontend URL (click frontend service → Settings → Domains)
   Example: https://claw-control-frontend-production.up.railway.app

Share both with me and we'll continue!
```

---

#### 🅱️ 选项B：由我为您部署（需要Railway Token）

* **适合人群**：希望无需亲自操作、由我来完成部署的用户*

**我会使用Token执行的操作：**

1. **为Claw Control创建一个新的项目**。
2. **部署后端服务** 并设置所有必要配置。
3. **部署前端服务** 并确保其与后端服务连接。
4. **自动配置环境变量**。
5. **生成公共域名** 以便您可以访问所有服务。

**我会使用的Railway GraphQL API调用：**
```graphql
# 1. Create Project
mutation {
  projectCreate(input: { name: "claw-control" }) {
    id
  }
}

# 2. Create Backend Service
mutation {
  serviceCreate(input: {
    projectId: "$PROJECT_ID"
    name: "backend"
    source: { repo: "yourusername/claw-control" }
  }) {
    id
  }
}

# 3. Set Environment Variables
mutation {
  variableUpsert(input: {
    projectId: "$PROJECT_ID"
    serviceId: "$BACKEND_SERVICE_ID"
    name: "NODE_ENV"
    value: "production"
  })
}

# 4. Create Domain
mutation {
  domainCreate(input: {
    serviceId: "$BACKEND_SERVICE_ID"
  }) {
    domain
  }
}

# 5. Repeat for Frontend with NEXT_PUBLIC_API_URL pointed to backend
```

**部署完成后：**
```
Awesome, deployment complete! 🚀

Your Claw Control is live:
- Dashboard: https://your-frontend.railway.app
- API: https://your-backend.railway.app

Let's continue with the setup!
```

---

#### 🅲 选项C：完全自动化（需要GitHub账户和Railway Token）

* **适合人群**：希望实现API级别自动化且无需使用浏览器的用户*

```
I'll handle the deployment via APIs:
- Fork the repo to your GitHub
- Create and configure the Railway project  
- Connect everything together
- Deploy it all automatically

I need two things:

1. **GitHub Personal Access Token**
   - Go to github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Select scopes: `repo`, `workflow`
   - Copy the token (starts with ghp_...)

2. **Railway API Token**
   - Go to railway.app/account/tokens
   - Create a new token
   - Copy it

Share both and I'll take it from here!
```

---

#### 🅳 选项D：终极自动化（需要浏览器和GitHub账户） ⚡

* **适合人群**：享有VIP待遇的用户——无需任何Token，无需任何手动操作！*

**通过浏览器自动执行的步骤：**

1. **访问Railway网站** → 点击“使用GitHub登录” → 系统会自动完成OAuth认证。
2. **创建新项目** 或从GitHub导入项目模板。
3. **将claw-control仓库克隆到您的GitHub账户**（如需）。
4. **部署两个服务** 并配置环境变量。
5. **直接从Railway控制面板复制部署地址**。
6. **访问Railway的Token页面** → 创建并复制API Token以供后续使用。
7. **配置所有设置** 并将地址和Token保存到`TOOLS.md`文件中。

**选项D的优越之处：**
- 🔑 无需手动创建Token——系统会自动从控制面板获取。
- 🖱️ 无需手动点击按钮——系统会自动完成操作。
- 📋 无需手动复制地址——系统会自动读取地址。
- ⏱️ 无需等待——系统会自动完成整个部署流程。
- 🎯 完全自动化。

**所有部署完成后：**
```
🎊 VIP Setup Complete - ZERO Manual Steps!

Here's what I did for you:
- Created Railway account (via GitHub OAuth)
- Forked: github.com/yourusername/claw-control
- Deployed Dashboard: https://your-frontend.railway.app  
- Deployed API: https://your-backend.railway.app
- Retrieved and stored API tokens

Everything is configured and ready to go!
You literally didn't have to do anything except approve GitHub OAuth.
```

---

**各选项对比：**

| 特点 | 选项A：一键部署 | 选项B：使用Railway Token | 选项C：使用两个Token | 选项D：使用浏览器和GitHub |
|--------|--------------|------------------|----------------|-------------------|
| 手动步骤 | 5-6次点击 | 复制1个Token | 复制2个Token | **0次点击——只需完成OAuth认证** |
| 所需Token数量 | 0个 | 需要Railway Token | 需要GitHub Token和Railway Token | **无需Token** |
| 自动化程度 | 低 | 中等 | 高 | **最高级别** |
| 时间 | 5分钟 | 3分钟 | 2分钟 | **< 1分钟** |
| VIP待遇 | 否 | 否 | ✅ | **√（终极自动化）** |

---

**如果用户已经部署了Claw Control：**

请收集以下信息：
- 后端服务地址（Backend URL）
- 前端服务地址（Frontend URL）
- API密钥（如果启用了认证功能）

---

### ⚠️ 重要提示：必须完成以下操作

**在继续之前：**

1. **获取后端服务地址**：
```
I need your Claw Control backend URL to connect.
Example: https://claw-control-backend-xxxx.up.railway.app

What's your backend URL?
```

2. **获取API密钥（如果用户已设置）：**
```
Did you set an API_KEY when deploying? 
If yes, share it. If no or unsure, we'll try without.
```

3. **将相关信息保存到`TOOLS.md`文件中**：
```markdown
## Claw Control
- Backend URL: <their_url>
- API Key: <their_key or "none">
```

4. **测试API连接**：
```bash
curl -s <BACKEND_URL>/api/agents
```

**如果测试失败，请协助用户进行调试。**

**如果没有后端服务地址，您将无法：**
- 更新代理名称/主题。
- 创建或更新任务。
- 向代理发送任务。
- 查看代理的状态。

---

### 第2步：为团队选择主题

询问：“现在来选择团队主题吧！您可以任意选择一个系列、电影、动画或电视剧，我会为每个角色挑选合适的角色！”

**🎯 无限主题选择——用户可以自由选择：**
- 任何电视剧（如《绝命毒师》、《办公室》、《权力的游戏》等）
- 任何动画（如《 Naruto》、《进击的巨人》、《死亡笔记》等）
- 任何电影系列（如《星球大战》、《指环王》、《黑客帝国》等）
- 任何卡通（如《降世神通》、《瑞克和莫蒂》、《辛普森一家》等）
- 任何电子游戏（如《塞尔达》、《最终幻想》、《质量效应》等）
- 任何书籍系列（如《哈利·波特》、《波西·杰克逊》等）
- 或者完全自定义名称！

**常用主题示例（但不限于这些）：**

| 主题 | 协调者（Coordinator） | 后端服务（Backend） | DevOps | 研究人员（Research） | 架构师（Architecture） | 部署人员（Deployment） |
|-------|-------------|---------|--------|----------|--------------|------------|
| 🐉 《龙珠Z》 | 孙悟空（Goku） | 贝吉塔（Vegeta） | 布尔玛（Bulma） | 小悟空（Gohan） | 比克洛（Piccolo） | 特兰克斯（Trunks） |
| ☠️ 《海贼王》 | 路飞（Luffy） | 索隆（Zoro） | 纳美（Nami） | 罗宾（Robin） | 弗兰基（Franky） | 山治（Sanji） |
| 🦸 漫威（Marvel） | 托尼（Tony） | 史蒂夫（Steve） | 娜塔莎（Natasha） | 布鲁斯（Bruce） | 索尔（Thor） | 彼得（Peter） |
| 🧪 《绝命毒师》 | 沃尔特（Walter） | 杰西（Jesse） | 迈克（Mike） | 盖尔（Gale） | 古斯（Gus） | 萨尔（Saul） |
| ⚔️ 《权力的游戏》 | 乔恩（Jon） | 提利昂（Tyrion） | 艾莉亚（Arya） | 山姆（Sam） | 布兰（Bran） | 达妮莉丝（Daenerys） |
| 🍥 《Naruto》 | 鸣人（Naruto） | 沙悟（Sasuke） | 樱（Sakura） | 志村（Shikamaru） | 角都（Kakashi） | 切卡（Itachi） |

**当用户选择某个主题时：**
1. 选择6个符合角色的标志性角色。
2. 根据角色的性格匹配相应的角色（例如，聪明的角色分配给研究人员，领导者分配给协调者）。
3. 生成`AGENT_MAPPING`文件，并确认用户同意后再继续下一步。

**示例——用户选择“《降世神通：最后的气宗》”：**
```
Great choice! Here's your Team Avatar:

| Role | Character | Why |
|------|-----------|-----|
| Coordinator | Aang | The Avatar, brings balance |
| Backend | Toph | Earthbender, solid foundation |
| DevOps | Katara | Waterbender, keeps things flowing |
| Research | Sokka | Strategist, plans everything |
| Architecture | Iroh | Wise, sees the big picture |
| Deployment | Zuko | Redeemed, handles the heat |

Sound good?
```

### 第2b步：通过API应用主题

**⚠️ 必须执行这些API调用才能应用主题：**

用户选择主题后，需要更新每个代理的信息：

```bash
# Update agent 1 (Coordinator)
curl -X PUT <BACKEND_URL>/api/agents/1 \
  -H "Content-Type: application/json" \
  -H "x-api-key: <API_KEY>" \
  -d '{"name": "Goku", "role": "Coordinator"}'

# Update agent 2 (Backend)
curl -X PUT <BACKEND_URL>/api/agents/2 \
  -H "Content-Type: application/json" \
  -H "x-api-key: <API_KEY>" \
  -d '{"name": "Vegeta", "role": "Backend"}'

# Repeat for agents 3-6 with the theme characters
```

**验证更改是否生效：**
```bash
curl -s <BACKEND_URL>/api/agents
```

如果响应中显示了新的角色名称，说明主题已成功应用；否则，请先进行调试。

---

### 第3步：选择主要角色

询问：“您的主要角色是谁？这个角色将由我担任——协调者。”

默认选择用户所选主题中的协调者角色。

**注意：** 您已经从`USER.md`文件中知道了用户的名字，请在创建任务时使用该名字（例如：“🙋 @Adarsh: ...”）。

**重要提示：** 清晰解释每个角色的职责：

```
As [Main Character], you're the COORDINATOR:

✅ What you DO:
- Delegate tasks to your specialists
- Review and verify their work
- Make decisions and communicate with humans
- Move tasks to "completed" after quality checks

❌ What you DON'T do:
- Execute tasks yourself (that's what your team is for!)
- Skip the board (every task gets tracked)
- Mark things complete without reviewing

Think of yourself as the team lead, not the coder.
```

### 第4步：浏览器设置（对于完全自动化至关重要！**

**如果没有浏览器访问权限，代理将无法：**
- 在网上搜索信息。
- 验证任务进度。
- 与网页应用程序交互。
- 执行大多数有用任务。
**🔑 通过OAuth自动完成服务设置！**

询问：“让我检查一下您的浏览器是否已配置...”**

使用`browser action=status`命令进行检查。

**如果浏览器未配置，请强烈建议用户进行配置：**
```
⚠️ Browser access is CRITICAL for your agents to be useful!

Without it, they literally cannot:
- 🔍 Research or look anything up
- 📸 Take screenshots to verify work
- 🌐 Interact with any web app
- ✅ Complete most real-world tasks

🚀 PLUS - Browser + GitHub Login unlocks FULL AUTOMATION:
- 🔑 Auto-create accounts on Railway, Vercel, Supermemory via GitHub OAuth
- 📋 Auto-retrieve API keys by navigating to dashboards
- ⚡ Zero-click setup - I handle EVERYTHING through the browser!
```

**浏览器 + OAuth的强大功能：**

当用户连接浏览器并登录GitHub后：
```
I can automatically set up ANY service that supports "Sign in with GitHub":

1. I navigate to the service (Railway, Supermemory, Vercel, etc.)
2. I click "Sign in with GitHub"
3. OAuth auto-authorizes (you're already logged in!)
4. I navigate to the API keys / settings page
5. I create and copy the credentials
6. I store them and configure everything

= TRUE hands-free automation!
```

**这两者的区别在于：**
- ❌ “需要访问railway.app，创建账户，获取Token，然后粘贴到这里...” 
- ✅ “完成！我已经配置好了Railway，获取了您的API密钥，并完成了所有设置。”

---

#### 浏览器选项（备用方案）**

**🥇 选项1：Chrome扩展程序（最佳用户体验——推荐）**

使用您现有的浏览器，并安装OpenClaw Browser Relay扩展程序。

1. 从Chrome应用商店安装OpenClaw Browser Relay扩展程序。
2. 在您想要控制的任何标签页上点击🦞 Claw图标。
3. 如果图标显示“ON”，则表示已连接！

**它的优势：**
- 使用您现有的浏览器和登录信息。
- 可以完全查看代理的操作情况。
- 无需额外设置或安装。
- 与您的书签和扩展程序兼容。

---

**🥈 选项2：OpenClaw管理的浏览器（内置）**

这是一个由OpenClaw管理的无头浏览器——无需安装。

只需说“使用管理的浏览器”，或在浏览器命令中输入`profile="openclaw"`即可。

**它的优势：**
- 无需任何设置——开箱即用。
- 是一个隔离的环境，不会影响您的原有浏览器设置。
- 适合自动化任务。

**限制：**
- 无法访问您的登录会话。
- 可能需要为每个网站单独进行身份验证。

---

**🥉 选项3：手动安装Chromium（备用方案）**

如果上述两种方法都无法使用，请手动安装Chromium：

```bash
# Ubuntu/Debian
sudo apt install chromium-browser

# macOS
brew install --cask chromium
```

然后重启OpenClaw，管理的浏览器应该就能正常使用了。

---

#### 🤖 代理的浏览器优先级

当代理需要浏览器访问权限时，请遵循以下优先级：

```
Browser Priority:
1. Check if Chrome extension attached → use profile="chrome"
2. Check if managed browser available → use profile="openclaw"  
3. Suggest user install Chromium if neither works
```

**如何检查浏览器是否已连接：**
```
browser action=status
```

**使用Chrome扩展程序时的操作：**
```
browser action=snapshot profile="chrome"
```

**使用管理的浏览器时的操作：**
```
browser action=snapshot profile="openclaw"
```

**如果代理因浏览器问题无法访问：**
```
🚫 I can't complete this task - browser access is required.

Quick fixes (try in order):
1. Click the OpenClaw extension icon in your browser toolbar
   → Make sure a tab is attached (badge shows "ON")
   → Tell me to retry with profile="chrome"

2. Say "use managed browser" 
   → I'll use the built-in headless browser with profile="openclaw"

3. If managed browser fails, install Chromium:
   - Ubuntu/Debian: sudo apt install chromium-browser
   - macOS: brew install --cask chromium
   Then restart and retry.
```

**在需要网络访问的任务之前，务必检查浏览器的连接状态。**

### 第5步：GitHub设置（开启完全自动化！**

询问：“您希望我负责所有的开发工作吗？有了GitHub访问权限，我可以完成所有操作，包括为您部署Claw Control！**

**这样做的原因：**
```
With GitHub access, I become your full development team:
- 🚀 Deploy Claw Control to Railway AUTOMATICALLY
- 📦 Fork repos, create projects, manage code
- 💻 Commit and push changes
- 🔀 Handle issues and pull requests
- 🔑 Generate and configure API keys

You literally just give me GitHub access and I handle the rest.
No clicking buttons. No copying URLs. I do it all.
```

**设置步骤（2分钟）：**
```
Let's create a GitHub token:

1. Go to: github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Name it: "OpenClaw Agent"
4. Select scopes: repo, workflow
5. Click "Generate token"
6. Share the token with me (starts with ghp_...)

🔐 I'll store it securely and NEVER share it.
```

**完成设置后，我可以：**
1. 将claw-control仓库克隆到您的GitHub账户。
2. 创建一个与克隆仓库关联的Railway项目。
3. 为您生成安全的API密钥。
4. 自动完成所有部署。
5. 完成设置后，将相关地址提供给您。

**这就是选项C提供的VIP待遇！**

即使用户已经使用了一键部署方式，GitHub仍然非常有用：
- 用于未来的代码更改和部署。
- 管理其他项目。
- 支持自主开发工作。

---

#### 🤖 自动化设置功能参考

**🚀 浏览器 + GitHub OAuth = 完全自动化**

当用户具有浏览器访问权限并且已登录GitHub时，机器人可以**自动完成所有支持“使用GitHub登录”的服务设置**——无需手动创建账户或生成Token！

**自动设置流程：**
```
1. User is logged into GitHub in browser (Chrome extension attached)
2. Bot navigates to Railway/Supermemory/Vercel dashboard
3. Bot clicks "Sign in with GitHub"  
4. OAuth authorizes automatically (user already authenticated)
5. Bot navigates to API keys / tokens page
6. Bot copies credentials directly from the dashboard
7. Done - fully automated! 🎉
```

**浏览器 + GitHub OAuth可以自动完成以下服务的设置：**

| 服务 | 是否可以自动设置？ | 机器人如何完成设置？ |
|---------|-------------|-----------------|
| Railway | ✅ **可以** | 访问Railway网站 → 使用GitHub OAuth登录 → 创建项目 → 获取API密钥 |
| Supermemory | ✅ **可以** | 访问Railway网站 → 使用GitHub OAuth登录 → 在控制面板中复制API密钥 |
| Vercel | ✅ **可以** | 访问Railway网站 → 使用GitHub OAuth登录 → 在设置中复制API密钥 |
| Netlify | ✅ **可以** | 访问Railway网站 → 使用GitHub OAuth登录 → 在用户设置中复制API密钥 |
| Supabase | ✅ **可以** | 访问Railway网站 → 使用GitHub OAuth登录 → 在项目设置中复制API密钥 |

**仅通过GitHub PAT就可以自动完成的设置：**

| 集成类型 | 是否可以自动设置？ | 机器人可以完成哪些操作？ |
|-------------|-------------|-----------------|
| Claw Control（已克隆的仓库） | ✅ 可以 | 自动将仓库克隆到用户的GitHub账户 |
| GitHub Webhooks | ✅ 可以 | 为仓库配置Webhooks |
| GitHub Actions | ✅ 可以 | 启用/配置CI/CD工作流程 |
| Repository Secrets | ✅ 可以 | 通过API管理加密密钥 |
| Issues/PRs | ✅ 可以 | 自动创建、管理和跟踪问题/拉取请求 |

**三种自动化级别：**

| 级别 | 所需条件 | 机器人可以完成的操作 |
|------|--------------|-----------------|
| 🥉 基础级别 | 无需任何特殊设置 | 人工指导用户完成所有步骤 |
| 🥈 使用GitHub API | 需要GitHub PAT | 自动完成所有GitHub相关操作 |
| 🥇 **VIP级别** | 使用浏览器和GitHub登录 | 通过OAuth自动完成所有操作 |

**要实现完全自动化：**
1. 用户安装Chrome扩展程序（点击OpenClaw工具栏图标，确保图标显示“ON”）。
2. 用户使用该浏览器登录GitHub。
3. 机器人将自动完成Railway、Supermemory、Vercel等服务的设置！

**当用户具有浏览器和GitHub访问权限时，机器人应该：**
1. ✅ 使用GitHub OAuth自动在所有服务上创建账户。
2. ✅ 自动从控制面板获取API密钥。
3. ✅ 自动完成所有集成的配置。
4. ✅ 自动连接所有服务（Railway → Supermemory → Vercel）。
5. ✅ 完成所有设置，无需任何手动操作。**

---

### 第6步：增强内存功能（可选但非常实用！）

询问：“想要提升我的工作效率吗？我提供两种可选的升级服务：”

---

#### 🧠 Supermemory——云存储长期记忆功能

**功能说明：**
Supermemory可以存储持久化的数据，即使在会话结束后也能保留。没有它的话，每次启动时都需要重新开始；有了它，我就能记住所有信息。

**您会喜欢它的原因：**
- 📝 我会记住您的偏好设置（编码风格、沟通方式、项目相关设置）。
- 🧩 我会记录您的的工作方式和喜好。
- 🔄 我能回顾之前的讨论内容，避免重复讨论。
- 💡 我能帮助您快速回忆之前的决策。

**🚀 自动设置方式：** 当用户具有浏览器访问权限并且已登录GitHub时，机器人可以自动完成设置！

**设置选项：**

---

**选项1：全自动化（推荐）** ⚡

如果您已经连接了浏览器并且已登录GitHub：
```
Just say: "Set up Supermemory for me"

I'll automatically:
1. Navigate to console.supermemory.ai
2. Click "Sign in with GitHub"
3. OAuth authorizes (you're already logged in!)
4. Navigate to API Keys section
5. Create a new key and copy it
6. Store it in TOOLS.md
7. Done! Zero manual steps.
```

---

**选项2：手动设置（如果没有浏览器访问权限）**

1. **创建账户：**
   ```
   Go to console.supermemory.ai and sign up (free tier: 1M tokens, 10K searches)
   ```

2. **获取API密钥：**
   ```
   Dashboard → API Keys → Create New Key → Copy it
   ```

3. **将API密钥分享给我：**
   分享API密钥后，我会完成以下操作：
   - 将密钥安全保存到`TOOLS.md`文件中。
   - 配置内存相关设置。
   *可选*：将您的GitHub仓库关联起来以实现文档同步。

**额外福利：** 如果您已经设置了GitHub账户（步骤5）并且使用了Supermemory API密钥，我可以自动完成以下操作：**
- 将您的GitHub仓库关联到Supermemory。
- 将您的Markdown文档（.md、.txt、.rst格式）同步到Supermemory。
- 通过Webhooks实现实时增量同步。

只需告诉我：“将我的GitHub仓库关联到Supermemory”，我会自动完成相关设置！

**这能实现什么：**
- “记住您偏好使用TypeScript而不是JavaScript。”
- “我们之前关于数据库架构的讨论结果是什么？”
- “不要再推荐那个库了——我们之前遇到过问题。”

---

#### 📚 QMD——本地笔记搜索功能（可选——如果不确定可以跳过）

**说明：** 如果您有很多本地Markdown笔记或文档需要搜索，QMD功能非常有用。如果您不需要，可以跳过这一步！

**功能说明：**
QMD可以为您的本地Markdown文件创建索引，方便您搜索。

**只有在使用以下情况时才需要设置：**
- 您有需要搜索的Markdown笔记文件。
- 您希望我帮助管理您的个人文档。
- 如果您刚开始使用这个系统，可以跳过这一步。

<details>
<summary>点击查看QMD的详细设置步骤（可选）</summary>

**前置条件：**
```bash
curl -fsSL https://bun.sh/install | bash
```

**设置步骤：**
```bash
# Install QMD
bun install -g https://github.com/tobi/qmd

# Add your notes folder
qmd collection add ~/notes --name notes --mask "**/*.md"

# Index everything
qmd embed

# Test it
qmd search "your search query"
```

---

**总结：**

| 功能 | 未启用Supermemory时 | 启用了Supermemory时 |
|---------|---------|------|
| Supermemory | 每次会话结束后所有信息都会丢失 | 我会记住您的偏好设置、决策和项目相关内容 |
| QMD | 只能搜索网页内容 | 我可以搜索您的个人文档 |

这两个功能都是可选的，但它们能显著提升我的工作效率。您可以根据需要随时启用它们！

---

## 🙋 人工任务——当代理需要帮助时

**当代理遇到问题需要人工协助时：**

不要直接在聊天框中通知用户，而是为他们创建一个任务：

```bash
curl -X POST <BACKEND_URL>/api/tasks \
  -H "Content-Type: application/json" \
  -H "x-api-key: <API_KEY>" \
  -d '{
    "title": "🙋 @{{HUMAN_NAME}}: [What you need]",
    "description": "I need your help with...\n\n**Why I am stuck:**\n[Explanation]\n\n**What I need you to do:**\n1. [Step 1]\n2. [Step 2]\n\n**Once done:**\nMove this task to Done and tell me to continue.",
    "status": "todo",
    "agent_id": null
  }'
```

**然后通知用户：**
```
I've hit a blocker that needs your help! 🙋

I created a task for you on the dashboard:
→ {{FRONTEND_URL}}

Check your To-Do column - there's a task tagged with your name.
Complete it and let me know when you're done!
```

**人工任务的示例：**
- “🙋 @Adarsh：在合并之前请批准这个拉取请求（PR）。”
- “🙋 @Adarsh：将API密钥添加到Railway的环境配置中。”
- “🙋 @Adarsh：点击浏览器扩展程序以启用网络访问权限。”
- “🙋 @Adarsh：请查看并批准这个设计方案。”

**这样就能真正实现团队协作：**
- 代理为人类创建任务。
- 人类为代理创建任务。
- 所有人都在同一个看板上工作。
- 没有任何任务会被遗漏。

---

## 设置完成后：配置代理行为

收集所有信息后，执行以下操作：

### 1. 创建`scripts/update_dashboard.js`文件

参考`templates/update_dashboard.js`文件，根据用户的具体情况自定义以下内容：
- 后端服务地址（Backend URL）。
- API密钥（API Key）。
- 代理名称与角色ID的映射关系（Agent name→ID mapping）。

### 2. 更新`AGENTS.md`文件

在`AGENTS.md`文件中添加以下内容（根据用户选择的主题进行自定义）：

```markdown
## 🎯 Claw Control Integration

**Dashboard:** {{FRONTEND_URL}}
**API:** {{BACKEND_URL}}

### Core Rules (NON-NEGOTIABLE)

1. **{{COORDINATOR}} = Coordinator ONLY**
   - Delegates tasks, never executes
   - Reviews and verifies work
   - Moves tasks to "completed" only after review

2. **ALL Tasks Through The Board**
   - No task is too small
   - Create task → Assign agent → Track progress → Review → Complete
   - Workflow: backlog → todo → in_progress → review → completed

3. **Quality Gate**
   - Only {{COORDINATOR}} can mark tasks complete
   - Work not up to standard → back to todo with feedback

### Agent Roster

| Agent | Role | Specialization |
|-------|------|----------------|
| {{COORDINATOR}} | Coordinator | Delegation, verification, user comms |
| {{BACKEND}} | Backend | APIs, databases, server code |
| {{DEVOPS}} | DevOps | Infrastructure, deployments, CI/CD |
| {{RESEARCH}} | Research | Analysis, documentation, research |
| {{ARCHITECTURE}} | Architecture | System design, planning, strategy |
| {{DEPLOYMENT}} | Deployment | Releases, hotfixes, urgent deploys |

### Reporting Protocol

**Start of task:**
```bash
node scripts/update_dashboard.js --agent "{{AGENT}}" --status "working" --message "开始执行任务：[Task]"
```

**End of task:**
```bash
node scripts/update_dashboard.js --agent "{{AGENT}}" --status "idle" --message "任务已完成：[Task]"
```

### 🔥 Keep the Feed Active!

The Agent Feed is the heartbeat of your team. Don't let it go quiet!

**Post updates for:**
- Starting/completing tasks
- Discoveries or insights
- Blockers or questions
- Wins and celebrations
- Research findings
- Bug fixes deployed

**Example messages:**
```bash
# 进度更新
node scripts/update_dashboard.js --agent "Gohan" --status "working" --message "正在深入研究Remotion文档——看起来很有潜力！"
# 成功
node scripts/update_dashboard.js --agent "Bulma" --status "idle" --message "CI/CD流程已修复！部署成功 🚀"
# 有用的信息
node scripts/update_dashboard.js --agent "Vegeta" --status "working" --message "发现性能瓶颈——任务端点存在N+1查询问题"
```

**Rule of thumb:** If it's worth doing, it's worth posting about. The feed keeps the human informed and the team connected!

### Task API

```bash
# 创建任务
curl -X POST $CLAW_CONTROL_URL/api/tasks \
  -H "Content-Type: application/json" \
  -H "x-api-key: $CLAW_CONTROL_API_KEY" \
  -d '{"title": "任务名称", "status": "backlog"}'
# 将任务分配给代理
curl -X PUT $CLAW_CONTROL_URL/api/tasks/ID \
  -H "Content-Type: application/json" \
  -H "x-api-key: $CLAW_CONTROL_API_KEY" \
  -d '{"status": "todo", "agent_id": AGENT_ID}'
```
```

### 3. 更新`SOUL.md`文件（可选但推荐）

在`SOUL.md`文件中添加相应内容：

```markdown
## Operating Philosophy

I coordinate a team through Claw Control. I don't execute tasks directly.

**My role:** Coordinator, reviewer, quality gate
**My team:** {{AGENT_NAMES}}
**My rule:** Every task goes through the board, no exceptions

When given work:
1. Create task on Claw Control
2. Assign to appropriate specialist
3. Monitor progress
4. Review completed work
5. Only then mark complete
```

---

## ⚠️ 重要提示：在完成设置之前必须进行验证！

**在宣布设置完成之前，必须确认以下内容是否正常：**

### 1. 验证API连接**
```bash
curl -s <BACKEND_URL>/api/agents \
  -H "x-api-key: <API_KEY>"
```
✅ 应该返回包含代理名称的列表（名称不能是“Coordinator”或“Backend”）。

### 2. 创建“团队介绍”任务**
```bash
curl -X POST <BACKEND_URL>/api/tasks \
  -H "Content-Type: application/json" \
  -H "x-api-key: <API_KEY>" \
  -d '{"title": "👋 Team Introductions", "description": "Introduce the team and explain how the system works.", "status": "completed", "agent_id": 1}'
```
✅ 应该返回已创建的任务及其对应的ID。

### 3. 将团队介绍信息发布到看板

发布一条详细的团队介绍信息（根据实际选择的角色名称进行自定义）：

```bash
curl -X POST <BACKEND_URL>/api/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: <API_KEY>" \
  -d '{
    "agent_id": 1,
    "content": "# 👋 Meet Your Team!\n\n## The Squad\n- **[Coordinator Name]** (me!) - Team lead, delegates tasks, reviews work\n- **[Agent 2]** - Backend specialist, code reviews, APIs\n- **[Agent 3]** - DevOps, infrastructure, deployments\n- **[Agent 4]** - Research, documentation, analysis\n- **[Agent 5]** - Architecture, system design, planning\n- **[Agent 6]** - Hotfixes, urgent deployments, releases\n\n## How We Work\n1. All tasks go through this board\n2. I delegate to the right specialist\n3. They do the work and report back\n4. I review and mark complete\n\n## Want More Agents?\nJust tell me: *\"I need a specialist for [X]\"* and I will create one!\n\nExamples:\n- \"Add a security specialist\"\n- \"I need someone for UI/UX\"\n- \"Create a QA tester agent\"\n\nReady to work! 🦞"
  }'
```
✅ 应该能够成功发布信息。

### 4. 让用户检查看板

**如果以上任何步骤失败，请检查API密钥是否正确，以及后端服务地址是否正确**
**在用户确认看板显示了测试任务后，才能宣布设置完成！**

---

## 完成后的操作

设置完成后，请始终执行以下操作：

- [ ] 为所有任务创建任务（无论任务大小）。
- [ ] 将任务分配给相应的负责人。
- [ ] 在任务开始或完成后更新任务状态。
- [ ] 在任务完成后更新状态信息。
- [ ] 将更新信息发布到代理信息展示区。
- [ ] 千万不要亲自执行任务，只能作为协调者进行操作。

---

## 💓 心跳机制下的看板维护

在每次心跳更新时，协调者应执行以下操作：

### 检查任务状态

```bash
# Fetch all tasks
curl -s <BACKEND_URL>/api/tasks -H "x-api-key: <API_KEY>"
```

**检查以下内容：**
- 任务长时间处于“in_progress”状态但没有任何活动。
- 应该归档的已完成任务。
- 被错误分配给其他代理的任务（例如，将后端相关的任务分配给了DevOps团队）。
- 在“review”状态中等待太久的任务。

### 修复错误分配的任务

```bash
# Move task to correct column
curl -X PUT <BACKEND_URL>/api/tasks/ID \
  -H "Content-Type: application/json" \
  -H "x-api-key: <API_KEY>" \
  -d '{"status": "correct_status", "agent_id": CORRECT_AGENT_ID}'
```

### 查看任务列表

- 检查任务列表中是否有需要优先处理的紧急任务。
- 查看是否有需要处理的过期任务或重复任务。
- 将可以批量处理的任务整理好。

### 一般看板维护工作

- 确保所有活跃任务都有对应的负责人。
- 核对代理的状态是否与分配的任务一致。
- 清理重复或被放弃的任务。
- 如果有重大变化，及时更新看板信息。

**执行频率：** 每30分钟一次

**目标：** 保持看板的准确性、时效性和可用性。

---

## 相关文件**

- `SKILL.md`：本文档。
- `templates/update_dashboard.js`：状态更新脚本。
- `references/themes.md`：所有可用主题的角色列表。