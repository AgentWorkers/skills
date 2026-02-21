# agent-chat-ux

**名称:** agent-chat-ux  
**版本:** 1.3.0  
**作者:** Charles Sears  
**描述:** 该升级改进了 OpenClaw 控制界面的聊天功能和代理管理体验：包括聊天界面中的代理选择下拉菜单、按代理会话过滤功能、新的会话创建按钮、创建代理的向导（手动和 AI 模式）、表情符号选择器、直接编辑/删除代理的功能、代理特定的定时任务统计信息，以及代理相关的后端 CRUD 方法。

---

## ⚠️ 安全性与透明度说明

在应用此技能的补丁之前，请注意以下事项：

### 凭据访问（`agents.wizard`）

AI 向导的后端（`agents.wizard` RPC）会通过 HTTP 直接调用配置的模型提供者 API。为此，它需要一个 API 密钥。凭证的解析顺序如下：

1. **默认配置认证** — 如果解析模式为 `api-key`（最常见），则使用该方式  
2. **认证配置文件** — 搜索与提供者匹配的第一个 `api_key` 类型的配置文件。仅读取 `provider` 和 `type` 字段；不会记录日志或返回其他信息。  
3. **环境变量** — 作为最后手段，使用 `ANTHROPIC_API_KEY` 或 `OPENAI_API_KEY`  

> **如果您不希望向导读取您的认证配置文件**，请在环境中设置 `ANTHROPIC_API_KEY`，并确保默认认证模式为 `api-key` — 在这种情况下，步骤 2 将被完全跳过。  

### 外部 API 调用

`agents.wizard` 会向以下地址发送一个 HTTP POST 请求：  
- `https://api.anthropic.com/v1/messages`（Anthropic 模型）  
- `https://api.openai.com/v1/chat/completions`（OpenAI 兼容模型）  

没有其他出站请求。请求中仅包含用户提供的描述信息，不包含来自您系统的其他数据。  

### 补丁范围

这些补丁仅修改与代理相关的文件：  

| 补丁 | 被修改的文件 | 修改内容 |
|---|---|---|
| `schema-agents.txt` | `src/gateway/protocol/schema/agents-models-skills.ts` | 在 `AgentsUpdateParamsSchema` 中添加了 `emoji` 可选参数 |
| `server-agents.txt` | `src/gateway/server-methods/agents.ts` | 添加了 `agents.wizard` RPC；修复了 `agents.update` 方法，使其写入 `- Emoji:`（而不是 `- Avatar:`），以确保表情符号编辑能够正确保存 |
| `app-main.txt` | `ui/src/ui/app.ts` | 添加了 19 个 `@state()` 字段：10 个用于创建代理/向导操作，9 个用于编辑和删除代理操作 |
| `app-render.txt` | `ui/src/ui/app-render.ts` | 更新了创建/向导操作的属性处理逻辑；保存时发送 `emoji` 参数；保存后会清除身份缓存 |
| `app-render-helpers.txt` | `ui/src/ui/app-renderhelpers.ts` | 聊天界面头部添加了代理选择下拉菜单（使用 `resolveAgentEmoji()` 函数选择正确的表情符号）；添加了按代理会话过滤功能；新增了“新建会话”按钮 |
| `agents-view.txt` | `ui/src/ui/views/agents.ts` | 创建代理的面板（包含手动和 AI 向导模式；添加了表情符号选择器）；可以直接编辑代理信息；添加了删除代理的确认对话框 |
| `agents-utils.txt` | `ui/src/ui/views/agents-utils.ts` | 为多选功能修改了 `buildModelOptionsMulti()` 函数 |
| `agents-panels-cron.txt` | `ui/src/ui/views/agents-panels-status-files.ts` | 定时任务卡上的调度器卡片现在显示特定代理的任务数量和下次唤醒时间（而非全局网关统计信息） |

每个补丁都针对单一功能进行修改。如果某个补丁修改了上述文件之外的内容，请停止操作——您使用的可能是过时的版本。  

### LLM 输出验证

向导模型的输出在使用前会被解析为 JSON 并进行验证：  
- 必须是一个包含 `name`（字符串）、`emoji`（字符串）和 `soul`（字符串）的 JSON 对象；  
- `name` 的长度限制为 100 个字符，`emoji` 的长度限制为 10 个字符；  
- `soul` 的长度必须大于等于 20 个字符；  
- 如果返回空值或非 JSON 格式的内容，系统会显示用户可见的错误信息，并且不会自动创建任何内容。  

### 源代码修改

此技能需要使用 `git apply` 命令将补丁应用到 `~/openclaw` 目录中，并且需要对用户界面和网关进行重新构建。修改内容是永久性的。**应用补丁之前，请务必备份**：  

---

