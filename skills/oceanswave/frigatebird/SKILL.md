---
name: frigatebird
description: 使用 `frigatebird` npm 包，可以通过命令行界面（CLI）以类似于 `bird` 的命令格式与 X 交互，支持发布/回复/文章操作以及列表自动化功能，且无需使用 X 的 API 密钥。
argument-hint: 'whoami, read https://x.com/user/status/123, tweet "hello", article "Launch notes" "We shipped", add "AI News" @openai @anthropicai'
---

# Frigatebird 技能

Frigatebird 是一个基于 Playwright 的命令行界面（CLI）和 npm 包（`frigatebird`），它在通过浏览器会话 cookie 与 X 交互时，保留了 `bird` 命令的使用体验。

## 适用场景

- 当用户需要在 X 上使用类似 `bird` 的 CLI 功能时。
- 当用户需要通过 CLI 进行发布、回复或创建文章等操作时。
- 当用户需要自动化执行列表管理操作（如添加、删除、批量处理或查看列表）时。
- 当用户希望在不使用 API 密钥的情况下，仅通过浏览器 cookie 来操作 X 时。

## 安装与使用方法

- 通过 npm 安装：`npm install frigatebird`
- 全局安装：`npm install -g frigatebird`
- 本地使用：`npx frigatebird <命令>`

## 核心工作流程

1. 验证用户身份和会话状态：
   - `frigatebird check`
   - `frigatebird whoami`

2. 读取数据（脚本编写时使用 JSON 格式）：
   - `frigatebird read <推文 ID 或 URL> --json`
   - `frigatebird search "<查询内容>" --json`
   - `frigatebird home --json`

3. 执行数据操作：
   - `frigatebird tweet "<内容>"`
   - `frigatebird reply <推文 ID 或 URL> "<内容>"`
   - `frigatebird article "<标题>" "<正文>`

4. 自动化列表管理：
   - `frigatebird add "<列表名称>" @处理者1 @处理者2`
   - `frigatebird remove @处理者 "<列表名称>"`
   - `frigatebird batch accounts.json`

5. 对于大量数据读取，可以使用分页功能：
   - `--all`, `--max-pages`, `--cursor`, `-n`

## 支持的功能

- 发布/修改数据：`tweet`, `post`, `reply`, `article`, `like`, `retweet`, `follow`, `unfollow`, `unbookmark`
- 读取数据/时间线：`read`, `replies`, `thread`, `search`, `mentions`, `user-tweets`, `home`, `bookmarks`, `likes`, `list-timeline`, `news`, `about`
- 用户身份/状态查询：`check`, `whoami`, `query-ids`, `help`
- 列表管理：`add`, `remove`, `batch`, `lists`, `list`, `refresh`

## 关键配置选项

- 身份验证/cookie 设置：`--auth-token`, `--ct0`, `--cookie-source`, `--chrome-profile`, `--firefox-profile`
- 测试设置：`--base-url`, `--plain`, `--no-color`
- 分页设置：`-n`, `--all`, `--max-pages`, `--cursor`, `--delay`
- 输出格式：`--json`, `--json-full`
- 媒体上传：`--media`, `--alt`

## 实时端到端测试说明

- 标准的实时端到端测试默认不包含高级功能检查。
- 如需启用高级功能测试：`npm run test:e2e:live -- --list-name <列表名称> --enable-premium-features-e2e --article-cookie-source chrome --article-expected-handle-prefix <前缀>`

## 注意事项

- 该工具依赖于 X 的 Web UI 选择器；选择器的变化可能会导致功能异常。
- `query-ids` 参数仅用于保持与 `bird` 命令的兼容性，实际并不影响 Playwright 的执行逻辑。
- 原始 `bird` 中的一些 GraphQL 特性在 Playwright 模式下通过配置标志来模拟实现。