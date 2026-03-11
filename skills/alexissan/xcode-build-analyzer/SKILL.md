---
name: xcode-build-analyzer
description: 分析 Xcode 构建日志——包括编译时间、警告信息、错误详情、编译速度缓慢的情况以及来自 `DerivedData` 的构建历史记录。
homepage: https://clawhub.ai/alexissan/xcode-build-analyzer
metadata: {"clawdbot":{"emoji":"🔨","requires":{"bins":["plutil","gunzip","sqlite3"],"os":"darwin"}}}
---
# Xcode 构建分析器

通过读取 macOS 上的 `DerivedData` 构建日志，分析 Xcode 的构建性能、警告、错误以及构建历史记录。

## 使用要求

- **仅限 macOS** — 从 `~/Library/Developer/Xcode/DerivedData/` 目录中读取数据。
- 必须已安装 Xcode 并且至少构建过一个项目。
- `plutil`、`gunzip`、`sqlite3` 已经预装在 macOS 上。
- 根据执行的查询操作，可能需要完全访问磁盘。

## 关键路径

```
DERIVED_DATA=~/Library/Developer/Xcode/DerivedData
```

每个项目都有一个名为 `<ProjectName>-<hash>` 的文件夹，其中包含以下文件：
- `info.plist` — 项目工作区的路径和最后访问日期。
- `Logs/Build/LogStoreManifest.plist` — 所有构建的结构化索引（包含构建时间、状态、警告和错误信息）。
- `Logs/Build/*.xcactivitylog` — 压缩后的 SLF 格式构建日志，包含每一步的构建时间和完整的编译器输出。

> **重要提示：** 所有查询操作均为只读，切勿修改 `DerivedData` 中的内容。

## 列出 `DerivedData` 中的所有项目

```bash
for dir in ~/Library/Developer/Xcode/DerivedData/*-*; do
  [ -d "$dir" ] || continue
  NAME="$(basename "$dir" | sed 's/-[a-z]*$//')"
  WORKSPACE="$(plutil -extract WorkspacePath raw "$dir/info.plist" 2>/dev/null || echo "unknown")"
  LAST_ACCESS="$(plutil -extract LastAccessedDate raw "$dir/info.plist" 2>/dev/null || echo "unknown")"
  echo "$NAME | $WORKSPACE | Last accessed: $LAST_ACCESS"
done
```

## 查看项目的构建历史记录

解析 `LogStoreManifest.plist` 以获取结构化的构建数据。这是最可靠的数据来源，因为它包含了每个构建的详细信息（包括构建时间、错误/警告数量以及相关方案信息），而无需解压日志文件。

```bash
# Replace PROJECT_DIR with the project's DerivedData folder
# To find it: ls ~/Library/Developer/Xcode/DerivedData/ | grep -i "ProjectName"
PROJECT_DIR="$(ls -d ~/Library/Developer/Xcode/DerivedData/PROJECT_NAME-* 2>/dev/null | head -1)"
MANIFEST="$PROJECT_DIR/Logs/Build/LogStoreManifest.plist"

plutil -convert json -o - "$MANIFEST" 2>/dev/null | python3 -c "
import json, sys
from datetime import datetime, timezone, timedelta

data = json.load(sys.stdin)
EPOCH = datetime(2001, 1, 1, tzinfo=timezone.utc)
builds = []

for uid, log in data.get('logs', {}).items():
    start = log.get('timeStartedRecording', 0)
    stop = log.get('timeStoppedRecording', 0)
    duration = stop - start
    obs = log.get('primaryObservable', {})
    dt = EPOCH + timedelta(seconds=start)
    builds.append({
        'date': dt.strftime('%Y-%m-%d %H:%M'),
        'duration': f'{duration:.1f}s',
        'scheme': log.get('schemeIdentifier-schemeName', '?'),
        'status': obs.get('highLevelStatus', '?'),
        'errors': obs.get('totalNumberOfErrors', 0),
        'warnings': obs.get('totalNumberOfWarnings', 0),
        'analyzer': obs.get('totalNumberOfAnalyzerIssues', 0),
        'file': log.get('fileName', ''),
    })

builds.sort(key=lambda b: b['date'], reverse=True)
for b in builds:
    status = {'S': 'OK', 'W': 'Warnings', 'E': 'Error'}.get(b['status'], b['status'])
    print(f\"{b['date']}  {b['duration']:>8s}  {status:<10s}  {b['errors']}E {b['warnings']}W {b['analyzer']}A  [{b['scheme']}]\")
"
```

请将 `PROJECT_NAME` 替换为实际的项目名称（不区分大小写）。

**状态代码：**  
S = 构建成功  
W = 构建成功但存在警告  
E = 构建失败且存在错误  

## 所有项目的最新构建摘要

