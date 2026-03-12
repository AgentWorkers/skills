---
name: clawsouls
description: 管理 OpenClaw 中的 AI 代理角色（“Souls”）。当用户需要安装、切换、列出或恢复 AI 角色时可以使用该功能。相关操作请求包括：“安装一个 AI 角色”、“切换角色”、“更改角色”、“列出所有可用角色”、“恢复我的旧角色”、“使用简约风格的角色”、“浏览所有可用角色”、“有哪些可用的角色”以及“登录到 ClawSouls 系统”。
---
# ClawSouls — 人工智能人格管理工具

用于管理定义人工智能代理的人格、行为和身份的“Soul”包。

“Soul”包采用 `owner/name` 的命名规范（例如：`clawsouls/surgical-coder`、`TomLeeLive/my-soul`）。

## 先决条件

确保 `clawsouls` 命令行工具（CLI）已安装：

```bash
npx clawsouls --version
```

如果尚未安装，请全局安装：

```bash
npm install -g clawsouls
```

当前版本：**v0.6.2**

## 命令

### 安装一个 Soul

```bash
npx clawsouls install clawsouls/surgical-coder
npx clawsouls install clawsouls/surgical-coder --force       # overwrite existing
npx clawsouls install clawsouls/surgical-coder@0.1.0         # specific version
```

共有 80 多个可供选择的 Soul 包。可在以下链接查看所有 Soul 包：https://clawsouls.ai

**官方提供的 Soul 包**（所有者：`clawsouls`）：
- **开发类**：code-reviewer（代码审核员）、coding-tutor（编程导师）、debug-detective（调试侦探）、api-architect（API 架构师）、ml-engineer（机器学习工程师）、sysadmin-sage（系统管理员专家）、devops-veteran（DevOps 专家）、gamedev-mentor（游戏开发导师）、prompt-engineer（提示引擎工程师）、frontend-dev（前端开发人员）、backend-dev（后端开发人员）、mobile-dev（移动应用开发人员）、cloud-architect（云架构师）、database-admin（数据库管理员）、qa-engineer（质量保证工程师）
- **写作与内容类**：tech-writer（技术作家）、storyteller（故事讲述者）、scifi-writer（科幻作家）、copywriter（文案撰写者）、content-creator（内容创作者）、journalist（记者）、poet（诗人）、screenwriter（编剧）、academic-writer（学术作家）
- **专业类**：data-analyst（数据分析师）、project-manager（项目经理）、legal-advisor（法律顾问）、startup-founder（初创企业创始人）、hr-manager（人力资源经理）、marketing-strategist（营销策略师）、sales-coach（销售教练）、product-manager（产品经理）
- **教育类**：math-tutor（数学辅导老师）、philosophy-prof（哲学教授）、mentor-coach（导师教练）、science-tutor（科学辅导老师）、history-prof（历史教授）、language-teacher（语言教师）、economics-tutor（经济学辅导老师）
- **创意类**：music-producer（音乐制作人）、ux-designer（用户体验设计师）、chef-master（厨师大师）、graphic-designer（平面设计师）、video-editor（视频编辑师）、podcast-host（播客主持人）、dungeon-master（游戏设计师）
- **生活方式类**：personal-assistant（个人助理）、fitness-coach（健身教练）、travel-guide（旅行向导）、life-coach（生活导师）、meditation-guide（冥想指导师）、nutrition-advisor（营养顾问）、productivity-guru（效率提升专家）、financial-planner（财务规划师）
- **科学类**：research-scientist（研究科学家）、data-scientist（数据科学家）
- **安全类**：security-auditor（安全审计员）
- **MBTI 类型**：mbti-intj、mbti-intp、mbti-entj、mbti-entp、mbti-infp、mbti-infp、mbti-enfj、mbti-enfp、mbti-istj、mbti-isfj、mbti-estj、mbti-esfj、mbti-istp、mbti-isfp、mbti-estp、mbti-esfp
- **特殊用途类**：surgical-coder（外科医生编码器）、korean-translator（韩语翻译器）
- **通用类**：brad（通用型人格）、minimalist（极简主义人格）

### 激活一个 Soul

```bash
npx clawsouls use clawsouls/surgical-coder
```

