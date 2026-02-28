---
name: sxsw-skill
description: >
  **SXSW 2026 日程查询、活动搜索、演讲者信息及推荐**  
  适用于用户查询关于 SXSW 活动、会议环节、音乐演出、电影放映、演讲者、场地或日程安排的信息。  
  **功能说明：**  
  - **日程查询**：可快速查找 2026 年 3 月 12 日至 18 日在德克萨斯州奥斯汀举行的 SXSW 大会及各类节日的具体时间安排。  
  - **活动搜索**：通过关键词或类别筛选相关活动。  
  - **演讲者信息**：查看每位演讲者的背景资料、演讲主题及简介。  
  - **活动推荐**：根据用户兴趣提供个性化的活动推荐。  
  **使用场景：**  
  - 当用户询问 SXSW 的具体活动时  
  - 当用户需要了解会议或节日的详细安排时  
  - 当用户对特定演讲者或表演感兴趣时  
  **适用领域：**  
  - SXSW 参与者  
  - 软件开发者  
  - 文化活动爱好者  
  - 媒体工作者  
  **注意事项：**  
  - 本工具提供实时更新的 SXSW 日程信息。  
  - 若数据更新不及时，建议用户直接访问 SXSW 官网或官方应用程序获取最新信息。
homepage: "https://github.com/brianleach/sxsw-skill"
license: MIT
metadata:
  clawdbot:
    emoji: "🎸"
    tags: [sxsw, austin, conference, schedule, events, music, film, tech, speakers]
    requires:
      bins: ["node"]
      env: []
    files: ["scripts/sxsw.ts"]
    install: []
---
# SXSW 2026 日程查询技能

实时查询 SXSW 2026 的日程安排、搜索活动信息、查看演讲者资料，并为 3 月 12 日至 18 日在德克萨斯州奥斯汀举行的会议和节庆活动提供推荐。

## 使用场景

- 用户询问 SXSW 2026 的日程、活动、分会场或演讲者信息
- 用户询问“今天/明天/[特定日期] SXSW 有什么活动？”
- 用户希望获得 SXSW 的活动推荐、必看的活动或主题演讲
- 用户询问 SXSW 的场馆位置或活动时间
- 用户询问音乐演出、电影放映或喜剧活动
- 用户询问 SXSW 上的特定演讲者或主题
- 用户提出与 SXSW 2026 相关的任何问题
- 用户提到 SXSW、South by Southwest 或奥斯汀三月会议

## 数据来源

该技能采用“优先使用本地数据”的策略，使用预先抓取的日程数据集：

| 数据源 | 类型 | 说明 |
|--------|------|-------------|
| `data/sxsw-2026-schedule.json` | 本地 JSON | 包含 3,400 多个活动的完整日程 |
| `data/sxsw-2026-index.json` | 本地 JSON | 搜索索引（按日期、主题、场馆、形式、演讲者、关键词分类） |
| 网络搜索 | 实时 | 用于补充日程变更、取消信息或突发新闻 |

### 何时使用网络搜索

在以下情况下，使用网络搜索来补充本地数据集：
- 用户询问日程变更、取消信息或最后一刻添加的活动
- 用户询问新闻、公告或 SXSW 的突发新闻
- 查询内容在本地数据集中找不到
- 活动日期在 48 小时内（SXSW 的活动经常在最后一刻发生变化）

## 实现方式

### 快速入门

```bash
node scripts/sxsw.ts info           # dataset overview
node scripts/sxsw.ts today          # today's events
node scripts/sxsw.ts recommend      # keynotes & featured sessions
```

### 脚本用法

`scripts/sxsw.ts` 中的 CLI 支持以下命令：

```bash
# List/filter events
node scripts/sxsw.ts events --date 2026-03-14
node scripts/sxsw.ts events --track "AI"
node scripts/sxsw.ts events --venue "JW Marriott"
node scripts/sxsw.ts events --format "keynote"
node scripts/sxsw.ts events --search "machine learning"
node scripts/sxsw.ts events --search "climate" --date 2026-03-15 --verbose

# Speaker search
node scripts/sxsw.ts speakers --search "Amy Webb"

# Browse
node scripts/sxsw.ts venues
node scripts/sxsw.ts tracks
node scripts/sxsw.ts today
node scripts/sxsw.ts tomorrow
node scripts/sxsw.ts recommend
node scripts/sxsw.ts info
```