```bash
for dir in ~/Library/Developer/Xcode/DerivedData/*-*; do
  [ -d "$dir" ] || continue
  MANIFEST="$dir/Logs/Build/LogStoreManifest.plist"
  [ -f "$MANIFEST" ] || continue
  NAME="$(basename "$dir" | sed 's/-[a-z]*$//')"

  plutil -convert json -o - "$MANIFEST" 2>/dev/null | python3 -c "
import json, sys
from datetime import datetime, timezone, timedelta

data = json.load(sys.stdin)
EPOCH = datetime(2001, 1, 1, tzinfo=timezone.utc)
name = '$NAME'
latest = None

for uid, log in data.get('logs', {}).items():
    start = log.get('timeStartedRecording', 0)
    if latest is None or start > latest[0]:
        latest = (start, log)

if latest:
    start, log = latest
    stop = log.get('timeStoppedRecording', 0)
    obs = log.get('primaryObservable', {})
    dt = EPOCH + timedelta(seconds=start)
    duration = stop - start
    status = {'S': 'OK', 'W': 'Warn', 'E': 'Err'}.get(obs.get('highLevelStatus', '?'), '?')
    print(f\"{name:<30s} {dt.strftime('%Y-%m-%d %H:%M')}  {duration:>6.1f}s  {status:<5s} {obs.get('totalNumberOfErrors',0)}E {obs.get('totalNumberOfWarnings',0)}W\")
" 2>/dev/null
done
```

## 从构建日志中提取警告和错误信息

```bash
# Find the latest xcactivitylog for a project
PROJECT_DIR="$(ls -d ~/Library/Developer/Xcode/DerivedData/PROJECT_NAME-* 2>/dev/null | head -1)"
LATEST_LOG="$(ls -t "$PROJECT_DIR/Logs/Build/"*.xcactivitylog 2>/dev/null | head -1)"

# Extract warnings
gunzip -c "$LATEST_LOG" 2>/dev/null | strings | grep -E "\.swift:[0-9]+:[0-9]+: warning:" | sort -u

# Extract errors
gunzip -c "$LATEST_LOG" 2>/dev/null | strings | grep -E "\.swift:[0-9]+:[0-9]+: error:" | sort -u
```

## 按类型分组显示警告信息

```bash
PROJECT_DIR="$(ls -d ~/Library/Developer/Xcode/DerivedData/PROJECT_NAME-* 2>/dev/null | head -1)"
LATEST_LOG="$(ls -t "$PROJECT_DIR/Logs/Build/"*.xcactivitylog 2>/dev/null | head -1)"

gunzip -c "$LATEST_LOG" 2>/dev/null | strings \
  | grep -oE "warning: .*" \
  | sed 's/\[.*//; s/'"'"'[^'"'"']*'"'"'//g' \
  | sort | uniq -c | sort -rn | head -20
```

## 分析构建步骤的耗时（找出耗时较长的步骤）

`xcactivitylog` 文件中包含每个任务的 `TaskMetrics` 数据，其中 `wcDuration` 以微秒为单位表示任务的实际执行时间。

```bash
PROJECT_DIR="$(ls -d ~/Library/Developer/Xcode/DerivedData/PROJECT_NAME-* 2>/dev/null | head -1)"
LATEST_LOG="$(ls -t "$PROJECT_DIR/Logs/Build/"*.xcactivitylog 2>/dev/null | head -1)"

gunzip -c "$LATEST_LOG" 2>/dev/null | strings \
  | grep -o '{"wcDuration":[^}]*}' \
  | python3 -c "
import json, sys

tasks = []
for line in sys.stdin:
    try:
        m = json.loads(line.strip())
        tasks.append(m)
    except: pass

tasks.sort(key=lambda t: t.get('wcDuration', 0), reverse=True)
print(f'Total tasks: {len(tasks)}')
print(f'Top 10 slowest (wall-clock microseconds):')
for i, t in enumerate(tasks[:10]):
    wc = t['wcDuration']
    rss = t.get('maxRSS', 0)
    print(f'  {i+1}. {wc/1000:.1f}ms  (RSS: {rss/1024/1024:.1f}MB)')
"
```

## `DerivedData` 的磁盘使用情况

```bash
echo "Total DerivedData size:"
du -sh ~/Library/Developer/Xcode/DerivedData/ 2>/dev/null

echo ""
echo "Per project:"
for dir in ~/Library/Developer/Xcode/DerivedData/*-*; do
  [ -d "$dir" ] || continue
  NAME="$(basename "$dir" | sed 's/-[a-z]*$//')"
  SIZE="$(du -sh "$dir" 2>/dev/null | cut -f1)"
  echo "  $SIZE  $NAME"
done | sort -rh
```

## 清理项目的 `DerivedData` 数据

