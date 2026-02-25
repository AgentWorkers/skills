---
name: sentry
description: 通过 Sentry REST API 查看问题、事件和生产环境中的错误。当用户需要检查错误、列出最近的问题、获取堆栈跟踪或总结生产环境的运行状况时，可以使用此功能。需要具备具有只读权限的 SENTRY_AUTH_TOKEN。
allowed-tools: Bash(python3:*), Bash(export:*)
metadata: {"openclaw":{"emoji":"🐛","primaryEnv":"SENTRY_AUTH_TOKEN","requires":{"bins":["python3"],"env":["SENTRY_AUTH_TOKEN"]}}}
---
# Sentry（仅限读取）

用于查看来自Sentry的生产环境中的错误和问题。

## 设置

```bash
# Check token is set (does not print the value)
[ -n "$SENTRY_AUTH_TOKEN" ] && echo "SENTRY_AUTH_TOKEN: set" || echo "SENTRY_AUTH_TOKEN: MISSING"
echo "ORG=${SENTRY_ORG:-not set}"
echo "PROJECT=${SENTRY_PROJECT:-not set}"
```

如果缺少`SENTRY_AUTH_TOKEN`：
1. 访问 https://sentry.io/settings/account/api/auth-tokens/
2. 创建一个具有以下权限范围的令牌：`project:read`、`event:read`、`org:read`
3. 将`SENTRY_AUTH_TOKEN`设置到您的环境变量中

为了避免每次使用时都需要传递参数，可以设置可选的默认值：
```bash
export SENTRY_ORG=your-org-slug
export SENTRY_PROJECT=your-project-slug
```

## 脚本路径

```bash
SKILL_DIR="$(python3 -c "import os; print(os.path.dirname(os.path.realpath('$0')))" 2>/dev/null || echo "$HOME/.claude/skills/sentry")"
SENTRY_API="$SKILL_DIR/scripts/sentry_api.py"
```

## 命令

### 列出最近的问题

```bash
python3 "$SENTRY_API" list-issues \
  --org "$SENTRY_ORG" \
  --project "$SENTRY_PROJECT" \
  --time-range 24h \
  --environment prod \
  --limit 20 \
  --query "is:unresolved"
```

### 获取问题详情

```bash
python3 "$SENTRY_API" issue-detail ISSUE_ID
```

### 获取问题的事件记录

```bash
python3 "$SENTRY_API" issue-events ISSUE_ID --limit 10
```

### 获取事件详情（默认不包含堆栈跟踪）

```bash
python3 "$SENTRY_API" event-detail \
  --org "$SENTRY_ORG" \
  --project "$SENTRY_PROJECT" \
  EVENT_ID
```

添加`--include-entries`选项可包含堆栈跟踪信息。

### 将简短ID（例如ABC-123）转换为问题ID

```bash
python3 "$SENTRY_API" list-issues \
  --org "$SENTRY_ORG" \
  --project "$SENTRY_PROJECT" \
  --query "ABC-123" \
  --limit 1
```

## 参数

| 参数 | 默认值 | 说明 |
|------|---------|-------------|
| `--org` | `$SENTRY_ORG` | 组织名称 |
| `--project` | `$SENTRY_PROJECT` | 项目名称 |
| `--time-range` | `24h` | 统计时间范围（例如`7d`、`30d`） |
| `--environment` | `prod` | 环境过滤器 |
| `--limit` | `20` | 最大结果数量（最多50条） |
| `--query` | | Sentry搜索查询 |
| `--base-url` | `https://sentry.io` | 用于自托管的Sentry |
| `--no-redact` | | 禁用个人身份信息（PII）的隐藏 — **请勿在共享或日志环境中使用** |

## 注意事项

- 默认情况下，个人身份信息（如电子邮件、IP地址）会被隐藏。
- 默认情况下，事件详情中不包含堆栈跟踪信息 — 仅在需要查看堆栈跟踪且信任当前环境时才添加`--include-entries`选项。
- `--no-redact`选项会禁用个人身份信息的隐藏 — 请勿在共享或日志环境中使用。
- 对于自托管的Sentry，请设置`SENTRY_BASE_URL`或使用`--base-url`参数。