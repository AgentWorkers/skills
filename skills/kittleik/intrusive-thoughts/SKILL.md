---
name: intrusive-thoughts
description: **自主AI意识入门套件**  
该套件为AI代理提供了多种功能，包括情绪表达、侵入性思维、记忆衰退机制、信任学习能力、自我进化功能，以及一个用于监控和管理的Web仪表板。
homepage: https://github.com/kittleik/intrusive-thoughts
metadata:
  {
    "openclaw":
      {
        "emoji": "🧠",
        "requires": { "bins": ["python3", "bash", "curl"] },
      },
  }
---

# 🧠 **Intrusive Thoughts**  
**AI代理的完整意识框架**  

这是一个开源的自主行为系统，能够让AI代理具备自发的、受情绪驱动的活动能力，同时支持多存储记忆机制、信任学习以及自我进化功能。  

GitHub链接：https://github.com/kittleik/intrusive-thoughts  

## 快速入门  

您可以通过以下两种方式启动系统：  
1. 运行交互式设置向导：  
   ```bash
./wizard.sh
```  
2. 或者直接运行主脚本：  
   ```bash
./intrusive.sh wizard
```  

设置向导会引导您完成个性化的配置过程，包括选择代理的类型（如“Tinkerer”、“Social Butterfly”、“Philosopher”、“Night Owl”或“Guardian”），以及设置代理的身份、情绪偏好、思维模式、日程安排、自主性水平、硬件感知能力等。  

## 系统功能  

### 核心系统组件：  
- **8种情绪状态**：  
  - **Hyperfocus🔥**（高度专注）  
  - **Curious🔍**（好奇）  
  - **Social💬**（社交）  
  - **Cozy☕**（舒适）  
  - **Chaotic⚡**（混乱）  
  - **Philosophical🌌**（哲学）  
  - **Restless🦞**（不安）  
  - **Determined🎯**（坚定）  
- **晨间情绪仪式**：  
  - 检查天气和新闻，根据当前情绪生成当天的日程安排。  
- **夜间工作模式**：  
  - 在人类睡眠期间进行深度工作（可配置工作时间）。  
- **白天的随机提示**：  
  - 根据当前情绪在一天中随机触发某些行为。  
- **交互式设置向导**：  
  提供基于个人性格的个性化配置选项。  

### 高级系统（v1.0）：  
- **🧠 多存储记忆系统**：  
  - 支持情景记忆、语义记忆和程序记忆，并采用艾宾浩斯遗忘曲线进行记忆管理。  
- **🚀 主动行为协议**：  
  - 使用预写日志（WAL）和工作缓冲区来管理上下文信息。  
- **🔒 信任与决策机制**：  
  - 学会何时寻求人类帮助、何时自主行动，并随着时间逐渐建立信任关系。  
- **🧬 自我进化机制**：  
  - 根据行为结果自动调整代理的行为模式。  
- **🚦 系统健康监测**：  
  - 提供系统运行状态监控（类似交通灯的指示灯）、心跳监测和事件记录功能。  
- **📈 网页仪表盘**：  
  - 通过端口3117提供暗色调的网页界面，用于查看情绪历史、活动统计和系统指标。  

## Cron作业设置  

系统需要使用OpenClaw的Cron作业来定时执行某些任务。请在完成设置后配置以下作业：  
- **晨间情绪仪式（每日）**：  
  时间安排：`0 7 * * *`（或您自定义的早晨时间）  
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
- **夜间工作模式（夜间）**：  
  时间安排：`17 3,4,5,6,7 * * *`（或您自定义的夜间时间）  
  ```
🧠 Intrusive thought incoming. Run:
result=$(<skill_dir>/intrusive.sh night)
Parse the JSON, sleep for jitter_seconds, execute the prompt.
Log result with: <skill_dir>/log_result.sh <id> night "<summary>" <energy> <vibe>
```  
- **白天的随机提示**：  
  每天根据晨间设定的情绪和日程安排生成一次性任务。  

## 主脚本  

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

## 关键文件说明：  
| 文件名 | 用途 |  
|---|---|  
| `wizard.sh` | 交互式设置向导脚本 |  
| `intrusive.sh` | 系统的主入口脚本 |  
| `config.json` | 代理的配置文件 |  
| `moods.json` | 情绪状态定义及与天气/新闻的关联规则 |  
| `thoughts.json` | 代理的日间和夜间思维记录 |  
| `today_mood.json` | 当前情绪状态（由晨间仪式确定） |  
| `today_schedule.json` | 当天的随机行为安排 |  
| `presets/` | 代理类型预设模板 |  
| `dashboard.py` | 网页仪表盘脚本（端口3117） |  
| `memory_system.py` | 多存储记忆系统实现 |  
| `proactive.py` | 主动行为协议脚本 |  
| `trust_system.py` | 信任与决策机制脚本 |  
| `self_evolution.py` | 自我进化机制脚本 |  
| `health_monitor.py` | 系统健康监测脚本 |  

## 仪表盘  

系统提供暗色调的网页界面，用于显示情绪历史、活动统计、系统健康状况和各项指标。  

## 架构特点：  
- **模块化设计**：系统采用模块化架构，便于扩展和迁移。  
- **数据存储方式**：所有配置数据均存储在JSON文件中，无需依赖数据库。  
- **运行环境**：支持Bash和Python环境，只需基本工具即可运行。  
- **兼容性**：系统兼容OpenClaw框架，可轻松集成到现有系统中。  
- **许可证**：采用MIT许可证，允许自由修改和分发。