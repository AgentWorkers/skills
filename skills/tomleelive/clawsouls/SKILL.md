---
name: clawsouls
description: 管理 OpenClaw 的 AI 代理角色（“Soul”）。当用户需要安装、切换、列出或恢复 AI 角色时，可以使用该功能。相关操作请求包括：“安装一个 AI 角色”、“切换角色”、“更改角色”、“列出所有可用角色”、“恢复我的旧角色”、“使用简约风格的角色”、“浏览所有可用角色”、“有哪些角色可供选择”以及“登录到 ClawSouls 系统”等。
---

# ClawSouls — 人工智能角色管理工具

该工具用于管理定义人工智能代理的个性、行为和身份的“灵魂”包（Soul packages）。

“灵魂”包采用 `owner/name` 的命名规范（例如：`clawsouls/brad`、`TomLeeLive/my-soul`）。

## 先决条件

确保已安装 `clawsouls` 命令行工具（CLI）：

```bash
npx clawsouls --version
```

如果尚未安装，请全局安装：

```bash
npm install -g clawsouls
```

当前版本：**v0.2.5**

## 命令

### 安装一个“灵魂”包

```bash
npx clawsouls install clawsouls/brad
npx clawsouls install clawsouls/brad --force       # overwrite existing
npx clawsouls install clawsouls/brad@0.1.0         # specific version
```

