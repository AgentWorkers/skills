# ContextClaw 插件使用说明

## 适用场景

当用户询问以下问题时，可以使用此插件：
- 会话管理或清理
- 会话上下文的使用情况或令牌消耗情况
- 会话占用的存储空间
- 删除旧会话
- 清理无关联的会话文件
- 会话分析或统计
- 哪些会话占用了大量存储空间
- 会话中包含的消息/令牌数量

## 先决条件

必须已安装 ContextClaw 插件：
```bash
npm install -g @rmruss2022/contextclaw
openclaw plugins install @rmruss2022/contextclaw
```

## 快速入门

检查 ContextClaw 是否已安装并正在运行：
```bash
openclaw contextclaw status
```

## 命令

### 分析会话
获取所有会话的详细信息：
```bash
openclaw contextclaw analyze
```

输出内容包括：
- 总会话数、消息数、令牌数、存储空间大小
- 最大的会话（前 10 个）
- 最旧的会话（前 10 个）
- 无关联的会话（orphaned sessions）

### 删除旧会话
删除创建超过 N 天的会话（默认值：30 天）：
```bash
# Dry run (preview only, safe)
openclaw contextclaw prune --days 30

# Live run (actually deletes)
openclaw contextclaw prune --days 30 --dryRun false
```

**安全特性：**
- 默认情况下会先进行模拟删除（预览操作）
- 会保留主代理的会话
- 会保留定时任务的会话
- 删除前会显示确认提示

### 清理无关联的会话
删除 `sessions.json` 文件中未引用的会话文件：
```bash
# Dry run
openclaw contextclaw clean-orphaned

# Live run
openclaw contextclaw clean-orphaned --dryRun false
```

### 仪表板
打开会话管理可视化仪表板：
```bash
openclaw contextclaw dashboard
```
访问地址：http://localhost:18797

### 简要统计
显示会话的简要状态和统计信息：
```bash
openclaw contextclaw status
```

### 配置
重新配置端口或 OpenClaw 的安装路径：
```bash
openclaw contextclaw setup
```

## 仪表板功能

位于 http://localhost:18797 的仪表板提供以下功能：
- **会话统计**：总会话数、消息数、令牌数、存储空间
- **多种视图**：所有会话、最大会话、最旧会话、无关联会话、图表视图
- **条形图**：会话的存储空间分布
- **类型分类**：按代理类型（主代理、定时任务代理、子代理）划分的会话
- **快速操作**：通过界面直接删除或清理会话（仅提供预览功能）

## 示例用法

**用户询问：**“我的会话占用了多少存储空间？”
**回答：**
```bash
openclaw contextclaw analyze
```
请查看汇总表中的“总存储空间”指标。

**用户询问：**“清理旧会话。”
**回答：**
```bash
# First preview what would be deleted
openclaw contextclaw prune --days 30

# If approved, run live:
openclaw contextclaw prune --days 30 --dryRun false
```

**用户询问：**“哪些会话占用了最多的存储空间？”
**回答：**
```bash
openclaw contextclaw analyze
```
请查看“最大会话”表格，或直接打开仪表板：
```bash
openclaw contextclaw dashboard
```

**用户询问：**“删除无关联的会话文件。”
**回答：**
```bash
# Preview first
openclaw contextclaw clean-orphaned

# If user approves, run live:
openclaw contextclaw clean-orphaned --dryRun false
```

## 会话类型

ContextClaw 将会话分为以下几类：
- **主代理会话**（main）：不会被删除
- **定时任务会话**（cron）：不会被删除
- **子代理会话**（subagent）：可以被删除
- **未知类型会话**：无法识别的会话类型

## 无关联的会话

如果满足以下条件，会话被视为无关联的会话：
- `sessions` 目录下存在 `.jsonl` 文件
- 该会话的 ID 未出现在 `sessions.json` 文件中

常见原因：
- 完成的子代理任务从索引中移除
- 手动操作的文件
- 会话崩溃
- 开发/测试环境中的会话

无关联的会话可以安全地删除。

## 最佳实践：
1. **定期分析**：每周或每月执行一次 `openclaw contextclaw analyze` 命令
2. **始终先进行模拟删除**：删除前先预览结果
3. **调整会话删除的时长阈值**：默认为 30 天，可根据需要调整
4. **检查无关联的会话**：在删除前进行确认
5. **如有需要，请备份数据**：尽管主代理和定时任务会话受到保护

## 故障排除

如果仪表板无法加载：
```bash
openclaw contextclaw status  # Check if running
openclaw contextclaw start   # Start if stopped
```

如果端口已被其他程序占用：
```bash
openclaw contextclaw setup
# Choose a different port
```

## 技术细节：
- **端口**：18797（默认值，可配置）
- **数据解析**：解析 `~/.openclaw/agents/main/sessions/` 目录下的所有 `.jsonl` 文件
- **令牌估算**：1 个令牌约等于 4 个字符
- **存储方式**：仅读存储，不使用数据库

## 示例输出：

### 分析会话的命令示例：
```
📊 Session Analysis

┌──────────────────┬────────┐
│ Metric           │ Value  │
├──────────────────┼────────┤
│ Total Sessions   │ 45     │
│ Total Messages   │ 3,842  │
│ Total Tokens     │ 156,234│
│ Total Size       │ 12.4 MB│
│ Orphaned         │ 8      │
└──────────────────┴────────┘
```

### 删除会话的命令示例：
```
🧹 Session Pruning

⚠️  DRY RUN MODE - No files will be deleted

Sessions older than 30 days:
  ✓ Would delete: 12
  - Would keep: 33
  - Space freed: 4.2 MB

? Run prune in LIVE mode (actually delete files)? (y/N)
```

## 项目仓库
GitHub：https://github.com/rmruss2022/ContextClaw
npm：@rmruss2022/contextclaw