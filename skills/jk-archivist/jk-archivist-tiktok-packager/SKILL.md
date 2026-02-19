---
name: jk-archivist-tiktok-skill
description: 生成用于 TikTok 风格发布工作流的确定性 6 张幻灯片的肖像 PNG 幻灯片素材及配文文本，包括可重用的模板和严格的验证流程。
homepage: https://github.com/J-a-m-e-s-o-n/jk-archivist-tiktok-skill
metadata: {"openclaw":{"emoji":"🎬","requires":{"bins":["node","python3"]}}}
---
# JK Archivist TikTok Skill

该技能用于生成用于TikTok的6张幻灯片的 portrait 格式幻灯片素材，内容由文本驱动，且结果具有确定性。

## 该技能的用途

当您需要以下功能时，可以使用此技能：
- 无需外部图像生成即可重复使用6张幻灯片的视觉内容
- 为短视频平台提供统一的尺寸和易读的布局
- 简单的工作流程：输入幻灯片文案 -> 生成经过验证的PNG格式输出文件及标题文本
- 该工具可以作为后续上传流程的基础（例如通过Postiz）

典型使用场景：
- 品牌或创作者的介绍幻灯片
- 教育性迷你讲解视频
- 产品更新快照
- 基于故事的新闻发布序列

## 快速入门

1. 安装依赖项：
   - `python3 -m pip install -r requirements.txt`
2. （可选）自定义字体路径：
   - `export TIKTOK_FONT_PATH=/absolute/path/to/font.ttf`
3. 运行脚本：
   - `node scripts/tiktok-intro-draft.mjs`

**自定义输入方式：**
- 使用您自己的6张幻灯片文案文件：
  - `node scripts/tiktok-intro-draft.mjs --spec /absolute/path/to/spec.json`
- 通过指定主题自动生成文案：
  - `node scripts/tiktok-intro-draft.mjs --topic "your topic"`
- （可选）通过Postiz上传生成的幻灯片：
  - `node scripts/tiktok-intro-draft.mjs --postiz`

**高级配置选项：**
- `--template intro|educational|product-update|announcement`
- `--style default|high-contrast|clean|midnight`
- `--audience beginner|operator|expert`
- `--cta-pack follow-focused|link-focused|engagement-focused`
- `--hashtag-policy tcg-default|general`
- `--locale en|es|fr`
- `--ab-test caption-cta|style|template`
- `--dry-run`（仅用于编写规格和审查，不进行渲染/上传）
- `--postiz-only`（仅重新使用已生成的幻灯片进行上传）
- `--no-upload`（即使使用了`--postiz`，也强制仅保留本地文件）
- `--resume-upload`（恢复部分上传的任务）
- `--max-retries <n>`（设置最大重试次数）
- `--timeout-ms <n>`（设置超时时间）
- `--verbose`（显示详细日志）

**模板选项：**
- `intro`
- `educational`
- `product-update`
- `announcement`

**样式选项：**
- `default`
- `high-contrast`
- `clean`
- `midnight`

**目标受众选项：**
- `beginner`（初学者）
- `operator`（操作者）
- `expert`（专家）

**CTA（Call to Action）选项：**
- `follow-focus`（关注导向）
- `link-focus`（链接导向）
- `engagement-focus`（互动导向）

**标签策略选项：**
- `tcg-default`（默认策略）
- `general`（通用策略）

## 核心输出要求：
- 共6张幻灯片
- 幻灯片尺寸为1024x1536像素（portrait 格式）
- 输出格式为PNG
- 文本清晰可读，边缘有适当的间距

## 可定制的内容：
- 幻灯片上的文字内容（最多6行）
- 通过`TIKTOK FONT_PATH`自定义字体
- 标题文本的显示方式（通过模板、CTA（Call to Action）和标签来控制）
- 根据目标受众调整展示内容
- 提供A/B测试选项（用于测试不同方案）

**自定义方法：**
- 更改`slides`数组中的内容（通过`--spec` JSON文件或指定主题）
- 修改`src/node/write-caption.mjs`中的标题模板
- 调整`src/node/hashtags`和`src/node/cta`中的标签/CTA策略
- 根据目标受众调整展示内容（通过`src/node/audience`选项）
- 如果启用`--postiz`，可以自定义Postiz相关的环境变量

