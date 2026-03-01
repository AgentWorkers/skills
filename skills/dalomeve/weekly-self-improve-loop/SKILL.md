---
name: weekly-self-improve-loop
description: 每周对内存使用情况以及被阻塞的资源进行审查。分析资源使用中的异常模式（即“摩擦”现象），根据分析结果创建新的技能（功能或解决方案），并更新系统的自主运行基线（即系统在没有人工干预下的运行状态）。
---
# 每周自我提升循环

每周进行一次自我评估，以促进持续成长。

## 问题

如果没有定期回顾：
- 同样的错误会反复出现
- 一些常见的问题或行为模式被忽视
- 技能无法得到提升
- 自主性会逐渐下降

## 工作流程

### 1. 每周回顾（每7天一次）

```powershell
# Get last 7 days of memory
$startDate = (Get-Date).AddDays(-7)
$memoryFiles = Get-ChildItem "memory/" -Filter "*.md" | 
    Where-Object { $_.LastWriteTime -ge $startDate }

# Aggregate metrics
$totalTasks = 0
$completedTasks = 0
$blockedTasks = 0
$patterns = @{}

foreach ($file in $memoryFiles) {
    $content = Get-Content $file.FullName -Raw
    
    # Count tasks
    $totalTasks += ([regex]::Matches($content, "Task:")).Count
    $completedTasks += ([regex]::Matches($content, "Status: complete")).Count
    $blockedTasks += ([regex]::Matches($content, "Blocker:")).Count
    
    # Extract patterns
    $blockers = [regex]::Matches($content, "Blocker: (.+)")
    foreach ($b in $blockers) {
        $key = $b.Groups[1].Value
        $patterns[$key] = $patterns[$key] + 1
    }
}

# Calculate rates
$completionRate = [math]::Round(($completedTasks / $totalTasks) * 100, 1)
$blockerRate = [math]::Round(($blockedTasks / $totalTasks) * 100, 1)
```

### 2. 问题模式提取

```powershell
# Find top friction patterns
$topPatterns = $patterns.GetEnumerator() | 
    Sort-Object Value -Descending | 
    Select-Object -First 3

foreach ($p in $topPatterns) {
    Write-Host "Pattern: $($p.Key) ({$p.Value} occurrences)"
    
    # Create or update skill
    $skillName = $p.Key -replace '[^a-z]', '-' -replace '-+', '-'
    $skillPath = "skills/local/$skillName-recovery"
    
    if (Test-Path $skillPath) {
        Write-Host "  Updating existing skill..."
    } else {
        Write-Host "  Creating new skill..."
        # Create skill (see memory-to-skill-crystallizer)
    }
}
```

### 3. 报告生成

```markdown
## Weekly Report (YYYY-MM-DD)

**Metrics**:
- Total tasks: X
- Completion rate: Y%
- Blocker rate: Z%

**Top Friction Patterns**:
1. Pattern A (N occurrences)
2. Pattern B (N occurrences)
3. Pattern C (N occurrences)

**New Skills Created**:
- skill-name-1
- skill-name-2

**Next Week Focus**:
- Address pattern A with automated fix
- Review skill effectiveness
```

## 可执行完成标准

| 标准 | 验证方式 |
|----------|-------------|
| 回顾是否完成 | 是否生成了报告文件 |
| 指标是否计算完毕 | 是否包含了完成率/障碍率数据 |
| 问题模式是否提取出来 | 是否识别出前三类常见问题模式 |
| 是否创建/更新了技能 | 是否至少采取了一项与技能提升相关的行动 |

## 隐私/安全注意事项

- 仅汇总数据（不包含具体细节）
- 收集的是完成率和统计数据，而非具体内容
- 报告为内部使用（不会公开）

## 自动触发条件

在以下情况下自动执行：
- 当日期为周日时（或根据配置）
- 当需要手动进行回顾时
- 在完成重大项目后

---

**每周进行回顾，持续提升自己。**