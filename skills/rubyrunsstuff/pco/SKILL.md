# PCO CLI - 规划中心服务

这是一个用于规划中心服务 API 的命令行工具（CLI），专为 Shadow 教堂的工作（FBC Gulfport）设计。

## 仓库地址

https://github.com/rubysworld/pco-cli

## 安装方式

```
/Users/ruby/Projects/pco-cli/pco.ts
```

## 运行方式

```bash
tsx /Users/ruby/Projects/pco-cli/pco.ts <command>
```

或者，你可以创建一个别名来简化使用：
```bash
alias pco="tsx /Users/ruby/Projects/pco-cli/pco.ts"
```

## 认证

认证信息存储在 `~/.config/pco-cli/config.json` 文件中。

```bash
# Check auth status
pco auth status

# Setup (interactive)
pco auth setup

# Logout
pco auth logout
```

## 全局选项

所有列表相关的命令都支持以下选项：
- `--json`：以 JSON 格式输出（默认）
- `--table`：以表格格式输出
- `--quiet`：仅输出项目 ID
- `--limit <n>`：限制输出结果的数量（默认值：25）
- `--offset <n>`：设置结果输出的偏移量
- `--all`：获取所有页面的数据

## 命令列表

### 组织结构相关命令
```bash
pco org get                    # Get org info
```

### 服务类型相关命令
```bash
pco service-types list         # List all service types
pco st list                    # Alias
pco service-types get <id>     # Get specific service type
```

### 计划相关命令
```bash
# List plans (service-type required)
pco plans list --service-type <id>
pco plans list --service-type <id> --filter future
pco plans list --service-type <id> --filter past

# Get specific plan
pco plans get <planId> --service-type <id>
pco plans get <planId> --service-type <id> --include items,team_members
```

过滤条件：`future`（未来的）、`past`（过去的）、`after`（之后的）、`before`（之前的）、`no_dates`（无日期限制）

### 计划详情相关命令
```bash
pco items list --service-type <id> --plan <planId>
pco items get <itemId> --service-type <id> --plan <planId>
```

### 已安排的人员（团队成员）相关命令
```bash
pco scheduled list --service-type <id> --plan <planId>
```

### 人员相关命令
```bash
pco people list
pco people list --search "John Doe"
pco people get <id>
```

### 团队相关命令
```bash
pco teams list --service-type <id>
pco teams get <teamId> --service-type <id>
```

### 歌曲相关命令
```bash
pco songs list
pco songs list --search "Amazing Grace"
pco songs get <id>
pco songs arrangements <songId>
```

### 媒体相关命令
```bash
pco media list
pco media get <id>
```

### 文件夹相关命令
```bash
pco folders list
pco folders get <id>
```

### 系列相关命令
```bash
pco series list
pco series get <id>
```

### 标签组相关命令
```bash
pco tag-groups list
pco tag-groups tags <groupId>
```

### 电子邮件模板相关命令
```bash
pco email-templates list
```

### 附件类型相关命令
```bash
pco attachment-types list
```

### 报告模板相关命令
```bash
pco report-templates list
```

### 原始 API 相关命令
```bash
# Direct API access
pco api GET /service_types
pco api POST /endpoint --data '{"key": "value"}'
pco api PATCH /endpoint --file data.json
pco api DELETE /endpoint
```

## 常用工作流程

### 获取本周日的服务计划
```bash
# 1. Find service type ID
pco st list --table

# 2. Get future plans
pco plans list --service-type <id> --filter future --limit 1

# 3. Get plan details with includes
pco plans get <planId> --service-type <id> --include items,team_members
```

### 本周有哪些人被安排参与服务？
```bash
pco scheduled list --service-type <id> --plan <planId> --table
```

### 搜索歌曲
```bash
pco songs list --search "Great Are You Lord"
```

## 注意事项

- 本工具仅用于 **PCO 服务**（不包括人员管理、捐赠等相关功能）。
- API 文档请参考：https://developer.planning.center/docs/#/apps/services
- 仅适用于教堂工作，请勿与 Buape 相关的内容混淆。

---

*更新时间：2026-01-08*