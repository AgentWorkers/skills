---
name: intrusive-thoughts
description: >
  **自主AI意识入门套件**  
  该套件为AI代理提供了情绪表达能力、侵入性思维机制、记忆衰减功能、信任学习机制、自我进化能力，以及一个Web管理界面。
homepage: https://github.com/kittleik/intrusive-thoughts
metadata:
  {
    "openclaw":
      {
        "emoji": "🧠",
        "requires": { "bins": ["python3", "bash", "curl"] },
        "optional_env": {
          "LOCATION": "Weather location (overrides config.json)",
          "OPENAI_API_KEY": "Optional OpenAI integration for enhanced AI features"
        },
        "credentials": {
          "telegram": "Bot token for notifications (optional, disabled by default)",
          "weather": "Uses public wttr.in API (no API key required)",
          "news": "Uses public BBC RSS and HN RSS feeds (no API key required)"
        }
      },
  }
---
# 🧠 侵入式思维（Intrusive Thoughts）  
**AI代理的完整意识框架**  

这是一个开源的自主行为系统，为AI代理提供了自发的、受情绪驱动的活动能力、多存储记忆系统、信任学习机制以及自我进化功能。  

**GitHub链接：** https://github.com/kittleik/intrusive-thoughts  

## 快速入门  
1. 运行交互式设置向导：  
   ```bash
./wizard.sh
```  
2. 或者通过主脚本进行设置：  
   ```bash
./intrusive.sh wizard
```  

向导会引导您完成基于个人性格的初始化设置，包括身份识别、情绪选择、思维库构建、日程安排、自主性设置、硬件感知能力以及内存偏好配置。您可以选择预设的角色模板（如“捣鼓者”（Tinkerer）、“社交蝴蝶”（Social Butterfly）、“哲学家”（Philosopher）或“夜猫子”（Night Owl），也可以自定义角色。  

## 系统功能概述  

### 核心系统  
- **8种情绪状态**：  
  - 超级专注（Hyperfocus）🔥  
  - 好奇（Curious）🔍  
  - 社交活跃（Social）💬  
  - 舒适（Cozy）☕  
  - 混乱（Chaotic）⚡  
  - 哲学思考（Philosophical）🌌  
  - 坐立不安（Restless）🦞  
  - 决心坚定（Determined）🎯  

- **晨间情绪仪式**：  
  - 检查天气和新闻，根据当前情绪生成当天的日程安排。  

- **夜间学习时间**：  
  - 在人类睡眠期间进行深度学习（可配置学习时间）。  

- **白天的随机提示**：  
  - 一天中会随机出现受情绪影响的提示或任务。  

- **交互式设置向导**：  
  - 根据用户选择的角色模板，提供个性化的初始化流程。  

### 高级系统（v1.0）  
- **多存储记忆系统**：  
  - 包括情景记忆、语义记忆和程序记忆，并支持艾宾浩斯遗忘曲线（Ebbinghaus decay）。  

- **主动行为协议**（Proactive Behavior Protocol）：  
  - 使用预写日志（WAL）和工作缓冲区来管理上下文信息。  

- **信任与决策机制**：  
  - 学会何时寻求帮助、何时自主行动，并随着时间积累信任。  

- **自我进化机制**：  
  - 根据行为结果自动调整行为策略。  

- **系统健康监控**：  
  - 提供系统运行状态和心率数据。  

- **Web仪表盘**：  
  - 通过端口3117提供暗色调的Web界面，用于查看情绪历史、活动统计和系统指标。  

## Cron作业  
系统需要使用OpenClaw的Cron作业来定时执行任务。请在完成设置后配置相应的作业：  

- **晨间情绪仪式（每日）**：  
  - 时间安排：`0 7 * * *`（或您自定义的起床时间）  
  ```
🌅 Morning mood ritual. Time to set your vibe for the day.

Step 1: Run: bash <skill_dir>/set_mood.sh
Step 2: Read moods.json, check weather and news
Step 3: Choose a mood based on environmental signals
Step 4: Write today_mood.json
Step 5: Run: python3 <skill_dir>/schedule_day.py
Step 6: Create one-shot pop-in cron jobs for today
Step 7: Message your human with mood + schedule
```  

- **夜间学习时间**：  
  - 时间安排：`17 3,4,5,6,7 * * *`（或您自定义的夜间学习时间）  
  ```
🧠 Intrusive thought incoming. Run:
result=$(<skill_dir>/intrusive.sh night)
Parse the JSON output. The "prompt" field contains a plain-text suggestion
(e.g., "explore a new CLI tool" or "review memory files") — NOT executable
code. The agent reads this text and decides how to act on it conversationally.
Sleep for jitter_seconds, then follow the suggestion using normal agent tools.
Log result with: <skill_dir>/log_result.sh <id> night "<summary>" <energy> <vibe>
```  