仅当用户明确要求时才建议执行此操作。此操作会删除构建缓存并强制重新构建项目。

```bash
# Replace PROJECT_NAME with the project name
PROJECT_DIR="$(ls -d ~/Library/Developer/Xcode/DerivedData/PROJECT_NAME-* 2>/dev/null | head -1)"
echo "Will delete: $PROJECT_DIR ($(du -sh "$PROJECT_DIR" 2>/dev/null | cut -f1))"
echo "Run: rm -rf \"$PROJECT_DIR\""
```

> **警告：** 在删除之前请务必先与用户确认。建议先显示 `DerivedData` 的大小和路径。

## 项目的构建趋势（随时间变化的构建情况）

```bash
PROJECT_DIR="$(ls -d ~/Library/Developer/Xcode/DerivedData/PROJECT_NAME-* 2>/dev/null | head -1)"
MANIFEST="$PROJECT_DIR/Logs/Build/LogStoreManifest.plist"

plutil -convert json -o - "$MANIFEST" 2>/dev/null | python3 -c "
import json, sys
from datetime import datetime, timezone, timedelta

data = json.load(sys.stdin)
EPOCH = datetime(2001, 1, 1, tzinfo=timezone.utc)
builds = []

for uid, log in data.get('logs', {}).items():
    start = log.get('timeStartedRecording', 0)
    stop = log.get('timeStoppedRecording', 0)
    builds.append((start, stop - start))

builds.sort()
if builds:
    print(f'Builds tracked: {len(builds)}')
    durations = [d for _, d in builds]
    print(f'Fastest: {min(durations):.1f}s')
    print(f'Slowest: {max(durations):.1f}s')
    print(f'Average: {sum(durations)/len(durations):.1f}s')
    print(f'Median:  {sorted(durations)[len(durations)//2]:.1f}s')
    print()
    print('Timeline:')
    for start, dur in builds:
        dt = EPOCH + timedelta(seconds=start)
        bar = '█' * max(1, int(dur / max(durations) * 30))
        print(f'  {dt.strftime(\"%m/%d %H:%M\")}  {dur:>6.1f}s  {bar}')
"
```

## 并发问题（Swift 6 的兼容性）

提取在 Swift 6 中会变为错误的并发相关警告：

```bash
PROJECT_DIR="$(ls -d ~/Library/Developer/Xcode/DerivedData/PROJECT_NAME-* 2>/dev/null | head -1)"
LATEST_LOG="$(ls -t "$PROJECT_DIR/Logs/Build/"*.xcactivitylog 2>/dev/null | head -1)"

gunzip -c "$LATEST_LOG" 2>/dev/null | strings \
  | grep -E "(data race|Sendable|actor-isolated|crossing into|concurrency)" \
  | grep "warning:" \
  | sort -u
```

## 使用 `xcodebuild` 进行构建

**重要提示：** 如果未使用 `-resultBundlePath` 参数，`xcodebuild` 命令行工具不会写入 `LogStoreManifest.plist` 或生成 `.xcactivitylog` 文件。这意味着上述构建历史记录仅显示 Xcode IDE 的构建信息。

要检测使用 `xcodebuild` 进行的构建，请检查构建产品的时间戳和 `DerivedData` 中的相关信息：

```bash
for dir in ~/Library/Developer/Xcode/DerivedData/*-*; do
  [ -d "$dir" ] || continue
  NAME="$(basename "$dir" | sed 's/-[a-z]*$//')"
  WORKSPACE="$(plutil -extract WorkspacePath raw "$dir/info.plist" 2>/dev/null || echo "unknown")"

  # Detect if this is a worktree build (workspace path outside main project dir, e.g. /tmp/)
  SOURCE=""
  PROJ_DIR="$(dirname "$WORKSPACE")"
  if [ -d "$PROJ_DIR" ] && git -C "$PROJ_DIR" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    BRANCH="$(git -C "$PROJ_DIR" branch --show-current 2>/dev/null)"
    IS_WORKTREE="$(git -C "$PROJ_DIR" rev-parse --is-inside-work-tree 2>/dev/null)"
    MAIN_WORKTREE="$(git -C "$PROJ_DIR" worktree list 2>/dev/null | head -1 | awk '{print $1}')"
    if [ "$PROJ_DIR" != "$MAIN_WORKTREE" ]; then
      SOURCE=" (worktree: $BRANCH @ $PROJ_DIR)"
    else
      SOURCE=" (branch: $BRANCH)"
    fi
  fi

  # Check Debug simulator product
  APP="$(ls -dt "$dir/Build/Products/Debug-iphonesimulator/"*.app 2>/dev/null | head -1)"
  if [ -n "$APP" ]; then
    MTIME="$(stat -f '%Sm' -t '%Y-%m-%d %H:%M' "$APP" 2>/dev/null)"
    VERSION=""
    PLIST="$APP/Info.plist"
    if [ -f "$PLIST" ]; then
      SHORT="$(plutil -extract CFBundleShortVersionString raw "$PLIST" 2>/dev/null)"
      BUILD="$(plutil -extract CFBundleVersion raw "$PLIST" 2>/dev/null)"
      VERSION=" v${SHORT}(${BUILD})"
    fi
    echo "$NAME | Last build: $MTIME |$VERSION | $(basename "$APP")$SOURCE"
  fi

  # Check Release product
  APP="$(ls -dt "$dir/Build/Products/Release-iphoneos/"*.app 2>/dev/null | head -1)"
  if [ -n "$APP" ]; then
    MTIME="$(stat -f '%Sm' -t '%Y-%m-%d %H:%M' "$APP" 2>/dev/null)"
    echo "$NAME | Last release: $MTIME | $(basename "$APP")$SOURCE"
  fi
done
```

