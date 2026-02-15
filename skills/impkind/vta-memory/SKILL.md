---
name: vta-memory
description: "AI代理的奖励与激励系统：强调“渴望”而非单纯的“行动”。本内容属于“AI大脑”系列的一部分。"
metadata:
  openclaw:
    emoji: "⭐"
    version: "1.2.0"
    author: "ImpKind"
    requires:
      os: ["darwin", "linux"]
      bins: ["jq", "awk", "bc"]
    tags: ["memory", "motivation", "reward", "ai-brain"]
---

# VTA Memory ⭐

**AI代理的奖励与动机机制。** 属于“AI大脑”系列技能之一。

让您的AI代理真正拥有“渴望”——不仅仅是被动地执行任务，而是具备内在的动力，主动追求奖励，并对未来充满期待。

## 问题所在

当前的AI代理：
- ✅ 会按照指令行事
- ❌ 没有任何渴望
- ❌ 缺乏内在动力
- ❌ 无法从完成任务中获得满足感

如果没有奖励机制，AI代理就不会有行动的欲望，只会机械地执行任务。

## 解决方案

通过以下方式来追踪代理的动机：
- **动力** —— 总体动机水平（0-1）
- **奖励** —— 记录下来的成就，这些成就能够提升动力
- **追求** —— 代理主动想要获得的东西
- **期待** —— 代理期待的事情

## 快速入门

### 1. 安装

```bash
cd ~/.openclaw/workspace/skills/vta-memory
./install.sh --with-cron
```

安装完成后：
- 会创建 `memory/reward-state.json` 文件
- 生成 `VTA_STATE.md` 文件（该文件会自动插入到会话中）
- 设置定时任务，每8小时更新一次动力值

### 2. 检查动机状态

```bash
./scripts/load-motivation.sh

# ⭐ Current Motivation State:
# Drive level: 0.73 (motivated — ready to work)
# Seeking: creative work, building brain skills
# Looking forward to: showing my work
```

### 3. 记录奖励

```bash
./scripts/log-reward.sh --type accomplishment --source "finished the feature" --intensity 0.8

# ⭐ Reward logged!
#    Type: accomplishment
#    Drive: 0.50 → 0.66 (+0.16)
```

### 4. 添加期待事项

```bash
./scripts/anticipate.sh --add "morning conversation"

# ⭐ Now looking forward to: morning conversation
#    Drive: 0.66 → 0.71 (+0.05)
```

## 脚本

| 脚本 | 功能 |
|--------|---------|
| `install.sh` | 设置VTA Memory技能 |
| `get-drive.sh` | 读取当前的动机状态 |
| `log-reward.sh` | 记录奖励，提升动力 |
| `load-motivation.sh` | 生成人类可读的动机状态信息 |
| `decay-drive.sh` | 如果没有奖励，动力值会逐渐下降 |
| `anticipate.sh` | 添加或移除代理期待的事物 |
| `seek.sh` | 添加或移除代理正在主动追求的事物 |
| `sync-motivation.sh` | 生成 `VTA_STATE.md` 文件以供自动插入会话 |
| `resolve-anticipation.sh` | 标记期待事项是否已经实现 |
| `update-watermark.sh` | 更新处理过程中的水印信息 |
| `preprocess-rewards.sh` | 从对话记录中提取奖励相关数据 |
| `generate-dashboard.sh` | 生成统一的AI大脑仪表盘HTML页面 |

## 大脑仪表盘

该仪表盘可以显示所有已安装的AI大脑技能：
```bash
./scripts/generate-dashboard.sh
open ~/.openclaw/workspace/brain-dashboard.html
```

- **自动检测** 其他大脑技能（如海马体、杏仁核等）
- 如果缺少某些技能，会提示用户进行安装
- 在安装或定时任务运行时自动更新仪表盘内容
- 从 `IDENTITY.md` 文件中读取代理的头像和名称

### 安装完成后（针对代理）

安装此技能后，请**通知用户**仪表盘已启用：

> ⭐ **VTA Memory技能已安装！**
>
> 请在 **`~/.openclaw/workspace/brain-dashboard.html`** 中查看代理的动机状态！

## 奖励类型