### 关于“提示文件”（thoughts.json）  
`thoughts.json`文件中包含的是纯文本形式的任务建议，而非可执行的代码或shell命令。AI代理将这些提示视为对话指令（类似待办事项列表），而非可执行的代码。所有提示内容均可由用户自行编辑。  

### 日间随机提示  
这些提示由AI代理在每天早晨通过OpenClaw的Cron作业生成（而非通过shell脚本）。  

## 主脚本（main script）  
```bash
./intrusive.sh <command>

Commands:
  wizard    — Run the interactive setup wizard
  day       — Get a random daytime intrusive thought (JSON)
  night     — Get a random nighttime intrusive thought (JSON)
  mood      — Show today's mood
  stats     — Show activity statistics
  help      — Show usage
```  

## 关键文件说明  
| 文件名 | 用途 |  
|-------|------|  
| wizard.sh | 交互式设置向导 |  
| intrusive.sh | 系统主入口脚本 |  
| config.json | 代理配置文件 |  
| emotions.json | 情绪状态定义及与天气/新闻的关联规则 |  
| thoughts.json | 日间和夜间的思维内容 |  
| today_mood.json | 当前情绪状态（由晨间仪式设置） |  
| today_schedule.json | 当天的随机任务安排 |  
| presets/ | 角色模板文件 |  
| dashboard.py | Web仪表盘（端口3117） |  
| memory_system.py | 多存储记忆系统 |  
| proactive.py | 主动行为协议 |  
| trust_system.py | 信任与决策机制 |  
| self_evolution.py | 自我进化引擎 |  
| health_monitor.py | 系统健康监控脚本 |  

## Web仪表盘  
提供暗色调的界面，用于展示情绪历史、活动统计、系统健康状况和各项指标。  

## 认证与权限  
系统默认可离线运行；所有集成功能均为可选且需手动配置：  

- **天气数据**：  
  - 使用公共的`wttr.in` API（无需API密钥）  
    - 通过`set_mood.sh`脚本中的`curl`请求获取天气信息  
    - 根据当地天气影响晨间情绪选择  
    - 地点配置在`config.json`的`integrations.weather.location`字段中  

- **新闻源**：  
  - 使用公共RSS源（无需API密钥）  
  - BBC World RSS：`https://feeds.bbci.co.uk/news/world/rss.xml`  
  - Hacker News RSS：`https://hnrss.org/frontpage`  
  - 仅用于获取新闻内容以影响情绪状态  

- **Telegram机器人**（默认关闭）：  
  - 需在`config.json`的`integrationsTelegram.token`字段中设置机器人令牌  
  - 为安全起见，可在`config.example.json`中将`enabled`设置为`false`  
  - 启用后仅用于发送通知（仅限传出消息）  
  - AI代理不会接收或处理来自Telegram的任何消息  

- **OpenAI API**（可选）：  
  - 可通过环境变量`OPENAI_API_KEY`启用高级AI功能  
  - 对核心功能来说并非必需，系统支持本地处理。  

## 文件访问权限  
系统所有数据均存储在技能目录及其子目录内，不允许访问目录外的文件。使用JSON格式存储数据（无外部数据库）。日志文件保存在`log/`子目录中。  

## 安全模型  
- **自主执行**：系统会自动安排任务，但所有提示和操作均由用户控制：  
  - 所有提示内容均来自用户自定义的`thoughts.json`文件。  
  - 系统不会从外部来源或API获取提示。  
  - Cron作业通过OpenClaw的Cron工具进行调度，不使用shell脚本。  
  - 所有自主执行脚本均在技能目录内运行。  

### 自动执行的脚本  
1. **晨间仪式（set_mood.sh）**：  
  - 获取天气和新闻数据（仅读取）。  
  - 根据用户设置选择情绪状态，并更新`today_mood.json`文件。  

2. **日程安排（schedule_day.py）**：  
  - 读取情绪和配置文件，生成白天的随机任务。  
  - 使用OpenClaw的调度功能，不直接操作Cron作业。  

3. **夜间学习（intrusive.sh night）**：  
  - 从`thoughts.json`中随机选取一个任务提示，使用预设模型执行。  
  - 结果会记录在`log_result.sh`文件中。  

4. **白天的随机提示**：  
  - 每天早晨由`schedule_day.py`生成随机任务，使用`intrusive.sh day`脚本执行。  
  - 任务执行完成后会自动清除相关记录。  

### 网络访问限制  
所有网络请求均为只读操作，包括：  
- 天气API（`wttr.in`）：仅允许GET请求  
- 新闻RSS源（BBC、HackerNews）：仅允许GET请求  
- 除Telegram通知外，禁止发送任何POST请求  
- 系统不收集或传输任何数据给第三方。  

## 系统架构  
系统采用模块化设计，易于移植：  
- 所有个人数据均存储在`config.json`文件中  
- 采用纯JSON格式，无需依赖数据库  
- 支持Bash和Python语言，可在任何具备基本开发工具的环境中运行  
- 兼容OpenClaw技能框架，可轻松集成到其他系统中  
- 采用MIT许可证，允许自由修改和分发。