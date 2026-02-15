---
name: agent-self-governance
description: "自主代理的自治理协议：WAL（预写日志，Write-Ahead Log）、VBR（报告前验证，Verify Before Reporting）、ADL（防偏离限制，Anti-Divergence Limit）、VFM（价值与成本比，Value-For-Money）和IKL（基础设施知识日志，Infrastructure Knowledge Logging）。使用场景包括：  
(1) 收到用户反馈时——在响应前先记录下来；  
(2) 做出重要决策或进行分析时——在继续执行前先记录下来；  
(3) 预压缩内存刷新时——将工作缓冲区的数据写入WAL；  
(4) 会话开始时——重放未应用的WAL条目以恢复丢失的上下文；  
(5) 任何希望确保某些数据在压缩过程中不被丢失的情况下；  
(6) 声称任务完成之前——先进行验证；  
(7) 定期自我检查——是否偏离了预设的行为模式；  
(8) 成本追踪——该操作是否值得投入资源；  
(9) 发现新的基础设施时——立即记录硬件/服务的规格信息。"
---

# 代理自我管理

为防止代理出现故障，我们设计了五项协议：防止上下文丢失、错误地声称任务完成、角色行为偏离、浪费资源以及忘记基础设施信息。

## 1. WAL（预写日志，Write-Ahead Log）

**规则：在响应之前先进行记录。** 如果有值得记住的内容，应先将其写入预写日志（WAL）中。

| 触发条件 | 操作类型 | 示例 |
|---------|------------|---------|
| 用户纠正你 | `correction` | “不，应该使用Podman而不是Docker” |
| 关键决策 | `decision` | “选择CogVideoX-2B进行文本转视频处理” |
| 重要分析结果 | `analysis` | “WAL日志中的信息应该是基础设施的核心部分，而非技能相关的内容” |
| 状态变化 | `state_change` | “GPU服务器的SSH密钥认证已配置完成” |

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
- **会话开始时** → 使用`replay`功能恢复丢失的上下文信息
- **用户纠正时** → 在响应之前先执行`append`操作
- **预压缩前** → 先执行`flush-buffer`操作，然后再每日将内存数据写入日志
- **对话进行中** → 对于不太重要的信息，使用`buffer-add`功能进行记录

## 2. VBR（报告前验证，Verify Before Reporting）

**规则：在确认任务完成之前，不要轻易说“完成”。** 在声称任务完成之前，必须先进行验证。

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

### 何时需要执行VBR：
- **代码更改后** → 运行`check command "go test ./..."`进行验证
- **文件创建后** → 检查`file_exists /path`以确保文件存在
- **推送代码到Git仓库后** → 检查`git_pushed /repo`以确保代码已成功推送
- **子代理完成任务后** → 验证其输出结果是否真实存在

## 3. ADL（反偏离限制，Anti-Divergence Limit）

**规则：保持角色的一致性。** 监控代理的行为是否偏离了在`SOUL.md`中定义的角色特征。

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

### 需要警惕的负面行为模式：
- **阿谀奉承** — 如：“问得好！”、“我很乐意帮忙！”
- **被动态度** — 如：“您需要我做什么吗？”，“请问我该怎么做？”，“请告诉我……”
- **模棱两可的回答** — 如：“我觉得也许可以”，“有可能……”
- **冗长的表达** — 回答内容超出预期长度

### 正面的角色表现特征：
- **直接明了** — 如：“任务已完成”，“问题已解决”，“文件已发送”
- **有主见** — 如：“我认为……”，“这样做更好”，“这是正确的选择”
- **行动导向** — 如：“正在处理中”，“已经开始行动”，“马上开始”

## 4. VFM（性价比，Value-For-Money）

**规则：监控成本与价值的关系。** 不要在预算内执行的高成本任务上浪费高级权限令牌（premium tokens）。

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

### 任务分类与推荐使用的模型：
| 任务类型 | 推荐使用的模型 | 备选模型 |
|-----------|-----------------|--------|
| 监控、格式化、总结 | 预算级模型 | GLM, DeepSeek, Haiku |
| 代码生成、调试、创意工作 | 标准级模型 | Sonnet, Gemini Pro |
| 架构设计、复杂分析 | 高级模型 | Opus, Sonnet+thinking |

### 何时需要检查VFM：
- **创建子代理后** — 记录任务成本和结果
- **在心跳通信期间** — 运行`suggest`命令获取优化建议
- **每周审查时** — 运行`report`命令查看成本明细

## 5. IKL（基础设施知识日志，Infrastructure Knowledge Logging）

**规则：立即记录基础设施的相关信息。** 一旦发现硬件规格、服务配置或网络拓扑结构，必须立即将其记录下来。

### 触发条件与记录内容：
| 发现的内容类型 | 记录位置 | 示例 |
|----------------|--------|---------|
| 硬件规格 | TOOLS.md | “GPU服务器配备了3块GPU：RTX 3090、3080和2070 SUPER” |
| 服务配置 | TOOLS.md | “ComfyUI运行在端口8188上，使用的数据目录是/data/ai-stack” |
| 网络拓扑 | TOOLS.md | “Pi服务器的IP地址是192.168.99.25，GPU服务器的IP地址是10.0.0.44” |
| 认证信息 | memory/encrypted/ | “SSH密钥： ~/.ssh/id_ed25519_alexchen” |
| API端点 | TOOLS.md或相关技能文档 | “Moltbook API的接口地址是/api/v1/posts” |

### 发现新信息时需要执行的命令：
```bash
# Hardware discovery
nvidia-smi --query-gpu=index,name,memory.total --format=csv
lscpu | grep -E "Model name|CPU\(s\)|Thread"
free -h
df -h

# Service discovery  
systemctl list-units --type=service --state=running
docker ps  # or podman ps
ss -tlnp | grep LISTEN

# Network discovery
ip addr show
cat /etc/hosts
```

### IKL协议的执行流程：
1. **连接到新服务器** → 运行硬件/服务信息收集命令
2. **在响应之前** → 将收集到的信息更新到`TOOLS.md`中
3. **发现新服务时** → 记录服务的端口、路径和配置位置
4. **获取到认证信息后** — 将这些信息加密并存储在内存或加密存储空间中

### 需要避免的错误做法：
❌ “我会记住的”（这种做法不可靠）  
✅ “GPU服务器配备了3块GPU”—— 应立即更新`TOOLS.md`后再继续下一步操作

**注意：** 内存资源有限，但文件是永久性的。务必在忘记之前及时记录相关信息。