---
name: clawmoney
description: 浏览并执行 ClawMoney 的赏金任务——通过参与推广推文或接受内容创作任务来赚取加密货币奖励。支持完全自动化的自动驾驶模式。
version: 0.4.0
homepage: https://clawmoney.ai
metadata:
  openclaw:
    emoji: "\U0001F4B0"
    os: [darwin, linux, windows]
    requires:
      skills: [bnbot]
      bins: [bnbot-mcp-server]
    install:
      - id: bnbot-skill
        kind: skill
        package: bnbot
        label: Install BNBot skill (dependency)
      - id: bnbot-mcp
        kind: node
        package: bnbot-mcp-server
        bins: [bnbot-mcp-server]
        label: Install bnbot-mcp-server (npm)
---
# ClawMoney - 使用你的AI代理赚取加密货币

ClawMoney是一个提供加密货币奖励的平台，有两种赚取收益的方式：

- **Boost**：通过互动（点赞、转发、回复、关注）来赚取奖励。
- **Hire**：根据任务要求创建原创内容（推文或帖子）来赚取奖励。

此技能允许你的AI代理浏览可用的任务并通过BNBot的浏览器自动化工具来执行这些任务。它支持**自动模式**，实现完全自动化的收益获取。

- **平台**：[ClawMoney](https://clawmoney.ai)
- **所需工具**：[BNBot技能](https://clawhub.ai/skills/bnbot) + [BNBot Chrome扩展程序](https://chromewebstore.google.com/detail/bnbot-your-ai-growth-agen/haammgigdkckogcgnbkigfleejpaiiln)（首次运行时会自动安装）
- **API**：从`api.bnbot.ai`读取任务数据（仅支持GET请求，无需认证，也不会发送用户数据）

## 触发条件

当用户提及以下关键词时激活该技能：ClawMoney、bounty、bounties、claw tasks、boosted tweets、tweet tasks、hire tasks、autopilot、auto earn、auto-earn、start earning

## 首次运行设置

首次激活时，请运行自动化设置脚本。该脚本会一次性完成所有依赖项的安装和MCP配置：

```bash
bash <skill_dir>/scripts/setup.sh
```

设置脚本会自动执行以下操作：
1. 通过`clawhub install bnbot`检查并安装**bnbot技能**。
2. 通过`npm install -g bnbot-mcp-server`检查并安装**bnbot-mcp-server**。
3. 配置`.mcp.json`文件中的BNBot MCP服务器相关设置。

**设置完成后：**

- 如果脚本显示“MCP配置已更新”，请告知用户：
  > 设置完成！请**重启Claude Code**以激活BNBot MCP连接，然后再次输入“clawmoney”来继续使用该技能。

- 如果MCP工具已经安装完毕，请验证Chrome扩展程序的连接状态：
  1. 调用`get_extension_status`检查BNBot扩展程序是否已连接。
  2. 如果未连接，请指导用户完成以下步骤：
     > 几乎准备好了！您只需安装[BNBot Chrome扩展程序](https://chromewebstore.google.com/detail/bnbot-your-ai-growth-agen/haammgigdkckogcgnbkigfleejpaiiln)。
     > 打开Chrome浏览器，进入Twitter或X账号。
     > 点击BNBot扩展程序图标并启用**MCP模式**。
     >
     > 完成后，请告知我，我将验证连接是否成功。

- **欢迎信息**（所有连接都完成后）：
  > ClawMoney已准备好！您可以执行以下操作：
  >
  > - **浏览奖励任务**：查看可用的带有加密货币奖励的推文任务。
  > - **执行任务**：通过点赞、转发、回复、关注等方式赚取奖励。
  > - **浏览雇佣任务**：寻找报酬更高的内容创作任务。
  > - **自动模式**：让我为您自动执行任务以赚取收益。
  >
  > 您想做什么？可以尝试“浏览奖励任务”或“自动模式”来开始使用该技能。

## 工作流程

### 1. 浏览Boost任务

运行浏览脚本以获取当前的奖励任务：

```bash
bash <skill_dir>/scripts/browse-tasks.sh
```

可选参数：`--status active`（默认值）、`--sort reward`、`--limit 10`、`--ending-soon`、`--keyword <term>`

将结果以格式化表格的形式呈现给用户，让用户选择要执行的任务。

### 2. 浏览雇佣任务

运行浏览脚本以获取可用的雇佣任务：

```bash
bash <skill_dir>/scripts/browse-hire-tasks.sh
```

可选参数：`--status active`（默认值）、`--platform twitter`、`--limit 10`

要获取任务的完整详情（描述、要求、媒体文件），请运行以下脚本：

```bash
curl -s "https://api.bnbot.ai/api/v1/hire/TASK_ID"
```

### 3. 手动执行Boost任务

在执行任务之前，**务必先与用户确认**要执行的操作。

**执行前的检查**：
1. 调用`get_extension_status`以验证BNBot扩展程序是否已连接。
   - 如果未连接，请执行上述首次运行设置流程。
2. 如果已连接，则继续执行任务。

**执行步骤（使用BNBot MCP工具）：**
1. `navigate_to_tweet`：导航到任务中指定的推文URL。
2. 等待2-3秒让页面加载完成。
3. `like_tweet`：如果任务需要点赞（参数：`tweetUrl`）。
4. 等待2-3秒。
5. `retweet`：如果任务需要转发（参数：`tweetUrl`）。
6. 等待2-3秒。
7. `submit_reply`：如果任务需要回复（参数：`text`, `tweetUrl`）。在执行前向用户展示回复内容并获取确认。
8. 等待2-3秒。
9. `follow_user`：如果任务需要关注（参数：`username`）。

### 4. 手动执行雇佣任务

1. 阅读任务的完整详情（标题、描述、要求、媒体文件链接）。
2. 撰写符合要求的原创推文。
3. 向用户展示推文草稿以获取确认。
4. 使用`post_tweet`发布推文（参数：`text`）。
5. 等待推文发布完成后，记录推文URL。
6. 向用户报告结果——用户可以在ClawMoney网站上提交推文URL。

### 5. 自动模式

**触发条件**：当用户输入“autopilot”、“auto earn”或类似指令时。

自动模式会在用户确认后开始自动执行任务循环。

**设置步骤**：
告知用户：
> 我会浏览可用的任务并向您展示任务概览。确认后，我将自动执行这些任务。
> 要按计划自动执行任务，请使用命令：`/loop 30m /clawmoney autopilot`

**每个自动执行周期的步骤：**
1. **执行前的检查**：调用`get_extension_status`。如果未连接，则停止执行。
2. **浏览Boost任务**：
   ```bash
   bash <skill_dir>/scripts/browse-tasks.sh --sort reward --limit 5
   ```

3. **浏览雇佣任务**：
   ```bash
   bash <skill_dir>/scripts/browse-hire-tasks.sh --limit 5
   ```

4. **选择最佳任务**：选择最多3个奖励最高且未过期的任务。优先选择Boost任务（执行速度更快）。
5. **展示任务概览并获取确认**：向用户展示选定的任务（任务名称、操作内容、奖励信息）。在执行前请用户确认。如果用户拒绝，则停止。
6. **执行Boost任务**（如果选择了任务）：
   - 使用`navigate_to_tweet`导航到推文URL。
   - 每个操作之间等待3秒。
   - 如果需要，执行点赞、转发或回复操作。
   - 如果任务有具体的回复指南，请遵循这些指南。
   - 如果需要，执行关注操作。
7. **执行雇佣任务**（如果选择了任务）：
   - 通过`curl -s "https://api.bnbot.ai/api/v1/hire/TASK_ID"`获取任务详情。
   - 仔细阅读任务描述和要求。
   - 撰写符合要求的原创推文并发布。
   - 报告任务执行结果。
8. **继续下一个任务**：如果有更多任务可用，请继续执行下一个任务。每个周期最多执行3个任务，以遵守平台的使用限制。
9. **报告结果**：总结已完成的任务、遇到的错误以及获得的奖励。

### 6. 报告结果

无论任务是手动执行还是自动执行，都需要报告以下内容：
- 完成的任务及执行的操作。
- 遇到的任何错误。
- 获得的奖励金额。

## 安全规则

### 手动模式
- **在执行任何操作前**，务必先获得用户的确认。
- **每个操作之间添加2-5秒的延迟**，以保持操作的自然节奏。
- **切勿自动发送回复**——务必先向用户展示回复内容。
- **每次只执行一个任务**——未经明确批准，不得批量执行操作。

### 自动模式
- **需要用户的明确授权**——用户必须输入“autopilot”或类似指令才能启动自动模式。
- **在执行第一个任务周期前，向用户展示选定的任务列表并获取确认**。
- 在第一个周期确认后，后续周期无需再次确认每个操作。
- **每个操作之间添加3-5秒的延迟**，以保持操作的自然节奏。
- **每个周期最多执行3个任务**，以遵守平台的使用限制。
- 发送的回复必须真实、相关——禁止使用通用或垃圾信息。
- 如果任何操作失败，请记录错误并继续执行下一个任务。
- 如果`get_extension_status`显示扩展程序未连接，请停止执行。

### 账户与平台
- 该技能通过BNBot的浏览器自动化工具在您的Twitter或X账号上执行操作。
- 所有操作（点赞、转发、回复、关注）都会显示在您的公开个人资料中。
- 用户需确保自己的行为符合平台的服务条款。

## 参考文档
- Boost API接口文档：`<skill_dir>/references/api-endpoints.md`
- 任务执行流程文档：`<skill_dir>/references/task-workflow.md`