---
name: justcalendar
description: 当用户需要安装、认证或操作 Just Calendar CLI 时，请使用此技能。该 CLI 支持与 https://justcalendar.ai 进行交互，包括在 Web 界面生成代理令牌（agent token），以及通过终端命令进行日历/日期数据的管理。
---
# JustCalendar CLI 技能

## 目的

本技能为 `justcalendar` 提供了完整的操作指南。`justcalendar` 是一个 Node.js CLI 工具，用于通过以下方式管理 Google Drive 中的日历数据：

- 从 `https://justcalendar.ai` 获取后端提供的 Google Drive 访问令牌
- 直接使用 Google Drive API 读取/写入日历数据文件

使用本技能可以完成设置、登录、故障排除以及日常的 CLI 操作。

## 何时使用本技能

当用户需要执行以下操作时，请使用本技能：

- 安装或更新 `justcalendar`
- 使用在 Just Calendar 网页界面生成的令牌登录
- 添加、列出、重命名、删除或选择日历
- 设置/获取/删除日历中的日期值
- 从终端执行批量数据操作
- 故障排除令牌/认证/权限问题

## 先决条件

- Node.js 版本 `>=18`
- `npm`
- 可以访问 `https://justcalendar.ai`
- 在网页应用中已连接 Google Drive（生成令牌和执行基于 Drive 的操作需要此连接）

## 安装

通过 npm 全局安装：

```bash
npm install -g justcalendar
justcalendar --help
```

从本地项目路径安装：

```bash
cd ~/justcalendar-cli
npm install
npm install -g .
justcalendar --help
```

如果从 GitHub 安装：

```bash
git clone git@github.com:AndredAlmeida/justcalendar-cli.git
cd justcalendar-cli
npm install
npm install -g .
justcalendar --help
```

## 认证流程（网页 -> CLI）

### 第 1 步：在网页上生成令牌

1. 打开 `https://justcalendar.ai`
2. 在应用中登录并连接 Google Drive
3. 点击 **连接到您的代理**（OpenClaw 按钮）
4. 点击 **生成新令牌**
5. 立即复制令牌

重要提示：

- 令牌仅显示一次
- 生成新令牌会使之前的令牌失效
- 如果弹窗显示令牌已存在但被隐藏，请生成新令牌以获取可见的令牌

### 第 2 步：使用令牌登录 CLI

```bash
justcalendar login --token <YOUR_TOKEN> --url https://justcalendar.ai
```

验证登录：

```bash
justcalendar status
```

预期的状态包括后端 URL、令牌状态以及当前已登录的日历列表（如果认证成功）。

## CLI 数据模型说明

- 日历选择方式可以是 **日历 ID** 或 **日历名称**
- 日期格式必须严格遵循 `YYYY-MM-DD` 格式
- 数据存储在 Google Drive 中的 `JustCalendar.ai` 文件夹下
- 主配置文件：`justcalendar.json`
- 日历数据文件：`<account-id>_<calendar-id>.json`
- CLI 本地配置文件：`~/.justcalendar-cli/config.json`

## 命令参考

### 会话/认证相关命令

```bash
justcalendar login --token <TOKEN> --url https://justcalendar.ai
justcalendar logout
justcalendar status
```

### 日历相关命令

```bash
justcalendar calendars list
justcalendar calendars add "Workout" --type score --color red --display heatmap --pinned
justcalendar calendars rename "Workout" "Workout Intensity"
justcalendar calendars remove "Workout Intensity"
justcalendar calendars select "Energy Tracker"
```

日历类型选项：

- `signal-3`
- `score`
- `check`
- `notes`

颜色选项：

- `green`（绿色）、`red`（红色）、`orange`（橙色）、`yellow`（黄色）、`cyan`（青色）、`blue`（蓝色）

`score` 类型的显示选项：

- `number`（数字）、`heatmap`（热力图）、`number-heatmap`（数字热力图）

### 设置日历数据

单个日历数据的设置：

```bash
justcalendar data set "Energy Tracker" 2026-03-01 green
```

批量设置（一次调用多个 `<date> <value>` 对）：

```bash
justcalendar data set "Energy Tracker" 2026-03-01 green 2026-03-02 yellow 2026-03-03 red
```

### 删除日历数据

单个日历数据的删除：

```bash
justcalendar data delete "TODOs" 2026-03-01
```

批量删除日历数据（一次调用多个日期）：

```bash
justcalendar data delete "TODOs" 2026-03-01 2026-03-02 2026-03-03
```

### 获取日历数据

单个日历数据的获取：

```bash
justcalendar data get "Sleep" 2026-03-01
```

批量获取日历数据（一次调用多个日期）：

```bash
justcalendar data get "Sleep" 2026-03-01 2026-03-02 2026-03-03
```

