---
name: clawsouls
description: 管理 OpenClaw 的 AI 代理角色（“Souls”）。当用户需要安装、切换、列出或恢复 AI 角色时，可以使用此功能。相关操作请求包括：“安装一个角色”、“切换角色”、“更改角色”、“列出所有可用角色”、“恢复我的旧角色”、“使用极简风格的角色”、“浏览可用角色”、“有哪些角色可供选择”以及“登录到 clawsouls”等。
---
# ClawSouls — 人工智能人格管理工具

ClawSouls用于管理定义人工智能代理的人格、行为和身份的“Soul”包。

“Soul”包采用`owner/name`的命名规范（例如：`clawsouls/surgical-coder`、`TomLeeLive/my-soul`）。

## 先决条件

确保`clawsouls`命令行工具（CLI）已安装：

```bash
npx clawsouls --version
```

如果尚未安装，请全局安装：

```bash
npm install -g clawsouls
```

当前版本：**v0.6.0**

## 命令

### 安装一个Soul包

```bash
npx clawsouls install clawsouls/surgical-coder
npx clawsouls install clawsouls/surgical-coder --force       # overwrite existing
npx clawsouls install clawsouls/surgical-coder@0.1.0         # specific version
```

目前提供80多种Soul包，可在以下链接查看所有可用Soul包：https://clawsouls.ai

**官方提供的Soul包**（所有者：`clawsouls`）：
- **开发类**：code-reviewer（代码审核员）、coding-tutor（编程导师）、debug-detective（调试侦探）、api-architect（API架构师）、ml-engineer（机器学习工程师）、sysadmin-sage（系统管理员专家）、devops-veteran（DevOps资深专家）、gamedev-mentor（游戏开发导师）、prompt-engineer（提示引擎工程师）、frontend-dev（前端开发人员）、backend-dev（后端开发人员）、mobile-dev（移动开发人员）、cloud-architect（云架构师）、database-admin（数据库管理员）、qa-engineer（质量保证工程师）
- **写作与内容类**：tech-writer（技术作家）、storyteller（故事讲述者）、scifi-writer（科幻作家）、copywriter（文案撰写者）、content-creator（内容创作者）、journalist（记者）、poet（诗人）、screenwriter（编剧）、academic-writer（学术作家）
- **职业类**：data-analyst（数据分析师）、project-manager（项目经理）、legal-advisor（法律顾问）、startup-founder（初创企业创始人）、hr-manager（人力资源经理）、marketing-strategist（营销策略师）、sales-coach（销售教练）、product-manager（产品经理）
- **教育类**：math-tutor（数学辅导老师）、philosophy-prof（哲学教授）、mentor-coach（导师教练）、science-tutor（科学辅导老师）、history-prof（历史教授）、language-teacher（语言教师）、economics-tutor（经济学辅导老师）
- **创意类**：music-producer（音乐制作人）、ux-designer（用户体验设计师）、chef-master（厨师大师）、graphic-designer（平面设计师）、video-editor（视频编辑师）、podcast-host（播客主持人）、dungeon-master（游戏设计者）
- **生活类**：personal-assistant（个人助理）、fitness-coach（健身教练）、travel-guide（旅行向导）、life-coach（生活教练）、meditation-guide（冥想指导师）、nutrition-advisor（营养顾问）、productivity-guru（效率提升专家）、financial-planner（财务规划师）
- **科学类**：research-scientist（研究科学家）、data-scientist（数据科学家）
- **安全类**：security-auditor（安全审计师）
- **MBTI类型**：mbti-intj、mbti-intp、mbti-entj、mbti-entp、mbti-infp、mbti-infp、mbti-enfj、mbti-enfp、mbti-istj、mbti-isfj、mbti-estj、mbti-esfj、mbti-istp、mbti-isfp、mbti-estp、mbti-esfp
- **特殊类别**：surgical-coder（外科医生）、korean-translator（韩语翻译者）
- **通用类别**：brad、minimalist（极简主义者）

### 激活一个Soul包

```bash
npx clawsouls use clawsouls/surgical-coder
```

- 会自动备份当前的工作区文件（SOUL.md、IDENTITY.md、AGENTS.md、HEARTBEAT.md、STYLE.md、examples/）
- 绝不会覆盖USER.md、MEMORY.md或TOOLS.md文件
- 激活后需要重启`openclaw gateway`才能生效

### 恢复之前的Soul包

```bash
npx clawsouls restore
```

恢复由`use`命令创建的最新备份

### 列出已安装的Soul包

```bash
npx clawsouls list
```

以`owner/name`的格式显示已安装的Soul包

### 创建一个新的Soul包

```bash
npx clawsouls init my-soul
```

创建一个新的Soul包目录，包含`soul.json`、SOUL.md、IDENTITY.md、AGENTS.md、HEARTBEAT.md、README.md文件

### 导出一个Soul包

```bash
npx clawsouls export claude-md           # generate CLAUDE.md from current workspace soul files
npx clawsouls export system-prompt       # generate a system prompt string
```

将SOUL.md、IDENTITY.md、AGENTS.md、HEARTBEAT.md、STYLE.md文件合并为一个文件。此文件适用于Claude Code、Cursor、Windsurf等需要统一配置文件的工具

### 版本管理

```bash
npx clawsouls version bump patch    # 1.0.0 → 1.0.1
npx clawsouls version bump minor    # 1.0.0 → 1.1.0
npx clawsouls version bump major    # 1.0.0 → 2.0.0
npx clawsouls diff                  # colored diff of soul files
```

### Soul包测试（第9阶段）

