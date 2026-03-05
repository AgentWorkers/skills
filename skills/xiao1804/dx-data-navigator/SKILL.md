---
name: dx-data-navigator
description: 通过 DX Data MCP 服务器的 PostgreSQL 数据库查询开发者体验（Developer Experience, DX）相关数据。此技能适用于分析开发者生产力指标、团队绩效、代码审查指标、部署频率、事件数据、AI 工具使用情况、调查反馈、DORA 指标以及任何工程分析场景。当遇到关于 DX 评分、团队对比、周期时间、代码质量、开发者情绪、AI 编码助手使用情况、冲刺速度或工程关键绩效指标（KPIs）的问题时，可使用该技能进行数据查询。
---
# DX 数据导航器

## 安装

```bash
npx skills add pskoett/pskoett-ai-skills/dx-data-navigator
```

使用 `mcp__dx-mcp-server__queryData` 工具查询 DX Data Cloud 的 PostgreSQL 数据库。

## 工具使用方法

```
mcp__dx-mcp-server__queryData(sql: "SELECT ...")
```

如果不确定表名或列名，请务必先查询 `information_schema.columns`：

```sql
SELECT column_name, data_type FROM information_schema.columns
WHERE table_name = 'table_name' ORDER BY ordinal_position;
```

## 重要提示：团队相关表格

系统中共有三种团队表格，请根据实际需求选择正确的表格：

| 表格 | 使用场景 |
|-------|----------|
| `dx_teams` | 当前组织结构，用于关联用户和团队，以便查看 PR/部署指标 |
| `dx_snapshot_teams` | DX 调查快照中的团队信息（用于获取 DX 评分） |
| `dx_versioned_teams` | 指定日期的历史团队结构 |

**用于获取 DX 调查评分：** 通过 `dx_snapshot_teams` 表进行关联。使用 `GROUP BY` 语句避免重复记录（团队名称可能在多个快照中出现）：
```sql
SELECT st.name as team, i.name as metric, MAX(ts.score) as score, MAX(ts.vs_industry50) as vs_industry
FROM dx_snapshot_team_scores ts
JOIN dx_snapshot_teams st ON ts.snapshot_team_id = st.id
JOIN dx_snapshot_items i ON ts.item_id = i.id AND i.snapshot_id = ts.snapshot_id
WHERE ts.snapshot_id = (SELECT id FROM dx_snapshots ORDER BY end_date DESC LIMIT 1)
  AND st.name = 'Your Team Name'
  AND i.item_type = 'core4'
GROUP BY st.name, i.name;
```

**按团队查看 PR/部署指标：** 通过 `dx_users` 表与 `dx_teams` 表进行关联：
```sql
SELECT t.name, COUNT(*) as prs
FROM pull_requests p
JOIN dx_users u ON p.dx_user_id = u.id
JOIN dx_teams t ON u.team_id = t.id
WHERE p.merged IS NOT NULL GROUP BY t.name;
```

## 查找团队名称

查询数据库以获取可用的团队列表：
```sql
SELECT name FROM dx_teams WHERE deleted_at IS NULL ORDER BY name;
```

## 数据领域

### 核心 DX 指标

包含团队评分、基准测试结果和情感分析数据的调查快照。

**相关表格：** `dx_snapshots`, `dx_snapshot_teams`, `dx_snapshot_items`, `dx_snapshot_team_scores`

**`dx_snapshots` 表的字段：** id, account_id, contributors, participation_rate, start_date (日期), end_date (日期)

**`dx_snapshot_teams` 表的字段：** id, snapshot_id, team_id, name, parent (布尔值), flattened_parent, contributors, participation_rate

**`dx_snapshot_items` 表的字段：** id, snapshot_id, name, item_type, prompt, target_label

**`dx_snapshot_team_scores` 表的字段：** id, snapshot_id, snapshot_team_id (外键，关联 `dx_snapshot_teams` 表的 id), team_id (外键，关联 `dx_teams` 表的 id), item_id (外键，关联 `dx_snapshot_items` 表的 id), score, vs_org, vs_prev, vs_industry50, vs_industry75, vs_industry90, unit

**`dx_snapshot_items` 中的项类型：**
- `core4`：有效性、影响力、质量、速度
- `kpi`：交付难度、参与度、每周时间损失、质量、速度
- `sentiment`：深度工作、变更信心、文档编写、跨团队协作、客户关注度、决策能力等
- `workflow`：评审等待时间、持续集成/持续交付（CI/CD）等待时间、部署频率、PR 合并频率、人工智能节省的时间、官僚主义等
- `workflow_averages`：工作流程指标的原始平均值（实际数值，非百分位数）
- `csat`：工具满意度评分（例如代码编辑器、问题跟踪工具等）