**规格文件格式：**
```json
{
  "slides": [
    "Slide line 1",
    "Slide line 2",
    "Slide line 3",
    "Slide line 4",
    "Slide line 5",
    "Slide line 6"
  ],
  "caption": "Optional caption override",
  "template": "intro",
  "audience": "operator",
  "ctaPack": "follow-focused",
  "hashtagPolicy": "tcg-default",
  "hashtagOverrides": ["#customtag"],
  "locale": "en",
  "ab_test": {
    "strategy": "caption-cta"
  },
  "style": {
    "preset": "default"
  }
}
```

### 自定义参数矩阵

| 需要的功能 | 可选参数 |
|---|---|
| 使用自己的幻灯片文案 | `--spec /path/spec.json` |
| 从指定主题生成文案 | `--topic "your topic"` |
- 使用预设的叙事结构 | `--template educational`（或其他模板） |
- 更改视觉样式 | `--style high-contrast` |
- 根据目标受众调整阅读难度 | `--audience beginner|operator|expert` |
- 调整CTA的行为 | `--cta-pack ...` |
- 应用标签策略 | `--hashtag-policy ...` |
- 添加自定义标签 | `--hashtag #customtag`（可重复使用） |
- 根据语言调整CTA文本 | `--locale es` |
- 生成多个备选方案 | `--ab-test caption-cta|style|template` |
- 仅保留本地文件 | 不使用`--postiz`或添加`--no-upload` |
- 通过Postiz上传生成的幻灯片 | 使用`--postiz`并设置相关环境变量 |
- 恢复部分上传的任务 | `--postiz --resume-upload` |
- 调整网络上传行为 | `--max-retries N --timeout-ms N` |
- 仅进行流程验证（不进行渲染/上传） | `--dry-run` |

## 预设配置：JK Archivist Intro（具体输出要求）

### 目标

生成一个具有确定性的6张幻灯片的TikTok介绍幻灯片（PNG格式），包含标题文本，并可选择通过Postiz将其作为TikTok的草稿或私密帖子上传。发布者可以选择热门音乐后手动发布。

### 草稿/私密上传规则（可选）：
- `privacy_level = SELF_ONLY`（仅限自己查看）
- `content_posting_method = UPLOAD`（选择上传方式）

### 幻灯片文案示例：
1. 卡片交易市场依赖于混乱的数据。
2. 价格波动不定，信号往往具有误导性。
3. 收藏者需要根据不完整的信息做出决策。
4. JK Index 是集换式卡牌（TCG）市场的智能分析工具。
5. 事实优先，避免猜测，数据公开透明。
6. 今天是Alpha版本，每周持续优化。逐步完善。👑🧱

### 标题模板示例：
TCG的价格看似确定——但仔细观察会发现问题。
JK Index 提供了真实的数据：清晰的卡片ID、实际价格、市场信号。
如果您希望获得以收藏者为中心的市场分析，就关注我们吧。👑🧱

#pokemon #tcg #cardcollecting #marketdata #startup

## 注意事项：
- 禁止提及任何代币相关内容
- 禁止使用美元符号（$）
- 禁止任何买卖提示
- 禁止使用任何预测性语言
- 禁止使用未经授权的夸张表述（如“保证”、“最准确”等）

## 必需/可选的环境变量：
- **上传Postiz相关变量：**
  - `POSTIZ_API_KEY`
  - `POSTIZ_TIKTOK_INTEGRATION_ID`
- **可选变量：**
  - `POSTIZ_BASE_URL`（默认为`https://api.postiz.com/public/v1`）
  - `TIKTOK_FONT_PATH`（字体文件的绝对路径）

## 参考文档：
- `references/setup.md`
- `references/spec-schema.md`
- `references renderer-spec.md`
- `references/outputs-and-validation.md`
- `references/troubleshooting.md`
- `references/publish-checklist.md`
- `examples/sample-slide-spec.json`