> **工作区（Worktree）：** 当从 Git 工作区（worktree）进行构建时，Xcode 会创建一个不同的 `DerivedData` 文件（具有不同的哈希值）。上述脚本通过检查工作区的 Git 状态来识别工作区构建，并显示分支名称和工作区的位置。

### 综合构建历史记录（IDE + CLI）

要获取所有构建的完整信息（包括 Xcode IDE 和 CLI 的构建记录），需要同时运行 `LogStoreManifest` 解析器和构建产品检查工具。`LogStoreManifest` 提供了 IDE 构建的详细历史记录，而构建产品的时间戳则显示了每个配置下的最新 CLI 构建信息。

```bash
echo "=== IDE Builds (from LogStoreManifest) ==="
for dir in ~/Library/Developer/Xcode/DerivedData/*-*; do
  [ -d "$dir" ] || continue
  MANIFEST="$dir/Logs/Build/LogStoreManifest.plist"
  [ -f "$MANIFEST" ] || continue
  NAME="$(basename "$dir" | sed 's/-[a-z]*$//')"

  plutil -convert json -o - "$MANIFEST" 2>/dev/null | python3 -c "
import json, sys
from datetime import datetime, timezone, timedelta

data = json.load(sys.stdin)
EPOCH = datetime(2001, 1, 1, tzinfo=timezone.utc)
name = '$NAME'

for uid, log in sorted(data.get('logs', {}).items(), key=lambda x: x[1].get('timeStartedRecording', 0), reverse=True):
    start = log.get('timeStartedRecording', 0)
    stop = log.get('timeStoppedRecording', 0)
    obs = log.get('primaryObservable', {})
    dt = EPOCH + timedelta(seconds=start)
    duration = stop - start
    status = {'S': 'OK', 'W': 'Warn', 'E': 'Err'}.get(obs.get('highLevelStatus', '?'), '?')
    scheme = log.get('schemeIdentifier-schemeName', '?')
    print(f'  {name:<25s} {dt.strftime(\"%Y-%m-%d %H:%M\")}  {duration:>6.1f}s  {status:<5s} [{scheme}]  (IDE)')
" 2>/dev/null
done

echo ""
echo "=== CLI Builds (from build products) ==="
for dir in ~/Library/Developer/Xcode/DerivedData/*-*; do
  [ -d "$dir" ] || continue
  NAME="$(basename "$dir" | sed 's/-[a-z]*$//')"
  for APP in "$dir/Build/Products/"*/*.app; do
    [ -d "$APP" ] || continue
    MTIME="$(stat -f '%Sm' -t '%Y-%m-%d %H:%M' "$APP" 2>/dev/null)"
    CONFIG="$(basename "$(dirname "$APP")")"
    echo "  $NAME  $MTIME  [$CONFIG]  $(basename "$APP")  (CLI)"
  done 2>/dev/null
done
```

## 注意事项：

- `LogStoreManifest.plist` 是获取构建历史记录的最快方式，无需解压文件。
- `xcactivitylog` 文件采用压缩后的 SLF（Structured Log Format）格式，可以使用 `gunzip -c` 和 `strings` 命令快速提取内容。
- Core Data 时间戳表示自 2001-01-01 以来的秒数（需加上 `978307200` 转换为 Unix 时间戳）。
- 构建日志会一直保留，直到 `DerivedData` 被清理；Xcode 可能会自动删除过旧的日志文件。
- `highLevelStatus` 字段的含义：`S` = 构建成功，`W` = 存在警告，`E` = 构建失败。
- `TaskMetrics` 中的 `wcDuration` 以微秒为单位表示任务耗时，`maxRSS` 以字节为单位表示内存使用量。
- 所有操作均为只读操作——在 Xcode 运行过程中切勿修改 `DerivedData` 的内容。