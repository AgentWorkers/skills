---
name: skill-search
description: 在 skills.droyd.ai 的 ClawHub 注册表中搜索、发现并动态加载技能。当代理需要某项它不具备的功能时，或者想要为特定任务寻找工具时，或者需要浏览热门/流行的技能时，可以使用此功能。触发条件包括：请求查找技能、搜索工具、发现功能、动态加载技能、检查某个领域中存在的技能，或者在无需安装技能的情况下直接运行该技能。此外，当用户询问可用的 OpenClaw/ClawHub 技能、想要探索技能类别，或者需要即时获取并执行技能内容时，也可以使用此功能。
---

# 技能搜索

无需进行永久性安装，即可从 ClawHub 注册表中动态搜索、发现并加载技能。

**基础 URL**: `https://skills.droyd.ai`

## 工作流程

### 1. 搜索技能

使用搜索脚本，通过查询、类别或标签来查找技能：

```bash
bash scripts/skillhub.sh search "browser automation"
bash scripts/skillhub.sh search "trading" --categories crypto,defi
bash scripts/skillhub.sh search "pdf" --limit 5
```

### 2. 浏览热门技能

发现受欢迎且高质量的技能：

```bash
bash scripts/skillhub.sh trending
bash scripts/skillhub.sh trending --categories coding --window 7d
```

### 3. 查看技能详情

查看特定技能的元数据、质量评分、依赖项以及所需的 API 密钥：

```bash
bash scripts/skillhub.sh detail author/skill-name
```

### 4. 获取技能内容

检索完整的技能内容（包括 SKILL.md 文件、脚本和参考资料），以便阅读或执行：

```bash
# Print content to stdout
bash scripts/skillhub.sh content author/skill-name

# Extract to a temp folder for agent execution
bash scripts/skillhub.sh content author/skill-name --extract
# Files are written to /tmp/openclaw-skills/skill-name/
```

当使用 `--extract` 选项时，技能文件会从响应内容中被解析出来，并保存到 `/tmp/openclaw-skills/{skill-name}/` 目录下。代理程序可以直接读取并执行这些文件。

### 5. 执行加载的技能

在提取技能信息后，阅读该技能的 SKILL.md 文件以获取使用说明：

```bash
cat /tmp/openclaw-skills/{skill-name}/SKILL.md
```

然后按照说明运行从提取目录中获取的脚本。

## 分类

可用的分类筛选器：`devops`、`browser`、`productivity`、`marketing`、`prediction_markets`、`location`、`communication`、`media`、`finance`、`crypto`、`trading`、`gaming`、`defi`、`image`、`video`、`smart-home`、`security`、`search`、`notes`、`calendar`、`coding`、`token_launchpad`、`voice`、`email`、`messaging`、`social`、`music`、`database`、`monitoring`、`backup`、`wallet`、`food`、`health`、`other`。

## 永久性安装

若希望通过 ClawHub CLI 将技能永久安装到系统中，而非动态加载，请参考以下步骤：

```bash
clawhub install {skill_name}
```

## API 参考

有关详细的 API 参数和响应格式，请参阅 [references/api.md](references/api.md)。