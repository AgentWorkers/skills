# ActivityClaw 插件使用说明

## 使用场景

当用户询问以下内容时，可以使用此插件：
- 最近的代理活动或操作
- 代理执行了哪些任务
- 工具使用情况跟踪或监控
- 文件操作历史（读取、写入、编辑）
- 命令执行历史
- 执行的网页搜索或数据获取操作
- 发送的消息
- 生成的子代理（sub-agent）

## 先决条件

必须已安装 ActivityClaw 插件：
```bash
npm install -g @rmruss2022/activityclaw
openclaw plugins install @rmruss2022/activityclaw
```

## 快速入门

检查 ActivityClaw 是否已安装并正在运行：
```bash
openclaw activityclaw status
```

## 命令

### 查看仪表盘
在浏览器中打开可视化活动仪表盘：
```bash
openclaw activityclaw dashboard
```
这将打开 http://localhost:18796，显示实时的活动记录。

### 检查状态
显示当前的状态和配置信息：
```bash
openclaw activityclaw status
```

### 启动/停止
手动控制该服务的运行状态：
```bash
openclaw activityclaw start
openclaw activityclaw stop
```

### 配置
重新配置端口或数据库位置：
```bash
openclaw activityclaw setup
```

## ActivityClaw 跟踪的内容

- **📝 文件操作**：创建、编辑、读取文件
- **⚡ 命令**：通过 `exec` 执行的 Shell 命令
- **🔍 网页活动**：执行的网页搜索和数据获取操作
- **💬 消息**：发送到通道的消息
- **🚀 子代理**：生成的代理会话

## 仪表盘功能

位于 http://localhost:18796 的仪表盘提供以下功能：
- **实时活动记录**：所有代理操作的实时流
- **活动筛选**：按类型（文件、命令、网页、消息）查看
- **统计信息**：总活动次数、过去一小时的活动数量、活跃的代理数量
- **自动刷新**：每 5 秒更新一次

## 示例用法

**用户询问：**“我今天处理了哪些文件？”
**回答：**
```bash
openclaw activityclaw dashboard
```
然后在仪表盘中查看 “📝 创建” 和 “✏️ 编辑” 筛选条件，以查看最近的文件操作记录。

**用户询问：**“显示最近的命令执行记录”
**回答：**
```bash
openclaw activityclaw dashboard
```
通过 “⚡ Exec” 进行筛选，查看命令执行历史。

**用户询问：**“代理最近在做什么？”
**回答：**
```bash
openclaw activityclaw status
```
系统会显示活动摘要，然后建议用户打开仪表盘查看详细信息：
```bash
openclaw activityclaw dashboard
```

## 故障排除

如果活动记录未显示：
1. 检查插件状态：`openclaw plugins list`
2. 确认服务正在运行：`openclaw activityclaw status`
3. 如果服务已停止，请重新启动：`openclaw activityclaw start`
4. 检查仪表盘地址：http://localhost:18796

如果端口已被其他程序占用：
```bash
openclaw activityclaw setup
# Choose a different port
```

## 技术细节

- **端口**：18796（默认值，可配置）
- **数据库**：存储在 `~/.openclaw/activity-tracker/activities.db` 文件中（使用 SQLite）
- **跟踪方式**：通过 `tool_result_persist` 钩子实现实时跟踪
- **数据存储**：所有数据均保存在本地

## 代码仓库

GitHub：https://github.com/rmruss2022/ActivityClaw
npm：@rmruss2022/activityclaw