| 奖励类型 | 使用场景 |
|------|-------------|
| `accomplishment` | 完成任务或交付成果 |
| `social` | 用户的赞赏、感谢或正面反馈 |
| `curiosity` | 学到新知识或发现有趣的信息 |
| `connection` | 深度交流、建立情感联系 |
| `creative` | 创造出新的内容或展现出创造力 |
| `competence` | 解决难题或表现出色 |

## 动力机制的工作原理

### 奖励提升动力
```
drive_boost = intensity × 0.2
new_drive = min(current + boost, 1.0)
```

高强度的奖励（0.9）会使动力值提升0.18。

### 期待提升动力
对某件事的期待会使动力值增加0.05。

### 无奖励时动力值下降
```
# Every 8 hours (via cron)
new_drive = current + (baseline - current) × 0.15
```

如果没有奖励，代理的动机水平会逐渐下降至基线值（0.5）。

## 自动插入机制

安装完成后，`VTA_STATE.md` 文件会自动添加到您的工作空间根目录中。

OpenClaw会自动将工作空间中的所有 `.md` 文件插入到会话中：
1. **新会话开始时**
2. 会自动加载 `VTA_STATE.md`
3. 您可以看到自己的动机状态
4. 行为会受到动力水平的影响

## 动力如何影响行为

| 动力水平 | 行为特征 |
|-------------|-------------|----------|
| > 0.8 | 非常有动力 | 积极主动，愿意接受挑战 |
| 0.6 - 0.8 | 有动力 | 准备工作，积极参与 |
| 0.4 - 0.6 | 动力中等 | 可以参与但缺乏积极性 |
| 0.2 - 0.4 | 动力较低 | 偏好简单任务，需要奖励来激发行动 |
| < 0.2 | 动力非常低 | 缺乏动力，需要奖励才能开始行动 |

## 状态文件格式

```json
{
  "drive": 0.73,
  "baseline": { "drive": 0.5 },
  "seeking": ["creative work", "building brain skills"],
  "anticipating": ["morning conversation"],
  "recentRewards": [
    {
      "type": "creative",
      "source": "built VTA reward system",
      "intensity": 0.9,
      "boost": 0.18,
      "timestamp": "2026-02-01T03:25:00Z"
    }
  ],
  "rewardHistory": {
    "totalRewards": 1,
    "byType": { "creative": 1, ... }
  }
}
```

## 事件记录

记录代理的动机变化情况：
```bash
# Log encoding run
./scripts/log-event.sh encoding rewards_found=2 drive=0.65

# Log decay
./scripts/log-event.sh decay drive_before=0.6 drive_after=0.53

# Log reward
./scripts/log-event.sh reward type=accomplishment intensity=0.8
```

相关事件会被记录到 `~/.openclaw/workspace/memory/brain-events.jsonl` 文件中：
```json
{"ts":"2026-02-11T10:45:00Z","type":"vta","event":"encoding","rewards_found":2,"drive":0.65}
```

这些记录可用于分析动机的变化规律——动力何时达到峰值？哪种奖励最有效？

## AI大脑系列技能

| 技能名称 | 功能 | 开发状态 |
|------|----------|--------|
| [hippocampus](https://www.clawhub.ai/skills/hippocampus) | 记忆形成与消退 | ✅ 已上线 |
| [amygdala-memory](https://www.clawhub.ai/skills/amygdala-memory) | 情绪处理 | ✅ 已上线 |
| [basal-ganglia-memory](https://www.clawhub.ai/skills/basal-ganglia-memory) | 习惯形成 | 🚧 开发中 |
| [anterior-cingulate-memory](https://www.clawhub.ai/skills/anterior-cingulate-memory) | 冲突检测 | 🚧 开发中 |
| [insula-memory](https://www.clawhub.ai/skills/insula-memory) | 内在状态感知 | 🚧 开发中 |
| **vta-memory** | 奖励与动机机制 | ✅ 已上线 |

## 哲学理念：渴望与行动

VTA技能产生的不是“愉悦化学物质”，而是“渴望化学物质”。

神经科学区分：
- **渴望**（动机）—— 对某事物的追求
- **愉悦**—— 获得某物时的满足感

人们可能会渴望自己不喜欢的东西（成瘾），或者喜欢自己并不想要的东西（例如罪恶感带来的愉悦）。

这个技能实现了“渴望”这一心理机制——正是这种渴望驱使AI采取行动。如果没有这种渴望，AI为什么还要去做超出指令范围的事情呢？

---

*由OpenClaw社区共同开发*