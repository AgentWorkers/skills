# 日常灵修自动技能

这是一个为 OpenClaw 设计的自动化日常灵修生成工具。它能够获取新闻、根据新闻内容生成灵修内容、使用您的声音录制视频，并自动上传到 YouTube。

## 概述

**daily-devotional-auto** 提供了灵修内容生成的完整自动化流程：
- 基于新闻的上下文获取（国内/国际）
- 人工智能驱动的灵修内容生成
- 使用 ElevenLabs 的文本转语音（TTS）技术进行自定义语音朗读
- 通过可视化效果制作视频
- 自动上传视频到 YouTube 并管理播放列表
- 监控 YouTube 评论以获取用户主题建议
- 通过 cron 表达式实现每日定时执行

## 特点

### 📰 基于新闻的内容
- 获取当前的国内和国际新闻
- 根据实时新闻生成相关的灵修内容
- 选择具有灵性意义的故事
- 保持与信仰内容相匹配的语气

### 💬 用户建议
- 监控 YouTube 评论中的主题请求
- 支持的关键词包括：“suggest”（建议）、“topic”（主题）、“pray for”（为……祈祷）、“devotional about”（关于……的灵修）、“question about”（关于……的问题）、“help with”（需要帮助）、“request”（请求）
- 在内容生成中优先考虑用户的建议
- 如果使用了用户的建议，会在视频描述中注明来源

### 🎙️ 您的声音
- 使用您在 ElevenLabs 注册的定制语音进行朗读
- 预先配置好您的语音 ID
- 提供专业质量的音频输出
- 所有视频中的语音效果保持一致

### 🎬 自动视频制作
- 为视频生成与灵修主题相关的标题
- 制作音频可视化效果（蓝色波形图）
- 包含圣经引用和日期信息
- 在视频中注明用户的建议来源
- 优化以适应 YouTube 的播放体验

### 📤 自动上传
- 使用正确的元数据上传视频到 YouTube
- 将视频设置为公开状态
- 自动添加到您的灵修播放列表中
- 包含包含圣经引用和背景信息的描述
- 可以设置发布时间

### ⏰ 每日定时
- 在美国山区标准时间（MST）上午 9:00 自动运行（可配置）
- 通过系统 cron 表达式确保定时执行的可靠性
- 记录所有操作以供调试
- 可通过可选的 webhook 接收错误通知

## 设置

### 1. 先决条件
```bash
# Ensure youtube-studio is installed and configured
cd ~/clawd/skills/youtube-studio
npm install
# Run auth once for YouTube access
node scripts/auth-handler.js
```

### 2. 安装依赖项
```bash
cd ~/clawd/skills/daily-devotional-auto
npm install
```

### 3. 环境配置
```bash
cp .env.example .env
# Edit .env with your credentials:
```

**必需变量：**
- `NEWS_API_KEY` - 从 https://newsapi.org 获取（免费 tier 可用）
- `ELEVENLABS_API_KEY` - 从 https://elevenlabs.io 获取
- `YOUTUBE_CHANNEL_ID` - 您的 YouTube 频道 ID（格式：UCxxxxxxxxxx）
- `VOICE_ID` - 您在 ElevenLabs 注册的定制语音 ID

**可选变量：**
- `DEVOTIONAL_PLAYLIST_ID` - 用于存放灵修视频的特定播放列表（未设置时自动创建）
- `WEBHOOK_URL` - 用于接收错误通知的 Slack/Discord webhook 地址
- `LOG_LEVEL` - 调试、信息、警告、错误（默认：info）

### 4. 设置 cron 定时
```bash
# Edit crontab
crontab -e

# Add this line to run daily at 9:00 AM MST
0 9 * * * ~/clawd/skills/daily-devotional-auto/run-daily.sh

# Or using local time (replace TZ as needed)
TZ=America/Denver 0 9 * * * ~/clawd/skills/daily-devotional-auto/run-daily.sh
```

