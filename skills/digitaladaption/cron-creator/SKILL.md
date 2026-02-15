---
name: cron-creator
description: "**从自然语言创建 Clawdbot 定时任务**  
**适用场景**：用户希望在不使用终端命令的情况下，安排重复发送的消息、提醒或定期检查任务。  
**示例**：  
- “创建一个每天早上 8 点的提醒”  
- “设置每周一进行一次定期检查”  
- “每 2 小时提醒我喝水”"
---

# Cron Creator

该技能能够根据自然语言请求自动为Clawdbot创建定时任务（cron jobs）。

## 快速安装（一个命令）

在终端中运行以下命令：

```bash
bash -c "$(curl -sL https://raw.githubusercontent.com/digitaladaption/cron-creator/main/install.sh)"
```

或者手动安装：

```bash
# Install skill
mkdir -p ~/.clawdbot/skills
git clone https://github.com/digitaladaption/cron-creator.git ~/.clawdbot/skills/cron-creator

# Configure and restart
clawdbot gateway restart
```

安装完成后，你可以使用类似以下的指令来创建定时任务：
- “在早上8:45创建一个每日‘Ikigai’提醒”
- “每2小时提醒我喝水”
- “设置每周一上午9点的每周检查”

## 功能介绍

1. **接收**你创建定时任务的请求
2. **解析**时间、频率、发送渠道和提醒内容
3. **自动创建**定时任务
4. **确认**任务已成功创建

## 常用指令

- “为……创建一个定时任务”
- “设置一个提醒……”
- “安排一次……”
- “提醒我……”
- “创建一个每日/每周的检查任务……”
- “添加一个重复性任务……”

## 示例

| 你输入的指令 | 执行的结果 |
|----------------|----------------------|
| “在早上8:45创建一个每日‘Ikigai’提醒” | 创建每天早上8:45的‘Ikigai’日记提醒 |
| “每2小时提醒我喝水” | 创建每小时一次的喝水提醒 |
| “设置每周一上午9点的每周检查” | 创建每周一上午9点的每周检查任务 |
| “每天早上7点叫我起床” | 创建每天早上7点的闹钟/提醒 |
| “每天早上6:30给我发送一条名言” | 创建每天早上6:30发送名言的提醒 |

## 支持的时间格式

| 你输入的指令 | Cron表达式 |
|----------------|----------------------|
| “8am” | `0 8 * * *` |
| “8:45am” | `45 8 * * *` |
| “9pm” | `0 21 * * *` |
| “noon” | `0 12 * * *` |
| “midnight” | `0 0 * * *` |

## 支持的频率

| 你输入的指令 | Cron表达式 |
|----------------|----------------------|
| “daily” / “every day” | 每天指定时间 |
| “weekdays” | 周一至周五指定时间 |
| “mondays” / “every monday” | 每周一 |
| “hourly” / “every hour” | 每小时 |
| “every 2 hours” | 每2小时 |
| “weekly” | 每周（默认为周一） |
| “monthly” | 每月1日 |

## 发送渠道

只需在指令中指定渠道：
- “在WhatsApp上发送” → 通过WhatsApp发送
- “在Telegram上发送” → 通过Telegram发送
- “在Slack上发送” → 通过Slack发送
- “在Discord上发送” → 通过Discord发送
默认发送渠道：WhatsApp

## 默认提醒内容

该技能会自动生成合适的提醒内容：
- **Ikigai**：包含每日目标、饮食、运动、社交互动和感恩内容的提醒
- **喝水**：“💧 该喝水了！保持水分！🚰”
- **早晨**：“🌅 早上好！是时候进行每日检查了。”
- **晚上**：**🌙 晚上好！今天过得怎么样？”
- **每周**：每周目标回顾
- **默认**：**⏰ 你的定时提醒已发送！**

## 使用方法

1. 安装该技能（参见上面的快速安装说明）
2. 自然地发送指令，例如：“在早上8点创建一个提醒”
3. 完成后，定时任务会自动创建

## 开发者指南

### 相关文件

- `SKILL.md`：本文档
- `scripts/cron_creator.py`：自然语言解析脚本
- `install.sh`：自动安装脚本

### 解析流程

`cron_creator.py`脚本会：
- 从自然语言指令中提取时间、频率、发送渠道和提醒内容
- 生成相应的`clawdbot cron add`命令
- 返回包含解析结果和命令的JSON数据

### 手动测试

```bash
# Test the parser
python3 scripts/cron_creator.py "Create a daily reminder at 8:45am"

# Output includes:
# - parsed time, frequency, channel
# - generated cron expression
# - full clawdbot cron add command
```

### 配置说明

安装脚本会自动配置以下内容：
- `clawdbot tools.exec.host=gateway`（用于运行Clawdbot命令）
- 技能文件存储在`~/.clawdbot/skills/cron-creator`目录下
- 需要重启gateway以应用配置更改

### 常见问题解答

- **技能无法加载？**  
  ```bash
clawdbot skills list | grep cron
```

- **定时任务未创建？**  
  ```bash
# Check clawdbot is running
clawdbot status

# Check cron jobs
clawdbot cron list
```

- **需要重新安装？**  
  ```bash
# Run install again
bash -c "$(curl -sL https://raw.githubusercontent.com/digitaladaption/cron-creator/main/install.sh)"
```

## 项目仓库

该项目托管在GitHub上：  
https://github.com/digitaladaption/cron-creator  

欢迎在GitHub上报告问题或贡献代码！