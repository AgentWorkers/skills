---
name: bug-audit
description: 针对 Node.js 网络项目的全面漏洞审计服务。当用户需要审计、检查漏洞、发现安全问题或进行质量评估时，可激活该服务。该服务适用于游戏项目（使用 Canvas/Phaser/Three.js 技术）、数据工具（爬虫/调度器）、微信小程序、API 服务、仪表盘以及机器人应用。系统会根据项目特性动态生成定制的审计计划，而非使用固定的检查清单。
---
# 错误审计流程

在对任何 Node.js Web 项目进行审计之前，首先对其进行性能分析（profiling），然后选择相关的审计模块。

## 审计流程

```
Step 1: Profile → Step 2: Plan → Step 3: Execute → Step 4: Regress → Step 5: Archive
```

## 第一步：项目分析（5分钟）

阅读项目的关键文件并回答以下问题：

### 1.1 基本信息
- 项目名称
- `server.js` 文件的行数
- `index.html` 文件的行数
- 总文件数量
- 使用的框架和技术栈：Express / Socket.IO / Phaser / Three.js / 仅使用 DOM
- 数据库类型：SQLite / MySQL / PostgreSQL / 无数据库
- 最近是否有模块化重构？（模块化重构可能导致变量顺序错误）

### 1.2 类型标签（多选）

| 信号（Signal） | 标签（Tag） |
|--------|-----|
| Canvas/Phaser/物理引擎/游戏循环 | 🎮 游戏（Game） |
| 数据爬取/调度器/数据同步/Feishu 库的导入 | 📊 数据工具（Data Tool） |
| WeChat OAuth/JS-SDK/官方账户 API | 🔧 微信（WeChat） |
| Socket.IO/WebSocket 实时通信 | ⚡ 实时系统（Realtime） |
| 需要密钥认证的外部 API | 🔌 API 服务（API Service） |
- 图表/仪表板/监控 | 📈 仪表板（Dashboard） |
- 财务/交易/资产管理 | 💰 金融（Finance） |
- 管理面板/config.json 的热加载 | 🛠️ 管理（Admin） |
- 机器人/自动回复/消息处理 | 🤖 机器人（Bot） |

### 1.3 风险扫描

| 问题 | 如果是 → 重点关注 |
|----------|-------------------|
- `server.js` 文件超过 1000 行？ | 代码密度高，需先了解代码结构 |
- 用户登录/资源管理系统？ | 安全性及潜在的经济漏洞 |
- Cron 任务/定时任务？ | 任务可靠性及错误隔离 |
- 是否使用第三方 API？ | 超时处理/重试机制/备用方案 |
- 项目在微信 WebView 中运行？ | ES6 兼容性/内容分发网络（CDN）/调试问题 |
- 多玩家实时游戏？ | 并发处理/状态同步/内存泄漏 |
- 最近是否有模块化重构？ | 变量顺序问题/跨文件引用/代码回归 |
- 是否有 `config.json` 文件？ | 代码是否实际读取了该文件中的配置信息？ |

## 第二步：制定审计计划

根据项目分析的结果，从 `references/modules.md` 中选择相应的审计模块。仅阅读与项目标签匹配的模块部分。不要对每个项目都运行所有模块。

**所有项目都必须执行的模块：** S（安全审计，如果项目有用户）；D1（原子操作审计，如果项目使用数据库）；R1（部署基础审计）。

**按标签选择模块：**
- 🎮 游戏 → G1 G2 G3 G4
- 📊 数据工具 → D3
- 🔧 微信 → W1 W2 W3
- ⚡ 实时系统 → P1
- 🔌 API 服务 → A1 A2 A3
- 🤖 机器人 → B1
- 💰 金融 → D1（额外严格审计）
- 🛠️ 管理 → G4（配置验证）

**务必添加项目特定的审计内容**——这些模块只是审计的起点，而非固定范围。如果在分析过程中发现异常情况，请将其添加到审计计划中。

## 第三步：执行审计

按照风险优先级顺序执行审计任务：

```
Round 1: Quick scan (node -c syntax + HTML tag matching + obvious issues)
Round 2: Security (S modules)
Round 3: Core logic (G/D/A/B modules by type)
Round 4: User path simulation (login → core feature, full walkthrough)
Round 5: Red team (simulate attacker: resource exploits, level skipping, parameter forgery, race conditions)
Round 6: Performance + memory (P modules)
Round 7: Config + compatibility (G4/W modules)
Round 8: Deploy verification (R modules)
```

**每轮审计的输出格式：**
```
Bug N: [🔴/🟡/🟢] Brief description
- Cause: ...
- Fix: ...
- File: ...
```

**提前结束条件：** 连续两轮审计均未发现新错误 → 审计完成。
**小型项目（代码量 < 1000 行）：** 3-4 轮审计即可。
**仅包含 API 的项目（无前端代码）：** 跳过与 Web 和微信相关的审计模块。

## 第四步：回归测试与实时验证

### 回归测试（强制执行）
- 检查修复措施是否引入了新的错误
- 在进行模块化重构后，验证跨文件的变量和函数是否仍能正常使用
- 如果修改了文件 A，需要检查依赖于 A 的其他文件

### 实时测试
- 首页是否返回 200 状态码
- 关键 API 是否返回有效的 JSON 数据
- 登录流程是否正常工作
- 核心功能是否能够正常使用

## 第五步：归档审计结果

更新 `memory/projects/<project>.md` 文件中的日志：
- 记录审计日期、完成的审计轮次以及修复的错误数量
- 记录发现的重大问题（供下次审计参考）

## 参考文件

- `references/modules.md` — 所有审计模块（安全、数据、性能、游戏、微信、API、机器人、部署相关）
- `references/pitfalls.md` — 来自 30 多个项目中的 200 多个实际问题的总结，以及微信 WebView 的远程调试技巧