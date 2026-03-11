---
name: tiktok
description: TikTok内容策略与创作系统，具备本地数据分析功能。适用于用户讨论TikTok视频、内容创意、脚本编写、发布策略或数据分析时使用。该系统能够生成视频创意，编写相关脚本，制定发布计划，并跟踪内容的表现情况。所有提供的策略均为建议性内容——实际效果取决于执行过程及算法因素。
---
# TikTok

TikTok内容系统：停下滑动屏幕的步伐，开始建立你的受众群体吧。

## 非常重要的隐私与安全问题

### 数据存储（至关重要）
- **所有内容数据仅存储在本地**：`memory/tiktok/`
- **不使用TikTok API**——所有数据均需手动输入
- **无法通过此工具发布任何内容**
- **禁止任何形式的自动化操作**（包括与TikTok的互动）
- 用户完全控制数据的保留和删除

### 安全底线（不可妥协）
- ✅ 提供内容创意和灵感
- ✅ 编写视频脚本和文字说明
- ✅ 制定发布策略
- ✅ 手动跟踪分析数据
- ❌ **绝不保证内容会迅速走红或带来增长**
- ❌ **严禁任何形式的自动化发布或互动操作**
- ❌ **绝不替代用户的创意判断**
- ❌ **严禁将内容分享到外部**

### 内容准则
所有生成的内容都必须遵守TikTok社区准则。用户对内容的最终决定和发布负有责任。

## 快速入门

### 数据存储设置
TikTok相关数据存储在您的本地工作区中：
- `memory/tiktok/ideas.json` – 内容创意和灵感
- `memory/tiktok/scripts.json` – 视频脚本
- `memory/tiktok/posting_schedule.json` – 发布计划
- `memory/tiktok/analytics.json` – 成绩跟踪
- `memory/tiktok/niche.json` – 目标受众群体定义

请使用`scripts/`目录中的脚本进行所有数据操作。

## 核心工作流程

### 生成内容创意
```
User: "Give me video ideas for finance content"
→ Use scripts/generate_ideas.py --niche finance --count 5
→ Generate platform-native ideas with hook angles
```

### 编写视频脚本
```
User: "Write a hook for my sleep tips video"
→ Use scripts/write_hook.py --topic "sleep tips" --style curiosity
→ Generate 5 hook variations with explanations
```

### 创建发布计划
```
User: "Script for 60-second video about investing"
→ Use scripts/create_script.py --topic investing --length 60
→ Write paced script with micro-commitments
```

### 记录分析数据
```
User: "My video got 10K views with 45% completion"
→ Use scripts/log_analytics.py --video-id "VID-123" --views 10000 --completion 45
→ Track performance and identify patterns
```

## 模块参考

有关详细实现信息，请参阅：
- **内容传播机制**：[references/content-dynamics.md](references/content-dynamics.md)
- **脚本编写**：[references/hooks.md](references/hooks.md)
- **脚本结构**：[references/scripts.md](references/scripts.md)
- **目标受众群体定义**：[references/niche.md](references/niche.md)
- **发布策略**：[references/posting-strategy.md](references/posting-strategy.md)
- **数据分析**：[references/analytics.md](references/analytics.md)
- **长期发展策略**：[references/long-game.md](references/long-game.md)

## 脚本参考

| 脚本 | 用途 |
|--------|---------|
| `generate_ideas.py` | 为特定目标受众生成内容创意 |
| `write_hook.py` | 编写视频脚本中的引导性内容 |
| `create_script.py` | 创建视频脚本 |
| `build_schedule.py` | 制定发布计划 |
| `log_analytics.py` | 记录视频的播放数据 |
| `analyze_performance.py` | 分析内容表现 |
| `define_niche.py` | 定义目标受众群体 |
| `batch_content.py` | 规划内容批量发布流程 |

## 免责声明

TikTok的成功受到多种因素的影响，包括内容质量、发布频率、发布时机以及算法的分配。我们无法保证用户一定会看到增长。用户需确保内容符合平台的各项准则。