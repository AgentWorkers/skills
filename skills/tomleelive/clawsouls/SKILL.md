---
name: clawsouls
description: 管理 OpenClaw 的 AI 代理角色（“Soul”）。当用户需要安装、切换、列出或恢复 AI 角色时，可以使用此功能。相关操作包括：“安装一个角色”、“切换角色”、“更改角色”、“列出所有可用角色”、“恢复旧角色”、“使用简约风格的角色”、“浏览可用角色”、“查看有哪些角色可用”，以及“登录到 ClawSouls 系统”等。
---
# ClawSouls — 人工智能角色管理工具

该工具用于管理定义人工智能代理的个性、行为和身份的“Soul”包。

Soul包采用 `owner/name` 的命名规范（例如：`clawsouls/surgical-coder`、`TomLeeLive/my-soul`）。

## 先决条件

确保 `clawsouls` 命令行工具（CLI）已安装：

```bash
npx clawsouls --version
```

如果未安装，请全局安装：

```bash
npm install -g clawsouls
```

当前版本：**v0.4.0**

## 命令

### 安装一个 Soul

```bash
npx clawsouls install clawsouls/surgical-coder
npx clawsouls install clawsouls/surgical-coder --force       # overwrite existing
npx clawsouls install clawsouls/surgical-coder@0.1.0         # specific version
```

共有 79 个以上的 Soul 包可供选择。可在以下链接查看所有 Soul 包：https://clawsouls.ai

**官方提供的 Soul 包**（所有者：`clawsouls`）：
- **开发类**：code-reviewer、coding-tutor、debug-detective、api-architect、ml-engineer、sysadmin-sage、devops-veteran、gamedev-mentor、prompt-engineer、frontend-dev、backend-dev、mobile-dev、cloud-architect、database-admin、qa-engineer
- **写作与内容类**：tech-writer、storyteller、scifi-writer、copywriter、content-creator、journalist、poet、screenwriter、academic-writer
- **专业类**：data-analyst、project-manager、legal-advisor、startup-founder、hr-manager、marketing-strategist、sales-coach、product-manager
- **教育类**：math-tutor、philosophy-prof、mentor-coach、science-tutor、history-prof、language-teacher、economics-tutor
- **创意类**：music-producer、ux-designer、chef-master、graphic-designer、video-editor、podcast-host、dungeon-master、game-designer
- **生活类**：personal-assistant、fitness-coach、travel-guide、life-coach、meditation-guide、nutrition-advisor、productivity-guru、financial-planner
- **科学类**：research-scientist、data-scientist
- **安全类**：security-auditor
- **MBTI 类型**：mbti-intj、mbti-intp、mbti-entj、mbti-entp、mbti-infp、mbti-infp、mbti-enfj、mbti-enfp、mbti-istj、mbti-isfj、mbti-estj、mbti-esfj、mbti-istp、mbti-isfp、mbti-estp、mbti-esfp
- **特殊用途类**：surgical-coder、korean-translator
- **通用类**：brad、minimalist

### 激活一个 Soul

```bash
npx clawsouls use clawsouls/surgical-coder
```

- 会自动备份当前的工作区文件（SOUL.md、IDENTITY.md、AGENTS.md、HEARTBEAT.md、STYLE.md、examples/）
- 严禁覆盖 USER.md、MEMORY.md 或 TOOLS.md 文件
- 激活后需要重启 `openclaw gateway` 才能生效

### 恢复之前的 Soul

```bash
npx clawsouls restore
```

可恢复到最近一次使用的备份状态。

### 列出已安装的 Soul

```bash
npx clawsouls list
```

以 `owner/name` 的格式显示已安装的 Soul 包。

### 创建一个新的 Soul

```bash
npx clawsouls init my-soul
```

系统会创建一个新的 Soul 目录，其中包含 `soul.json`、SOUL.md、IDENTITY.md、AGENTS.md、HEARTBEAT.md 和 README.md 文件。

### 验证一个 Soul

```bash
npx clawsouls validate ./my-soul/
npx clawsouls validate --soulscan ./my-soul/   # with SoulScan security analysis
npx clawsouls check ./my-soul/                 # alias
```

根据规范进行验证（包括文件结构、文件内容等）。使用 `--soulscan` 选项可进行全面的安全性和质量分析（包含评分）。此步骤在发布前会自动执行。

