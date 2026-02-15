---
name: clawflows
version: 1.0.0
description: 从 clawflows.com 搜索、安装并运行多技能自动化任务。通过逻辑、条件以及步骤之间的数据流，将多个技能组合成强大的工作流程。
metadata:
  clawdbot:
    requires:
      bins: ["clawflows"]
    install:
      - id: node
        kind: node
        package: clawflows
        bins: ["clawflows"]
        label: "Install ClawFlows CLI (npm)"
---

# ClawFlows

发现并运行能够结合数据库、图表、社交搜索等多种功能的自动化任务。

## 安装 CLI

```bash
npm i -g clawflows
```

## 命令

### 搜索自动化任务

```bash
clawflows search "youtube competitor"
clawflows search "morning brief"
clawflows search --capability chart-generation
```

### 检查需求

在安装之前，请查看该自动化任务需要哪些功能：

```bash
clawflows check youtube-competitor-tracker
```

系统会显示所需的功能以及您是否具备提供这些功能的技能。

### 安装自动化任务

```bash
clawflows install youtube-competitor-tracker
```

自动化任务会被下载到 `./automations/youtube-competitor-tracker.yaml` 文件中。

### 列出已安装的自动化任务

```bash
clawflows list
```

### 运行自动化任务

```bash
clawflows run youtube-competitor-tracker
clawflows run youtube-competitor-tracker --dry-run
```

`--dry-run` 标志用于显示不执行任务时的结果。

### 启用/禁用调度功能

```bash
clawflows enable youtube-competitor-tracker   # Shows cron setup instructions
clawflows disable youtube-competitor-tracker
```

### 查看日志

```bash
clawflows logs youtube-competitor-tracker
clawflows logs youtube-competitor-tracker --last 10
```

### 发布您的自动化任务

```bash
clawflows publish ./my-automation.yaml
```

系统会提供通过 Pull Request (PR) 将自动化任务提交到注册中心的说明。

## 工作原理

自动化任务使用的是 **功能**（抽象概念），而不是具体的 **技能**：

```yaml
steps:
  - capability: youtube-data      # Not a specific skill
    method: getRecentVideos
    args:
      channels: ["@MrBeast"]
    capture: videos
    
  - capability: database
    method: upsert
    args:
      table: videos
      data: "${videos}"
```

这意味着自动化任务具有 **可移植性**——它们可以在任何具备所需功能的 Clawbot 上运行。

## 标准功能

| 功能            | 功能描述                | 示例技能                |
|-----------------|------------------|----------------------|
| `youtube-data`     | 获取视频/频道信息           | youtube-api             |
| `database`       | 存储和查询数据             | sqlite-skill            |
| `chart-generation`   | 生成图表图像             | chart-image             |
| `social-search`    | 在 X/Twitter 上搜索           | search-x                 |
| `prediction-markets` | 查询比赛赔率             | polymarket               |
| `weather`        | 获取天气预报             | weather                 |
| `calendar`       | 读写日历事件             | caldav-calendar           |
| `email`        | 发送/接收电子邮件           | agentmail                |
| `tts`          | 文本转语音                 | elevenlabs-tts            |

## 使您的技能兼容 ClawFlows

要使您的技能与 ClawFlows 的自动化任务配合使用，请添加一个 `CAPABILITY.md` 文件：

```markdown
# my-capability Capability

Provides: my-capability
Skill: my-skill

## Methods

### myMethod

**Input:**
- param1: description
- param2: description

**How to fulfill:**
\`\`\`bash
./scripts/my-script.sh --param1 "${param1}"
\`\`\`

**Output:** Description of output format
```

并在您的 SKILL.md 文件的头部（frontmatter）中声明该功能：

```yaml
---
name: my-skill
provides:
  - capability: my-capability
    methods: [myMethod]
---
```

## 链接

- **注册中心**: https://clawflows.com
- **npm 上的 CLI**: https://www.npmjs.com/package/clawflows
- **GitHub**: https://github.com/Cluka-399/clawflows-registry