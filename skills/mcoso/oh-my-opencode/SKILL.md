---
name: oh-my-opencode
description: OpenCode的多代理编排插件：适用于用户需要安装、配置或操作oh-my-opencode的场景，包括代理委托、超工作模式（ultrawork mode）、Prometheus监控计划、后台任务处理、基于类别的任务路由、模型解析（model resolution）、tmux集成等功能。该插件涵盖了安装、配置过程，以及所有类型的代理（如Sisyphus、Oracle、Librarian、Explore、Atlas、Prometheus、Metis、Momus）和所有类别的任务管理。同时，还提供了对相关命令（slash commands）、钩子（hooks）、技能（skills）、MCPs（Management Control Panels）的详细说明，并提供了故障排除（troubleshooting）的指导。
metadata:
  clawdbot:
    emoji: "🏔️"
    homepage: "https://github.com/code-yeongyu/oh-my-opencode"
    requires:
      bins: ["opencode"]
---

# Oh My OpenCode

这是一个多代理编排插件，它可以将 OpenCode 转换为一个功能齐全的代理系统，支持专用代理、后台任务执行、基于类别的任务路由以及自主工作模式。

**包名**: `oh-my-opencode`（通过 `bunx oh-my-opencode install` 安装）  
**仓库**: https://github.com/code-yeongyu/oh-my-opencode  
**模式定义**: https://raw.githubusercontent.com/code-yeongyu/oh-my-opencode/master/assets/oh-my-opencode.schema.json  

---

## 先决条件

1. **已安装并配置了 OpenCode**（`opencode --version` 应显示 1.0.150 或更高版本）  
2. 至少有一个经过身份验证的 LLM 提供商（使用 `opencode auth login` 进行登录）  
**强烈推荐**: 订阅 Anthropic 的 Claude Pro/Max 订阅服务（Sisyphus 使用的是 Claude Opus 4.5 版本）  

---

## 安装

运行交互式安装程序：  
（安装步骤在此处省略）

非交互式安装（使用提供商参数）：  
（安装步骤在此处省略）

安装完成后，请进行验证：  
（验证步骤在此处省略）  

---

## 两种工作模式

### 模式 1：Ultrawork（快速自主工作）

在命令提示符中输入 `ultrawork` 或 `ulw` 即可。  

代理将自动执行以下操作：  
1. 浏览你的代码库以了解现有模式；  
2. 通过专用代理研究最佳实践；  
3. 根据你的规范实现功能；  
4. 通过诊断和测试进行验证；  
5. 持续工作直至任务 100% 完成。  

### 模式 2：Prometheus（精确规划的工作）

对于复杂或关键任务：  
1. 按下 Tab 键切换到 Prometheus（规划器）模式；  
2. 描述你的工作内容，Prometheus 会通过分析代码库来提出问题；  
3. 确认计划内容（计划文件位于 `.sisyphus/plans/*.md`）；  
4. 运行 `/start-work` 命令，Atlas 编排器将接管任务：  
   - 将任务分配给专用子代理；  
   - 独立验证每个任务的完成情况；  
   - 收集任务中的学习成果；  
   - 跟踪任务进度（可随时恢复会话）。  

**重要规则**：**切勿在没有运行 `/start-work` 的情况下使用 Atlas**。Prometheus 和 Atlas 必须一起使用。  

---

## 代理

所有代理默认都是启用的。每个代理都有默认模型和提供商优先级链。  