目前提供了78多种“灵魂”包，可在 [https://clawsouls.ai](https://clawsouls.ai) 上查看全部列表。

**官方提供的“灵魂”包（所有者：clawsouls）：**
- **开发类**：code-reviewer（代码审核员）、coding-tutor（编程导师）、debug-detective（调试侦探）、api-architect（API架构师）、ml-engineer（机器学习工程师）、sysadmin-sage（系统管理员专家）、devops-veteran（DevOps老手）、gamedev-mentor（游戏开发导师）、prompt-engineer（提示引擎开发者）、frontend-dev（前端开发人员）、backend-dev（后端开发人员）、mobile-dev（移动应用开发人员）、cloud-architect（云架构师）、database-admin（数据库管理员）、qa-engineer（质量保证工程师）
- **写作与内容类**：tech-writer（技术作家）、storyteller（故事讲述者）、sci-fi-writer（科幻作家）、copywriter（文案撰写者）、content-creator（内容创作者）、journalist（记者）、poet（诗人）、screenwriter（编剧）、academic-writer（学术作家）
- **职业类**：data-analyst（数据分析师）、project-manager（项目经理）、legal-advisor（法律顾问）、startup-founder（初创企业创始人）、hr-manager（人力资源经理）、marketing-strategist（营销策略师）、sales-coach（销售教练）、product-manager（产品经理）
- **教育类**：math-tutor（数学辅导老师）、philosophy-prof（哲学教授）、mentor-coach（导师教练）、science-tutor（科学辅导老师）、history-prof（历史老师）、language-teacher（语言教师）、economics-tutor（经济学辅导老师）
- **创意类**：music-producer（音乐制作人）、ux-designer（用户体验设计师）、chef-master（厨师大师）、graphic-designer（平面设计师）、video-editor（视频编辑师）、podcast-host（播客主持人）、dungeon-master（游戏设计者）
- **生活方式类**：personal-assistant（个人助理）、fitness-coach（健身教练）、travel-guide（旅行向导）、life-coach（生活导师）、meditation-guide（冥想指导师）、nutrition-advisor（营养顾问）、productivity-guru（效率提升专家）、financial-planner（财务规划师）
- **科学类**：research-scientist（研究科学家）、data-scientist（数据科学家）
- **安全类**：security-auditor（安全审计员）
- **MBTI类型**：mbti-intj、mbti-intp、mbti-entj、mbti-entp、mbti-infp、mbti-infp、mbti-enfj、mbti-enfp、mbti-istj、mbti-isfj、mbti-estj、mbti-esfj、mbti-istp、mbti-isfp、mbti-estp、mbti-esfp
- **特殊类别**：surgical-coder（受Karpathy的CLAUDE.md启发设计）、korean-translator（韩语翻译者）
- **通用类别**：brad（通用角色示例）、minimalist（极简主义角色）

### 激活一个“灵魂”包

```bash
npx clawsouls use clawsouls/brad
```

- 会自动备份当前的工作区文件（SOUL.md、IDENTITY.md、AGENTS.md、HEARTBEAT.md、STYLE.md等）。
- 绝不会覆盖USER.md、MEMORY.md或TOOLS.md文件。
- 激活后需要重启`openclaw gateway`才能生效。

### 恢复之前的“灵魂”设置

```bash
npx clawsouls restore
```

可以恢复由 `use` 命令创建的最新备份设置。

### 列出已安装的“灵魂”包

```bash
npx clawsouls list
```

以 `owner/name` 的格式显示已安装的“灵魂”包。

### 创建一个新的“灵魂”包

```bash
npx clawsouls init my-soul
```

会创建一个新的“灵魂”包目录，其中包含 `clawsoul.json`、SOUL.md、IDENTITY.md、AGENTS.md、HEARTBEAT.md 和 README.md 文件。

### 验证一个“灵魂”包

```bash
npx clawsouls validate ./my-soul/
npx clawsouls check ./my-soul/   # alias
```

根据规范进行验证（包括架构检查、文件完整性检测和安全扫描），并在发布前自动执行验证。

### 发布一个“灵魂”包

```bash
export CLAWSOULS_TOKEN=<token>
npx clawsouls publish ./my-soul/
```

自动将“灵魂”包发布到 `username/soul-name` 的命名空间中，需要使用认证令牌。发布前会自动进行验证，验证失败将阻止发布。

### 登录 / 获取令牌

```bash
npx clawsouls login
```

获取API令牌的步骤：登录 [https://clawsouls.ai](https://clawsouls.ai) → 进入控制台 → 生成API令牌。

## 工作流程

### 安装与切换角色

1. **浏览**：在 [https://clawsouls.ai](https://clawsouls.ai) 查看可用的“灵魂”包，或从上面的分类列表中选择。
2. **安装**：使用 `npx clawsouls install clawsouls/brad` 命令进行安装。
3. **激活**：使用 `npx clawsouls use clawsouls/brad` 命令激活新角色。
4. **重启**：运行 `openclaw gateway restart` 以应用新角色设置。
5. **恢复**：如果需要恢复之前的设置，使用 `npx clawsouls restore` 命令。

### 发布一个“灵魂”包

1. **登录**：使用 `npx clawsouls login` 命令登录。
2. **获取令牌**：从控制台获取API令牌。
3. **创建**：使用 `npx clawsouls init my-soul` 命令创建新的“灵魂”包，并编辑相关文件。
4. **发布**：使用 `npx clawsouls publish ./my-soul/` 命令发布“灵魂”包。
5. **管理**：通过 [https://clawsouls.ai/dashboard](https://clawsouls.ai/dashboard) 进行管理（删除或查看下载内容）。

## 重要说明

- 使用 `use` 命令后，务必提醒用户重启 `openclaw gateway`。
- `use` 命令会自动创建备份，因此数据丢失的可能性很低。
- “灵魂”包可能包含 `STYLE.md` 和 `examples/` 文件，以便进一步自定义角色表现。
- 已发布的“灵魂”包会显示在 [https://clawsouls.ai/souls/owner/name](https://clawsouls.ai/souls/owner/name) 上。
- 用户可以对非自己拥有的“灵魂”包进行评分（1-5星）。
- 如需进行本地测试，请设置环境变量 `CLAWSOULS_CDN=/path/to/souls`。
- 网站提供五种语言版本：英语、韩语、日语、中文和西班牙语（例如：`clawsouls.ai/ko/souls/...`）。
- 可将任何“灵魂”包分享给您的OpenClaw机器人，分享链接包含相应的安装命令。
- 法律声明：[隐私政策](https://clawsouls.ai/en/privacy) · [服务条款](https://clawsouls.ai/en/terms)