可以组合使用各种过滤条件。添加 `--verbose` 选项可显示详细信息和演讲者详情。添加 `--limit N` 可限制结果数量。

## 关键日期参考

| 日期 | 星期 | 备注 |
|------|-----|-------|
| 2026-03-12 | 星期四 | 开幕日——主题演讲和特色分会场开始 |
| 2026-03-13 | 星期五 | 全部节目开始，电影首映式启动 |
| 2026-03-14 | 星期六 | 最高峰日——所有分会场同时进行 |
| 2026-03-15 | 星期日 | 音乐演出活动增多 |
| 2026-03-16 | 星期一 | 音乐节进入高潮 |
| 2026-03-17 | 星期二 | 会议最后一天，音乐活动继续 |
| 2026-03-18 | 星期三 | 结束日 |

## 用户使用提示

- 询问具体日期：例如：“3 月 12 日有什么活动？”
- 询问主题：例如：“这周有哪些关于 AI 的分会场？”
- 询问演讲者：例如：“Mark Rober 什么时候演讲？”
- 请求推荐：例如：“有哪些必看的主题演讲？”
- 询问场馆：例如：“星期六在 Convention Center 有哪些活动？”
- 组合使用过滤条件：例如：“星期五在 Paramount 有哪些电影放映？”

## 响应格式

- 对于“[特定日期] 有什么活动？”的查询：按时间段分组显示活动，并注明场馆信息
- 对于演讲者查询：显示演讲者的所有分会场、时间和场馆信息
- 对于主题/分场查询：按日期/时间排序显示相关活动
- 对于推荐请求：突出显示主题演讲、特色分会场和现场对话环节
- 在引用具体活动时，务必提供 `schedule.sxsw.com` 的活动链接
- 当列出多个活动时，优先显示最相关的活动，并注明总数

## 奥斯汀当地信息

由于用户可能在 SXSW 期间身处奥斯汀：
- Convention Center 位于 500 E Cesar Chavez St（原名为 Convention Center Blvd）
- JW Marriott、Hilton、Fairmont 是主要的酒店场馆——均位于市中心，步行即可到达
- 音乐演出活动集中在 6th Street、Red River Cultural District 和 Rainey Street 区域
- SXSW 期间 CapMetro 免费（包括 Red Line 地铁和公交车）
- 可使用 capmetro-skill 获取交通信息
- SXSW 期间共享出行服务的接送点会有所变动——请查看 sxsw.com/attend 获取地图信息

## 错误处理

- 如果无法加载数据文件，报告错误并建议重新运行数据抓取程序
- 如果搜索没有结果，建议扩大查询范围或尝试使用网络搜索
- 如果用户询问的数据不在数据集中，使用网络搜索查找答案

## 外部接口

| 接口 | 发送的数据 | 接收的数据 |
|----------|-----------|---------------|
| 网络搜索（由代理发起） | 搜索查询文本 | 用于查询日程变更、取消信息或突发新闻的结果 |

该技能脚本本身不进行网络请求——它们仅读取本地的 JSON 数据文件。但是，技能说明指导代理在本地数据不足时使用内置的网络搜索功能（例如，最后一刻的日程变更、查询未在数据集中找到）。

## 安全性与隐私

- 不需要 API 密钥或凭证
- 技能脚本不进行任何外部网络请求
- 不收集或传输用户数据
- 所有数据仅从预先抓取的本地 JSON 文件中读取
- 数据来源公开可在 schedule.sxsw.com 查看

## 信任声明

该技能读取的是预先抓取的 SXSW 2026 公开日程副本。它不进行网络请求，不需要 API 密钥，也不存储用户数据。可以通过运行附带的抓取程序来更新数据。