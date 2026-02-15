---
name: agent-self-governance
description: "自主代理的自治理协议：WAL（预写日志，Write-Ahead Log）、VBR（报告前验证，Verify Before Reporting）、ADL（防偏离限制，Anti-Divergence Limit）和VFM（价值与成本比，Value-For-Money）。适用场景包括：  
(1) 收到用户反馈时——在响应之前先记录下来；  
(2) 做出重要决策或进行分析时——在继续执行之前先记录下来；  
(3) 进行内存预压缩时——将工作缓冲区的数据写入WAL；  
(4) 会话开始时——重放未应用的WAL记录以恢复丢失的信息；  
(5) 任何需要确保数据在压缩过程中不被丢失的情况下；  
(6) 在声称任务完成之前——先进行验证；  
(7) 定期自我检查——是否偏离了既定的行为准则；  
(8) 成本跟踪——该操作是否值得投入资源。"
---

# 代理自我管理

有四种协议用于防止代理出现故障，这些故障包括：上下文丢失、错误地声称任务已完成、行为偏离预设的“人格”（persona），以及浪费资源（如过度消耗高级资源）。

## 1. WAL（预写日志，Write-Ahead Log）

**规则：** 在响应之前先进行记录。** 如果有内容值得记住，就先将其写入预写日志中。

| 触发条件 | 操作类型 | 示例 |
|---------|------------|---------|
| 用户纠正你的错误 | `correction` | “不，应该使用 Podman 而不是 Docker” |
| 需要做出关键决策 | `decision` | “选择 CogVideoX-2B 来处理文本转视频的任务” |
| 需要进行分析 | `analysis` | “预写日志中的规则应该是核心基础设施的一部分，而不仅仅是技能” |
| 状态发生变化 | `state_change` | “GPU 服务器的 SSH 密钥认证已配置完成” |

```bash
# Write before responding
python3 scripts/wal.py append <agent_id> correction "Use Podman not Docker"

# Working buffer (batch, flush before compaction)
python3 scripts/wal.py buffer-add <agent_id> decision "Some decision"
python3 scripts/wal.py flush-buffer <agent_id>

# Session start: replay lost context
python3 scripts/wal.py replay <agent_id>

# After incorporating a replayed entry
python3 scripts/wal.py mark-applied <agent_id> <entry_id>

# Maintenance
python3 scripts/wal.py status <agent_id>
python3 scripts/wal.py prune <agent_id> --keep 50
```

### 集成点：
- **会话开始时** → 使用 `replay` 功能来恢复丢失的上下文信息
- **用户纠正错误时** → 在响应之前先执行 `append` 操作
- **预压缩之前** → 先执行 `flush-buffer` 操作，然后再每天将内存数据写入日志
- **对话进行中** → 对于不太重要的信息，使用 `buffer-add` 功能进行记录

## 2. VBR（报告前验证，Verify Before Reporting）

**规则：** 在确认任务完成之前，不要直接说“完成”。** 在声称任务完成之前，先进行验证。

```bash
# Verify a file exists
python3 scripts/vbr.py check task123 file_exists /path/to/output.py

# Verify a file was recently modified
python3 scripts/vbr.py check task123 file_changed /path/to/file.go

# Verify a command succeeds
python3 scripts/vbr.py check task123 command "cd /tmp/repo && go test ./..."

# Verify git is pushed
python3 scripts/vbr.py check task123 git_pushed /tmp/repo

# Log verification result
python3 scripts/vbr.py log <agent_id> task123 true "All tests pass"

# View pass/fail stats
python3 scripts/vbr.py stats <agent_id>
```

### 何时需要执行 VBR：
- **代码更改后** → 运行 `check command "go test ./..."` 来验证代码是否正确
- **文件创建后** → 使用 `check file_exists /path` 来确认文件是否存在
- **执行 git push 操作后** → 使用 `check git_pushed /repo` 来验证代码是否已成功推送
- **子代理任务完成后** → 验证任务生成的输出是否确实存在

## 3. ADL（防偏离规则，Anti-Divergence Limit）

**规则：** 坚持你的“人格”（预设的行为模式）。** 监控你的行为是否偏离了在 `SOUL.md` 文件中定义的“人格”规范。

```bash
# Analyze a response for anti-patterns
python3 scripts/adl.py analyze "Great question! I'd be happy to help you with that!"

# Log a behavioral observation
python3 scripts/adl.py log <agent_id> anti_sycophancy "Used 'Great question!' in response"
python3 scripts/adl.py log <agent_id> persona_direct "Shipped fix without asking permission"

# Calculate divergence score (0=aligned, 1=fully drifted)
python3 scripts/adl.py score <agent_id>

# Check against threshold
python3 scripts/adl.py check <agent_id> --threshold 0.7

# Reset after recalibration
python3 scripts/adl.py reset <agent_id>
```

### 被监控的负面行为模式：
- **阿谀奉承** — “问得好！”、“我很乐意帮忙！”
- **被动态度** — “您需要我做什么吗？”、“我可以……吗？”、“请告诉我……”
- **模棱两可的回答** — “我觉得也许可以……”，“有可能……”
- **冗长的回答** — 回答内容超出预期长度

### 表现出积极“人格”的信号：
- **直接明了** — “完成了”、“修复好了”、“发送了”、“构建完成了”
- **有主见** — “我认为……”，“更好的做法是……”，“这是正确的决定”
- **以行动为导向** — “正在处理中”、“已经开始行动了”，“即将开始执行”

## 4. VFM（性价比规则，Value-For-Money）

**规则：** 监控成本与收益的关系。** 不要在预算内的任务上浪费高级资源（如高级令牌）。

```bash
# Log a completed task with cost
python3 scripts/vfm.py log <agent_id> monitoring glm-4.7 37000 0.03 0.8

# Calculate VFM scores
python3 scripts/vfm.py score <agent_id>

# Cost breakdown by model and task
python3 scripts/vfm.py report <agent_id>

# Get optimization suggestions
python3 scripts/vfm.py suggest <agent_id>
```

### 任务分类及推荐使用的模型：
| 任务类型 | 推荐使用的模型 | 特点 |
|-----------|-----------------|--------|
| 监控、格式化、总结 | 预算级模型 | GLM、DeepSeek、Haiku |
| 代码生成、调试、创造性任务 | 标准级模型 | Sonnet、Gemini Pro |
| 架构设计、复杂分析 | 高级模型 | Opus、Sonnet+thinking |

### 何时需要检查 VFM：
- **创建子代理后** — 记录任务的成本和结果
- **在心跳通信期间** — 运行 `suggest` 命令以获取优化建议
- **每周审查时** — 运行 `report` 命令来查看成本明细