| 代理 | 角色 | 默认模型 | 提供商优先级链 |  
|-------|------|---------------|------------------------|  
| **Sisyphus** | 主要编排器 | `claude-opus-4-5` | anthropic → kimi-for-coding → zai-coding-plan → openai → google |  
| **Sisyphus-Junior** | 专注任务执行器（用于分类任务） | 根据任务类别选择模型 | 按类别分配模型 |  
| **Hephaestus** | 自主深度工作代理 | `gpt-5.2-codex`（中等难度） | openai → github-copilot → opencode（需要 gpt-5.2-codex） |  
| **Oracle** | 用于架构设计、调试和高智商推理（仅读） | `gpt-5.2` | openai → google → anthropic |  
| **Librarian** | 提供官方文档、开源代码库搜索和远程代码库分析 | `glm-4.7` | zai-coding-plan → opencode → anthropic |  
| **Explore** | 快速代码库搜索工具 | `claude-haiku-4-5` | anthropic → github-copilot → opencode |  
| **Multimodal Looker** | 图像/PDF/图表分析工具 | `gemini-3-flash` | google → openai → zai-coding-plan → kimi-for-coding → anthropic |  
| **Prometheus** | 基于对话的规划工具 | `claude-opus-4-5` | anthropic → kimi-for-coding → openai → google |  
| **Metis** | 预规划顾问（用于分析歧义和失败点） | `claude-opus-4-5` | anthropic → kimi-for-coding → openai → google |  
| **Momus** | 计划审核工具 | `gpt-5.2` | openai → anthropic → google |  
| **Atlas** | 通过 `/start-work` 执行计划工具 | `k2p5` / `claude-sonnet-4-5` | kimi-for-coding → opencode → anthropic → openai → google |  
| **OpenCode-Builder** | 默认构建代理（当 Sisyphus 活动时禁用） | 系统默认设置 | 系统默认设置 |  

### 代理调用

代理通过 `delegate_task()` 或 `--agent` CLI 参数调用（**不要使用 `@` 前缀**）。  

---

## 如何选择合适的代理

| 任务类型 | 推荐代理 |  
|---------|-------|  
| 一般编码任务 | Sisyphus（默认） |  
| 自主目标导向的任务 | Hephaestus（需要 gpt-5.2-codex） |  
| 架构决策、多次失败后的调试 | Oracle |  
| 查找库文档、开源示例 | Librarian |  
| 在代码库中查找代码模式 | Explore |  
| 分析图像、PDF、图表 | Multimodal Looker |  
| 复杂的多日项目（需要规划） | Prometheus + Atlas（通过 Tab → `/start-work`） |  
| 预规划分析 | Metis |  
| 审查生成的计划 | Momus |  
| 快速的单文件修改 | 使用 `quick` 类别的 `delegate_task` |  

---

## 类别

通过 `delegate_task()`，类别会将任务路由到使用相应模型的 Sisyphus-Junior 代理。  

| 类别 | 默认模型 | 可选模型 | 提供商优先级链 | 适用场景 |  
|----------|---------------|---------|------------------------|----------|  
| `visual-engineering` | `gemini-3-pro` | — | google → anthropic → zai-coding-plan | 前端、UI/UX、设计、样式、动画 |  
| `ultrabrain` | `gpt-5.2-codex` | `xhigh` | openai → google → anthropic | 深度逻辑推理、复杂架构 |  
| `deep` | `gpt-5.2-codex` | `medium` | openai → anthropic | 目标导向的自主问题解决（类似 Hephaestus） |  
| `artistry` | `gemini-3-pro` | `max` | google → anthropic | 创意/非传统解决方案 |  
| `quick` | `claude-haiku-4-5` | — | anthropic → google → opencode | 简单任务、单文件修改、拼写校正 |  
| `unspecified-low` | `claude-sonnet-4-5` | — | anthropic → openai | 一般任务、低难度 |  
| `unspecified-high` | `claude-opus-4-5` | `max` | anthropic → openai | 一般任务、高难度 |  
| `writing` | `gemini-3-flash` | — | google → zai-coding-plan → openai | 文档编写、散文、技术写作 |  

### 类别的使用方法  

---

## 关键事项：模型选择优先级

除非另有配置，否则类别不会使用内置的默认模型。模型选择顺序如下：  
1. **用户配置的模型**（在 `oh-my-opencode.json` 中设置）——最高优先级；  
2. **类别内置的默认模型**（如果配置中存在）；  
3. **系统默认模型**（来自 `opencode.json`）。  
要使用最佳模型，请在配置文件中添加相应的类别。详情请参阅 [references/configuration.md]。  

---

## 内置技能

| 技能 | 用途 | 使用方法 |  
|-------|---------|-------|  
| `playwright` | 通过 Playwright MCP 实现浏览器自动化 | `load_skills=["playwright"]` |  
| `agent-browser` | Vercel 提供的浏览器自动化工具 | 通过 `browser_automation_engine` 配置切换浏览器 |  
| `git-master` | Git 专家工具：原子提交、合并/压缩、历史记录搜索 | `load_skills=["git-master"]` |  
| `frontend-ui-ux` | 专为设计师设计的开发工具 | `load_skills=["frontend-ui-ux"]` |  

