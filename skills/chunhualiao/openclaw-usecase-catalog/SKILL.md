---
name: usecase-catalog
description: "这是一个关于人们如何使用 OpenClaw 的综合目录，涵盖了 15 个以上类别，并提供了实际案例、相关资源和灵感来源。当有人询问 OpenClaw 的使用场景、其他人正在开发的项目，或者 OpenClaw 能够实现的功能时，这个文档可以提供非常有用的信息。关键词包括：使用场景、项目创意、灵感来源、实际应用示例等。"
---
# OpenClaw 使用案例目录

这是一个精选的 OpenClaw 实际使用案例集，来源于 Twitter/X、Reddit、博客、GitHub 以及社区展示。更新日期：2026-02-04。

## 使用方法

当您的上级询问使用案例或需要灵感时，请参考以下目录以及 `findings/` 目录中的过往发现：

1. 在网上搜索新的案例（Twitter/X、Reddit、Discord、博客）。
2. 将新发现的案例保存到结构化的 `findings/YYYY-MM-DD.md` 文件中。
3. 使用 Git 提交并推送到 `{github_org}/openclaw-skill-usecases`。

### 保存使用案例（双语）

每次发现新的使用案例后，将其添加到 `findings/YYYY-MM-DD.md` 文件中（或创建新文件）。**所有案例必须提供双语版本**——先写中文，再写英文。这样您的上级可以方便地阅读中文内容，同时也能保留英文版本以供参考和搜索。

---  
然后提交并推送：
---  

---

## 1. 消息传递与沟通自动化

- **Inbox Zero**：扫描电子邮件，归档垃圾邮件，将高优先级事项汇总到每日晨报中。自动创建 Gmail 过滤器。(@andrewjiang: “这帮我清理了数百封邮件。之后还设置了一个每周的定时任务。所有操作都在 WhatsApp 上完成。”)
- **iMessage/SMS 监控**：每 15 分钟扫描一次消息记录，检测出“我明天会处理”的承诺，并自动在日历上设置提醒。(@brandon.wang)
- **群聊总结**：每日总结大量 WhatsApp/Signal 群组的聊天内容（每天超过 100 条消息），筛选出有趣的话题并忽略无关信息。
- **自动回复草稿**：在发送前草拟邮件或消息的回复内容以供审核。

## 2. 日历与日程安排

- **晨间简报**：每晚 8 点汇总第二天的日程安排——会议、准备工作、通勤时间。(@benemredoganer: “每日日历简报，通过语音在 Basecamp 中创建任务，为会议做准备。”)
- **智能冲突检测**：在发送计划信息时，自动在日历上设置“待定”事件，以避免时间冲突。
- **预约牙医/医生**：登录门户网站，根据日历可用时间和地理位置选择合适的预约时间。(@brandon.wang)
- **跨日历协调**：查看双方的日历，寻找共同的空闲时间安排晚餐。

## 3. 远程编码与开发

- **基于手机的开发**：在移动过程中通过 WhatsApp/Telegram 构建和部署代码项目。(@christinetyip)
- **在家中重建网站**：在看 Netflix 时，通过 Telegram 完整迁移网站（从 Notion 到 Astro，18 个帖子，DNS 到 Cloudflare）。(@davekiss)
- **自动部署**：运行 git 命令，通过 SSH 脚本自动将最新代码部署到测试环境。
- **代码重构**：扫描代码目录，识别需要重构的部分，并提出重构方案。
- **服务器监控**：定期检查服务器性能（htop/disk），在负载过高时通过 Telegram 发出警报。
- **GitHub 工作流程**：管理问题、Pull Request（PR），通过 Webhook 自动分配标签和关闭任务。

## 4. 价格监控与购物

- **复杂的价格提醒**：同时接收来自酒店、Airbnb 和产品的 30 多个价格提醒。支持自定义筛选条件（例如“如果床铺与其他床铺不在同一房间，则不选择该选项”）。查看房源照片进行验证。(@brandon.wang)
- **酒店/Airbnb 跟踪**：每隔几小时检查价格变化，并在价格变动时通知用户。可以评估主观因素（如房间氛围、装修质量）。
- **包裹追踪**：跟踪 USPS/FedEx 的包裹状态，每日更新进度，并标记滞留的包裹。
- **杂货价格比较**：通过浏览器自动化比较亚马逊上的商品价格，并推荐最优选择。

## 5. 智能家居与物联网

- **Home Assistant 集成**：通过自然语言实现全屋智能控制。(@WolframRvnwlf: “OpenClaw 真的是下一代工具……我的智能助手 Amy 终于可以持续在我的 Home Assistant 设备上运行了。”)
- **空气净化器/设备控制**：发现并控制 Winix、Philips Hue、Elgato 等设备。(@antonplex)
- **场景自动化**：根据 WiFi 覆盖范围和睡眠数据自动切换到家/外出/睡眠模式。
- **全面的生活管理**：通过单个 Telegram 聊天窗口管理电子邮件、Home Assistant、远程实验室、待办事项列表和购物清单。

## 6. 餐厅与预订

- **Resy/OpenTable 自动化**：登录系统（包括通过短信进行双重身份验证），逐页浏览可用房间，结合您和伴侣的日历推荐合适的选项。(@brandon.wang)
- **填写表格**：自动填写供应商表格和问卷，自动处理营销邮件。
- **航班登机**：自动完成航班登机手续，并根据目的地天气生成打包清单。

## 7. 健康与健身追踪

- **健身教练**：分析 Garmin/Apple Health 的健康数据。“你昨晚只睡了 5 小时，也许今天应该避免高强度运动。”
- **医学实验室分析**：上传血液检测报告，并提供通俗易懂的解读。
- **可穿戴设备数据仪表盘**：按需显示步数、睡眠质量和心率数据。