```bash
npx clawsouls test                  # Level 1 (schema) + Level 2 (soulscan)
npx clawsouls test --level 3       # + Level 3 (behavioral LLM tests)
```

使用第3级Soul包时，需要在Soul包目录中提供`soul.test.yaml`文件，并且需要连接LLM提供商（如OpenAI/Anthropic/Ollama）

### Doctor、Migrate、Search、Info、Update（第10阶段）

```bash
npx clawsouls doctor                # 12 environment checks
npx clawsouls migrate               # migrate soul from v0.3 → v0.4 → v0.5
npx clawsouls search "engineer"     # search souls from registry
npx clawsouls info TomLeeLive/brad  # show soul metadata
npx clawsouls update                # update installed soul to latest
```

### 验证一个Soul包

```bash
npx clawsouls validate ./my-soul/
npx clawsouls validate --soulscan ./my-soul/   # with SoulScan security analysis
npx clawsouls check ./my-soul/                 # alias
```

根据规范和所需文件进行验证。使用`--soulscan`选项可进行全面的安全性和质量分析（包括评分）。该验证会在发布前自动执行

### SoulScan — 安全性与完整性扫描工具

```bash
npx clawsouls soulscan              # scan current OpenClaw workspace
npx clawsouls soulscan ./my-soul/   # scan a specific directory
npx clawsouls soulscan --init       # initialize baseline checksums
npx clawsouls soulscan -q           # quiet mode for cron (SOULSCAN_OK / SOULSCAN_ALERT)
npx clawsouls scan                  # alias
```

SoulScan会检查活跃的Soul包文件：
- **完整性**：通过SHA-256校验和来检测自上次扫描以来的篡改情况
- **安全性**：进行53项安全检查（包括提示注入、代码执行、XSS攻击、数据泄露、权限提升、社会工程攻击、有害内容检测等）
- **质量**：检查文件结构和内容长度，验证是否符合规范
- **人格一致性**：对比SOUL.md、IDENTITY.md和soul.json文件中的名称和语气是否一致

**Cron任务** — 定期检测篡改行为：
```bash
# Run every hour to monitor workspace integrity
npx clawsouls soulscan -q
# Exit code 0 = OK, 1 = alert (tampered or security issue)
```

**首次运行**：使用`--init`命令建立基准校验和，不会触发警报

SOULSCAN™评分范围：0-100分；等级划分：已验证（90分及以上）/ 低风险（70分及以上）/ 中等风险（40分及以上）/ 高风险 / 被阻止

### 发布一个Soul包

```bash
export CLAWSOULS_TOKEN=<token>
npx clawsouls publish ./my-soul/
```

自动将Soul包发布到`username/soul-name`命名空间。需要认证令牌。发布前会自动进行验证，验证失败时会阻止发布

### 登录 / 获取令牌

```bash
npx clawsouls login
```

获取API令牌的步骤：登录https://clawsouls.ai → 进入仪表板 → 生成API令牌

## 工作流程

### 安装与切换人格

1. **浏览**：在https://clawsouls.ai查看可用Soul包，或从上述分类列表中选择
2. **安装**：使用`npx clawsouls install clawsouls/surgical-coder`命令安装Soul包
3. **激活**：使用`npx clawsouls use clawsouls/surgical-coder`命令激活Soul包
4. **重启**：运行`openclaw gateway restart`以应用新的人格设置
5. **恢复**：如需恢复之前的设置，使用`npx clawsouls restore`命令

### 发布一个Soul包

1. **登录**：使用`npx clawsouls login`命令登录
2. **获取令牌**：从仪表板获取API令牌
3. **创建新Soul包**：使用`npx clawsouls init my-soul`命令创建新Soul包并编辑相关文件
4. **发布**：使用`npx clawsouls publish ./my-soul/`命令发布Soul包
5. **管理**：通过https://clawsouls.ai/dashboard进行管理（删除或查看下载内容）

## MCP服务器（适用于Claude Desktop / Cowork）

对于Claude Desktop或Cowork用户，还提供了专门的MCP服务器：

```bash
npx -y soul-spec-mcp
```

或者将相关配置添加到Claude Desktop的`claude_desktop_config.json`文件中：

```json
{"mcpServers":{"soul-spec":{"command":"npx","args":["-y","soul-spec-mcp"]}}}
```

提供的工具包括：`search_souls`、`get_soul`、`install_soul`、`preview_soul`、`list_categories`、`apply_persona`

GitHub仓库：https://github.com/clawsouls/soul-spec-mcp

## 重要说明

- 使用`use`命令后，务必提醒用户重启`openclaw gateway`
- `use`命令会自动创建备份，因此数据丢失的可能性很小
- Soul包可能包含STYLE.md和examples/文件，以便进一步定制人格
- 已发布的Soul包会显示在`https://clawsouls.ai/souls/owner/name`页面
- 用户可以对非自己拥有的Soul包进行评分（1-5星）
- 如需自定义注册表（用于本地测试），请设置环境变量`CLAWSOULS_CDN=/path/to/souls`
- 网站提供多种语言版本：英语、韩语、日语、中文、西班牙语（例如：`clawsouls.ai/ko/souls/...`）
- 可将Soul包分享给OpenClaw机器人：分享文本中包含相应的安装命令
- **Soul包宣言**：请阅读官方宣言：https://clawsouls.ai/en/manifesto
- **研究论文**：《Soul-Driven Interaction Design》：https://doi.org/10.5281/zenodo.18772585
- 法律声明：[隐私政策](https://clawsouls.ai/en/privacy) · [服务条款](https://clawsouls.ai/en/terms)