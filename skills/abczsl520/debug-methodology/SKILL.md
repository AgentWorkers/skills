---
name: debug-methodology
description: 系统化的调试与问题解决方法。在遇到意外错误、服务故障、回归性漏洞、部署问题，或者修复尝试失败两次时，应立即启用此方法。在提出任何修复方案时，也应使用该方法来验证其是否真正解决了根本问题（而不仅仅是临时性的解决方案）。该方法有助于避免连续发布多个补丁、在错误的环境中重启系统、过度依赖临时解决方案，以及随意、无计划的修复行为。
---
# 调试方法论

这是一种系统化的调试和问题解决方法，基于实际生产中的案例以及行业最佳实践总结而成。

## ⚠️ 必须找到根本原因

**任何修复措施都必须针对问题的根本原因。除非得到明确批准，否则禁止使用临时解决方案（即变通方法）。**

在提出任何解决方案之前，必须先通过“根本原因检查”（Root Cause Check）：

```
┌─────────────────────────────────────────────┐
│            ROOT CAUSE GATE                  │
│                                             │
│  1. What is the ACTUAL problem?             │
│  2. WHY does it happen? (not just WHAT)     │
│  3. Does my fix eliminate the WHY?           │
│     YES → proceed                           │
│     NO  → this is a workaround → STOP       │
│                                             │
│  Workaround test:                           │
│  "If I remove my fix, does the bug return?" │
│     YES → workaround (fix the cause instead)│
│     NO  → genuine fix ✅                    │
└─────────────────────────────────────────────┘
```

### “五个为什么”（5 Whys）——针对不明显的问题必须使用

```
Problem: API returns 524 timeout
  Why? → Cloudflare cuts connections >100s
  Why? → The API call takes >100s
  Why? → Using non-streaming request, server holds connection silent
  Why? → Code uses regular fetch, not streaming
  Fix: → Use streaming (server sends data continuously, Cloudflare won't cut)

  ❌ WRONG: Switch to faster model (workaround — avoids the timeout instead of fixing it)
  ✅ RIGHT: Use streaming API (root cause — Cloudflare needs ongoing data)
```

### 常见的变通方法陷阱

| 问题 | 变通方法（❌） | 根本原因的修复方法（✅） |
|---------|----------------|-------------------|
| API超时 | 更换更快的模型 | 使用流式处理方式或优化查询速度 |
| 数据精度丢失 | 按名称搜索而非ID搜索 | 修复BigInt类型的解析问题 |
| 搜索结果为空 | 尝试不同的搜索策略 | 修复搜索功能的实现 |
| 依赖冲突 | 降级或固定依赖版本 | 使用正确的环境（venv） |
| 功能无法使用 | 移除该功能 | 调试导致功能故障的原因 |

**自我检查问题**：“我是在解决问题，还是在回避问题？”

## 第一阶段：暂停——行动前进行评估

在尝试任何修复之前：

```
□ What is the EXACT symptom? (error message, behavior, screenshot)
□ When did it last work? What changed since then?
□ How is the service running? (process, env, startup command)
```

对于正在运行的服务：
```bash
ps -p <PID> -o command=        # How was it started?
ls .venv/ venv/ env/           # Virtual environment?
which python3 && python3 --version
which node && node --version
```

**在未记录服务原始启动命令的情况下，切勿重启服务。**

## 第二阶段：假设——形成一个理论

优先考虑的排查方向：
1. **我是否对某些配置进行了修改？** → 首先使用差异对比（diff）或回滚修改
2. **环境是否发生了变化？** → 检查版本、依赖关系和配置文件
3. **外部输入是否发生了变化？** → 检查API响应和数据格式
4. **这是否是一个全新的错误？** → 只有在排除了前三个可能性后才能考虑这一点

## 第三阶段：逐步测试——一次只进行一项修改

```
Change X → Test → Works? → Done
                → Fails? → REVERT X → new hypothesis
```

**切勿同时进行多项修改。**

## 第四阶段：修复链检测

**如果两次修复尝试都失败了，立即停止操作，回滚所有更改，并返回到第一阶段。**

可能的情况包括：
- 你只是修复了错误的症状，而未解决根本问题
- 你可能处于错误的环境中
- 你可能对系统的架构理解有误

## 第五阶段：修复后的验证

在任何修复操作之后，都需要进行验证：

```
□ Does it solve the ORIGINAL problem? (not just silence the error)
□ Did I introduce new issues? (regression check)
□ Would removing my fix bring the bug back? (confirms causality)
□ Is the fix in the right layer? (not patching symptoms upstream)
```