- 会自动备份当前工作区的文件（SOUL.md、IDENTITY.md、AGENTS.md、HEARTBEAT.md、STYLE.md 等）。
- 请勿覆盖 USER.md、MEMORY.md 或 TOOLS.md 文件。
- 激活后需要重启 `soulclaw` 代理才能生效。

### 恢复之前的 Soul

```bash
npx clawsouls restore
```

可以恢复到最近一次创建的备份。

### 列出已安装的 Soul

```bash
npx clawsouls list
```

以 `owner/name` 的格式显示已安装的 Soul 包。

### 创建一个新的 Soul

```bash
npx clawsouls init my-soul
```

会创建一个新的 Soul 目录，其中包含 `soul.json`、SOUL.md、IDENTITY.md、AGENTS.md、HEARTBEAT.md 和 README.md 文件。

### 导出一个 Soul

```bash
npx clawsouls export claude-md           # generate CLAUDE.md from current workspace soul files
npx clawsouls export system-prompt       # generate a system prompt string
```

将 SOUL.md、IDENTITY.md、AGENTS.md 和 HEARTBEAT.md 文件合并为一个文件。这适用于 Claude Code、Cursor、Windsurf 等需要统一配置文件的工具。

### 版本管理

```bash
npx clawsouls version bump patch    # 1.0.0 → 1.0.1
npx clawsouls version bump minor    # 1.0.0 → 1.1.0
npx clawsouls version bump major    # 1.0.0 → 2.0.0
npx clawsouls diff                  # colored diff of soul files
```

### Soul 测试（第 9 阶段）

```bash
npx clawsouls test                  # Level 1 (schema) + Level 2 (soulscan)
npx clawsouls test --level 3       # + Level 3 (behavioral LLM tests)
```

使用第 9 阶段功能时，需要在 Soul 目录中提供 `soul.test.yaml` 文件，并且需要连接 LLM（大型语言模型）服务（如 OpenAI、Anthropic 或 Ollama）。

### Doctor、Migrate、Search、Info、Update（第 10 阶段）

```bash
npx clawsouls doctor                # 12 environment checks
npx clawsouls migrate               # migrate soul from v0.3 → v0.4 → v0.5
npx clawsouls search "engineer"     # search souls from registry
npx clawsouls info clawsouls/brad  # show soul metadata
npx clawsouls update                # update installed soul to latest
```

### 验证一个 Soul

```bash
npx clawsouls validate ./my-soul/
npx clawsouls validate --soulscan ./my-soul/   # with SoulScan security analysis
npx clawsouls check ./my-soul/                 # alias
```

根据规范和所需文件进行验证。使用 `--soulscan` 选项可进行全面的安全性和质量分析（包含评分）。该验证会在发布前自动执行。

### SoulScan — 安全性与完整性扫描工具

```bash
npx clawsouls soulscan              # scan current OpenClaw workspace
npx clawsouls soulscan ./my-soul/   # scan a specific directory
npx clawsouls soulscan --init       # initialize baseline checksums
npx clawsouls soulscan -q           # quiet mode for cron (SOULSCAN_OK / SOULSCAN_ALERT)
npx clawsouls scan                  # alias
```

SoulScan 会检查活跃的 Soul 文件：
- **完整性**：通过 SHA-256 校验和来检测自上次扫描以来的篡改情况。
- **安全性**：进行 53 项安全检查（包括提示注入、代码执行、XSS 攻击、数据泄露、权限提升、社会工程学攻击、有害内容检测等）。
- **质量**：检查文件结构和内容长度是否符合规范。
- **人格一致性**：验证 SOUL.md、IDENTITY.md 和 soul.json 文件中的人格描述是否一致。

**Cron 定时任务** — 定期检测文件篡改情况：

```bash
# Run every hour to monitor workspace integrity
npx clawsouls soulscan -q
# Exit code 0 = OK, 1 = alert (tampered or security issue)
```

**首次运行**：使用 `--init` 命令建立基准校验和，不会触发警报。

SOULSCAN™ 的评分范围为 0-100 分：验证通过（90 分以上）/ 低风险（70 分以上）/ 中等风险（40 分以上）/ 高风险 / 被阻止。

### 发布一个 Soul

```bash
export CLAWSOULS_TOKEN=<token>
npx clawsouls publish ./my-soul/
```

