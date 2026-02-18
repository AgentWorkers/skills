---
name: trail-nav-telegram
description: "通过 Telegram 的位置信息提供离线徒步路线引导功能（基于 OpenClaw）。适用于构建或运行以下功能的 LLM（大型语言模型）代理工作流程：  
(1) 导入 GPX/KML 格式的路线数据；  
(2) 以低计算成本（即使用少量计算资源）回答“我是否偏离了路线？我应该往哪个方向走？”这样的问题；  
(3) 从 2bulu 的 track_search 网站抓取并公开分享路线链接；  
(4) 为夜间徒步活动准备行程风险检查清单和装备清单。"
---
# 通过 Telegram 进行路线导航（低token消耗）

## 目标
- 使用 Telegram（iOS）作为用户界面：用户发送位置信息及简短指令。
- 将 token 消耗降至最低：所有几何计算均通过确定性算法完成，仅使用大型语言模型（LLM）生成可选的文字描述。
- 遵守访问控制规则：不得绕过外部网站的登录/验证码机制。

## 快速工作流程
1) **导入路线数据**（GPX/KML）→ 构建简洁的 RoutePack 数据结构（包含简化后的折线路径、边界框及终点信息）。
2) **将路线数据绑定到聊天界面**（使用命令 `/use <routeId>`）。
3) **提供导航指导**：用户发送位置信息（或输入 `/g` + 位置坐标），系统会回复两条信息的导航提示（机器生成的文本 + 中文模板）。

## 降低 token 消耗的规则
- 绝不要将完整的 KML/GPX 数据发送给大型语言模型。
- 路线数据只需解析一次；保存 `routeId` 及简化后的位置点信息。
- 输出数据遵循固定格式（详见参考文档 `guide-protocol.md`）。
- 为每次聊天会话维护缓存状态：`activeRouteId`、`lastIdx`。

## 外部数据获取方式（2bulu）
支持两种模式：

1) **公开数据获取（无需登录）**
- 仅抓取公开的路线列表/搜索页面内容（例如 `/track/track_search.htm`、`/track/search-<keyword>.htm`）。
- 保存抓取到的信息：路线名称、网址及抓取时间。

2) **手动登录辅助（可选）**
- 如果用户在浏览器中手动登录（微信/QQ 等），自动化流程可以在该登录账号下继续进行。
- 登录/验证码步骤必须由用户完成，不得绕过任何访问控制机制。

**推荐方案（通常最简单）**：请求用户通过 Telegram 导出或发送 GPX/KML 文件，之后完全基于用户提供的文件进行导航操作。

## 安全提示
- 提供明确的“无信号”/紧急求助指南（详见参考文档 `safety-checklist.md`）。
- 对夜间徒步活动设置明确的“强制停止条件”（如时间限制、天气状况、水分补充等）。

## 配置资源
- **脚本文件**：
  - `scripts/scrape_2bulu_tracks.js`：用于抓取路线列表页面的数据，输出格式为 JSON/CSV，并生成截图。
  - `scripts/parse_2bulu_kml.js`：解析 KML 数据，生成统计信息、地理 JSON 数据及 RoutePack 结构。
  - `scripts/render_route_map.js`：将路线信息渲染为 HTML+PNG 格式的地图供分享。
  - `scripts/render_route_map_annotated.js`：将带有注释的地图数据（GeoJSON 格式）渲染为 HTML+PNG 格式。
  - `scripts/guide_route.js`：根据 GeoJSON 数据及当前位置生成详细的导航提示（包含 2-4 条指令）。
  - `scripts/weather_alert.js`：根据 Open-Meteo 数据提供天气变化警报（适用于日间徒步、山顶露营或越野跑模式）。
  - `scripts/outsideclaw_setup.sh`：通过一条命令将 outsideclaw 仓库安装到用户系统的 `~/.outsideclaw/app/outsideclaw` 目录。
  - `scripts/generate_openclaw_snippet.js`：生成指向已安装 outsideclaw 插件的配置片段。
  - `scripts/patch_openclaw_config.js`：修改 OpenClaw 配置文件以包含该插件的路径（同时生成备份文件）。
  - `scripts/openclaw_oneclick_setup.sh`：一键完成 outsideclaw 的安装及配置更新（可选重启）。

**参考文档**：
- `references/2bulu-notes.md`
- `references/guide-protocol.md`
- `references/safety-checklist.md`
- `references/gear-list-overnight.md`
- `references/qiniangshan_alerts.json`：基于风险的节点警报信息（用于地图标注和警报触发）。
- `references/route-alerts.md`：警报信息的格式及应用方法。
- `references/share-bundles.md`：用于在多个 outsideclaw 用户端之间共享路线数据包。
- `references/outsideclaw-integration.md`：安装 outsideclaw 仓库并生成 OpenClaw 配置片段。
- `references/openclaw-oneclick.md`：一键完成 OpenClaw 的集成（包括安装、配置更新及可选的重启操作）。