```sql
-- Latest snapshot info
SELECT id, start_date, end_date, contributors, participation_rate
FROM dx_snapshots ORDER BY end_date DESC LIMIT 1;

-- Team scores for specific metric (use GROUP BY to dedupe)
SELECT st.name as team, i.name as metric, MAX(ts.score) as score, MAX(ts.vs_industry50) as vs_industry
FROM dx_snapshot_team_scores ts
JOIN dx_snapshot_teams st ON ts.snapshot_team_id = st.id
JOIN dx_snapshot_items i ON ts.item_id = i.id AND i.snapshot_id = ts.snapshot_id
WHERE ts.snapshot_id = (SELECT id FROM dx_snapshots ORDER BY end_date DESC LIMIT 1)
  AND st.name = 'Your Team Name'
  AND i.item_type = 'core4'
GROUP BY st.name, i.name;

-- All teams comparison on one metric
SELECT st.name as team, MAX(ts.score) as score, MAX(ts.vs_industry50) as vs_industry
FROM dx_snapshot_team_scores ts
JOIN dx_snapshot_teams st ON ts.snapshot_team_id = st.id
JOIN dx_snapshot_items i ON ts.item_id = i.id AND i.snapshot_id = ts.snapshot_id
WHERE ts.snapshot_id = (SELECT id FROM dx_snapshots ORDER BY end_date DESC LIMIT 1)
  AND i.name = 'Effectiveness' AND i.item_type = 'core4'
  AND st.parent = false
GROUP BY st.name
ORDER BY score DESC NULLS LAST;
```

### 团队与用户

组织结构、团队层级结构以及用户信息。

**相关表格：** `dx_teams`, `dx_users`, `dx_team_hierarchies`, `dx_groups`

**`dx_teams` 表的字段：** id, name, contributors, deleted_at

**`dx_users` 表的字段：** id, name, email, team_id, ai_light_adoption_date, ai_moderate_adoption_date, ai_heavy_adoption_date

```sql
-- Teams with contributor counts
SELECT name, contributors FROM dx_teams WHERE deleted_at IS NULL ORDER BY contributors DESC;

-- Users with AI adoption status
SELECT name, email, ai_heavy_adoption_date FROM dx_users
WHERE ai_heavy_adoption_date IS NOT NULL ORDER BY ai_heavy_adoption_date DESC;

-- Team members
SELECT u.name, u.email FROM dx_users u
JOIN dx_teams t ON u.team_id = t.id
WHERE t.name = 'Your Team Name';
```

### 提交请求（Pull Requests）

包括周期时间、评审等待时间和处理量在内的 PR 指标。

**相关表格：** `pull_requests`, `pull_request_reviews`, `repos`

**`pull_requests` 表的字段：** id, dx_user_id, repo_id, title, base_ref, head_ref, additions, deletions, created, merged, closed, draft, bot_authored

**关键指标（所有指标单位为秒，除以 3600 可转换为小时）：**
- `open_to_merge`：PR 的总周期时间
- `open_to_first_review`：首次评审所需时间
- `open_to_first_approval`：通过审批所需时间
- **营业时间相关指标**：在字段名后添加 `_business_hours` 后缀

```sql
-- PR metrics by team last 30 days
SELECT t.name, COUNT(*) as prs,
       AVG(p.open_to_merge)/3600 as avg_hours_to_merge,
       AVG(p.open_to_first_review)/3600 as avg_hours_to_first_review
FROM pull_requests p
JOIN dx_users u ON p.dx_user_id = u.id
JOIN dx_teams t ON u.team_id = t.id
WHERE p.merged IS NOT NULL AND p.created > NOW() - INTERVAL '30 days'
GROUP BY t.name ORDER BY prs DESC;

-- PR size distribution
SELECT
    CASE
        WHEN additions + deletions < 50 THEN 'XS (<50)'
        WHEN additions + deletions < 200 THEN 'S (50-199)'
        WHEN additions + deletions < 500 THEN 'M (200-499)'
        ELSE 'L (500+)'
    END as size_bucket,
    COUNT(*) as count,
    AVG(open_to_merge)/3600 as avg_hours
FROM pull_requests
WHERE merged IS NOT NULL AND created > NOW() - INTERVAL '90 days'
GROUP BY size_bucket ORDER BY avg_hours;
```

