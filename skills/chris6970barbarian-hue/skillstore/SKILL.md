# SkillStore - OpenClaw 技能管理器

通过智能匹配功能，您可以搜索、安装和创建 OpenClaw 技能。

## 技能元数据

- **名称**: skillstore
- **类型**: OpenClaw 技能
- **用途**: 搜索现有技能、从 GitHub 安装技能或创建新技能

## 设置命令

无需额外设置，即可直接使用。

## 使用命令

### 搜索与安装

```bash
# Search for a skill (applies 30% threshold)
skillstore <query>

# Examples:
skillstore home assistant
skillstore weather
skillstore smart home
skillstore email gmail
skillstore github
```

### 列出与显示

```bash
# List installed skills
skillstore list

# Show all known skills (20 built-in)
skillstore known
```

### 创建新技能

```bash
# Create new skill with templates
skillstore create <name>
skillstore new <name>

# Examples:
skillstore create my-awesome-skill
skillstore new weather-widget
```

## 搜索原理

### 匹配算法

1. **分词** - 将查询内容拆分为关键词
2. **计算** - 使用 Jaccard 相似度算法，并根据关键词对结果进行加权
3. **过滤** - 删除相似度低于 30% 的结果
4. **排序** - 按相关性得分对结果进行排序
5. **显示** - 以可视化的方式展示结果（包括得分条）

### 匹配得分

```
Score >= 50% = Strong match (green bar)
Score >= 30% = Weak match (yellow bar)  
Score < 30% = Not shown (filtered)
```

### 搜索来源（按顺序）

1. **内置技能** - 内置的 20 个技能
2. **本地技能** - 位于 `~/.openclaw/workspace/skills/` 目录下的技能
3. **GitHub** - 在 GitHub 仓库中搜索技能

## 用户交互流程

```
1. User runs: skillstore home assistant
2. System searches all 3 sources
3. System filters by threshold
4. Results shown with scores:

   1. [KNOWN] homeassistant ████████░░ 85%
      Control smart home devices...
   2. [LOCAL] homeassistant ███████░░░ 78%
   3. [GIT] openclaw-homeassistant ██████░░░░ 62%

5. User chooses:
   - Enter number → Install from GitHub
   - n → Create new skill
   - q → Quit
```

## 内置技能数据库

可搜索的内置技能：

| 技能 | 描述 |
|-------|-------------|
| homeassistant | 智能家居控制（HA API） |
| gog | Google Workspace（Gmail、日历、云端硬盘） |
| weather | 天气预报 |
| github | GitHub 命令行工具集成 |
| himalaya | 通过 IMAP/SMTP 发送邮件 |
| obsidian | Obsidian 文档管理工具集成 |
| sonoscli | Sonos 音响控制 |
| blucli | BluOS 音响控制 |
| eightctl | Eight 睡眠辅助工具 |
| ordercli | 食品配送订单管理 |
| blogwatcher | RSS 源监控工具 |
| gifgrep | GIF 图片搜索/下载工具 |
| video-frames | 视频帧提取工具 |
| youtube-summarizer | YouTube 视频字幕提取工具 |
| ga4 | Google Analytics 4 |
| gsc | Google Search Console（搜索分析工具） |
| wacli | WhatsApp 聊天工具 |
| browser | 浏览器自动化工具 |
| healthcheck | 系统安全加固工具 |

## 错误处理

- 如果未找到满足条件的结果：提示用户创建新技能
- 如果 GitHub 搜索失败：回退到本地或内置技能列表
- 安装失败：显示失败原因及具体错误信息

## 相关技能

- homeassistant
- openclaw-migrate
- skill-templates（旧版技能模板，建议使用 skillstore）

## 相关文件

```
skillstore/
├── SKILL.md       # This file
├── README.md      # User docs
├── main.js        # CLI with intelligent search
└── config.json    # Install history
```