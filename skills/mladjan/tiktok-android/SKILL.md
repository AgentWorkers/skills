---
name: tiktok-android-bot
description: **使用ADB在Android设备上自动化TikTok互动**  
- 可搜索特定话题  
- 通过AI或预设模板发表评论  
- 配备详细的设置向导  

**适用场景**：  
- TikTok自动化营销活动  
- 通过策略性评论提升品牌在TikTok上的影响力  

**功能介绍**：  
- **自动搜索话题**：轻松找到热门或感兴趣的TikTok话题。  
- **AI辅助评论**：利用AI技术生成自然、有趣的评论内容。  
- **模板化评论**：提供多种评论模板，便于快速发布内容。  
- **便捷的设置流程**：用户可按照向导逐步完成自动化脚本的配置。  

**优势**：  
- 高效率：自动化处理大量评论任务，节省人力成本。  
- 精准定位：根据目标受众定制评论内容。  
- 增强互动性：有效提升视频的观看量和点赞数。  

**适用人群**：  
- 营销人员  
- 社交媒体运营者  
- 内容创作者  

**技术要求**：  
- 安装并配置ADB（Android Debug Bridge）工具。  
- 熟悉Android开发环境和TikTok平台规则。  

**下载与安装**：  
- 访问官方网站下载ADB工具并安装到您的Android设备上。  
- 根据官方文档配置ADB连接。  

**立即开始使用！**  
通过简单的步骤，您就能在Android设备上实现TikTok互动的自动化操作，提升您的内容传播效果。
---

# TikTok Android Bot

使用ADB在Android设备上自动化TikTok互动。无需网络爬虫，无需验证码，成功率100%。

## 功能介绍

- **交互式设置**：向导帮助首次配置
- **两种评论方式**：静态模板（快速）或AI生成（智能）
- **两种操作模式**：搜索特定主题或浏览“为你推荐”视频
- **防止重复评论**：同一视频不会被重复评论
- **灵活配置**：用户可自定义主题和评论风格

## 先决条件

- 已开启USB调试功能的Android设备
- 安装了ADB（Android调试桥）
- 设备上已登录TikTok账号
- Python 3.9及以上版本
- USB数据线

## 首次设置

该工具包含一个自动运行的交互式设置向导：

```bash
python3 tiktok_bot.py search --topics fitness --videos 5
```

**或手动进行设置：**

```bash
python3 setup.py
```

向导会询问以下内容：
1. **关注的主题**：例如“健身”、“烹饪”、“旅行”
2. **评论方式**：
   - **静态模板**：预定义的评论模板（快速、免费、无需API）
   - **AI生成**：使用Claude/GPT Vision分析视频内容（智能，每条评论费用约0.01-0.05美元）
3. **配置**：
   - 静态模板：为每个主题提供6-8条评论内容
   - AI生成：选择服务提供商（Anthropic/OpenAI/OpenRouter）并输入API密钥

设置信息将保存在`config.py`和`.env`文件中（这两个文件在Git仓库中会被忽略）。

## 使用方法

### 搜索模式 - 定位特定主题

搜索感兴趣的主题并在相关视频下发表评论：

```bash
# Single topic, 5 videos
python3 tiktok_bot.py search --topics fitness --videos 5

# Multiple topics, 3 videos each  
python3 tiktok_bot.py search --topics "fitness,cooking,travel" --videos 3

# Specify device (optional)
python3 tiktok_bot.py search --topics gaming --videos 5 --device 001431538002547
```

**操作流程：**
1. 搜索指定主题
2. 从搜索结果中打开对应的视频
3. 生成评论（AI分析或使用预设模板）
4. 发布评论
5. 返回搜索结果，继续查找下一条视频

### 浏览模式 - “为你推荐”视频

在“为你推荐”的视频列表中随机评论：

```bash
# Comment on 10 random videos
python3 tiktok_bot.py explore --videos 10
```

**操作流程：**
1. 从“为你推荐”的视频列表开始
2. （如果使用AI）分析当前视频内容，或使用预设评论模板
3. 发布评论
4. 向下滚动，查看下一条视频

## 评论方式

### 静态模板

快速、可靠，无需使用API。用户为每个主题提供6-8条评论内容。

**示例配置文件：**
```python
COMMENT_STYLE = "static"

COMMENTS_BY_TOPIC = {
    "fitness": [
        "That form looks perfect! What's your workout routine?",
        "Impressive progress! How long training?",
        # ... more variations
    ]
}
```

### AI生成

使用Claude Vision或GPT-4 Vision分析视频截图并生成相关评论。

**示例配置文件：**
```python
COMMENT_STYLE = "ai"
AI_PROVIDER = "anthropic"
AI_MODEL = "claude-3-5-sonnet-20241022"
```

**API密钥存放位置：`.env`文件**

**费用：**每条评论费用根据服务提供商不同，约为0.01-0.05美元。

## 配置文件

设置完成后，系统会生成以下文件：
- `config.py`：包含主题、评论方式和模板/AI配置信息
- `.env`：存放API密钥（仅在使用AI生成评论时需要）
- `.bot_settings.json`：保存用户偏好设置

这些文件在Git仓库中默认会被忽略。