### 部署与事件

部署频率、成功率以及事件跟踪（用于 DORA 指标的统计）。

**相关表格：** `deployments`, `incidents`, `incident_services`

**`deployments` 表的字段：** id, service, repository, environment, deployed_at, success, commit_sha

**`incidents` 表的字段：** id, name, priority, source, source_url, started_at, resolved_at, started_to_resolved (秒), deleted

**部署环境：** dev（开发环境）、stage（测试环境）、prod（生产环境）
**事件优先级：** '1 - 关键', '2 - 高', '3 - 中等', '4 - 低', '5 - 规划'
**事件来源：** 可通过 `SELECT DISTINCT source FROM incidents` 查看所有可能的事件来源

```sql
-- Deploy frequency by environment
SELECT environment, COUNT(*) FROM deployments
WHERE deployed_at > NOW() - INTERVAL '30 days' GROUP BY environment;

-- Deployment success rate
SELECT
    COUNT(*) as total,
    COUNT(*) FILTER (WHERE success) as successful,
    COUNT(*) FILTER (WHERE success)::float / COUNT(*) * 100 as success_rate
FROM deployments WHERE deployed_at > NOW() - INTERVAL '30 days';

-- Mean Time to Recovery (MTTR)
SELECT AVG(started_to_resolved)/3600 as avg_hours_to_resolve
FROM incidents
WHERE resolved_at IS NOT NULL AND priority IN ('1 - Critical', '2 - High');

-- Incidents by priority
SELECT priority, COUNT(*) FROM incidents
WHERE started_at > NOW() - INTERVAL '90 days' AND deleted = false
GROUP BY priority ORDER BY priority;
```

### 人工智能工具

跟踪人工智能编码辅助工具（如 GitHub Copilot）的使用情况。

**相关表格：** `ai_tools`, `ai_tool_daily_metrics`, `github_copilot_daily_usages`, `github_users`

**`github_copilot_daily_usages` 表的字段：** id, login, date, enterprise_slug, active (布尔值)

**`github_users` 表的字段：** id, login, verified_emails, bot, active

**将 Copilot 与团队关联：** GitHub 用户的登录信息与 DX 系统中的用户邮箱不直接匹配。请使用 `github_users.verified_emails` 字段进行关联：
```sql
-- Copilot usage by team (via github_users email linking)
SELECT t.name as team, COUNT(DISTINCT c.login) as active_copilot_users
FROM github_copilot_daily_usages c
JOIN github_users gu ON c.login = gu.login
JOIN dx_users u ON gu.verified_emails = u.email
JOIN dx_teams t ON u.team_id = t.id
WHERE c.date > NOW() - INTERVAL '30 days' AND c.active = true
GROUP BY t.name ORDER BY active_copilot_users DESC;
```

```sql
-- Daily Copilot active users (overall)
SELECT date, COUNT(*) FILTER (WHERE active) as active_users
FROM github_copilot_daily_usages
WHERE date > NOW() - INTERVAL '30 days'
GROUP BY date ORDER BY date;

-- Copilot adoption rate (latest day)
SELECT
    COUNT(DISTINCT login) FILTER (WHERE active) as active_users,
    COUNT(DISTINCT login) as total_users,
    COUNT(DISTINCT login) FILTER (WHERE active)::float / COUNT(DISTINCT login) * 100 as adoption_pct
FROM github_copilot_daily_usages
WHERE date = (SELECT MAX(date) FROM github_copilot_daily_usages);

-- Weekly trend
SELECT DATE_TRUNC('week', date) as week,
       COUNT(DISTINCT login) FILTER (WHERE active) as active_users
FROM github_copilot_daily_usages
WHERE date > NOW() - INTERVAL '90 days'
GROUP BY week ORDER BY week;
```

### 问题跟踪

项目管理数据，包括问题、冲刺计划和周期时间（例如 Jira 系统）。

**相关表格：** `jira_issues`, `jira_projects`, `jira_sprints`, `jira_issue_sprints`, `jira_issue_types`, `jira_statuses`

**`jira_issues` 表的字段：** id, key, summary, story_points, cycle_time (秒), created_at, completed_at, project_id, status_id, issue_type_id, user_id

**`jira_sprints` 表的字段：** id, name, state ('active', 'closed', 'future'), start_date, end_date, complete_date

