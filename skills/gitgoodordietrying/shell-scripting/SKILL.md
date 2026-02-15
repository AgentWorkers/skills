---
name: shell-scripting
description: 编写健壮且可移植的 shell 脚本。这些脚本可用于解析命令参数、正确处理错误、编写符合 POSIX 标准的脚本、管理临时文件、并行执行命令、管理后台进程，以及为脚本添加 `--help` 命令以提供使用说明。
metadata: {"clawdbot":{"emoji":"🐚","requires":{"bins":["bash"]},"os":["linux","darwin","win32"]}}
---

# Shell 脚本编程

编写可靠且易于维护的 Bash 脚本。内容包括参数解析、错误处理、脚本的可移植性、临时文件的使用、并行执行、进程管理以及脚本的自我文档化。

## 适用场景

- 编写供他人或未来自己使用的脚本
- 自动化多步骤工作流程
- 解析命令行参数（包括标志和选项）
- 正确处理错误并进行清理
- 并行执行任务
- 使脚本在 Linux 和 macOS 系统上都能正常运行
- 为复杂的命令提供更简单的使用接口

## 脚本模板

```bash
#!/usr/bin/env bash
set -euo pipefail

# Description: What this script does (one line)
# Usage: script.sh [options] <required-arg>

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_NAME="$(basename "$0")"

# Defaults
VERBOSE=false
OUTPUT_DIR="./output"

usage() {
    cat <<EOF
Usage: $SCRIPT_NAME [options] <input-file>

Description:
  Process the input file and generate output.

Options:
  -o, --output DIR    Output directory (default: $OUTPUT_DIR)
  -v, --verbose       Enable verbose output
  -h, --help          Show this help message

Examples:
  $SCRIPT_NAME data.csv
  $SCRIPT_NAME -v -o /tmp/results data.csv
EOF
}

log() { echo "[$(date '+%H:%M:%S')] $*" >&2; }
debug() { $VERBOSE && log "DEBUG: $*" || true; }
die() { log "ERROR: $*"; exit 1; }

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        -o|--output) OUTPUT_DIR="$2"; shift 2 ;;
        -v|--verbose) VERBOSE=true; shift ;;
        -h|--help) usage; exit 0 ;;
        --) shift; break ;;
        -*) die "Unknown option: $1" ;;
        *) break ;;
    esac
done

INPUT_FILE="${1:?$(usage >&2; echo "Error: input file required")}"
[[ -f "$INPUT_FILE" ]] || die "File not found: $INPUT_FILE"

# Main logic
main() {
    debug "Input: $INPUT_FILE"
    debug "Output: $OUTPUT_DIR"
    mkdir -p "$OUTPUT_DIR"

    log "Processing $INPUT_FILE..."
    # ... do work ...
    log "Done. Output in $OUTPUT_DIR"
}

main "$@"
```

## 错误处理

### 设置标志（Setting Flags）

```bash
set -e          # Exit on any command failure
set -u          # Error on undefined variables
set -o pipefail # Pipe fails if any command in the pipe fails
set -x          # Debug: print each command before executing (noisy)

# Combined (use this in every script)
set -euo pipefail

# Temporarily disable for commands that are allowed to fail
set +e
some_command_that_might_fail
exit_code=$?
set -e
```

### 定义清理脚本（Defining Cleanup Scripts）

```bash
# Cleanup on exit (any exit: success, failure, or signal)
TMPDIR=""
cleanup() {
    [[ -n "$TMPDIR" ]] && rm -rf "$TMPDIR"
}
trap cleanup EXIT

TMPDIR=$(mktemp -d)
# Use $TMPDIR freely — it's cleaned up automatically

# Trap specific signals
trap 'echo "Interrupted"; exit 130' INT    # Ctrl+C
trap 'echo "Terminated"; exit 143' TERM    # kill
```

### 错误处理模式（Error Handling Patterns）

```bash
# Check command exists before using it
command -v jq >/dev/null 2>&1 || die "jq is required but not installed"

# Provide default values
NAME="${NAME:-default_value}"

# Required variable (fail if unset)
: "${API_KEY:?Error: API_KEY environment variable is required}"

# Retry a command
retry() {
    local max_attempts=$1
    shift
    local attempt=1
    while [[ $attempt -le $max_attempts ]]; do
        "$@" && return 0
        log "Attempt $attempt/$max_attempts failed. Retrying..."
        ((attempt++))
        sleep $((attempt * 2))
    done
    die "Command failed after $max_attempts attempts: $*"
}

retry 3 curl -sf https://api.example.com/health
```

## 参数解析（Argument Parsing）

### 简单方式：位置参数 + 标志（Simple Method: Positional Parameters + Flags）