## 该技能新增的功能  

### 1. 聊天界面头部中的代理选择下拉菜单  
当配置了多个代理时，聊天界面头部会显示一个下拉菜单，位于会话选择下拉菜单的左侧。选择某个代理后，系统会切换到该代理的最新会话（如果没有找到该代理，则会使用该代理的新 Webchat 密钥）。会话选择下拉菜单会自动过滤，仅显示属于所选代理的会话。  

### 2. 按代理会话过滤（最新会话优先显示）  
现在会话信息仅限于当前激活的代理，并按最新顺序显示。不会再将其他代理的定时任务和子代理的会话信息混入当前会话选择列表中。  

### 3. 聊天界面头部中的“新建会话”按钮  
会话选择下拉菜单右侧新增了一个“+”图标按钮，用户可以点击该按钮直接创建新会话，而无需输入 `/new` 命令。  

### 4. 创建代理的面板（手动和 AI 向导模式）  
“代理”选项卡新增了一个“+ 创建代理”按钮，点击该按钮会弹出一个面板，提供两种创建代理的模式：  

**手动模式：**  
- 代理名称  
- 工作区路径（如果未输入名称，系统会自动生成）  
- 表情符号选择器  

**AI 向导模式：**  
- 用简单的英语描述代理；  
- 点击“生成代理”后，AI 会生成代理的名称、表情符号和完整的 `SOUL.md` 文件；  
- 查看预览后，点击“✅ 创建此代理”。  

创建代理后，代理列表和配置表单会自动更新——不会出现“未在配置中找到”的错误，也不需要手动重新加载页面。  

### 5. 表情符号选择下拉菜单  
“创建代理”和“编辑代理”表单中的表情符号字段是一个下拉菜单，包含 103 个精选的表情符号，这些表情符号分为 5 个类别（科技与 AI、人物与角色、动物与自然、物体与符号）。下拉菜单旁边会显示所选表情符号的实时预览图。  

### 6. 直接编辑代理信息（代理概览页面）  
代理概览页面现在可以直接编辑代理信息：  
- **名称**、**表情符号**（下拉菜单，包含 103 个表情符号）和 **工作区** 都可以随时编辑；  
- 修改后，底部的“保存”按钮会被激活；没有单独的“保存/取消”按钮；  
- 表情符号会以 `- Emoji:` 的格式保存到 `IDENTITY.md` 文件中（后续操作会覆盖创建时的默认值）；保存后会清除身份缓存，使更改立即生效；  
- 编辑操作使用 `agents.update` 方法中的 `emoji` 参数（而不是 `avatar` 参数），以确保正确的 `IDENTITY.md` 文件内容被写入。  

### 7. 删除代理  
对于非默认代理，代理概览页面的顶部会显示一个 🗑️ “删除”按钮；删除操作前会显示确认对话框；默认代理则没有此按钮。  

### 8. 代理特定的定时任务统计信息  
“定时任务”卡上的调度器卡片现在会显示特定代理的任务数量和下次唤醒时间（如果没有任务，则显示 “n/a”）。  

### 9. “代理”选项卡——模型选择功能改进  
- 删除了概览表格中多余的只读“主要模型”行（该信息可以在下方的模型选择部分直接编辑）；  
- “备用模型”选择方式从原来的自由文本输入方式改为使用与主要模型选择器相同的模型目录的多选下拉菜单；  
- 在主要模型选择字段和备用模型选择字段之间添加了分隔符和清晰的标签；  
- 备用模型选择器上添加了提示信息：“按 Ctrl/⌘ 键可以选择多个模型”。  

### 10. 后端接口（`agents.create` / `agents.update` / `agents.delete` / `agents.wizard`）  
新增了后端接口处理逻辑：  

| 方法 | 描述 |
|--------|-------------|
| `agents.create` | 在配置中添加新的代理条目，并创建相应的工作区文件（`SOUL.md`、`AGENTS.md`、`USER.md`）；  
| `agents.update` | 修改代理的配置信息（名称、工作区、模型、身份等）；  
| `agents.delete` | 从配置中删除代理；  
| `agents.wizard` | 调用配置的 LLM 生成代理的名称、表情符号和 `SOUL.md` 文件。  

**`agents.wizard` 中的认证修复**：直接调用模型 API 时需要 `api_key` 令牌，而不是 OAuth 或 bearer 令牌。当默认的认证模式为 `oauth` 或 `token` 时，向导会使用明确的 `api_key` 配置文件或 `ANTHROPIC_API_KEY` 环境变量。  

---

## 修改的文件  