## 常见的错误调试模式

### 🚨 依赖临时解决方案（最常见的问题！）
**绕过问题本身，而不是直接解决它。**（例如：“虽然这种方法效率较低，但至少能解决问题”）
→ **问自己：“我是在解决问题，还是在回避问题？”** 如果是在回避问题，那就需要找到真正的解决方案。
→ 变通方法只有在以下情况下才可接受：（1）得到用户的明确批准；（2）明确标注为临时解决方案；（3）为真正的修复问题创建了待办事项。

### 🚨 随机修改模式
**盲目地随意修改代码，直到问题消失。**  
→ 每次修改都应该基于一个明确的假设。

### 🚨 错误定位的误区
**总是从自己熟悉的地方开始查找问题，而不是从问题实际发生的地方开始。**  
→ “问题真的出在这里吗？还是我只是知道该如何在这里查找问题？”

### 🚨 机械复制修复代码
**不理解代码的工作原理就直接复制他人的修复方案。**  
→ 首先需要理解代码的实现机制。

### 🚨 忽视用户反馈
**用户反馈称“在您修改了X之后系统出故障了” → 立即检查是否是X导致了问题。**  
→ 用户的观察结果是最有价值的信息来源。

## 环境检查清单

```
□ Runtime: system or venv/nvm?
□ Dependencies: match expected versions?
□ Config: .env, config.json — recent changes?
□ Process manager: PM2/systemd — restart method?
□ Logs: tail -f before reproducing
□ Backup: snapshot before any change
```

## 部署安全（严格遵循SCP流程）

**铁律：切勿直接在服务器上编辑文件；在没有备份的情况下切勿覆盖服务器文件。**

```
Standard deployment (every time, no exceptions):

1. PULL    scp server:/opt/apps/项目/ ./local-项目/
           (pull the files you need + related files)

2. EDIT    Make changes locally
           (complex multi-line → write full file, never sed)

3. VERIFY  node -c *.js                    # syntax check
           node -e "require('./file')"     # module load check
           (STOP if verification fails — do not proceed)

4. BACKUP  ssh server "cp file file.bak.$(date +%s)"

5. PUSH    scp ./local-file server:/opt/apps/项目/file

6. RESTART pm2 restart <app>
           (use SAME method as original — check ps/pm2 show first)

7. HEALTH  curl -s http://localhost:<port>/health
           pm2 logs <app> --lines 5 --nostream
           (if unhealthy → revert backup immediately)
```

### 代码推送范围控制规则
```
Changing 1 file    → pull that file + its imports/importers
Changing routes    → also pull server.js (check mount points)
Changing frontend  → also pull index.html (check script tags)
Changing config    → also pull code that reads the config
Unsure what to pull → pull the whole project directory
```

### 不应该做的事情
```
❌ sed -i for multi-line code on server
❌ Skip node -c after editing .js
❌ pm2 restart before syntax verification
❌ Tell user to refresh before health check passes
❌ Push without backup
```

## 🚨 服务器代码修改规则
**服务器上的任何代码修改都必须经过语法验证后才能重新启动或加载。**

```
After editing .js files:
  □ node -c <file>                          # Syntax check
  □ node -e "require('./<file>')"           # Module load check (for route files)
  □ FAIL → DO NOT restart. DO NOT tell user to refresh. Fix first.

After editing .html files:
  □ Check critical tag closure (div/script/style)
  □ grep -c '<div' file && grep -c '</div' file   # Count match

Complex multi-line changes:
  □ Write complete file locally → scp upload
  □ NEVER use sed for multi-line code insertion (newlines get swallowed)
  □ If sed is unavoidable → verify with node -c immediately after

Restart sequence:
  □ node -c *.js passes → pm2 restart <app>
  □ Check pm2 logs --lines 5 for startup errors
  □ curl health endpoint to confirm service is up
```

**原因**：使用`sed -i`进行多行插入操作时，可能会默默地破坏JavaScript代码的结构（例如，将换行符替换为单行字符），从而导致语法错误，使得整个页面无法正常显示，而用户却无法察觉到这些问题。

## 决策树

```
Problem appears
  ├─ I just edited something? → DIFF → REVERT if suspect
  ├─ Service won't start? → CHECK startup command + env
  ├─ New error after fix? → STOP (patch chain!) → Revert → Phase 1
  ├─ User reports regression? → DIFF before/after
  ├─ Tempted to work around? → ROOT CAUSE GATE → fix the real issue
  └─ Intermittent? → CHECK logs + external deps + timing
```