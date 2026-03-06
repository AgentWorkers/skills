---
name: "rtk-compress"
version: "1.15.2"
published: false
description: "在shell命令、文件读取以及测试输出过程中，可以节省60%到90%的LLM（Large Language Model）相关资源（如计算成本或模型参数）。该工具对rtk CLI（Run Time Command Line Interface）进行了优化，实现了压缩输出功能。"
tags: rtk, token-saving, compression, cli, shell, devtools
---
**在shell命令、文件读取和测试输出中节省60-90%的LLM令牌**

此技能基于[rtk（Rust Token Killer）](https://github.com/rtk-ai/rtk)——一个CLI代理工具，它可以在命令输出到达LLM（大型语言模型）之前对其进行过滤和压缩。

## 安装

```bash
# 1. Install rtk
brew install rtk          # macOS
# or: curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh

# 2. Verify
rtk gain  # Should show token savings stats
```

然后将此`SKILL.md`文件复制到你的代理的技能目录中。

## 命令参考

### 智能文件操作
```bash
rtk ls .                                # Token-optimized directory tree
rtk read file.rs                         # Smart file reading (compressed output)
rtk read file.rs -l aggressive           # Signatures only (strips bodies)
rtk smart file.rs                      # 2-line heuristic code summary
```

### 搜索与差异比较
```bash
rtk find "*.rs" .                        # Compact find results
rtk grep "pattern" .                    # Grouped search results
rtk diff file1 file2                    # Condensed diff
```

### Git操作
```bash
rtk git status                         # Compact status
rtk git log -n 10                      # One-line commits
rtk git diff                           # Condensed diff
rtk git add                           # → "ok"
rtk git commit -m "msg"                    # → "ok abc1234"
rtk git push                          # → "ok main"
rtk git pull                           # → "ok 3 files +10 -2"
```

### GitHub CLI
```bash
rtk gh pr list                         # Compact PR listing
rtk gh pr view 42                       # PR details + checks
rtk gh issue list                      # Compact issue listing
rtk gh run list                        # Workflow run status
```

### 测试运行器
```bash
rtk test cargo test                    # Show failures only (-90%)
rtk err npm run build                 # Errors/warnings only
rtk vitest run                         # Vitest compact (failures only)
rtk playwright test                   # E2E results (failures only)
rtk pytest                            # Python tests (-90%)
rtk go test                            # Go tests (NDJSON, -90%)
rtk cargo test                        # Cargo tests (-90%)
```

### 构建与代码检查
```bash
rtk lint                               # ESLint grouped by rule/file
rtk lint biome                         # Supports other linters
rtk tsc                                # TypeScript errors grouped by file
rtk next build                          # Next.js build compact
rtk prettier --check .                 # Files needing formatting
rtk cargo build                        # Cargo build (-80%)
rtk cargo clippy                        # Cargo clippy (-80%)
rtk ruff check                          # Python linting (JSON, -80%)
rtk golangci-lint run                   # Go linting (JSON, -85%)
```

### 包管理器
```bash
rtk pnpm list                          # Compact dependency tree
rtk pip list                           # Python packages (auto-detect uv)
rtk pip outdated                         # Outdated packages
rtk prisma generate                     # Schema generation (no ASCII art)
```

### 容器
```bash
rtk docker ps                           # Compact container list
rtk docker images                       # Compact image list
rtk docker logs <container>                # Deduplicated logs
rtk docker compose ps                   # Compose services
rtk kubectl pods                        # Compact pod list
rtk kubectl logs <pod>                    # Deduplicated logs
rtk kubectl services                     # Compact service list
```

### 数据与分析
```bash
rtk json config.json                    # Structure without values
rtk deps                                # Dependencies summary
rtk env -f AWS                        # Filtered env vars
rtk log app.log                         # Deduplicated logs
rtk curl <url>                         # Auto-detect JSON + schema
rtk wget <url>                        # Download, strip progress bars
rtk summary <long command>          # Heuristic summary
rtk proxy <command>                     # Raw passthrough + tracking
```

### 令牌节省分析
```bash
rtk gain                               # Summary stats
rtk gain --graph                       # ASCII graph (last 30 days)
rtk gain --history                     # Recent command history
rtk gain --daily                       # Day-by-day breakdown
rtk gain --all --format json            # JSON export for dashboards
rtk discover                            # Find missed savings opportunities
rtk discover --all --since 7           # All projects, last 7 days
```

## 代理使用规则

尽可能使用`rtk <命令>`代替原始命令：

### 始终使用rtk执行以下操作：
- `rtk git status` / `rtk git log` / `rtk git diff`
- `rtk ls -la` / `rtk cat <file>`
- `rtk npm test` / `rtk pytest` / `rtk cargo test`
- `rtk npm run build` / `rtk ruff check`

### 不要使用rtk执行以下操作：
- 输出会被传递给其他工具的命令（例如：`git log | grep ...`）
- 需要解析原始输出的脚本
- 需要完整输出结果的命令

### 如果rtk失败：
切换回原始命令。切勿因为压缩而导致任务阻塞。

### 检查节省效果：
```bash
rtk gain           # current session
rtk gain --global  # all-time stats
```

## 令牌节省情况对比

| 操作        | 不使用rtk       | 使用rtk       | 节省百分比 |
|------------|------------|------------|---------|
| `git status`    | 约300个令牌    | 约60个令牌    | -80%     |
| `git log -20`    | 约2,000个令牌    | 约400个令牌    | -80%     |
| `cat file.ts`    | 约2,000个令牌    | 约600个令牌    | -70%     |
| `npm test`    | 约5,000个令牌    | 约500个令牌    | -90%     |
| `pytest`     | 约2,000个令牌    | 约200个令牌    | -90%     |
| **典型会话**    | 约150,000个令牌  | 约45,000个令牌  | -70%     |

## 链接

- rtk: https://github.com/rtk-ai/rtk
- OpenClaw特性请求：https://github.com/openclaw/openclaw/issues/35053