---
name: skills-search
description: 通过命令行界面（CLI）搜索 skills.sh 注册表。从 skills.sh 生态系统中查找并发现代理技能（agent skills）。
metadata:
  version: 1.0.4
  tags: ["search", "skills.sh", "cli"]
  clawdbot:
    requires:
      bins: ["node"]
    install:
      - id: "skill-install"
        kind: "skill"
        source: "clawdhub"
        slug: "skills-search"
        label: "Install skills-search skill"
---

# Skills.sh 搜索 CLI

您可以直接在终端中从 skills.sh 注册表中搜索技能。

## 安装（Clawdbot）

```bash
clawdhub install skills-search
```

## 使用方法

```bash
# Search for skills by name
skills-search "postgres"
skills-search "web design"
skills-search "twitter"

# Show most popular skills
skills-search --popular
skills-search --popular --limit 10

# Search with install command
skills-search "web design" --show-install
```

## 示例

```
❯ skills-search "web design"
🔍 Searching skills.sh for "web design"...

✅ web-design-guidelines (16,922 installs)
   Source: vercel-labs/agent-skills
   Install: npx skills add vercel-labs/agent-skills

✅ frontend-design (566 installs)
   Source: anthropics/skills
   Install: npx skills add anthropics/skills
```

### 热门技能

```
❯ skills-search --popular --limit 5
📈 Top 5 most popular skills:

✅ vercel-react-best-practices (22,475 installs)
   Source: vercel-labs/agent-skills

✅ web-design-guidelines (17,135 installs)
   Source: vercel-labs/agent-skills

✅ upgrading-expo (1,192 installs)
   Source: expo/skills
...
```

## 自动化（Clawdbot）

### 第一步：搜索技能

```bash
npx @thesethrose/skills-search "react"
```

### 第二步：通过 skills CLI 安装找到的技能

找到技能后，使用 `skills` CLI 进行安装：

```bash
npx skills add vercel-labs/agent-skills
```

**TUI 导航指南：**

`skills` CLI 使用交互式菜单。请按照提示进行操作：

1. **选择技能** → 使用空格键切换所需技能，按回车键确认
2. **选择代理** → 使用上下箭头键导航，使用空格键选择 `Clawdbot`，按回车键确认
3. **安装范围** → 选择项目（推荐），按回车键确认
4. **确认** → 按回车键继续

**重要提示：** TUI 界面可能会发生变化。请注意菜单选项，并在需要选择代理时选择 `Clawdbot`。如果对任何选项不确定，请向用户寻求帮助。

### 第三步：验证安装结果

```bash
ls ~/.clawdbot/workspace/.agents/skills/
```

## 添加自己的技能

Skills.sh 会自动索引包含 `SKILL.md` 文件的 GitHub 仓库。要添加自己的技能，请按照以下步骤操作：

1. 在您的 GitHub 仓库中创建一个包含 `SKILL.md` 文件的文件夹
2. 将该文件夹发布到 ClawdHub，以便 Clawdbot 能够识别您的技能：
   ```bash
   clawdhub publish ./your-skill/ --slug your-skill --name "Your Skill" --version 1.0.0
   ```
3. 在 Clawdbot 中安装该技能：
   ```bash
   clawdhub install your-skill
   ```

## 注意事项：

- 可以通过 https://skills.sh/api/skills 查询技能信息（官方 skills.sh API）
- 结果按安装次数排序（最受欢迎的技能排在最前面）
- **仅适用于 Clawdbot** 的技能：使用 `clawdhub install skills-search` 命令进行安装
- Skills.sh 的排行榜需要一个 GitHub 仓库（仅适用于需要发布到 ClawdHub 的技能的情况）