## 8. 家庭与生活管理

- **冰箱库存管理**：拍摄冰箱内物品的照片，AI 分析物品数量，并更新 Notion 中的清单，同时从购物清单中删除已有的物品。(@brandon.wang)
- **根据食谱生成购物清单**：截图食谱，自动将食材整理到 Apple Reminders 中。去除重复项并合并相似物品（例如“2 根胡萝卜合并为 3 根”）。
- **基于上下文的待办事项创建**：拍摄跑步鞋的照片，系统会自动关联品牌、型号和产品链接生成待办事项。
- **旅行规划**：搜索航班信息，并根据天气情况生成打包清单。

## 9. 数字机构/商业

- **单人机构**：AI “首席助理”协调所有业务操作——监控 SEO 客户、分类处理电子邮件、创建内容、管理 Shopify 账户，并在睡前审核提交的 Pull Request。(@openclaw.com.au)
- **项目管理**：整合代码、聊天记录（WhatsApp）和 Obsidian，实现无缝的项目管理工作流程。(@crossiBuilds)
- **内容创作流程**：撰写博客文章、元描述、生成报告和社交媒体内容。
- **24/7 负责人**：每日提醒、GitHub 进度跟踪，每周督促目标完成情况。(@tobi_bsf)

## 10. 人工智能电话与语音助手

- **电话通话助手**：代表您接听和拨打电话。(@steipete)
- **语音转文本**：将语音消息转录为文本并执行相应操作。
- **语音控制任务**：通过语音命令在 Basecamp 中创建任务。

## 11. 全栈生产力中心

- **统一聊天控制中心**：通过 Telegram 控制 Gmail、日历、WordPress 和 Hetzner 服务器。(@Abhay08: “通过 Telegram 如同一位老板一样管理 Gmail、日历和 WordPress。”)
- **完美的记忆助手**：记录所有对话内容，并随着时间学习用户的偏好。(@darrwalk)
- **工作流程自文档化**：自动将工作流程描述写入 Notion，并附带版本控制信息。(@brandon.wang)

## 12. 自定义技能与集成

- **按需创建技能**：“我想自动化 Todoist 的功能，OpenClaw 便在 Telegram 中为我创建了相应的技能。”(@iamsubhrajyoti)
- **ClawHub 生态系统**：在 clawhub.ai 上有 3,000 多个社区技能，其中 1,715 个被收录在 `awesome-openclaw-skills` 仓库中。
- **技能分类**：Web/Frontend（46 个）、编码工具（55 个）、Git/GitHub（34 个）、DevOps/云计算（144 个）、浏览器自动化（69 个）、图像/视频处理（41 个）、苹果应用（32 个）、搜索/研究（148 个）、命令行工具（88 个）、市场营销/销售（94 个）、生产力工具（93 个）、人工智能/大型语言模型（159 个）、笔记/项目管理（61 个）、智能家居（50 个）、通信工具（58 个）、语音助手（44 个）、健康与健身（35 个）、购物（33 个）、日历管理（28 个）、PDF 文档处理（35 个）、安全工具（21 个）、游戏（7 个）。

## 13. 内容与媒体

- **微信公众号文章插图**：使用 GPT-4o 或 GLM-Image 为文章生成插图。(@suwin-illustrator)
- **YouTube 文本转录**：利用 yt-dlp 和 Whisper API 进行视频转录和笔记记录。
- **新闻聚合**：整合 8 个以上的新闻来源（Hacker News、GitHub Trending、Product Hunt），每日提供科技资讯。
- **播客总结**：从音频内容中提取文本和关键点。
- **Remotion 视频制作**：使用 React 和 Remotion 框架制作程序化视频。

## 14. 人工智能驱动的研究

- **深度研究**：多源网络研究，合成研究报告。
- **学术论文分析**：解析 PDF 文件，解释研究结果并比较不同方法。
- **竞争情报**：监控竞争对手的网站、价格变化和产品更新。

## 15. 安全与隐私

- **本地数据存储**：所有数据都存储在本地，密钥从不发送给第三方。
- **容器化隔离**：通过沙箱环境执行任务，防止系统受损。
- **人工审核机制**：敏感操作需要明确授权。
- **专用账户策略**：使用临时账户进行集成，以限制影响范围。

---

## 来源

| 来源 | URL |
|--------|-----|
| 官方展示 | getclawdbot.com/showcase |
| OpenClaw 维基 | openclawwiki.org/blog/openclaw_clawdbot-usage-use-cases |
| Medium（10 个使用案例） | medium.com/@balazskocsis/10-clawdbot-use-cases |
| Brandon Wang 深度解析 | brandon.wang/2026/clawdbot |
| Awesome Skills（1715+ 个技能） | github.com/VoltAgent/awesome-openclaw-skills |
- 扩展程序生态系统 | help.apiyi.com/en/openclaw-extensions-ecosystem-guide-en |
- 数字机构案例 | openclaw.com.au/use-cases |
- r/OpenClaw | reddit.com/r/openclaw |
- r/OpenClawCentral | reddit.com/r/OpenClawCentral |
- ClawHub 技能库 | clawhub.ai/skills |

## 统计数据（2026 年 2 月）

- GitHub 星星评分：13.5 万+
- ClawHub 上发布的技能：3,000 多个，其中 1,715 个经过精选
- 支持的消息平台：12 个（WhatsApp、Telegram、Discord、Slack、iMessage、Signal、Google Chat、Teams、Matrix、BlueBubbles、Zalo、WebChat）
- Discord 社区：8,900 多名成员
- 相关 Reddit 子版块：5 个（r/openclaw、r/OpenClawCentral、r/openclawpirates、r/myclaw、r/OpenClawDevs）