| 文件 | 修改内容 |
|------|--------|
| `src/gateway/protocol/schema/agents-models-skills.ts` | 在 `AgentsUpdateParamsSchema` 中添加了 `emoji` 可选参数； |
| `src/gateway/server-methods/agents.ts` | 添加了 `agents.wizard` RPC；修复了 `agents.update` 方法，使其写入 `- Emoji:`（而不是 `- Avatar:`）； |
| `ui/src/ui/app-renderhelpers.ts` | 聊天界面中的代理选择下拉菜单（使用 `resolveAgentEmoji()` 函数）；添加了按代理会话过滤功能；新增了“新建会话”按钮； |
| `ui/src/ui/views/agents.ts` | 创建代理的面板；添加了表情符号选择器；修改了编辑和删除代理的界面； |
| `ui/src/ui/views/agents-utils.ts` | 为多选功能修改了 `buildModelOptionsMulti()` 函数； |
| `ui/src/ui/views/agents-panels-status-files.ts` | 定时任务卡上的调度器卡片现在显示特定代理的任务数量和下次唤醒时间； |
| `ui/src/ui/app-render.ts` | 更新了创建/向导操作的属性处理逻辑；保存时会清除缓存； |
| `ui/src/ui/app.ts` | 添加了 19 个 `@state()` 字段：10 个用于创建/向导操作，9 个用于编辑和删除代理操作； |

---

## 安装步骤  

应用此技能需要更新 OpenClaw 的源代码文件，并对用户界面和网关进行重新构建。  

### 先决条件  
- 确保 `~/openclaw` 目录中包含 OpenClaw 的源代码（可以是分支版本或本地克隆的版本）；  
- 安装 `pnpm`（通过 `npm install -g pnpm` 安装）；  
- 确保 Node.js 版本在 20.0 以上。  

### 安装步骤：  

### 第 1 步：应用补丁  
```bash
cd ~/openclaw

git apply ~/.openclaw/workspace/skills/agent-chat-ux/references/schema-agents.txt
git apply ~/.openclaw/workspace/skills/agent-chat-ux/references/agents-view.txt
git apply ~/.openclaw/workspace/skills/agent-chat-ux/references/agents-utils.txt
git apply ~/.openclaw/workspace/skills/agent-chat-ux/references/agents-panels-cron.txt
git apply ~/.openclaw/workspace/skills/agent-chat-ux/references/app-render-helpers.txt
git apply ~/.openclaw/workspace/skills/agent-chat-ux/references/app-render.txt
git apply ~/.openclaw/workspace/skills/agent-chat-ux/references/app-main.txt
git apply ~/.openclaw/workspace/skills/agent-chat-ux/references/server-agents.txt
```  

如果由于上游代码的变动导致某些补丁无法应用，请手动逐行执行补丁文件中的指令。  

### 第 2 步：重新构建用户界面  
```bash
cd ~/openclaw
pnpm ui:build
```  

### 第 3 步：重新构建网关（用于后端代理接口）  
```bash
cd ~/openclaw
pnpm build
```  

### 第 4 步：重启网关  
```bash
openclaw gateway restart
```  

### 第 5 步：验证效果  
1. 打开 `http://localhost:18789` 进入控制界面；  
2. 在“聊天”选项卡中，会看到会话选择下拉菜单左侧出现了代理选择下拉菜单（如果配置了多个代理）；会话选择下拉菜单右侧出现了“+”按钮；  
3. 在“代理”选项卡中，可以看到“+ 创建代理”按钮；  
4. 点击“创建代理”按钮后，系统会生成新的代理并显示在代理列表中，不会出现“未在配置中找到”的错误；  
5. 在“代理”选项卡的“概览”页面中，名称、表情符号和工作区都可以直接编辑；任何更改都会立即保存；  
6. 更改代理的表情符号后，更改会立即生效（不会恢复到创建时的默认值）；  
7. 在“代理”选项卡的“定时任务”页面中，没有定时任务的代理会显示“任务数量：0”/“下次唤醒：n/a”。  

---

## 使用说明  

### 聊天界面：切换代理和会话  
- **代理选择下拉菜单**：用于选择代理；会话列表会更新为仅显示所选代理的会话；  
- **会话选择下拉菜单**：可以在已选代理的现有会话之间切换；  
- “+”按钮：用于为当前代理创建新会话（功能与 `/new` 命令相同）。  

### 创建代理  
1. 点击“+ 创建代理”按钮；  
2. 在“手动”模式下，输入代理名称和工作区路径，然后选择表情符号；  
3. 在“AI 向导”模式下，描述代理的特征；  
4. 点击“生成代理”后，系统会生成代理的名称、表情符号和 `SOUL.md` 文件；  
5. 查看预览后，点击“✅ 创建此代理”。  

