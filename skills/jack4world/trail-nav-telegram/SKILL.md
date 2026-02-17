---
name: trail-nav-telegram
description: "通过 Telegram 的位置信息提供离线徒步路线引导功能（基于 OpenClaw）。适用于构建或运行以下流程的 LLM（大型语言模型）代理：  
(1) 导入 GPX/KML 格式的路线数据；  
(2) 以低消耗令牌量的方式回答“我是否偏离了路线？/我应该往哪个方向走？”这类问题；  
(3) 从 2bulu 的 track_search 网站抓取并公开路线链接；  
(4) 为夜间徒步活动准备行程风险检查清单和装备清单。"
---
# 通过 Telegram 进行路线导航（低token消耗）

## 目标
- 使用 Telegram（iOS）作为用户界面：用户发送位置信息及简短指令。
- 将 token 消耗量降至最低：所有几何计算均通过确定性算法完成，仅使用大型语言模型（LLM）生成可选的描述性文本。
- 遵守访问控制规则：不得绕过外部网站的登录或验证码机制。

## 快速工作流程
1) **导入路线数据**（GPX/KML 格式）→ 生成简洁的 RoutePack 数据结构（包含简化后的折线路径、边界框及终点信息）。
2) **将路线数据绑定到聊天界面**（使用命令 `/use <routeId>`）。
3) **导航指引**：用户发送位置信息（或输入 `/g` + 位置坐标）→ 系统返回包含路线信息的双行文本（机器生成的内容 + 中文提示）。

## 严格的 token 节约规则
- 绝不允许将完整的 KML/GPX 数据发送给大型语言模型。
- 路线数据仅解析一次；保存 `routeId` 及简化后的坐标点信息。
- 输出数据遵循固定格式（详见参考文档 `guide-protocol.md`）。
- 为每个聊天会话维护缓存信息：`activeRouteId`、`lastIdx`。

## 外部数据获取方式（2bulu）
支持两种模式：

1) **公开数据获取（无需登录）**
- 仅从公开列表或搜索页面（如 `/track/track_search.htm`、`/track/search-<keyword>.htm`）抓取数据。
- 保存抓取到的信息：路线名称、链接及抓取时间。

2) **手动登录辅助（可选）**
- 如果用户通过微信/QQ 等平台在浏览器中登录，自动化流程可在同一登录账户下继续进行。
- 所有登录及验证码操作必须由用户本人完成，不得绕过访问控制机制。

**推荐方案（通常最简单）**：请求用户通过 Telegram 导出或发送 GPX/KML 文件，之后完全基于用户提供的路线数据进行导航。

## 安全提示
- 提供明确的“无信号/紧急求助”指引（详见参考文档 `safety-checklist.md`）。
- 对夜间徒步活动设置明确的“安全截止条件”（如时间限制、天气状况、水分补充要求）。

## 随附资源
- **脚本**：
  - `scripts/scrape_2bulu_tracks.js`：用于抓取路线信息的脚本，输出格式为 JSON/CSV 及截图。
  - `scripts/parse_2bulu_kml.js`：用于解析 KML 文件，生成统计数据和 GeoJSON 数据结构。
  - `scripts/render_route_map.js`：用于生成可分享的路线地图（HTML+PNG 格式）。
- **参考文档**：
  - `references/2bulu-notes.md`
  - `references/guide-protocol.md`
  - `references/safety-checklist.md`
  - `references/gear-list-overnight.md`