技能可以通过 `delegate_task LOAD_skills=[...])` 注入到子代理中。  

---

## 命令行接口（CLI）命令

| 命令 | 说明 |  
|---------|-------------|  
| `/init-deep` | 初始化代理的知识库 |  
| `/start-work` | 通过 Atlas 编排器执行任务 |  
| `/ralph-loop` | 启动自循环开发模式 |  
| `/ulw-loop` | 启动 Ultrawork 循环 |  
| `/cancel-ralph` | 取消正在进行的循环 |  
| `/refactor` | 使用 LSP、AST 分析、架构分析和 TDD 进行智能重构 |  
| `/stop-continuation` | 停止所有持续执行机制 |  

---

## 进程管理

### 后台代理

可以并行启动多个代理进行探索和研究：  
（相关配置步骤在此处省略）  

### 并发配置  

优先级顺序：`modelConcurrency` > `providerConcurrency` > `defaultConcurrency`  

### Tmux 集成

可以在 tmux 窗口中分别运行后台代理，以实现多代理的可视化执行：  
（相关配置步骤在此处省略）  

### 注意事项：需要在服务器模式下运行 OpenCode，并在 tmux 会话中执行这些配置。  

### 布局选项

布局选项包括：`main-vertical`（默认）、`main-horizontal`、`tiled`、`even-horizontal`、`even-vertical`。  

---

## 并行执行模式

### 模式 1：Explore + Librarian（研究阶段）  
（相关步骤在此处省略）  

### 模式 2：基于类别的任务分配（实施阶段）  
（相关步骤在此处省略）  

### 模式 3：会话连续性  
（相关步骤在此处省略）  

---

## CLI 参考

### 核心命令  
（相关命令列表在此处省略）  

### 非交互式模式  
（相关配置步骤在此处省略）  

### 身份验证与提供商管理  
（相关配置步骤在此处省略）  

### 会话管理  
（相关配置步骤在此处省略）  

### 插件与 MCP 管理  
（相关配置步骤在此处省略）  

### 服务器模式  
（相关配置步骤在此处省略）  

## 内置的 MCP（模型控制程序）

