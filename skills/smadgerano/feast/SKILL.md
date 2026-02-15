---
name: feast
description: |
  Comprehensive meal planning system with cultural themes, authentic recipes, intelligent shopping, and surprise reveals. Use when:
  - Planning weekly meals or menus
  - Generating shopping lists
  - Asking for recipe ideas or cooking help
  - Reviewing past meals or planning ahead
  - Onboarding a new user to the meal system
  - Looking for cuisine inspiration or cultural food events
  - Tracking dietary goals or nutrition
  - Managing favourites, failures, or meal history
---

# Feast

这是一个 meal planning 工具，它将每周的烹饪活动转变为一种文化体验。

## 快速入门

1. **新用户？** 运行入职引导：“让我们设置 Feast”或“为我开启 meal planning 功能”。
2. **老用户？** 查看计划状态：“我的 meal plan 状态如何？”
3. **计划日？** 开始制定计划：“让我们规划下周的餐食”。
4. **烹饪日？** 查看当天的餐食安排：“晚餐吃什么？”

## 核心文件

用户数据存储在他们的工作区中：

```
workspace/meals/
├── profile.yaml          # User preferences (created during onboarding)
├── history.yaml          # What they've eaten
├── favourites.yaml       # Loved recipes
├── failures.yaml         # Never again
└── weeks/
    └── YYYY-MM-DD.md     # Each week's plan (self-contained)
```

**注意：** 每周的计划都是自包含的——每天的食谱、主题研究、音乐播放列表和文化背景都直接嵌入到周计划文件中。没有单独的食谱或主题文件。

## 每周的工作流程

默认时间表（可用户配置）：

| 时间 | 活动 | 触发条件 |
|-----|----------|---------|
| 星期四 | 研究与起草 | “让我们规划下周的餐食” |
| 星期五 | 确认计划 | “确认 meal plan” |
| 星期六 | 生成购物清单 | “生成购物清单” |
| 星期日 | 购物 | 用户去购物 |
| 每周结束时 | 回顾 | “回顾本周的餐食” |

## 通知

Feast 会在关键时间点发送提醒：计划日、确认计划、生成购物清单、每日餐食安排和每周回顾。这些提醒通过 cron 作业来发送。

### 通知渠道

用户可以在 `profile.yaml` 的 `schedule.notifications.channel` 配置中选择他们偏好的通知渠道：

| 渠道 | 通知方式 |
|---------|-----------------|
| `auto` | 通知当前会话或第一个可用的渠道 |
| `telegram` | 通过 Telegram 发送（需要在 OpenClaw 中配置 Telegram 频道） |
| `discord` | 通过 Discord 发送（需要在 OpenClaw 中配置 Discord 频道） |
| `signal` | 通过 Signal 发送（需要在 OpenClaw 中配置 Signal 频道） |
| `webchat` | 在聊天会话中显示通知 |

### 推送通知（可选）

为了在独立于聊天渠道的情况下向移动设备发送通知，用户可以启用推送通知：

```yaml
schedule:
  notifications:
    push:
      enabled: true
      method: "pushbullet"    # or "ntfy"
```

**支持的方法：**

- **Pushbullet** — 需要单独安装 `pushbullet-notify` 插件并配置 API 密钥 |
- **ntfy** — 使用 ntfy.sh（或自托管服务）；在个人资料中配置主题。

推送通知会作为主要通知渠道的补充发送，而不是替代它。如果推送失败，通知仍会发送到主要渠道。

### 通知时间

通知通过 OpenClaw 的 cron 系统发送，使用 `wakeMode: "next-heartbeat"`。这意味着通知会在预定时间后的心跳间隔（通常不超过 1 小时）内到达。对于大多数 meal planning 用途来说，这种轻微的延迟是可以接受的。

### 管理通知

用户可以随时调整他们的通知偏好：

- “将我的 Feast 通知改为 Telegram”
- “关闭早晨的提示”
- “启用 Pushbullet 通知”

更新通知设置时，需要使用存储的 ID 删除旧的 cron 作业，并创建新的作业。

## 工作流程

### 入职引导

请阅读 [references/onboarding.md](references/onboarding.md) 以了解完整的流程。

需要回答的关键问题：
1. 所在地（用于考虑食材的季节性、单位换算和购物地点）
2. 家庭人数及每人的食物需求
3. 每周的安排（开始日、烹饪日、休息日）
4. 饮食要求和饮食阶段
5. 厨具和烹饪能力
6. 偏好（菜系、香料、预算）

将信息保存到 `workspace/meals/profile.yaml` 中。

### 计划（星期四）

1. 查看用户个人资料
2. 查看历史记录（避免重复选择最近的食谱）
3. 查看即将到来的文化活动（参见 [references/events.md](references/events.md)）
4. 根据所在地考虑食材的季节性
5. 选择 6-7 道餐食，需满足以下条件：
   - 菜系多样性
   - 食材的重复使用
   - 营养均衡
   - 食材的易获取程度（快速准备或需要较多时间的）
6. **对于每道餐食，进行以下研究并记录：**
   - **地点**：确定具体的地域来源（细化到省份、城市或地区）。研究该地区的背景、历史和当前事件，并撰写生动的描述。
   - **菜肴**：从当地来源查找真实的食谱（使用原始语言搜索）。包括食材的来源故事、文化意义和制作方法。
   - **配乐**：精选 1-2 小时的播放列表，包含该地区的当代热门歌曲和经典/传统音乐（参见 [references/theme-research.md](references/theme-research.md)）。提供完整的曲目列表和链接。
   - **用餐环境**：提供用餐方式、饮品搭配和氛围建议。
