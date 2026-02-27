# Overkill Token Optimizer

这是一个用于 OpenClaw 代理的令牌优化工具，通过命令行界面（CLI）实现压缩、会话管理和内存优化，从而减少令牌的使用量。

## 先决条件

**必需条件：** 需要手动安装 `oktk` CLI：

```bash
npm install -g oktk
```

或访问：https://github.com/satnamra/oktk

## 功能

- **令牌统计**：查看会话中令牌的使用情况
- **会话索引**：为搜索创建旧会话的索引
- **混合搜索**：支持语义搜索和关键词搜索
- **CLI 压缩**：压缩命令输出（需要 `oktk`）

## CLI 命令

```bash
# Show token usage statistics
token-optimizer stats

# Check optimization level
token-optimizer check

# Index sessions for search
token-optimizer index

# Search sessions (use --hybrid for semantic+keyword)
token-optimizer search "query" --hybrid

# Compress command output (requires oktk)
token-optimizer compress git status
```

## 配置

设置自定义的 `oktk` 路径：
```bash
export OKTK_BIN=/path/to/oktk
```

## 存储

- 会话索引：`~/.openclaw/workspace-memory-builder/.session_index/`

---

*Overkill Token Optimizer v1.0.3*