```bash
# Manual parsing (no dependencies)
FORCE=false
DRY_RUN=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        -f|--force) FORCE=true; shift ;;
        -n|--dry-run) DRY_RUN=true; shift ;;
        -o|--output)
            [[ -n "${2:-}" ]] || die "--output requires a value"
            OUTPUT="$2"; shift 2 ;;
        --output=*)
            OUTPUT="${1#*=}"; shift ;;
        -h|--help) usage; exit 0 ;;
        --) shift; break ;;  # End of options
        -*) die "Unknown option: $1" ;;
        *) break ;;  # Start of positional args
    esac
done

# Remaining args are positional
FILES=("$@")
[[ ${#FILES[@]} -gt 0 ]] || die "At least one file is required"
```

### 使用 getopts（POSIX，仅支持短选项）（Using getopts (POSIX, only for short options)）

```bash
while getopts ":o:vhf" opt; do
    case "$opt" in
        o) OUTPUT="$OPTARG" ;;
        v) VERBOSE=true ;;
        f) FORCE=true ;;
        h) usage; exit 0 ;;
        :) die "Option -$OPTARG requires an argument" ;;
        ?) die "Unknown option: -$OPTARG" ;;
    esac
done
shift $((OPTIND - 1))
```

## 临时文件和目录（Temporary Files and Directories）

```bash
# Create temp file (automatically unique)
TMPFILE=$(mktemp)
echo "data" > "$TMPFILE"

# Create temp directory
TMPDIR=$(mktemp -d)

# Create temp with custom prefix/suffix
TMPFILE=$(mktemp /tmp/myapp.XXXXXX)
TMPFILE=$(mktemp --suffix=.json)  # GNU only

# Always clean up with trap
trap 'rm -f "$TMPFILE"' EXIT

# Portable pattern (works on macOS and Linux)
TMPDIR=$(mktemp -d 2>/dev/null || mktemp -d -t 'myapp')
trap 'rm -rf "$TMPDIR"' EXIT
```

## 并行执行（Parallel Execution）

### 使用 xargs -P（Using xargs -P）

```bash
# Run 4 commands in parallel
cat urls.txt | xargs -P 4 -I {} curl -sO {}

# Process files in parallel (4 at a time)
find . -name "*.csv" | xargs -P 4 -I {} ./process.sh {}

# Parallel with progress indicator
find . -name "*.jpg" | xargs -P 8 -I {} sh -c 'convert {} -resize 800x600 resized/{} && echo "Done: {}"'
```

### 在后台执行任务并等待完成（Running Jobs in the Background and Waiting for Completion）

```bash
# Run tasks in background, wait for all
pids=()
for file in data/*.csv; do
    process_file "$file" &
    pids+=($!)
done

# Wait for all and check results
failed=0
for pid in "${pids[@]}"; do
    wait "$pid" || ((failed++))
done
[[ $failed -eq 0 ]] || die "$failed jobs failed"
```

### 使用 GNU Parallel（如果可用）（Using GNU Parallel, if available）

```bash
# Process files with 8 parallel jobs
parallel -j 8 ./process.sh {} ::: data/*.csv

# With progress bar
parallel --bar -j 4 convert {} -resize 800x600 resized/{/} ::: *.jpg

# Pipe input lines
cat urls.txt | parallel -j 10 curl -sO {}
```

## 进程管理（Process Management）

### 启动后台进程（Starting Background Processes）

```bash
# Start in background
long_running_command &
BG_PID=$!

# Check if still running
kill -0 $BG_PID 2>/dev/null && echo "Running" || echo "Stopped"

# Wait for it
wait $BG_PID
echo "Exit code: $?"

# Kill on script exit
trap 'kill $BG_PID 2>/dev/null' EXIT
```

### 监控进程（Monitoring Processes）

```bash
# Run a command, restart if it dies
run_with_restart() {
    local cmd=("$@")
    while true; do
        "${cmd[@]}" &
        local pid=$!
        log "Started PID $pid"
        wait $pid
        local exit_code=$?
        log "Process exited with code $exit_code. Restarting in 5s..."
        sleep 5
    done
}

run_with_restart ./my-server --port 8080
```

### 设置超时（Setting Timouts）

```bash
# Kill command after 30 seconds
timeout 30 long_running_command

# With custom signal (SIGKILL after SIGTERM fails)
timeout --signal=TERM --kill-after=10 30 long_running_command

# Portable (no timeout command)
( sleep 30; kill $$ 2>/dev/null ) &
TIMER_PID=$!
long_running_command
kill $TIMER_PID 2>/dev/null
```

## 可移植性（Linux 与 macOS 的差异）（Portability: Differences between Linux and macOS）

### 常见差异（Common Differences）

```bash
# sed: macOS requires -i '' (empty backup extension)
# Linux:
sed -i 's/old/new/g' file.txt
# macOS:
sed -i '' 's/old/new/g' file.txt
# Portable:
sed -i.bak 's/old/new/g' file.txt && rm file.txt.bak

# date: different flags
# GNU (Linux):
date -d '2026-02-03' '+%s'
# BSD (macOS):
date -j -f '%Y-%m-%d' '2026-02-03' '+%s'

# readlink -f: doesn't exist on macOS
# Portable alternative:
real_path() { cd "$(dirname "$1")" && echo "$(pwd)/$(basename "$1")"; }

# stat: different syntax
# GNU: stat -c '%s' file
# BSD: stat -f '%z' file

# grep -P: not available on macOS by default
# Use grep -E instead, or install GNU grep
```