### 5. 验证设置
```bash
# Test manually (generates one devotional)
npm start

# Check logs
tail -f ~/.openclaw-devotional/logs/devotional.log
```

## 命令

### 生成灵修内容（手动）
```bash
npm start
# Generates, creates video, and uploads one devotional
```

### 检查评论中的建议
```bash
node scripts/check-comments.js
# Scans recent comments for user topic suggestions
# Prioritizes suggestions for next run
```

### 仅生成内容（不上传）
```bash
DRY_RUN=true npm start
# Creates files but doesn't upload to YouTube
```

### 调试模式
```bash
DEBUG=* npm start
# Verbose logging for troubleshooting
```

## 视频输出格式

每个生成的视频包含：

```
Title: Daily Devotional - [Theme] ([Date])
Duration: ~3-5 minutes
Content:
  - Title card with date
  - News hook / context
  - Devotional message
  - Scripture reference(s)
  - Viewer suggestion credit (if applicable)
  - Call to action
Audio: Your custom ElevenLabs voice
Visual: Blue waveform visualizer
```

示例文件名：`devotional-2024-02-05.mp4`

## 人工智能生成细节

### 提示结构
1. **背景信息：** 当前新闻/事件
2. **主题：** 基于新闻的灵性视角
3. **圣经引用：** 相关的圣经经文
4. **应用指导：** 实际的灵性建议
5. **行动号召：** 对观众的鼓励

### 生成选项（在 `.env` 文件中设置）
- `DEVOTIONAL_TONE` - 严肃、鼓励、反思、指导性
- `DEVOTIONAL_LENGTH` - 短（1-2 分钟）、中（3-4 分钟）、长（5 分钟以上）
- `TARGET_AUDIENCE` - 一般观众、家庭用户、年轻人、专业人士

## YouTube 集成

### 播放列表管理
- 如果不存在“Daily Devotionals”播放列表，则自动创建
- 将生成的每个视频添加到播放列表中
- 保持视频的顺序
- 处理播放列表的配额限制

### 评论监控
```javascript
// Check for suggestion keywords
const suggestionKeywords = [
  'suggest', 'topic', 'pray for',
  'devotional about', 'question about',
  'help with', 'request'
];
```

### 元数据
- 描述中包含：
  - 新闻背景信息
  - 圣经引用
  - 用户的建议（如果有的话）
  - 鼓励观众参与的提示
  - 频道链接

## 错误处理

| 错误情况 | 处理方式 |
|----------|----------|
| 新闻 API 失败 | 使用备用灵性主题 |
| 视频生成失败 | 跳过当前任务，继续执行后续步骤 |
| YouTube 上传失败 | 记录错误，下次尝试时重试 |
| 语音 API 失败 | 使用系统默认的 TTS 服务 |
| cron 定时失败 | 记录错误，可以手动触发任务 |

## 文件结构

```
daily-devotional-auto/
├── SKILL.md                               # This file
├── README.md                              # User guide
├── .env.example                           # Configuration template
├── package.json                           # Dependencies
├── LICENSE                                # MIT license
├── .gitignore                             # Exclude secrets
├── run-daily.sh                           # Cron script
├── scripts/
│   ├── daily-devotional.js                # Main automation
│   ├── check-comments.js                  # Comment scanner
│   └── devotional-generator.js            # Content generation
└── config/
    └── prompts.json                       # AI prompt templates
```

## 配置示例

### 简短的晨间灵修视频
```bash
DEVOTIONAL_LENGTH=short
DEVOTIONAL_TONE=encouraging
DEVOTIONAL_TIME=06:00  # 6 AM
```

### 较长的晚间反思视频
```bash
DEVOTIONAL_LENGTH=long
DEVOTIONAL_TONE=reflective
DEVOTIONAL_TIME=18:00  # 6 PM
```