## 批量操作规则（多日操作）

在处理多个日期时，建议使用 **批量命令** 而不是逐日循环执行命令。

默认使用以下批量命令格式：

- `justcalendar data set <calendar> <date1> <value1> <date2> ...`
- `justcalendar data delete <calendar> <date1> <date2> ...`
- `justcalendar data get <calendar> <date1> <date2> ...`

在请求范围涉及多天时，请使用批量命令，例如：

- 日期范围
- 整周或整月的操作
- 数据补录
- 批量修复

只有在以下情况下才使用逐日命令：

- 批量命令长度超过 shell/操作系统命令长度限制
- 需要对部分数据重新执行逐日操作

单日请求保持不变：继续使用现有的单日命令格式。

### 批量操作示例

- 一次调用完成一周的数据更新：

```bash
justcalendar data set "Energy Tracker" \
  2026-03-02 green 2026-03-03 yellow 2026-03-04 red \
  2026-03-05 green 2026-03-06 green 2026-03-07 yellow 2026-03-08 green
```

- 一次调用完成一个月的数据删除：

```bash
justcalendar data delete "TODOs" \
  2026-02-01 2026-02-02 2026-02-03 2026-02-04 2026-02-05 2026-02-06 2026-02-07 \
  2026-02-08 2026-02-09 2026-02-10 2026-02-11 2026-02-12 2026-02-13 2026-02-14 \
  2026-02-15 2026-02-16 2026-02-17 2026-02-18 2026-02-19 2026-02-20 2026-02-21 \
  2026-02-22 2026-02-23 2026-02-24 2026-02-25 2026-02-26 2026-02-27 2026-02-28
```

- 一次调用完成多天的数据验证：

```bash
justcalendar data get "Sleep" \
  2026-03-01 2026-03-02 2026-03-03 2026-03-04 2026-03-05 2026-03-06 2026-03-07
```

## 性能与一致性说明

- 批量命令可以减少 CLI/API 的开销，并降低部分数据写入的风险（相比多次逐日调用）。

## 各日历类型的值规则

### `signal-3`

`data set` 可接受的值：

- `red`（红色）
- `yellow`（黄色）
- `green`（绿色）
- `x`（其他自定义颜色）
- `clear` / `unset` / `none`（清除/取消设置）

### `score`

可接受的值：

- 整数，范围从 `-1` 到 `10`
- `-1` 表示取消设置/删除

### `check`

可接受的布尔值：

- `true`、`1`、`yes`、`on`、`checked`（表示已选中）

不可接受的值：

- `false`、`0`、`no`、`off`、`unchecked`、`clear`、`unset`、`none`（表示未选中）

### `notes`

可接受的值：

- 任何非空文本字符串（包含空格时需用引号括起）

取消设置：

- 空字符串（或使用 `data delete` 命令）

## 推荐的操作顺序

1. 检查连接是否正常：

```bash
justcalendar status
```

2. 列出所有日历：

```bash
justcalendar calendars list
```

3. 应用所需的日历/数据更改

4. 重新检查特定日期的数据：

```bash
justcalendar data get "<Calendar>" <date1> <date2> ...
```

## 故障排除

### “未登录。运行：justcalendar login ...”

- 使用有效的令牌重新登录

### “invalid_agent_token” / “missing_agent_token”

- 在网页应用中生成新令牌
- 重新运行命令：

```bash
justcalendar login --token <NEW_TOKEN> --url https://justcalendar.ai
```

### “missing_drive_scope”

- 在网页应用中重新连接 Google Drive 并批准访问权限（点击 “drive.file”）
- 生成新的代理令牌
- 在 CLI 中重新登录

### “token_refresh_failed” / “not_connected”

- 服务器上的 Google Drive 会话已过期/断开连接
- 在网页应用中重新连接 Google Drive，生成新令牌，然后重新登录

### 日期格式错误

- 必须使用精确的 `YYYY-MM-DD` 格式
- 确保日历日期有效（例如，`2026-02-30` 是无效的）

### 日历名称不明确

- 使用日历的 ID 进行操作：

```bash
justcalendar calendars list
```

## 安全性与行为说明

- `calendars remove` 命令会删除指定的日历及其关联的数据文件
- 批量 `data set`/`data delete` 操作每次调用只会执行一次最终写入操作
- 请妥善保管代理令牌，将其视为敏感信息
- 定期生成新令牌以替换旧令牌（旧令牌将失效）

## 快速入门示例

```bash
justcalendar login --token jca_... --url https://justcalendar.ai
justcalendar calendars list
justcalendar calendars add "Hydration" --type check --color cyan
justcalendar data set "Hydration" 2026-03-01 true 2026-03-02 true 2026-03-03 false
justcalendar data get "Hydration" 2026-03-01 2026-03-02 2026-03-03
```