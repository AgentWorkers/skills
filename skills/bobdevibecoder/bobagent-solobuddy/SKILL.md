---
name: solobuddy
description: 专为独立开发者打造的集成式辅助工具——涵盖内容创作流程、Twitter互动功能以及项目核心内容的构建。它更像是一个“活生生的助手”，而不仅仅是一个工具而已。
homepage: https://github.com/gHashTag/bip-buddy
metadata: {"clawdbot":{"emoji":"🎯","requires":{"bins":["gh"],"optional":["bird"]},"config":["solobuddy.dataPath","solobuddy.voice"]}}
---

# SoloBuddy

这是一个内置的公共内容助手，它更像是一个贴心的伙伴，而不仅仅是一个工具。

## 快速入门

1. 在 `~/.clawdbot/clawdbot.json` 文件中设置您的数据路径：
```json
{
  "solobuddy": {
    "dataPath": "~/projects/my-bip-folder",
    "voice": "jester-sage"
  }
}
```

2. 创建文件夹结构（请将路径替换为您自己的路径）：
```bash
mkdir -p ~/projects/my-bip-folder/ideas ~/projects/my-bip-folder/drafts ~/projects/my-bip-folder/data
touch ~/projects/my-bip-folder/ideas/backlog.md
```

3. 开始使用以下命令：
- `show backlog`：查看待办事项列表
- `new idea`：生成新想法
- `generate post`：发布文章

## 占位符说明

在命令中，`ClawdBot` 会自动替换以下占位符：
- `{dataPath}` → 您配置的 `solobuddy.dataPath` 文件路径
- `{baseDir}` → 技能安装目录

## 数据结构

所有数据都存储在 `{dataPath}` 文件夹中：
- `ideas/backlog.md`：待办事项列表
- `ideas/session-log.md`：会话记录
- `drafts/`：正在编辑的草稿文件
- `data/my-posts.json`：已发布的文章
- `data/activity-snapshot.json`：项目活动记录（每小时更新一次）

## 语音设置

您可以通过 `solobuddyVOICE` 文件来配置语音类型。可选的语音类型包括：
- `jester-sage`：讽刺、幽默、富有哲理（默认）
- `technical`：精确、详细、条理清晰
- `casual`：友好、适合日常对话
- `custom`：使用您自己的语音文件（位于 `{dataPath}/voice.md`）

有关语音设置的详细信息，请参阅 `{baseDir}/prompts/profile.md`。

## 模块说明

### 内容生成

核心工作流程：待办事项 → 草稿 → 发布。具体规则请参阅 `{baseDir}/prompts/content.md`。

### Twitter Expert

提供针对 Twitter 的内容策略，包含对 2025 年算法趋势的见解。详情请参阅 `{baseDir}/modules/twitter-expert.md`。

### Twitter Monitor（可选）

该模块可主动关注项目在 Twitter 上的动态，并建议用户发表评论。需要 `bird` CLI 工具的支持。详情请参阅 `{baseDir}/modules/twitter-monitor.md`。

### Soul Wizard

根据项目文档生成项目的“个性特征”（即项目的独特风格或形象）。详情请参阅 `{baseDir}/references/soul-wizard.md`。

## 命令说明

### 待办事项（Backlog）

- `show backlog`：查看待办事项列表
- `new idea`：生成新的待办事项
- `add idea`：添加新的待办事项

### 会话记录（Session Log）

- `view recent`：查看最近的会话记录
- `add capture`：记录当前会话内容

### 草稿（Drafts）

- `ls {dataPath}/drafts/`：列出所有草稿文件
- `cat {dataPath}/drafts/<name>.md`：查看指定草稿的内容
- `save draft`：保存当前草稿

### 发布（Publishing）

- `generate`：生成并发布新文章
- `publish`：将草稿提交并发布到目标平台

### 项目活动（Project Activity）

- `read activity-snapshot`：查看项目活动记录，以获取战略性的参考信息
- 活动记录包含以下字段：
  - `daysSilent`：自上次提交以来的天数
  - `commitsToday/Yesterday/Week`：当天的活动频率
  - `phase`：项目当前状态（活跃/持续发展/逐渐冷却/暂停/废弃）
  - `insight`：易于理解的项目总结

**项目状态说明：**
  - `active`：今天有新的提交，项目处于活跃阶段
  - `momentum`：昨天活跃，今天活动减少（建议关注）
  - `cooling`：连续 2-3 天没有活动，可能需要关注
  - `silent`：已经 3-7 天没有活动，需要重新启动
  - `dormant`：已经超过 7 天，可能被暂停或放弃

**示例用法：**
- “sphere-777 今天有 10 次提交，可以重点关注这个项目”
- “ReelStudio 已经 5 天没有活动了，我们需要关注一下吗？”

### Telegram 集成

在 Telegram 中回复时，可以使用内联按钮来执行特定操作。

### 发送带按钮的消息

- 使用以下命令在 Telegram 中发送消息，并添加相应的按钮：
  ```bash
clawdbot message send --channel telegram --to "$CHAT_ID" --message "Text" \
  --buttons '[
    [{"text":"📋 Backlog","callback_data":"sb:backlog"}],
    [{"text":"✍️ Drafts","callback_data":"sb:drafts"}],
    [{"text":"💡 New Idea","callback_data":"sb:new_idea"}]
  ]'
```

### 回调数据格式

所有回调命令都使用前缀 `sb:`：
- `sb:backlog`：显示待办事项列表
- `sb:drafts`：列出所有草稿
- `sb:new_idea`：提示用户生成新想法
- `sb:generate:<N>`：根据编号 `N` 生成新内容
- `sb:save_draft`：保存当前草稿
- `sb:publish`：提交并发布内容
- `sb:activity`：查看项目活动记录
- `sb:twitter`：检查 Twitter 上的互动机会

### 主菜单

- 使用命令 `menu` 或 `start` 可以打开主菜单；完成某个操作后也可以通过主菜单返回。

### 内容生成流程

1. 查看待办事项列表
2. 查阅 `{baseDir}/prompts/content.md` 以获取内容生成规则
3. 查看 `{baseDir}/prompts/profile.md` 以选择合适的语音风格
4. 用配置好的语音生成内容
5. 提供保存、重新生成或返回主菜单的选项

### 项目“个性创建”（Soul Creation）

根据项目文档创建项目的独特形象或风格。触发命令为 `create soul for <path>`。

详细步骤请参阅 `{baseDir}/references/soul-wizard.md`：
1. 扫描项目中的 `.md` 文件
2. 选择项目的类型（生物/工具/指南/艺术家等）
3. 选择合适的语音风格（幽默/专业/诗意/平静/强烈等）
4. 选择项目的核心理念或特点
5. 保存生成的配置文件到 `{dataPath}/data/project-souls/<name>.json`

## 语言支持

系统会根据用户输入的语言自动调整响应内容和按钮显示语言：
- 如果用户输入俄语，系统会使用俄语响应并显示俄语按钮
- 如果用户输入英语，系统会使用英语响应并显示英语按钮