Oh My OpenCode 默认包含以下 MCP 服务器：  
| MCP | 工具 | 用途 |  
|-----|------|---------|  
| **Exa** | `web_search_exa` | 提供简洁的 LLM 支持的网页搜索功能 |  
| **Context7** | `resolve-library-id`、`query-docs` | 查找官方库/框架的文档 |  
| **Grep.app` | `searchGitHub` | 从公共 GitHub 仓库中搜索代码示例 |  

## 钩子（Hooks）

所有钩子默认都是启用的。可以通过 `disabled_hooks` 配置来禁用特定钩子：  
| 钩子 | 用途 |  
|------|---------|  
| `todo-continuation-enforcer` | 强制代理在任务中途退出时继续执行 |  
| `context-window-monitor` | 监控和管理上下文窗口的使用 |  
| `session-recovery` | 在会话崩溃后恢复会话 |  
| `session-notification` | 会话事件发生时发送通知 |  
| `comment-checker` | 防止 AI 添加过多的代码注释 |  
| `grep-output-truncator` | 截断大型 grep 输出结果 |  
| `tool-output-truncator` | 截断大型工具的输出结果 |  
| `directory-agents-injector` | 从子目录中注入 AGENTS.md 文件（在 OpenCode 1.1.37 及更高版本中自动禁用） |  
| `directory-readme-injector` | 注入 README.md 文件的内容 |  
| `empty-task-response-detector` | 检测并处理空任务响应 |  
| `think-mode` | 控制扩展思维模式 |  
| `anthropic-context-window-limit-recovery` | 从 Anthropic 的上下文限制中恢复 |  
| `rules-injector` | 注入项目规则 |  
| `background-notification` | 在后台任务完成时发送通知 |  
| `auto-update-checker` | 检查 oh-my-opencode 的更新 |  
| `startup-toast` | 显示启动通知（自动更新功能的附加组件） |  
| `keyword-detector` | 检测触发模式的关键词（如 `ultrawork`/`ulw`） |  
| `agent-usage-reminder` | 提醒使用专用代理 |  
| `non-interactive-env` | 处理非交互式环境 |  
| `interactive-bash-session` | 管理交互式 bash/tmux 会话 |  
| `compaction-context-injector` | 在压缩过程中注入上下文信息 |  
| `thinking-block-validator` | 验证思维过程 |  
| `claude-code-hooks` | Claude 代码兼容性钩子 |  
| `ralph-loop` | Ralph 循环的继续执行机制 |  
| `preemptive-compaction` | 在上下文溢出前触发压缩 |  
| `auto-slash-command` | 自动触发相关命令 |  
| `sisyphus-junior-notepad` | 为 Sisyphus-Junior 代理提供的记事本 |  
| `edit-error-recovery` | 从编辑错误中恢复 |  
| `delegate-task-retry` | 重试失败的任务委托 |  
| `prometheus-md-only` | 强制使用 Prometheus 的 Markdown 输出格式 |  
| `start-work` | 处理 `/start-work` 命令 |  
| `atlas` | Atlas 编排器的钩子 |  

---

## 最佳实践

- **对于快速自主任务，使用 `ulw`**——只需在命令提示符中输入关键词；  
- **对于复杂项目，使用 Prometheus 和 `/start-work`**——基于对话的规划能带来更好的结果；  
- **为各个提供商配置相应的类别**——确保选择最佳模型；  
- **并行运行 `Explore`/`Librarian` 代理**——始终设置 `run_in_background=true`；  
- **使用会话连续性**——在后续交互中传递 `session_id`；  
- **让代理负责任务执行**——Sisyphus 是一个编排器，而非单独的执行者；  
- **运行 `bunx oh-my-opencode doctor` 来诊断问题。**  

### 注意事项

- **切勿在没有运行 `/start-work` 的情况下使用 Atlas**；  
- **不要为每个代理手动指定模型**——系统会自动选择合适的模型；  
- **不要禁用 `todo-continuation-enforcer`——它确保代理完成任务；  
- **不要为 Sisyphus 使用 Claude Haiku**——强烈推荐使用 Opus 4.5；  
- **不要同时运行 `Explore`/`Librarian` 代理**——它们应在后台运行。  

### 适用场景

- 安装或配置 oh-my-opencode；  
- 了解代理的角色和任务分配机制；  
- 解决模型选择或提供商相关的问题；  
- 配置 tmux 集成以实现多代理的可视化执行；  
- 优化类别设置以提升效率；  
- 理解 Ultrawork 与 Prometheus 的工作流程差异。  

### 不适用场景

- 与 oh-my-opencode 插件无关的 OpenCode 使用场景；  
- 提供商身份验证问题（直接使用 `opencode auth`）；  
- OpenCode 的核心配置（请参考官方文档：https://opencode.ai/docs/）。  

---

## 规则说明

1. **包名必须是 `oh-my-opencode`，**而非 `@anthropics/opencode` 或其他名称；  
2. **推荐使用 `bunx` 命令行工具（官方推荐）；**  
3. **代理调用使用 `--agent` 参数或 `delegate_task()`；**  
4. **除非用户明确要求，否则不要更改模型设置或禁用功能；  
5. **强烈推荐使用 Opus 4.5**——使用其他模型会严重影响使用体验；  
6. **除非另有配置，否则类别不会使用内置的默认模型**——务必使用 `bunx oh-my-opencode doctor --verbose` 进行验证；  
7. **Prometheus 和 Atlas 必须一起使用**；  
8. **后台代理必须始终设置 `run_in_background=true`；**  
9. **会话 ID 应该被保留并重复使用**——可节省 70% 以上的资源；  
10. **在使用 Ollama 时，设置 `stream: false`——以避免 JSON 解析错误。**  

## 完成通知

后台任务完成后会自动通过 `background-notification` 钩子发送通知。无需手动轮询——系统会自动推送完成事件。只有在需要查看结果时，才使用 `background_output(task_id="...")` 命令。  

---

## 参考文档

- [配置参考](references/configuration.md)：包含所有代理、类别、提供商链、钩子和配置选项的完整配置信息；  
- [故障排除指南](references/troubleshooting.md)：常见问题及解决方法。