7. 将计划草稿保存到 `workspace/meals/weeks/YYYY-MM-DD.md` 文件中（所有内容都嵌入在这个文件中）
8. 提供计划概要（仅包含主题信息，不包含完整的餐食详情）

### 确认计划（星期五）

1. 展示计划草稿并允许用户修改
2. 将计划标记为已确认
3. 设置每日餐食安排的提醒

### 生成购物清单（星期六）

1. 根据确认的计划生成购物清单
2. 优化清单：
   - 按类别分组食材
   - 合并重复使用的食材
   - 检查食材的包装规格是否满足需求
   - 标记季节性食材
3. **检查关键食材的价格**（参见 [references/price-checking.md](references/price-checking.md)：
   - 确定最昂贵的 3-5 种食材（通常是蛋白质类或特殊食材）
   - 在用户可购买的商店中比较价格
   - 记录当前的优惠活动、团购信息和使用会员卡的价格优惠
   - 在购物清单中添加价格建议
   - 提出购物策略（建议在一家商店购买或分批购买以节省费用）
4. 展示购物清单并征求用户意见
5. 允许用户修改清单
6. 将清单标记为已批准

### 每日餐食安排（星期日）

1. 确认当天是烹饪日
2. 公布完整的餐食信息：
   - 食谱（以用户选择的单位为准）
   - **主题简介：**
     - 地点的背景、历史和特色
     - 当地当前发生的事件
     - 菜品的来源故事、文化意义以及当地的食用方式
   - **精选的播放列表：**
     - 当地的热门歌曲
     - 该地区的经典/传统音乐
     - 完整的曲目列表和链接（Spotify/YouTube）
     - 用餐环境的建议和饮品搭配
3. （可选）在早晨发送提醒以增加期待感

### 回顾（每周结束时）

1. 为每道餐食评分（1-5 分）并记录反馈
2. 更新历史记录
3. 将喜欢的餐食添加到收藏列表
4. 将不成功的餐食记录到失败列表
5. 将改进意见提供给系统
6. 将回顾信息保存到周计划文件中

## 食谱的地域化处理

所有食谱都使用标准化的内部单位进行存储。在输出时，会转换为用户选择的单位：

- 温度：摄氏度 / 华氏度 / 烹饪火候标记
- 重量：公制（克/千克）/ 英制（盎司/磅）
- 体积：公制（毫升/升）/ 杯

详情请参阅 [references/conversions.md](references/conversions.md)。

## 真实性指南

在研究菜系时：
1. 尽可能使用原始语言进行搜索
2. 从当地来源查找食谱，而不仅仅是英文美食博客
3. **明确食材的具体地域来源**——例如，不是简单地写“泰国菜”，而是“北泰菜，清迈风格”
4. **研究真正来自该地区的音乐**：
   - 查找当地的流行歌曲
   - 查找经典/传统的音乐
   - 精选 1-2 小时的播放列表（而不是使用通用的 Spotify 搜索结果）
   - 参考 [references/theme-research.md](references/theme-research.md) 以获取更多指导
5. **研究该地区本身**——了解其历史、当前事件和社会背景
6. 尊重当地的饮食传统（例如，在中东菜系中不使用猪肉）
7. **将所有信息都嵌入到周计划中**——食谱、主题、音乐和背景信息都包含在同一个周计划文件中

有关各菜系的详细指南，请参阅 [references/cuisines/](references/cuisines/)。

## 模板

- [templates/profile.yaml](templates/profile.yaml) — 用户个人资料模板
- [templates/week.md](templates/week.md) — 包含食谱、主题、音乐和购物清单的周计划模板
- [templates/shopping-list.md](templates/shopping-list.md) — 独立的购物清单模板（仅供参考，通常会嵌入到周计划文件中）

## 参考资料

- [references/onboarding.md](references/onboarding.md) — 用户入职指南
- [references/theme-research.md](references/theme-research.md) — 如何研究文化主题和精选音乐
- [references/price-checking.md](references/price-checking.md) — 智能购物和价格比较指南
- [references/events.md](references/events.md) — 用于主题规划的 cultural events 日历
- [references/nutrition.md](references/nutrition.md) — 饮食阶段和均衡饮食指南
- [references/conversions.md](references/conversions.md) — 单位换算表
- [references/cuisines/](references/cuisines/) — 各菜系的研究指南
- [references/seasonality/](references/seasonality/) — 地区性食材指南

## 脚本

### 历史记录

在餐食信息公布并烹饪完成后，更新历史记录：

```bash
python scripts/update-history.py \
    --meals-dir ~/.openclaw/workspace/meals \
    --date 2026-02-03 \
    --name "Thai Green Curry" \
    --cuisine "Thai" \
    --region "Central Thailand" \
    --week-file "2026-02-02.md" \
    --rating 4 \
    --notes "Great, maybe more chilli next time"
```

这会更新 `history.yaml` 文件并自动重新计算相关统计数据。

在用户确认烹饪并评分后，运行此脚本以保持历史记录的准确性。

## 健康与营养

- 如果用户有饮食目标，记录每餐的热量摄入
- 确保每周摄入的食物种类多样化
- 遵循饮食计划（例如，减肥需要控制热量摄入）
- 标记任何营养方面的问题

详情请参阅 [references/nutrition.md](references/nutrition.md)。

## 季节性食材

在推荐食材之前，根据用户的所在地检查食材的季节性。季节性食材：
- 质量更好
- 价格通常更便宜
- 更环保

虽然不是所有食材都必须是当季的，但尽可能使用季节性食材。

有关地区性食材的更多信息，请参阅 [references/seasonality/](references/seasonality/)。