```sql
-- Sprint velocity (last 5 closed sprints)
SELECT s.name, SUM(i.story_points) as points, COUNT(*) as issues
FROM jira_sprints s
JOIN jira_issue_sprints jis ON s.id = jis.sprint_id
JOIN jira_issues i ON jis.issue_id = i.id
WHERE s.state = 'closed' AND i.completed_at IS NOT NULL
GROUP BY s.id, s.name ORDER BY s.complete_date DESC LIMIT 5;

-- Issue cycle time by type
SELECT it.name as issue_type, COUNT(*) as issues, AVG(i.cycle_time)/3600 as avg_hours
FROM jira_issues i
JOIN jira_issue_types it ON i.issue_type_id = it.id
WHERE i.completed_at IS NOT NULL AND i.completed_at > NOW() - INTERVAL '90 days'
GROUP BY it.name ORDER BY issues DESC;
```

### 服务目录

包含服务、团队、领域和所有权信息的目录系统。

**相关表格：** `dx_catalog_entities`, `dx_catalog_entity_owners`, `dx_catalog_entity_types`

**`dx_catalog_entities` 表的字段：** id, name, identifier, entity_type_identifier, description

**实体类型：** service（服务）、team（团队）、domain（领域）（请查看 `entity_type_identifier` 字段）

```sql
-- Services count by owning team
SELECT t.name as team, COUNT(*) as services
FROM dx_catalog_entity_owners eo
JOIN dx_catalog_entities e ON eo.entity_id = e.id
JOIN dx_teams t ON eo.team_id = t.id
WHERE e.entity_type_identifier = 'service'
GROUP BY t.name ORDER BY services DESC;

-- List services with owners
SELECT e.name as service, e.identifier, t.name as owner_team
FROM dx_catalog_entities e
JOIN dx_catalog_entity_owners eo ON e.id = eo.entity_id
JOIN dx_teams t ON eo.team_id = t.id
WHERE e.entity_type_identifier = 'service'
ORDER BY t.name, e.name;
```

### 流程与代码质量

CI/CD 流程的执行情况以及代码质量指标（例如 SonarCloud）。

**相关表格：** `pipeline_runs`, `sonarcloud_issues`, `sonarcloud_projects`, `sonarcloud_project_metrics`

**`pipeline_runs` 表的字段：** id, status, started_at, completed_at, duration

```sql
-- Pipeline success rate
SELECT COUNT(*) as runs,
       COUNT(*) FILTER (WHERE status = 'success') as successful,
       COUNT(*) FILTER (WHERE status = 'success') * 100.0 / COUNT(*) as success_pct
FROM pipeline_runs WHERE started_at > NOW() - INTERVAL '30 days';

-- Pipeline duration trend
SELECT DATE_TRUNC('week', started_at) as week,
       AVG(duration)/60 as avg_minutes
FROM pipeline_runs WHERE started_at > NOW() - INTERVAL '90 days'
GROUP BY week ORDER BY week;
```

### 问题数据

来自源代码控制平台（例如 GitHub Issues）的问题数据。

**相关表格：** `issues`, `github_issues`, `github_issue_labels`, `github_labels`

**`issues` 表的字段：** id, source, dx_user_id, title, status, created, completed, cycle_time

```sql
-- Issue throughput
SELECT DATE_TRUNC('week', completed) as week, COUNT(*) as completed
FROM issues WHERE completed > NOW() - INTERVAL '90 days'
GROUP BY week ORDER BY week;
```

### 文档与知识库

文档和知识库活动记录（例如 Confluence、Wiki）。

**相关表格：** `confluence_spaces`, `confluence_pages`, `confluence_page_versions`, `confluence_users`, `confluence_page_labels`

**`confluence_spaces` 表的字段：** id, name, external_key, space_type, status, source_url, created_at

**`confluence_pages` 表的字段：** id, page_id, author_id, title, status, views_count, created_at, updated_at

**`confluence_page_versions` 表的字段：** id, page_id, version_number, author_id, created_at

## 数据质量说明

**注意事项：**
- 有些团队名称可能存在拼写错误，请通过查询 `dx_teams` 表来核实名称的准确性。
- `incident_services` 表可能为空，这意味着事件无法与特定服务关联。
- `dx_users` 表中的 AI 采用日期字段大多为空值，建议使用 `github_copilot_daily_usages` 表代替。
- DX 调查评分可能存在重复记录，请在使用数据时始终使用 `GROUP BY` 语句并结合 `MAX()` 函数进行去重处理。

## 常见查询模式

### DORA 指标

