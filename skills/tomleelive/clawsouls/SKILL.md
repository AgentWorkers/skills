---
name: clawsouls
description: 管理 OpenClaw 的 AI 代理角色（“Souls”）。当用户需要安装、切换、列出或恢复 AI 角色时，可以使用该功能。相关操作请求包括：“安装一个 AI 角色”、“切换角色”、“更改角色”、“列出所有可用角色”、“恢复我的旧角色”、“使用简约风格的角色”、“浏览所有可用角色”、“有哪些角色可供选择”，以及“登录到 ClawSouls 系统”。
---

# ClawSouls — 人工智能角色管理工具

该工具用于管理定义人工智能代理的个性、行为和身份的“Soul”包。

“Soul”包采用 `owner/name` 的命名规范（例如：`clawsouls/brad`、`TomLeeLive/my-soul`）。

## 先决条件

确保 `clawsouls` 命令行工具（CLI）已安装：

```bash
npx clawsouls --version
```

如果尚未安装，请全局安装：

```bash
npm install -g clawsouls
```

当前版本：**v0.2.3**

## 命令

### 安装一个 Soul

```bash
npx clawsouls install clawsouls/brad
npx clawsouls install clawsouls/brad --force  # overwrite existing
```

目前提供 30 多个 Soul 包，可在 [https://clawsouls.ai](https://clawsouls.ai) 上查看所有 Soul 包。

**官方提供的 Soul 包**（所有者：`clawsouls`）：
- **开发类**：code-reviewer（代码审核员）、coding-tutor（编程导师）、debug-detective（调试侦探）、api-architect（API 架构师）、ml-engineer（机器学习工程师）、sysadmin-sage（系统管理员专家）、devops-veteran（DevOps 专家）、gamedev-mentor（游戏开发导师）、prompt-engineer（提示引擎开发者）
- **写作与内容类**：tech-writer（技术作家）、storyteller（故事讲述者）、sci-fi-writer（科幻作家）、copywriter（文案撰写者）、content-creator（内容创作者）
- **专业类**：data-analyst（数据分析师）、project-manager（项目经理）、legal-advisor（法律顾问）、startup-founder（初创企业创始人）
- **教育类**：math-tutor（数学导师）、philosophy-prof（哲学教授）、mentor-coach（导师教练）
- **创意类**：music-producer（音乐制作人）、ux-designer（用户体验设计师）、chef-master（烹饪大师）
- **生活类**：personal-assistant（个人助理）、fitness-coach（健身教练）、travel-guide（旅行向导）
- **安全类**：security-auditor（安全审计员）
- **通用类**：brad（通用角色）、minimalist（极简主义角色）

### 激活一个 Soul

```bash
npx clawsouls use clawsouls/brad
```

- 会自动备份当前的工作区文件（SOUL.md、IDENTITY.md、AGENTS.md、HEARTBEAT.md、STYLE.md、examples/ 等）。
- 绝不会覆盖 USER.md、MEMORY.md 或 TOOLS.md 文件。
- 激活后需要重启 `openclaw gateway` 才能生效。

### 恢复之前的 Soul

```bash
npx clawsouls restore
```

会恢复到上次使用 `use` 命令创建的备份状态。

### 列出已安装的 Soul

```bash
npx clawsouls list
```

以 `owner/name` 的格式显示已安装的 Soul 包。

### 创建一个新的 Soul

```bash
npx clawsouls init my-soul
```

会创建一个新的 Soul 目录，其中包含 `clawsoul.json`、SOUL.md、IDENTITY.md、AGENTS.md、HEARTBEAT.md 和 README.md 文件。

### 验证一个 Soul

```bash
npx clawsouls validate ./my-soul/
npx clawsouls check ./my-soul/   # alias
```

根据规范进行验证（包括文件结构、必需文件的完整性以及安全扫描）。在发布前也会自动执行验证。

### 发布一个 Soul

```bash
export CLAWSOULS_TOKEN=<token>
npx clawsouls publish ./my-soul/
```

会自动将 Soul 发布到 `username/soul-name` 的命名空间中。发布前需要 API 令牌。发布前会自动进行验证，验证失败时会阻止发布。

### 登录 / 获取令牌

```bash
npx clawsouls login
```

获取 API 令牌的步骤：登录 [https://clawsouls.ai](https://clawsouls.ai) → 进入仪表板 → 生成 API 令牌。

## 工作流程

### 安装与切换角色

1. **浏览**：在 [https://clawsouls.ai](https://clawsouls.ai) 上查看可用的 Soul 包，或从上面的分类列表中选择。
2. **安装**：使用 `npx clawsouls install clawsouls/brad` 命令安装所需的 Soul。
3. **激活**：使用 `npx clawsouls use clawsouls/brad` 命令激活新角色。
4. **重启**：运行 `openclaw gateway restart` 以应用新角色设置。
5. **恢复**：如果需要恢复之前的角色，使用 `npx clawsouls restore` 命令。

### 发布一个 Soul

1. **登录**：使用 `npx clawsouls login` 命令登录。
2. **获取令牌**：从仪表板获取 API 令牌。
3. **创建新角色**：使用 `npx clawsouls init my-soul` 命令创建新的 Soul。
4. **发布**：使用 `npx clawsouls publish ./my-soul/` 命令发布新角色。
5. **管理**：通过 [https://clawsouls.ai/dashboard](https://clawsouls.ai/dashboard) 进行角色管理（删除、查看下载内容）。

## 重要说明

- 使用 `use` 命令后，务必提醒用户重启 `openclaw gateway`。
- `use` 命令会自动创建备份，因此数据丢失的可能性很小。
- Soul 包可能包含 `STYLE.md` 和 `examples/` 文件，以便进一步自定义角色。
- 已发布的 Soul 会显示在 [https://clawsouls.ai/souls/owner/name](https://clawsouls.ai/souls/owner/name) 上。
- 用户可以对非自己拥有的 Soul 进行评分（1-5 星）。
- 如需进行本地测试（自定义注册表），请设置环境变量：`CLAWSOULS_CDN=/path/to/souls`。