### SoulScan — 安全性与完整性检测工具

```bash
npx clawsouls soulscan              # scan current OpenClaw workspace
npx clawsouls soulscan ./my-soul/   # scan a specific directory
npx clawsouls soulscan --init       # initialize baseline checksums
npx clawsouls soulscan -q           # quiet mode for cron (SOULSCAN_OK / SOULSCAN_ALERT)
npx clawsouls scan                  # alias
```

SoulScan 会检查活跃的 Soul 文件：
- **完整性**：通过 SHA-256 校验和来检测自上次扫描以来的篡改情况
- **安全性**：进行 53 项安全检查（包括提示注入、代码执行、XSS 攻击、数据泄露、权限提升、社会工程学攻击、有害内容检测等）
- **质量**：检查文件结构和内容长度是否符合规范
- **角色一致性**：验证 SOUL.md、IDENTITY.md 和 soul.json 中的角色描述是否一致

**Cron 任务** — 定期检测文件是否被篡改：
```bash
# Run every hour to monitor workspace integrity
npx clawsouls soulscan -q
# Exit code 0 = OK, 1 = alert (tampered or security issue)
```

**首次运行**：使用 `--init` 命令建立基准校验和，不会触发警报。

**SoulScan™ 评分标准**：0-100 分（90 分以上表示“已验证”；70 分以上表示“低风险”；40 分以上表示“中等风险”；低于 40 分表示“高风险”；0 分表示“被阻止”）

### 发布一个 Soul

```bash
export CLAWSOULS_TOKEN=<token>
npx clawsouls publish ./my-soul/
```

文件会自动发布到 `username/soul-name` 的命名空间中。发布前需要 API 令牌。发布前会自动进行验证；验证失败会导致发布失败。

### 登录 / 获取令牌

```bash
npx clawsouls login
```

获取 API 令牌的步骤：登录 https://clawsouls.ai → 进入控制面板 → 生成 API 令牌。

## 工作流程

### 安装与切换角色

1. **浏览**：在 https://clawsouls.ai 上查看可用的 Soul 包，或从上面的分类列表中选择合适的 Soul 包。
2. **安装**：使用 `npx clawsouls install clawsouls/surgical-coder` 命令进行安装。
3. **激活**：使用 `npx clawsouls use clawsouls/surgical-coder` 命令激活新角色。
4. **重启**：运行 `openclaw gateway restart` 以应用新角色设置。
5. **恢复**：如果需要恢复之前的角色，使用 `npx clawsouls restore` 命令。

### 发布一个 Soul

1. **登录**：使用 `npx clawsouls login` 命令登录。
2. **获取令牌**：从控制面板获取 API 令牌（格式：`export CLAWSOULS_TOKEN=<token>`）。
3. **创建新角色**：使用 `npx clawsouls init my-soul` 命令创建新角色文件。
4. **发布**：使用 `npx clawsouls publish ./my-soul/` 命令发布新角色。
5. **管理**：通过 https://clawsouls.ai/dashboard 进行角色管理（包括删除和查看下载文件）。

## 重要提示

- 使用新角色后，请务必提醒用户重启 `openclaw gateway`。
- `use` 命令会自动创建备份，因此数据丢失的可能性很低。
- Soul 包可能包含 `STYLE.md` 和 `examples/` 文件，以便进一步自定义角色表现。
- 已发布的 Soul 包会显示在 `https://clawsouls.ai/souls/owner/name` 上。
- 用户可以对非自己创建的 Soul 包进行评分（1-5 星）。
- 如需进行本地测试，请设置环境变量 `CLAWSOULS_CDN=/path/to/souls`。
- 网站提供多种语言版本：英语、韩语、日语、中文、西班牙语（例如：`clawsouls.ai/ko/souls/...`）。
- 可将 Soul 包分享给您的 OpenClaw 机器人；分享命令包含在相关文本中。
- **Soul 宣言**：请阅读官方宣言：https://clawsouls.ai/en/manifesto。
- **研究论文**：《Soul-Driven Interaction Design》：https://doi.org/10.5281/zenodo.18661656
- 法律声明：[隐私政策](https://clawsouls.ai/en/privacy) · [服务条款](https://clawsouls.ai/en/terms)