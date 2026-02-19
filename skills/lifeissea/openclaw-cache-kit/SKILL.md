---
name: OpenClaw Cache Kit
description: 自动为 OpenClaw 应用 Claude 提示缓存优化策略。通过设置较长的缓存保留时间（59 分钟）、定期更新缓存（心跳机制）、以及采用 CRON.md 文件进行缓存管理策略，可将 API 使用成本降低高达 89%。
version: 1.0.1
author: raon
inspired_by: https://slashpage.com/thomasjeong/36nj8v2wq5zqj25ykq9z
---
# openclaw-cache-kit

> **灵感来源**：[OpenClaw 提示缓存优化指南](https://slashpage.com/thomasjeong/36nj8v2wq5zqj25ykq9z)

这是一个用于优化 OpenClaw 缓存的工具包，可将 Claude API 的使用成本降低多达 89%。

---

## 为什么缓存很重要？

OpenClaw 会在 **每次请求时** 将以下文件作为系统提示发送到服务器：
- `SOUL.md` — 个人资料及操作规则（包含数百到数千个令牌）
- `AGENTS.md`、`TOOLS.md`、`MEMORY.md` — 相关配置文件
- `CRON.md` — 定时任务脚本（执行频率越高，成本越高）

在默认设置下，这些大型系统提示文件会 **每次请求时都被重新发送到服务器，且不进行缓存**，从而导致额外的费用。

以 Claude Sonnet 为例，令牌的价格如下：
| 类型 | 价格 |
|------|------|
| 输入请求（未命中缓存） | $3.00 / 100 万令牌 |
| 缓存读取（命中缓存） | $0.30 / 100 万令牌 |
| **节省比例** | **90%** |

---

## 四项核心配置

### 1. `cacheRetention: "long"`
将缓存保留时间设置为最长值（5 分钟）。此设置适用于 Sonnet 模型。

### 2. `contextPruning.ttl: "1h"`
每隔 1 小时清理一次旧的配置数据，以保持较高的缓存命中率。

### 3. `heartbeat.every: "59m"`
在 Claude 的缓存过期时间（通常为 1 小时）之前，通过发送心跳信号来更新缓存。
59 分钟的更新周期意味着在缓存过期前 1 分钟进行更新，从而保证缓存的连续性。

### 4. `diagnostics.cacheTrace.enabled: true`
在 `~/.openclaw/logs/cache-trace.jsonl` 文件中记录缓存命中/未命中的情况。
可以实时查看节省的费用。

---

## 安装与配置

```bash
# 1. 캐싱 최적화 적용 (openclaw.json 자동 업데이트 + gateway 재시작)
bash scripts/apply.sh

# 2. 오늘 캐시 절약액 확인
bash scripts/check-savings.sh
```

---

## 分离 `CRON.md` 文件的策略

如果 `CRON.md` 文件中的任务脚本过长，每次执行都会消耗更多令牌。因此，建议 **缩短 `CRON.md` 文件的长度**。
详细内容请参考 `scripts/cron-md-template.md`。

**核心原则**：
- `CRON.md` 文件中仅应包含调度任务和最基本的指令。
- 具体的操作规则应放在 `SOUL.md` 和 `AGENTS.md` 文件中。
- 每条定时任务脚本的目标消耗令牌数应控制在 50 个以内。

---

## 查看节省效果

```bash
bash scripts/check-savings.sh
# 예시 출력:
# 📊 오늘 캐시 절약 리포트 (2026-02-19)
# cacheRead 토큰: 1,234,567
# 절약 금액: $3.33 (vs 캐시 없을 때)
```

---

## 文件结构

```
openclaw-cache-kit/
├── SKILL.md                    # 이 파일
└── scripts/
    ├── apply.sh                # 캐싱 설정 적용
    ├── check-savings.sh        # 절약 금액 확인
    └── cron-md-template.md     # CRON.md 분리 전략 템플릿
```