### 代理设置  
- 在“代理”选项卡的“模型选择”部分，可以选择备用模型：  
  - **主要模型**：单选下拉菜单；  
  - **备用模型**：多选下拉菜单（按 Ctrl/⌘ 键选择多个模型）；如果主要模型失败，系统会依次尝试备用模型（例如由于速率限制或上下文超出等原因）。  

## 架构说明  

### 会话键格式  
`agent:<agentId>:<rest>` — 代理选择机制通过 `parseAgentSessionKey(state.sessionKey).agentId` 来确定当前激活的代理，并据此过滤会话列表。  

### 创建代理后的配置更新  
`agents.create` 操作成功后，用户界面会同时调用 `agents.list`（更新侧边栏）和 `loadConfig`（刷新配置表单）。如果没有调用 `loadConfig`，选择新代理时可能会显示“未在配置中找到”的错误，因为配置表单中的信息已经过时。  

### 向导的认证处理  
`agents.wizard` 会直接调用模型提供者的 API。直接调用 API 时需要 `api_key` 类型的凭证；认证顺序如下：  
1. 如果配置模式为 `api-key`，则使用默认的 `resolveApiKeyForProvider` 结果；  
2. 在认证配置文件中查找第一个 `api_key` 类型的配置文件；  
3. 使用 `ANTHROPIC_API_KEY` 或 `OPENAI_API_KEY` 环境变量。  

这种处理方式与 `enhanced-loop-hook.ts` 中的逻辑相同。  

### 备用模型  
备用模型存储在代理配置的 `model.fallbacks` 数组中。当主要模型返回错误时，运行时系统会通过 `runWithModelFallback()` 函数尝试使用备用模型。  

## 更新日志  

### 1.3.0 (2026-02-19)  
- 新增功能：可以直接编辑代理的名称、表情符号和工作区；任何更改都会立即保存；没有单独的“保存/取消”按钮；  
- 新增功能：删除代理时会出现确认对话框；默认代理没有此按钮；  
- 新增功能：定时任务卡上的调度器卡片现在显示特定代理的任务数量和下次唤醒时间；  
- 修复问题：保存后表情符号会保持修改后的值；`agents.update` 方法现在接受 `emoji` 参数，并将表情符号保存为 `- Emoji:`；  
- 修复问题：更新了 `AgentsUpdateParamsSchema` 文件；现在 `AgentsUpdateParamsSchema` 包含了 `emoji` 可选参数；  
- 修复问题：保存代理后会立即清除身份缓存，使更改立即显示；  
- 修复问题：聊天界面中的表情符号选择下拉菜单现在使用 `resolveAgentEmoji()` 函数正确获取 `IDENTITY.md` 文件中的表情符号；  
- 扩展了表情符号的数量，从 60 个增加到 103 个，覆盖了 5 个类别。  

### 1.2.1 (2026-02-19)  
- 修复关键问题：从 `app-render.txt` 中移除了与本技能无关的属性和代码；这些内容会导致 TypeScript 错误和运行时崩溃；  
- 修复问题：移除了 `app-render.txt` 中未使用的导入语句；  
- 修复问题：将代理创建处理函数中的类型断言替换为明确的类型声明（`{ ok?: boolean; error?: string } | null`）。  

### 1.2.0 (2026-02-19)  
- 添加了关于安全性和透明度的说明；  
- 明确指定了 `ANTHROPIC_API_KEY`/`OPENAI_API_KEY` 作为可选的环境变量；  
- 修复问题：从 `app-main.txt` 中移除了与本技能无关的状态字段；  
- 加强了安全性：`agents.wizard` 在接受模型输出前会进行结构验证，拒绝非对象格式、缺少字段或空字符串的输入；  
- 修复问题：限制了 `name` 和 `emoji` 的长度；  
- 添加了关于认证配置读取、外部 API 调用和源代码补丁的说明。  

### 1.1.0 (2026-02-18)  
- 修复问题：AI 向导在请求 API 时使用了错误的令牌类型；现在会使用 `api_key` 配置文件或环境变量；  
- 修复问题：创建代理后会出现“未在配置中找到”的错误；现在在手动和 AI 向导模式下，`agents.create` 操作后都会调用 `loadConfig` 函数；  
- 新增功能：表情符号选择下拉菜单（包含 60 个表情符号，分为 5 个类别）；  
- 更新了所有补丁内容。  

### 1.0.0 (2026-02-18)  
- 首次发布版本：  
- 聊天界面头部添加了代理选择下拉菜单；  
- 按代理会话过滤功能；  
- 聊天界面头部新增了“新建会话”按钮；  
- 添加了创建代理的面板（包含手动和 AI 向导模式）；  
- 代理设置页面增加了备用模型多选功能；  
- 删除了代理概览页面中重复的“主要模型”显示；  
- 更新了后端接口（`agents.create` / `agents.update` / `agents.delete` / `agents.wizard`）。