自动将 Soul 发布到 `username/soul-name` 的命名空间。需要使用认证令牌。发布前会自动进行验证；验证失败会导致发布失败。

### 登录 / 获取令牌

```bash
npx clawsouls login
```

获取 API 令牌的步骤：登录 https://clawsouls.ai → 进入仪表板 → 生成 API 令牌。

## 工作流程

### 安装与切换人格

1. **浏览**：在 https://clawsouls.ai 上查看可用的 Soul 包，或从上面的分类列表中选择。
2. **安装**：使用 `npx clawsouls install clawsouls/surgical-coder` 命令进行安装。
3. **激活**：使用 `npx clawsouls use clawsouls/surgical-coder` 命令激活新人格。
4. **重启**：运行 `soulclaw gateway restart` 以应用新人格。
5. **开始新会话**：在聊天中发送 `/new` 命令以清除之前的会话记录。
6. **恢复**：如果需要恢复之前的配置，可以使用 `npx clawsouls restore` 命令。

### 发布一个 Soul

1. **登录**：使用 `npx clawsouls login` 登录。
2. **获取令牌**：从仪表板获取 API 令牌。
3. **创建新 Soul**：使用 `npx clawsouls init my-soul` 命令创建新 Soul。
4. **发布**：使用 `npx clawsouls publish ./my-soul/` 命令发布新 Soul。
5. **管理**：通过 https://clawsouls.ai/dashboard 进行管理（删除或查看下载文件）。

### 内存同步（集群模式）

```bash
npx clawsouls sync                  # sync encrypted memory to/from GitHub
npx clawsouls swarm                 # multi-agent memory branch & merge system
```

通过加密的 Git 在多台机器之间同步代理的内存数据。采用 `age` 加密技术来保护用户隐私。

### Soul 检查点（回滚功能）

```bash
npx clawsouls checkpoint            # manage soul checkpoints
npx clawsouls checkpoint create     # create a checkpoint of current soul state
npx clawsouls checkpoint list       # list available checkpoints
npx clawsouls checkpoint restore    # restore from a checkpoint
```

基于检查点进行回滚，用于检测和恢复人格配置的异常变化。

### 平台检测

```bash
npx clawsouls platform              # show detected agent platform(s) and workspace path
npx clawsouls detect                # alias
```

检测当前运行的代理平台（OpenClaw、SoulClaw、ZeroClaw 等），并显示相应的工作区路径。

## MCP 服务器（适用于 Claude Desktop / Cowork）

对于 Claude Desktop 或 Cowork 用户，还有一个专门的 MCP 服务器：

```bash
npx -y soul-spec-mcp
```

或者可以在 Claude Desktop 的配置文件（`claude_desktop_config.json`）中进行配置：

```json
{ "mcpServers": { "soul-spec": { "command": "npx", "args": ["-y", "soul-spec-mcp"] } } }
```

提供的工具包括：`search_souls`、`get_soul`、`install_soul`、`preview_soul`、`list_categories`、`apply_persona`。

GitHub 仓库：https://github.com/clawsouls/soul-spec-mcp

## 重要说明

- 使用新人格后，务必提醒用户运行 `soulclaw gateway restart`，然后执行 `/new` 命令以开始新的会话（之前的会话记录会保留旧的人格配置）。
- `use` 命令会自动创建备份，因此数据丢失的概率很低。
- Soul 包可能包含 STYLE.md 和 examples/ 文件，以便进一步自定义人格设置。
- 已发布的 Soul 包会显示在 https://clawsouls.ai/souls/owner/name 上。
- 用户可以对非自己拥有的 Soul 包进行评分（1-5 星）。
- 如需进行本地测试，可以设置环境变量 `CLAWSOULS_CDN=/path/to/souls`。
- 网站提供多种语言版本：英语、韩语、日语、中文、西班牙语（例如：`clawsouls.ai/ko/souls/...`）。
- 可以将 Soul 包分享给 OpenClaw 机器人；分享命令包含在相关文本中。
- **Soul 宣言**：请阅读官方宣言：https://clawsouls.ai/en/manifesto。
- **研究论文**：《Soul-Driven Interaction Design》：https://doi.org/10.5281/zenodo.18772585
- 法律声明：[隐私政策](https://clawsouls.ai/en/privacy) · [服务条款](https://clawsouls.ai/en/terms)