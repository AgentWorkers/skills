---
name: debug-methodology
description: 系统化的调试和问题解决方法。在遇到意外错误、服务故障、回归性错误、部署问题，或者修复尝试失败两次时启用该方法。在提出任何修复方案时也应启用该方法，以验证其是否真正解决了根本问题（而不仅仅是临时性的解决方法）。该方法有助于防止连续发布多个补丁、在错误的环境中重启系统、过度依赖临时解决方案，以及随意、无计划的修复行为。
---
# 调试方法论

这是一种系统化的调试和问题解决方法，基于实际生产中的案例以及行业最佳实践总结而成。

## ⚠️ 必须找到根本原因

**任何修复措施都必须针对问题的根本原因。除非得到明确批准，否则禁止使用临时解决方案（即“变通方法”）。**

在提出任何解决方案之前，必须先通过“根本原因审核”（Root Cause Gate）：

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

### “五个为什么”（5 Whys）——针对非显而易见的问题

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

### 常见的临时解决方案陷阱

| 问题 | 临时解决方案（❌） | 根本原因的修复方法（✅） |
|---------|----------------|-------------------|
| API超时 | 更换更快的模型 | 使用流式处理方式或优化查询速度 |
| 数据精度丢失 | 按名称搜索而非ID搜索 | 修复BigInt类型的解析问题 |
| 搜索结果为空 | 尝试不同的搜索策略 | 修复搜索功能的实现 |
| 依赖冲突 | 降级或固定依赖版本 | 使用正确的开发环境（venv） |
| 功能无法使用 | 移除该功能 | 调试导致功能故障的原因 |

**自我检查问题**：“我是在解决问题，还是在逃避问题？”

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

**在未记录服务原始启动命令之前，绝对不要重启服务。**

## 第二阶段：假设——形成一个理论

优先检查以下方面：
1. **我是否对某些配置进行了修改？** → 首先使用差异对比（diff）或回滚操作
2. **环境是否发生了变化？** → 检查版本、依赖关系和配置文件
3. **外部输入是否发生了变化？** → 检查API响应和数据格式
4. **这是否是一个真正的新错误？** → 只有在排除了前三个可能性之后才考虑这个选项

## 第三阶段：逐步测试——一次只进行一项修改

```
Change X → Test → Works? → Done
                → Fails? → REVERT X → new hypothesis
```

**切勿同时进行多项修改。**

## 第四阶段：检测修复过程中的连锁问题

**如果两次修复尝试都失败了，立即停止，并回滚所有更改。然后重新回到第一阶段。**

你可能遇到的情况包括：
- 修复了错误的问题的表面症状
- 使用了错误的环境进行调试
- 对系统架构理解有误

## 第五阶段：修复后的验证

在任何修复操作之后，都需要进行验证：

```
□ Does it solve the ORIGINAL problem? (not just silence the error)
□ Did I introduce new issues? (regression check)
□ Would removing my fix bring the bug back? (confirms causality)
□ Is the fix in the right layer? (not patching symptoms upstream)
```

## 常见的错误调试模式

### 🚨 依赖临时解决方案的习惯（非常普遍！）
**绕过问题本身进行修复**。例如：“虽然这种方法效率较低，但至少能解决问题”。** 问自己：“我是在解决问题，还是在逃避问题？”** 如果只是暂时解决问题，必须明确：（1）用户已明确批准；（2）该临时解决方案被标记为临时性的；（3）必须为根本问题的修复创建相应的待办事项（TODO）。

### 🚨 随机修改问题的习惯
**在没有明确假设的情况下随意修改代码**，直到问题消失为止。** 每次修改都应基于一个明确的假设。

### 🚨 错误定位的误区
**总是从自己熟悉的地方开始查找问题**，而不是从问题实际发生的地方开始。** 问自己：“问题真的出在这里吗？还是我只是知道从这里开始查找？”**

### 🚨 机械地复制修复代码的习惯
**不理解代码修复原理就直接复制他人的解决方案**。** 应先理解修复机制的原理。

### 🚨 忽视用户反馈
**用户反馈指出“在您修改X之后系统出现了问题”** → 立即检查X是否是问题根源。** 用户的观察结果是最宝贵的信息来源。

## 环境检查清单

```
□ Runtime: system or venv/nvm?
□ Dependencies: match expected versions?
□ Config: .env, config.json — recent changes?
□ Process manager: PM2/systemd — restart method?
□ Logs: tail -f before reproducing
□ Backup: snapshot before any change
```

## 部署安全注意事项

```
□ Pull latest from server first
□ Backup current working version
□ Make changes on latest
□ Deploy with same startup method
□ Verify immediately
□ If broken → revert, THEN debug
```

## 🚨 服务器代码修改规则

**服务器上的任何代码修改都必须在重启或重新加载之前通过语法验证。**

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

**原因**：使用`sed -i`进行多行插入操作时，可能会默默地破坏JavaScript代码的结构（例如，将换行符替换为单行字符），从而导致语法错误，使整个页面无法正常显示，而用户却无法察觉到这些错误。

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