```sql
-- Deployment Frequency (daily average, production only)
SELECT COUNT(*)::float / 30 as deploys_per_day FROM deployments
WHERE deployed_at > NOW() - INTERVAL '30 days' AND environment IN ('prod', 'production');

-- Lead Time for Changes (PR cycle time)
SELECT
    AVG(open_to_merge)/3600 as avg_hours,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY open_to_merge)/3600 as median_hours
FROM pull_requests
WHERE merged IS NOT NULL AND created > NOW() - INTERVAL '30 days';

-- Mean Time to Recovery
SELECT AVG(started_to_resolved)/3600 as mttr_hours FROM incidents
WHERE resolved_at IS NOT NULL AND priority IN ('1 - Critical', '2 - High')
  AND started_at > NOW() - INTERVAL '90 days';

-- Change Failure Rate (requires correlating incidents with deployments)
```

### 基于时间的趋势分析

```sql
-- Weekly PR throughput trend
SELECT DATE_TRUNC('week', merged) as week, COUNT(*) as prs
FROM pull_requests WHERE merged > NOW() - INTERVAL '90 days'
GROUP BY week ORDER BY week;

-- Monthly deployment trend
SELECT DATE_TRUNC('month', deployed_at) as month, COUNT(*) as deploys
FROM deployments WHERE deployed_at > NOW() - INTERVAL '12 months'
GROUP BY month ORDER BY month;
```

### 历史 DX 调查结果对比

```sql
-- Compare team scores across all surveys
SELECT s.end_date as survey_date, i.name as metric, ts.score
FROM dx_snapshot_team_scores ts
JOIN dx_snapshots s ON ts.snapshot_id = s.id
JOIN dx_snapshot_teams st ON ts.snapshot_team_id = st.id AND st.snapshot_id = s.id
JOIN dx_snapshot_items i ON ts.item_id = i.id AND i.snapshot_id = s.id
WHERE st.name = 'Your Team Name'
  AND i.item_type = 'core4'
  AND ts.score IS NOT NULL
ORDER BY s.end_date, i.name;

-- Teams that improved most since last survey (use vs_prev)
SELECT st.name as team, i.name as metric, MAX(ts.score) as score, MAX(ts.vs_prev) as change
FROM dx_snapshot_team_scores ts
JOIN dx_snapshot_teams st ON ts.snapshot_team_id = st.id
JOIN dx_snapshot_items i ON ts.item_id = i.id AND i.snapshot_id = ts.snapshot_id
WHERE ts.snapshot_id = (SELECT id FROM dx_snapshots ORDER BY end_date DESC LIMIT 1)
  AND i.name = 'Effectiveness' AND i.item_type = 'core4'
  AND st.parent = false
GROUP BY st.name, i.name
ORDER BY change DESC NULLS LAST;
```

### 工具满意度分析

```sql
-- Tool satisfaction scores (csat)
SELECT i.name as tool, AVG(ts.score) as avg_satisfaction, COUNT(DISTINCT st.name) as teams_using
FROM dx_snapshot_team_scores ts
JOIN dx_snapshot_teams st ON ts.snapshot_team_id = st.id
JOIN dx_snapshot_items i ON ts.item_id = i.id AND i.snapshot_id = ts.snapshot_id
WHERE ts.snapshot_id = (SELECT id FROM dx_snapshots ORDER BY end_date DESC LIMIT 1)
  AND i.item_type = 'csat' AND st.parent = false AND ts.score IS NOT NULL
GROUP BY i.name ORDER BY avg_satisfaction ASC;
```

## 参考文件

如需详细的数据表结构文档，请查阅以下文件：

| 数据领域 | 文件名 | 阅读建议 |
|--------|------|--------------|
| DX 调查/评分 | references/developer-experience.md | 调查数据、快照结果、团队评分、情感分析信息 |
| 团队/用户 | references/teams-users.md | 团队结构、用户信息、AI 采用日期 |
| 提交请求 | references/pull-requests.md | PR 指标、评审记录、周期时间 |
| 部署 | references/deployments-incidents.md | 部署频率、事件记录、DORA 指标 |
| 人工智能工具 | references/ai-tools.md | AI 辅助工具的使用情况、采用情况跟踪 |
| 问题跟踪 | references/jira.md | 问题记录、冲刺计划、故事点数 |
| 服务目录 | references/catalog.md | 服务信息、团队所有权、领域划分 |
| 流程与代码质量 | references/pipelines-quality.md | CI/CD 流程执行情况、代码质量问题 |
| 问题管理 | references/issues-github.md | 来源控制平台中的问题记录、标签信息 |