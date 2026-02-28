---
name: openclaw-model-router-skill
description: OpenClaw的确定性模型路由功能支持前缀路由（@codex/@mini），具备时区感知的调度切换机制、切换后的验证机制、回滚功能以及锁定保护机制。此外，系统还支持JSONL格式的审计日志记录。
---
# OpenClaw 模型路由器技能

## 该技能提供的功能

- 前缀路由功能：
  - `@codex` -> `openai-codex/gpt-5.3-codex`
  - `@mini` -> `minimax/MiniMax-M2.5`
  - 别名：`@c`, `@m`
- 从 `router.schedule.json` 中获取的基于时间的调度器功能
- 生产环境安全的调度切换功能：
  - `schedule apply` / `schedule end`
- 身份验证环境检查 (`auth.requiredEnv`)
- 切换调度器后的回读验证
- 失败时的回滚机制
- 用于处理并发的锁定文件机制
- 审计日志记录 (`router.log.jsonl`)

## 快速命令

```bash
node src/cli.js validate
node src/cli.js route "@codex implement this" --json
node src/cli.js schedule validate
node src/cli.js schedule apply --json
node src/cli.js schedule end --id workday_codex --json
```

## 配置文件

- `router.config.json`
- `router.schedule.json`

## 测试

```bash
node --test
```