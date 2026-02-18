---
name: clawsouls
description: 管理 OpenClaw 的 AI 代理角色（“Souls”）。当用户需要安装、切换、列出或恢复 AI 角色时，可以使用该功能。相关操作请求包括：“安装一个角色”、“切换角色”、“更改角色”、“列出所有可用角色”、“恢复我的旧角色”、“使用极简风格的角色”、“浏览所有角色”、“有哪些角色可用”以及“登录到 clawsouls”等。
---
# ClawSouls — 人工智能人格管理工具

该工具用于管理定义人工智能代理的人格、行为和身份的“Soul”包。

“Soul”包采用 `owner/name` 的命名规范（例如：`clawsouls/surgical-coder`、`TomLeeLive/my-soul`）。

## 先决条件

确保已安装 `clawsouls` 命令行工具（CLI）：

```bash
npx clawsouls --version
```

如果尚未安装，请全局安装：

```bash
npm install -g clawsouls
```

当前版本：**v0.3.2**

## 命令

### 安装一个 Soul

```bash
npx clawsouls install clawsouls/surgical-coder
npx clawsouls install clawsouls/surgical-coder --force       # overwrite existing
npx clawsouls install clawsouls/surgical-coder@0.1.0         # specific version
```

目前共有 79 个可供选择的 Soul 包。可在 [https://clawsouls.ai](https://clawsouls.ai) 上查看所有 Soul 包。

**官方提供的 Soul 包**（所有者：`clawsouls`）：
- **开发类**：code-reviewer（代码审核员）、coding-tutor（编程导师）、debug-detective（调试侦探）、api-architect（API 架构师）、ml-engineer（机器学习工程师）、sysadmin-sage（系统管理员专家）、devops-veteran（DevOps 专家）、gamedev-mentor（游戏开发导师）、prompt-engineer（提示引擎开发者）、frontend-dev（前端开发者）、backend-dev（后端开发者）、mobile-dev（移动应用开发者）、cloud-architect（云架构师）、database-admin（数据库管理员）、qa-engineer（质量保证工程师）
- **写作与内容类**：tech-writer（技术作家）、storyteller（故事讲述者）、scifi-writer（科幻作家）、copywriter（文案撰写者）、content-creator（内容创作者）、journalist（记者）、poet（诗人）、screenwriter（编剧）、academic-writer（学术作家）
- **职业类**：data-analyst（数据分析师）、project-manager（项目经理）、legal-advisor（法律顾问）、startup-founder（初创企业创始人）、hr-manager（人力资源经理）、marketing-strategist（营销策略师）、sales-coach（销售教练）、product-manager（产品经理）
- **教育类**：math-tutor（数学导师）、philosophy-prof（哲学教授）、mentor-coach（导师教练）、science-tutor（科学导师）、history-prof（历史教授）、language-teacher（语言教师）、economics-tutor（经济学导师）
- **创意类**：music-producer（音乐制作人）、ux-designer（用户体验设计师）、chef-master（厨师大师）、graphic-designer（平面设计师）、video-editor（视频编辑师）、podcast-host（播客主持人）、dungeon-master（游戏设计师）
- **生活方式类**：personal-assistant（个人助理）、fitness-coach（健身教练）、travel-guide（旅行向导）、life-coach（生活导师）、meditation-guide（冥想指导师）、nutrition-advisor（营养顾问）、productivity-guru（效率提升专家）、financial-planner（财务规划师）
- **科学类**：research-scientist（研究科学家）、data-scientist（数据科学家）
- **安全类**：security-auditor（安全审计员）
- **MBTI 类型**：mbti-intj、mbti-intp、mbti-entj、mbti-entp、mbti-infp、mbti-infp、mbti-enfj、mbti-enfp、mbti-istj、mbti-isfj、mbti-estj、mbti-esfj、mbti-istp、mbti-isfp、mbti-estp、mbti-esfp
- **特殊用途类**：surgical-coder（外科医生）、korean-translator（韩语翻译者）
- **通用类**：brad（通用型人格）、minimalist（极简主义人格）

### 激活一个 Soul

```bash
npx clawsouls use clawsouls/surgical-coder
```

- 会自动备份当前工作区的文件（SOUL.md、IDENTITY.md、AGENTS.md、HEARTBEAT.md、STYLE.md、examples/ 等）。
- 请勿覆盖 USER.md、MEMORY.md 或 TOOLS.md 文件。
- 激活后需要重启 `openclaw` 服务器才能生效。

### 恢复之前的 Soul

```bash
npx clawsouls restore
```

可以恢复到最近一次使用的 Soul 配置。

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

### 验证一个 Soul

```bash
npx clawsouls validate ./my-soul/
npx clawsouls check ./my-soul/   # alias
```

根据规范进行验证（包括文件结构、安全扫描等），并在发布前自动执行验证。

### 发布一个 Soul

```bash
export CLAWSOULS_TOKEN=<token>
npx clawsouls publish ./my-soul/
```

会将 Soul 发布到 `username/soul-name` 的命名空间中。需要使用 API 令牌。发布前会自动进行验证；验证失败时会阻止发布。

### 登录 / 获取令牌

```bash
npx clawsouls login
```

获取 API 令牌的步骤：登录 [https://clawsouls.ai](https://clawsouls.ai) → 进入仪表板 → 生成 API 令牌。

## 工作流程

### 安装与切换人格

1. **浏览**：在 [https://clawsouls.ai](https://clawsouls.ai) 上查看可用的 Soul 包，或从上面的分类列表中选择。
2. **安装**：使用命令 `npx clawsouls install clawsouls/surgical-coder` 安装所需的 Soul。
3. **激活**：使用命令 `npx clawsouls use clawsouls/surgical-coder` 激活新的人格配置。
4. **重启**：运行 `openclaw gateway restart` 以应用新的人格设置。
5. **恢复**：如果需要恢复之前的配置，使用命令 `npx clawsouls restore`。

### 发布一个 Soul

1. **登录**：使用命令 `npx clawsouls login` 登录。
2. **获取令牌**：从仪表板获取 API 令牌（格式：`export CLAWSOULS_TOKEN=<token>`）。
3. **创建新 Soul**：使用命令 `npx clawsouls init my-soul` 创建新的 Soul 目录，并编辑相关文件。
4. **发布**：使用命令 `npx clawsouls publish ./my-soul/` 发布 Soul。
5. **管理**：通过 [https://clawsouls.ai/dashboard](https://clawsouls.ai/dashboard) 进行管理（删除、查看下载内容等）。

## 重要提示

- 使用新人格配置后，请务必提醒用户重启 `openclaw` 服务器。
- `use` 命令会自动创建备份，因此数据丢失的可能性很低。
- 部分 Soul 包可能包含 `STYLE.md` 和 `examples/` 文件，以便进一步自定义人格表现。
- 已发布的 Soul 会显示在 [https://clawsouls.ai/souls/owner/name](https://clawsouls.ai/souls/owner/name) 上。
- 用户可以对非自己拥有的 Soul 包进行评分（1-5 星）。
- 如需进行本地测试，请设置环境变量 `CLAWSOULS_CDN=/path/to/souls`。
- 网站提供多种语言版本：英语、韩语、日语、中文、西班牙语（例如：`clawsouls.ai/ko/souls/...`）。
- 可将 Soul 配置分享给您的 OpenClaw 机器人；分享功能包含在安装命令中。
- **Soul 宣言**：请阅读 [宣言文件](https://clawsouls.ai/en/manifesto)。
- **研究论文**：《Soul-Driven Interaction Design》：[链接](https://doi.org/10.5281/zenodo.18661656)。
- 法律声明：[隐私政策](https://clawsouls.ai/en/privacy) · [服务条款](https://clawsouls.ai/en/terms)