### 不依赖新闻的灵修内容
```bash
USE_NEWS_CONTEXT=false
# Uses preset inspirational themes instead
```

## 性能与配额

### YouTube API 配额
- 每个视频的上传量：约 1,600 单位
- 评论检索量：1 单位
- 播放列表操作量：每次操作 1-3 单位
- **每日配额：** 1,000,000 单位（足以生成 600 多个视频）

### 处理时间
- 新闻获取：约 2 秒
- 内容生成：约 10-30 秒（取决于 AI 模型）
- 视频制作：约 30-60 秒
- 上传：约 1-5 分钟（取决于文件大小和网络连接）
- **每个视频的总处理时间：** 约 2-6 分钟

### 存储需求
- 每个视频占用空间：约 50-200 MB（临时文件，上传后删除）
- 日志文件：约 1 MB
- 配置文件：<1 MB

## 故障排除

### “未找到新闻”
```bash
# Check NEWS_API_KEY is valid
# Verify API subscription tier allows requests
# Check internet connection
# Enable DEBUG mode for details
```

### 视频上传失败
```bash
# Check YouTube quota: youtube-studio quota-status
# Verify YOUTUBE_CHANNEL_ID is correct
# Check network connectivity
# Try smaller video (reduce LENGTH setting)
```

### 未检测到评论
```bash
# Verify YOUTUBE_CHANNEL_ID matches owner account
# Check channel comment settings allow comments
# Run: node scripts/check-comments.js --verbose
# Ensure channel has public videos with comments
```

### cron 定时未执行
```bash
# Test crontab: crontab -l
# Check system time: date
# Verify script permissions: chmod +x run-daily.sh
# Check cron logs: log stream --predicate 'eventMessage contains "cron"'
# Test manually: ~/clawd/skills/daily-devotional-auto/run-daily.sh
```

### 视频质量不佳
```bash
# Increase resolution in video-generator
# Check voice quality settings in .env
# Verify ffmpeg is installed: which ffmpeg
# Try different tone/length combinations
```

## API 参考

### 新闻 API (newsapi.org)
- 免费 tier：每天 100 次请求
- 高级 tier：无请求限制
- 支持的国家：60 多个
- 支持的语言：30 多种

### ElevenLabs TTS
- 定制语音：需要购买语音克隆服务
- 标准语音：预置的语音选项
- 音质等级：高音质（24kHz）、超高音质（48kHz）

### YouTube Data API v3
- 每天配额：1,000,000 单位
- 每个项目每秒的请求限制：1,000 次
- 视频文件大小限制：小于 256 GB

## 高级用法

### 批量生成（每周一次）
```bash
for i in {1..7}; do
  npm start
  sleep 300  # 5 minute delay between videos
done
```

### 自定义定时
```bash
# Instead of 9 AM daily, run on specific days:
# Run Monday through Friday at 8 AM
0 8 * * 1-5 ~/clawd/skills/daily-devotional-auto/run-daily.sh
```

### 上传前备份
```bash
DRY_RUN=true npm start
# Review generated videos in output folder
# Manually verify quality
npm start  # Upload after verification
```

## 未来计划
- [ ] 支持多语言
- [ ] 提供多种语音选项
- [ ] 自动生成视频缩略图
- [ ] 集成分析功能
- [ ] 收集观众互动数据
- [ ] 管理内容发布日程
- [ ] 提供批量调度接口
- [ ] 集成云存储服务

## 许可证

MIT 许可证 - 可在 OpenClaw 生态系统中自由使用

## 支持

如遇问题，请参考以下步骤：
1. 确认 `.env` 文件中的配置是否正确
2. 查看 `~/.openclaw-devotional/logs/` 目录下的日志文件
3. 单独测试各个组件（新闻 API、TTS 等）
4. 启用 DEBUG 模式以获取详细日志信息
5. 查看 GitHub 上的 issue：https://github.com/Snail3D/daily-devotional-auto/issues