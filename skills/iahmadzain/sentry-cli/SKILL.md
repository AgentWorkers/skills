---
name: sentry-cli
description: 通过 `sentry-cli` 实现 Sentry.io 的错误监控功能。适用于处理 Sentry 的发布版本、源代码映射文件（source maps）、动态链接库文件（dSYMs）、事件记录以及问题管理（issue management）等场景。该工具涵盖了身份验证（authentication）、发布工作流程（release workflows）、部署跟踪（deploy tracking）以及调试文件上传（debug file uploads）等关键功能。
---

# Sentry CLI

用于与Sentry.io交互，实现错误监控、版本管理以及调试文件的上传等功能。

## 安装

```bash
# macOS
brew install sentry-cli

# npm (cross-platform)
npm install -g @sentry/cli

# Direct download
curl -sL https://sentry.io/get-cli/ | bash
```

## 认证

```bash
# Interactive login (opens browser)
sentry-cli login

# Or set token directly
export SENTRY_AUTH_TOKEN="sntrys_..."

# Verify
sentry-cli info
```

将认证令牌存储在`.sentryclirc`文件中或通过环境变量设置：
```ini
[auth]
token=sntrys_...

[defaults]
org=my-org
project=my-project
```

## 版本管理

### 创建新版本

```bash
# Create release (usually git SHA or version)
sentry-cli releases new "$VERSION"

# Associate commits (links errors to commits)
sentry-cli releases set-commits "$VERSION" --auto

# Finalize when deployed
sentry-cli releases finalize "$VERSION"

# One-liner for CI
sentry-cli releases new "$VERSION" --finalize
```

### 完成版本发布

```bash
# Mark release as deployed to an environment
sentry-cli releases deploys "$VERSION" new -e production
sentry-cli releases deploys "$VERSION" new -e staging
```

### 列出所有版本

```bash
sentry-cli releases list
sentry-cli releases info "$VERSION"
```

## 源代码映射文件

上传源代码映射文件以帮助解析JavaScript错误：

```bash
# Upload all .js and .map files
sentry-cli sourcemaps upload ./dist --release="$VERSION"

# With URL prefix (match your deployed paths)
sentry-cli sourcemaps upload ./dist \
  --release="$VERSION" \
  --url-prefix="~/static/js"

# Validate before upload
sentry-cli sourcemaps explain ./dist/main.js.map
```

### 注入调试ID（推荐）

```bash
# Inject debug IDs into source files (modern approach)
sentry-cli sourcemaps inject ./dist
sentry-cli sourcemaps upload ./dist --release="$VERSION"
```

## 调试文件（iOS/Android）

### dSYMs（iOS）

```bash
# Upload dSYMs from Xcode archive
sentry-cli debug-files upload --include-sources path/to/dSYMs

# From derived data
sentry-cli debug-files upload ~/Library/Developer/Xcode/DerivedData/*/Build/Products/*/*.app.dSYM
```

### ProGuard（Android）

```bash
sentry-cli upload-proguard mapping.txt --uuid="$UUID"
```

### 检查调试文件

```bash
sentry-cli debug-files check path/to/file
sentry-cli debug-files list
```

## 事件与问题管理

### 发送测试事件

```bash
sentry-cli send-event -m "Test error message"
sentry-cli send-event -m "Error" --logfile /var/log/app.log
```

### 查询问题

```bash
# List unresolved issues
sentry-cli issues list

# Resolve an issue
sentry-cli issues resolve ISSUE_ID

# Mute/ignore
sentry-cli issues mute ISSUE_ID
```

## 监控任务（定时执行）

```bash
# Wrap a cron job
sentry-cli monitors run my-cron-monitor -- /path/to/script.sh

# Manual check-ins
sentry-cli monitors check-in my-monitor --status ok
sentry-cli monitors check-in my-monitor --status error
```

## 持续集成/持续部署（CI/CD）集成

### GitHub Actions

```yaml
- name: Create Sentry Release
  uses: getsentry/action-release@v1
  env:
    SENTRY_AUTH_TOKEN: ${{ secrets.SENTRY_AUTH_TOKEN }}
    SENTRY_ORG: my-org
    SENTRY_PROJECT: my-project
  with:
    environment: production
    sourcemaps: ./dist
```

### 通用CI配置

```bash
export SENTRY_AUTH_TOKEN="$SENTRY_TOKEN"
export SENTRY_ORG="my-org"
export SENTRY_PROJECT="my-project"
VERSION=$(sentry-cli releases propose-version)

sentry-cli releases new "$VERSION" --finalize
sentry-cli releases set-commits "$VERSION" --auto
sentry-cli sourcemaps upload ./dist --release="$VERSION"
sentry-cli releases deploys "$VERSION" new -e production
```

## 常用参数

| 参数          | 说明                          |
|--------------|------------------------------|
| `-o, --org`       | 组织名称                          |
| `-p, --project`    | 项目名称                          |
| `--auth-token`    | 认证令牌                          |
| `--log-level`     | 日志级别（debug/info/warn/error）           |
| `--quiet`      | 抑制输出                          |

## 故障排除

```bash
# Check configuration
sentry-cli info

# Debug upload issues
sentry-cli --log-level=debug sourcemaps upload ./dist

# Validate source map
sentry-cli sourcemaps explain ./dist/main.js.map

# Check connectivity
sentry-cli send-event -m "test" --log-level=debug
```