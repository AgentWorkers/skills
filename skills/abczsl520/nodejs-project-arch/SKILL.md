---
name: nodejs-project-arch
description: Node.js项目架构标准，适用于AI辅助开发。该标准强制要求代码文件长度控制在400行以内，实现配置项的外部化配置、路由功能的模块化设计以及管理后台的可视化展示（admin dashboards）。适用于新项目的创建、大型单文件代码库的重构，以及当AI功能需要处理过大文件时的场景。涵盖H5游戏（如Canvas/Phaser/Matter.js）、数据采集工具（crawlers/scrapers）、内容管理系统、监控仪表盘、API服务以及SDK库等应用场景。
---
# 适用于 AI 开发的 Node.js 项目架构

该架构旨在确保文件大小适中，以便 AI 代理能够轻松地读取和编辑文件，同时不会超出其处理上下文窗口的限制。

## 核心规则

- 单个文件的最大行数为 **400 行**；`index.html` 最多为 **200 行`；`server.js` 文件（项目入口文件）最多为 **100 行**。
- 所有可配置的值都存储在 `config.json` 文件中，该文件在运行时加载，并可通过管理员控制面板进行编辑。
- 后端代码结构如下：`routes/` 用于处理不同域的请求；`services/` 用于存放通用逻辑；`db.js` 用于管理数据库。
- 前端代码仅使用 HTML 框架，JavaScript 和 CSS 代码分别存储在单独的文件中。
- 每个项目都包含 `admin.html` 和 `routes/admin.js` 文件，用于实现配置的热重载功能。

## 项目类型选择

确定项目类型后，请查阅相应的参考文档：

| 项目类型 | 所需技术栈 | 参考文档 |
|------|---------|-----------|
| **H5 游戏** | Canvas、Phaser、Matter.js、游戏循环、精灵图 | [references/game.md](references/game.md) |
| **数据工具** | 爬虫程序、数据抓取工具、调度器、数据同步、数据分析 | [references/tool.md](references/tool.md) |
| **内容/工具** | 代码生成器、库、文件处理工具 | [references/tool.md](references/tool.md) |
| **仪表板/监控系统** | 数据图表、实时数据显示、警报功能、性能指标 | [references/tool.md](references/tool.md) |
| **API 服务** | REST 端点、中间件、微服务 | [references/tool.md](references/tool.md) |
| **SDK/库** | 可共享的模块、构建流程、多客户端支持 | [references/sdk.md](references/sdk.md) |

## 快速入门（适用于所有项目类型）

1. 根据上述表格确定项目类型。
2. 阅读相应的参考文档。
3. 按照参考文档创建项目目录结构。
4. 将所有硬编码的配置值提取到 `config.json` 文件中。
5. 将较大的文件按功能拆分为多个较小的文件（每个文件不超过 400 行）。
6. 添加 `routes/admin.js` 和 `admin.html` 文件。
7. 前端代码：在启动时通过 `config.js` 文件获取配置信息（例如 `GAME_CONFIG.xxx` 或 `APP_CONFIG.xxx`）。
8. 在本地进行测试 → 备份代码 → 部署项目。

## `config.json` 文件的通用格式

```javascript
// Server: load and serve config
const config = JSON.parse(fs.readFileSync('./config.json', 'utf8'));
app.get('/api/config', (req, res) => {
  const safe = { ...config };
  delete safe.admin; // strip secrets
  res.json(safe);
});

// Admin: hot-reload
app.post('/admin/config', requireAdmin, (req, res) => {
  fs.writeFileSync('./config.json.bak', fs.readFileSync('./config.json'));
  fs.writeFileSync('./config.json', JSON.stringify(req.body, null, 2));
  Object.assign(config, req.body);
  res.json({ ok: true });
});
```

## 管理员控制面板的通用实现方式

`admin.html` 根据 `config.json` 的结构自动生成表单：
- 支持密码登录（使用 `x-admin-password` 标签进行身份验证）。
- 提供可视化配置编辑器，支持保存和热重载功能。
- 显示用户信息、数据统计以及系统运行时间等统计信息。
- 提供配置文件的备份和恢复功能。

## 为什么这很重要？

当 AI 系统读取大型文件时，会消耗大量的处理资源（即“上下文令牌”）：
- 一个包含 3000 行的文件在读取时大约会消耗 40,000 个上下文令牌（占整个处理窗口容量的 20%）。
- 一个包含 200 行的文件在读取时大约会消耗 2,700 个上下文令牌（占窗口容量的 1.3%）。
- **结论：采用这种架构后，AI 系统的处理效率可以提高 10-15 倍**（相比不进行文件拆分和压缩的情况）。