### POSIX 安全编程模式（POSIX-Safe Programming Patterns）

```bash
# Use printf instead of echo -e (echo behavior varies)
printf "Line 1\nLine 2\n"

# Use $() instead of backticks
result=$(command)   # Good
result=`command`    # Bad (deprecated, nesting issues)

# Use [[ ]] for tests (bash), [ ] for POSIX sh
[[ -f "$file" ]]   # Bash (safer, no word splitting)
[ -f "$file" ]     # POSIX sh

# Array check (bash only, not POSIX)
if [[ ${#array[@]} -gt 0 ]]; then
    echo "Array has elements"
fi
```

## 配置文件解析（Config File Parsing）

### 从文件中读取配置信息（Reading Configuration from a File）

```bash
# Simple: source a key=value file
# config.env:
# DB_HOST=localhost
# DB_PORT=5432

# Validate before sourcing (security: check for commands)
if grep -qP '^[A-Z_]+=.*[;\`\$\(]' config.env; then
    die "Config file contains unsafe characters"
fi
source config.env
```

### 解析 INI 格式的配置文件（Parsing INI-Style Configuration Files）

```bash
# config.ini:
# [database]
# host = localhost
# port = 5432
# [app]
# debug = true

parse_ini() {
    local file="$1" section=""
    while IFS='= ' read -r key value; do
        [[ -z "$key" || "$key" =~ ^[#\;] ]] && continue
        if [[ "$key" =~ ^\[(.+)\]$ ]]; then
            section="${BASH_REMATCH[1]}"
            continue
        fi
        value="${value%%#*}"     # Strip inline comments
        value="${value%"${value##*[![:space:]]}"}"  # Trim trailing whitespace
        printf -v "${section}_${key}" '%s' "$value"
    done < "$file"
}

parse_ini config.ini
echo "$database_host"  # localhost
echo "$app_debug"      # true
```

## 有用的编程模式（Useful Programming Patterns）

### 在执行破坏性操作前进行确认（Confirming Before Performing Destructive Actions）

```bash
confirm() {
    local prompt="${1:-Are you sure?}"
    read -rp "$prompt [y/N] " response
    [[ "$response" =~ ^[Yy]$ ]]
}

confirm "Delete all files in /tmp/data?" || die "Aborted"
rm -rf /tmp/data/*
```

### 显示进度（Showing Progress Indicators）

```bash
# Simple counter
total=$(wc -l < file_list.txt)
count=0
while IFS= read -r file; do
    ((count++))
    printf "\rProcessing %d/%d..." "$count" "$total" >&2
    process "$file"
done < file_list.txt
echo "" >&2
```

### 加锁文件以防止并发执行（Locking Files to Prevent Concurrent Execution）

```bash
LOCKFILE="/tmp/${SCRIPT_NAME}.lock"

acquire_lock() {
    if ! mkdir "$LOCKFILE" 2>/dev/null; then
        die "Another instance is running (lock: $LOCKFILE)"
    fi
    trap 'rm -rf "$LOCKFILE"' EXIT
}

acquire_lock
# ... safe to proceed, only one instance runs ...
```

### 使用标准输入或文件作为参数（Using Standard Input or Files as Arguments）

```bash
# Read from file argument or stdin
input="${1:--}"   # Default to "-" (stdin)
if [[ "$input" == "-" ]]; then
    cat
else
    cat "$input"
fi | while IFS= read -r line; do
    process "$line"
done
```

## 技巧和建议（Tips and Suggestions）

- 始终使用 `set -euo pipefail`：这可以捕获 80% 的潜在错误。
- 对于临时文件，务必使用 `trap cleanup EXIT` 来确保文件被正确清理。不要依赖脚本执行到最后才执行清理操作。
- 变量引用时必须加引号：使用 `"$var"` 而不是 `$var`。未加引号的变量会在遇到空格或通配符时出错。
- 在 Bash 中使用 `[[ ]]` 而不是 `[ ]`，因为它能更好地处理空字符串、空格和模式匹配。
- `shellcheck` 是检查 Shell 脚本的优秀工具。运行 `shellcheck myscript.sh`；如果可用，请安装它。
- 使用 `readonly` 修饰符来保护常量，防止意外覆盖：`readonly DB_HOST="localhost"`。
- 编写一个 `usage()` 函数，并在 `-h`/`--help` 选项或缺少必要参数时调用它。未来的用户（包括你自己）会因此受益。
- 对于可能包含特殊字符或需要格式化的内容，优先使用 `printf` 而不是 `echo`。
- 在运行脚本之前，使用 `bash -n script.sh` 进行语法检查。