## 设备设置

### 启用USB调试

```
Settings → About Phone → Tap "Build Number" 7 times
Settings → Developer Options → Enable "USB Debugging"
```

通过USB连接设备，并授权计算机访问设备。

### 验证连接

```bash
adb devices
# Should show: <device_id>  device

adb shell wm size
# Note screen resolution (e.g., 1080x2392)
```

## 常见问题解决

### “未找到Android设备”

```bash
adb kill-server
adb start-server
adb devices
```

如有需要，请在设备上重新授权。

### 点击搜索图标失败

系统优化了搜索图标的点击位置（适用于1080x2392分辨率的屏幕）。对于其他分辨率的屏幕：
1. 截取屏幕截图：`adb shell screencap -p /sdcard/screen.png && adb pull /sdcard/screen.png`
2. 查找搜索图标的像素位置（通常位于屏幕右上角）
3. 在`src/bot/android/tiktok_navigation.py`文件中更新相关代码：
   ```python
   search_icon_x = 995  # Your X
   search_icon_y = 205  # Your Y
   ```

详细坐标信息请参考`references/COORDINATES.md`文件。

### AI生成失败

检查以下内容：
1. `.env`文件中的API密钥是否正确
2. API密钥是否有效且已支付相应费用
3. 使用的AI模型名称是否正确
4. 如果问题依旧，系统会自动切换到使用静态评论模式

### 发布评论按钮无法使用

确保在点击“发布”按钮前关闭键盘。机器人会自动通过`KEYCODE_BACK`键关闭键盘。

## 性能

### 执行时间

- **静态模板模式**：每条视频约25秒
- **AI生成模式**：每条视频约30秒（包含5秒的分析时间）
- **完整搜索流程（5条视频）**：2-2.5分钟
- **浏览“为你推荐”视频（10条视频）**：4-5分钟

### 成功率

- 如果坐标设置正确，成功率100%
- 如果点击位置错误，成功率降为0%

### AI生成模式的费用

- Claude Vision：每条评论0.01-0.02美元
- GPT-4 Vision：每条评论0.02-0.05美元
- 发布10条评论的总费用为1-5美元

## 使用建议

### 评论质量

✅ **优质评论**：
- 包含具体的观察或问题
- 10-25个单词
- 表达出真诚的热情
- 不使用表情符号（更真实）

❌ **低质量评论**：
- 通用性的赞美语句（如“视频很棒！”）
- 垃圾信息或自我推广内容
- 过于简短的评论（如“喜欢！”）

### 使用限制

- 每个账户每天最多可发表25-30条评论
- 每天使用一次，时间间隔要随机
- 定期休息：每周休息1-2天
- 监控账号是否被TikTok限制使用

### 账号安全

- 在开始自动化操作前，确保账号已使用7天以上
- 先进行人工互动：点赞、关注、正常浏览视频
- 多样化操作：尝试不同的主题、时间和评论风格
- 从小规模开始：先测试3-5条视频

## 高级功能

### 使用OpenClaw Cron进行定时任务调度

```bash
openclaw cron add \
  --name "Daily TikTok" \
  --schedule "0 10 * * *" \
  --tz "Your/Timezone" \
  --payload '{"kind":"agentTurn","message":"cd /path/to/skill && python3 tiktok_bot.py search --topics fitness,gaming --videos 5"}'
```

### 自定义AI生成内容

编辑`config.py`文件以自定义AI生成的内容：

```python
AI_COMMENT_PROMPT = """
Analyze this video and generate a comment.
Topic: {topic}

Your custom guidelines here...
- Be enthusiastic
- Ask specific questions
- Reference visible elements
"""
```

### 多设备支持

设置`ANDROID_DEVICE_ID`环境变量：

```bash
ANDROID_DEVICE_ID=device1 python3 tiktok_bot.py search --topics fitness --videos 5
```

或使用`--device`命令参数：

```bash
python3 tiktok_bot.py search --topics fitness --videos 5 --device device1
```

## 包含的文件

```
tiktok-android-bot/
├── SKILL.md                    # This file
├── README.md                   # Comprehensive docs
├── setup.py                    # Interactive setup wizard
├── tiktok_bot.py              # Main script (CLI)
├── config.example.py          # Example configuration
├── requirements.txt           # Python dependencies
├── scripts/
│   ├── run_full_campaign.py   # Legacy: 25-video campaign
│   └── run_complete_session.py # Legacy: 3-video session
├── src/
│   ├── bot/android/
│   │   ├── tiktok_android_bot.py    # Core automation
│   │   └── tiktok_navigation.py     # Navigation flows
│   ├── ai_comments.py         # AI comment generation
│   └── logger.py              # Logging utility
└── references/
    └── COORDINATES.md         # Tap coordinate guide
```

## 所需软件

**注意：**必须安装ADB，并确保ADB在系统的PATH环境变量中。

## 许可证

本工具遵循MIT许可证——请负责任地使用。自动化评论功能可能违反TikTok的服务条款。

## 相关文档

- `README.md`：完整的使用说明
- `references/COORDINATES.md`：坐标位置自定义指南
- 主代码仓库：https://github.com/mladjan/androidSkill